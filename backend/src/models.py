"""models for the inventory
"""
import re
from datetime import datetime
from itertools import chain

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Table, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# transition table because tags and packages versions have a many 2 many relation
_packages = Table('packages_association', Base.metadata,
                  Column('image_id', Integer,
                         ForeignKey('tags.sha')),
                  Column('package_id', Integer,
                         ForeignKey('packageversions.id'))
                  )


class RegistryConfig(Base):
    """the configuration for the docker registry to pull from
    """
    __tablename__ = "registryconfig"
    url = Column(String(128), primary_key=True)
    user = Column(String(128))
    password = Column(String(128))

    def serialize(self):
        return {
            'registry': self.url,
            'user': self.user,
            'password': '*' * len(self.password)
        }


class Image(Base):
    """An Image is the path of the image that does not change, eg alpine.
    """
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    # so we can sort by updates without checking the tags
    last_update = Column(DateTime, default=datetime.now)

    tags = relationship("Tag")  # Each image can have multiple tags

    def serialize(self, full=False):
        return {
            "id": self.id,
            "name": self.name,
            "last_update": self.last_update,
            "tags": [t.serialize() for t in self.tags]
        }


class Tag(Base):
    """A Tag is a specific version of an Image, eg alpine:3.12.

    There might be multiple tags with the same name, like latest, but the sha will be different
    """
    __tablename__ = "tags"
    sha = Column(String(64), primary_key=True)
    # this will be "latest" for example. We can have multiple "latest" but their sha must differ
    tag = Column(String(128))
    distro = Column(String(64))
    distro_version = Column(String(64))
    size = Column(Integer)
    date_added = Column(DateTime, default=datetime.now)

    # base image of this tag
    image_id = Column(Integer, ForeignKey('images.id'))
    image = relationship("Image", back_populates="tags")

    # list of packages of that tag
    packages = relationship(
        "PackageVersion", secondary=_packages, back_populates="tags")

    def serialize(self, full=False):
        spec = {
            "tag": self.tag,
            "sha": self.sha,
            "distro": {
                "name": self.distro,
                "version": self.distro_version,
            },
            "size": self.size,
            "date_added": self.date_added,
            "image": self.image.name,
            "image_id": self.image_id,
        }
        if full: # return the id of each related objects
            spec.update({"packages": [p.id for p in self.packages],
                         "outdated_packages": [p.id for p in self.packages if p.is_outdated()],
                         "vulnerabilities": [v.id for v in set(chain.from_iterable([p.vulnerabilities for p in self.packages]))]})
        else: # only return the len of the corresponding objects
            spec.update({"packages": len(self.packages),
                         "outdated_packages": len([p for p in self.packages if p.is_outdated()]),
                         "vulnerabilities": sum(set([v.id for v in set(chain.from_iterable([p.vulnerabilities for p in self.packages]))])),
                         'active_vulnerabilities':sum(set([v.id for v in set(chain.from_iterable([p.vulnerabilities for p in self.packages])) if v.active]))})
                        
        return spec

class Package(Base):
    """A Package is a python package on which a Tag is dependent. It has a given version.
    """
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    type = Column(String(64))
    minimum_version = Column(String(16), default="0.0.0")
    notes = Column(String(256), default="")
    date_added = Column(DateTime, default=datetime.now)

    # list of versions of this package
    versions = relationship("PackageVersion")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'minimum_version': self.minimum_version,
            'configured': self.minimum_version != '0.0.0',
            'notes': self.notes,
            "date_added": self.date_added,
            'versions': [v.serialize() for v in self.versions]
        }


class PackageVersion(Base):
    __tablename__ = "packageversions"
    id = Column(Integer, primary_key=True)
    version = Column(String(16))
    outdated = Column(Boolean, default=False)

    # to which package does we belong to
    package_id = Column(Integer, ForeignKey('packages.id'))
    package = relationship("Package", back_populates="versions")

    # list of vulns this specific package version has
    vulnerabilities = relationship("Vulnerability")

    # list of tags that have this package version
    tags = relationship("Tag", secondary=_packages, back_populates="packages")

    def refresh_outdated_status(self):
        self.outdated = self.is_outdated()
    
    def is_outdated(self) -> bool:
        """is this specific version < the package minimum version

        the comparison is based on numbers only, grouped by separators being everything __not__ a number.

        Args:
            version_one (str): first version
            version_two (str): second
        """
        version_one_ints = [int(x) for x in re.findall("[0-9]+", self.package.minimum_version)]
        version_two_ints = [int(x) for x in re.findall("[0-9]+", self.version)]

        # r-pad the shortest with 0s
        max_len = max(len(version_one_ints), len(version_two_ints))
        for l in [version_one_ints, version_two_ints]:
            if len(l) < max_len:
                l += [0] * (max_len - len(l))

        first_superior = next(
            (i for i in range(max_len) if version_one_ints[i] > version_two_ints[i]), None)
        first_inferior = next(
            (i for i in range(max_len) if version_one_ints[i] < version_two_ints[i]), None)
        return (first_superior if isinstance(first_superior, int) else max_len) <= (first_inferior if isinstance(first_inferior, int) else max_len)


    def serialize(self, full=False):
        spec = {
            "id": self.id,
            "package": self.package.name,
            "version": self.version,
            "outdated": self.outdated,
        }
        if full:
            spec["vulnerabilities"] = [v.id for v in self.vulnerabilities]
            spec["tags"] = [t.id for t in self.tags]
        else:
            spec["vulnerabilities"] = [v.serialize()
                                       for v in self.vulnerabilities]
            spec["tags"] = [t.serialize() for t in self.tags]

        return spec


class Vulnerability(Base):
    """A Vulnerability is a potential attribute of a Tag.
    """
    __tablename__ = "vulnerabilities"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    severity = Column(String(64))
    notes = Column(String(1024), default="")
    date_added = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)

    package_id = Column(Integer, ForeignKey('packageversions.id'))
    package = relationship("PackageVersion", back_populates="vulnerabilities")

    def serialize(self, full=False):
        spec = {
            "id": self.id,
            "name": self.name,
            "severity": self.severity,
            "notes": self.notes,
            "active": self.active,
            "affected_package_id": self.package.id,
            "affected_images_sha": [t.sha for t in self.package.tags]
        }

        return spec


def create_db():
    engine = create_engine("sqlite:///data/neptune.db?check_same_thread=false")
    Base.metadata.create_all(engine)
    del engine


def create_session():
    """creates a sqlalchemy session
    """
    engine = create_engine("sqlite:///data/neptune.db?check_same_thread=false")
    Base.metadata.create_all(engine)
    sqlite_session = sessionmaker(bind=engine)
    return sqlite_session()
