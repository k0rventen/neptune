"""API for neptune"""
import json
import time
from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from models import (HistoricalStatistics, Image, Package, PackageVersion,
                    RegistryConfig, Tag, Vulnerability, create_session)
from utils import (Logger, cleanup_images, database_housekeeping, grype_report,
                   human_readable_size, human_readable_time, skopeo_login, create_statistics,
                   skopeo_pull, syft_report, scan_mutex)

logger = Logger("api")
session = create_session()


class RegistryConfigRequest(BaseModel):
    registry: str
    user: str
    password: str


class ImageScanRequest(BaseModel):
    image: str
    return_error: Optional[bool]


class VulnPut(BaseModel):
    notes: Optional[str]
    active: Optional[bool]


class PackagePut(BaseModel):
    notes: Optional[str]
    minimum_version: Optional[str]


api_router = APIRouter(prefix='/api')


@api_router.post("/registries", tags=['config'])
def post_config(new_config: RegistryConfigRequest):
    """add a new registry login for skopeo"""
    registry_conf = session.query(RegistryConfig).filter(
        RegistryConfig.url == new_config.registry).one_or_none()
    if registry_conf:
        registry_conf.url = new_config.registry
        registry_conf.user = new_config.user
        registry_conf.password = new_config.password
        session.commit()
    else:
        registry_conf = RegistryConfig(
            url=new_config.registry, user=new_config.user, password=new_config.password)
        logger.info("trying registry auth")
    auth_ok, message = skopeo_login(
        new_config.registry, new_config.user, new_config.password)
    if auth_ok:
        session.add(registry_conf)
        session.commit()
        return {"message": message}
    raise HTTPException(status_code=400, detail=message)


@api_router.get("/registries", tags=['config'])
def get_config():
    """get the current registries configs"""
    registry_configs = session.query(RegistryConfig).all()
    return [c.serialize() for c in registry_configs]


@api_router.post("/scan", tags=['config'])
def scan_image(scan_request: ImageScanRequest):
    """add a new image to neptune"""
    db_session = create_session()
    image = scan_request.image
    logger.info("Processing %s", image)
    t0 = time.time()
    image_uuid = str(uuid4())
    logger.info("pulling image..")
    pull_ok, message = skopeo_pull(image, image_uuid)
    if not pull_ok:
        raise HTTPException(status_code=400, detail=message)

    logger.info("grabbing SBOM")
    syft_report_path, sbom_json = syft_report(image_uuid)
    if not syft_report_path:
        raise HTTPException(status_code=400, detail=sbom_json)

    image_distro = sbom_json["distro"].get("name", "distroless")
    image_distro_version = sbom_json["distro"].get("versionID", "unknown")
    sbom = [{"name": a['name'],
             "version":a["version"],
             "type":a["type"]}
            for a in sbom_json["artifacts"]]
    logger.info("fetched {} packages".format(len(sbom)))

    logger.info("checking vulns")
    grype_ok, vuln_json = grype_report(syft_report_path)
    if not grype_ok:
        raise HTTPException(status_code=400, detail=vuln_json)
    vulns = [{"id": v["vulnerability"]["id"],
              "severity":v["vulnerability"]["severity"],
              "description":v["vulnerability"].get("description", ""),
              "artifact_name":v["artifact"]["name"],
              "artifact_type":v["artifact"]["type"],
              "artifact_version":v["artifact"]["version"]}
             for v in vuln_json["matches"]]
    logger.info("found {} vulns".format(len(vulns)))

    image_details = vuln_json["source"]["target"]
    image_sha = image_details["imageID"]
    image_size = image_details["imageSize"]

    try:
        image_name, image_tag = image.split(":")
    except ValueError:
        image_name, image_tag = image, "latest"

    # mutex here to avoid race conditions when adding records concurrently
    with scan_mutex:
        sha_already_scanned = db_session.query(
            Tag).filter(Tag.sha == image_sha).one_or_none()
        if sha_already_scanned:
            logger.warning(
                "This image (%s) was already inventoried. deleting the record.", image_sha)
            db_session.delete(sha_already_scanned)

        # new image, add
        image = db_session.query(Image).filter(
            Image.name == image_name).one_or_none()

        if not image:
            db_session.add(Image(name=image_name, tags=[]))
            image = db_session.query(Image).filter(
                Image.name == image_name).one_or_none()
        else:
            image.last_update = datetime.now()
        # create tag
        s_image = Tag(tag=image_tag,
                      image_id=image.id,
                      distro=image_distro,
                      distro_version=image_distro_version,
                      sha=image_sha,
                      size=image_size,
                      packages=[])

        # packages
        for p in sbom:
            # check for base package
            package = db_session.query(Package).filter(Package.name == p["name"]).filter(
                Package.type == p["type"]).one_or_none()

            if not package:
                package = Package(name=p["name"], type=p["type"])
                db_session.add(package)
            # check for version
            if p["version"] not in [p.version for p in package.versions]:
                version = PackageVersion(version=p["version"])
                package.versions.append(version)

            else:
                version = [
                    v for v in package.versions if v.version == p["version"]][0]
            s_image.packages.append(version)

        # vulns
        for v in vulns:
            is_referenced = db_session.query(Vulnerability).filter(
                Vulnerability.name == v["id"]).one_or_none()
            if not is_referenced:
                # find the linked package
                _, version = db_session.query(Package, PackageVersion).filter(Package.id == PackageVersion.package_id).filter(
                    Package.name == v["artifact_name"]).filter(Package.type == v["artifact_type"]).filter(PackageVersion.version == v["artifact_version"]).one_or_none()
                if version:
                    v = Vulnerability(name=v["id"], severity=v["severity"])
                    version.vulnerabilities.append(v)
                    version.refresh_outdated_status()
                    db_session.add(version)
        db_session.add(s_image)
        logger.info("commiting to DB")
        db_session.commit()

    # now that we have updated the inventory, tell the client the stats of the image (size,packages, and vulns)
    # return 400 code if the image has active vulnerabilities and the client wants a 400 http error as a signal
    t1 = time.time() - t0
    active_vulns = []
    for package in s_image.packages:
        for v in package.vulnerabilities:
            if v.active:
                active_vulns.append(v.name)
    response = {"image": image_name,
                "tag": image_tag,
                "sha": image_sha,
                "size": human_readable_size(image_size),
                "scan_time": human_readable_time(int(t1)),
                "packages": len(s_image.packages),
                "vulnerabilities": active_vulns}
    return JSONResponse(response, status_code=400 if active_vulns and scan_request.return_error else 200)


@api_router.get("/statistics", tags=['ui'])
def statistics(current: bool = False):
    """statistics about the inventory
    if current is True, only returns the last element
    """
    if current:
        last_stat_json = create_statistics(save_to_db=False)
        last_stat_json.pop("timestamp")
        last_stat_json["severities"] = {k: session.query(Vulnerability).filter(Vulnerability.severity == k).count() for k in ["Low", "Medium", "High", "Critical", "Negligible", "Unknown"]}
        return last_stat_json
    else:
        stats = session.query(HistoricalStatistics).order_by(
            HistoricalStatistics.timestamp.asc()).all()
        stats = [s.serialize() for s in stats]
        return stats


@api_router.get("/images", tags=['images', "ui"])
def images(offset: int = 0, limit: int = 50):
    """list of images"""
    results = session.query(Image).order_by(
        Image.last_update.desc()).limit(limit).offset(offset).all()
    return [i.serialize() for i in results]


@api_router.get("/tags", tags=['images'])
def get_all_tags(offset: int = 0, limit: int = 50):
    """list of tags"""
    results = session.query(Tag).order_by(
        Tag.date_added.desc()).limit(limit).offset(offset).all()
    return [i.serialize() for i in results]


@api_router.get("/tags/featured", tags=['images'])
def get_featured_tags():
    """returns a curated list of 4 tags:
       ["active_vulnerabilities", "vulnerabilities", "outdated_packages", "packages"]
    """
    response = {"most_vulnerabilities": {}, "most_packages": {},
                "most_outdated_packages": {}, "most_active_vulnerabilities": {}}
    all_tags = session.query(Tag).all()
    for t in all_tags:
        tag = t.serialize()
        for feature in ["active_vulnerabilities", "vulnerabilities", "outdated_packages", "packages"]:
            if tag[feature] > response["most_"+feature].get(feature, -1):
                response["most_"+feature] = tag
    return list(response.values())


@api_router.get("/tags/{sha}", tags=['images'])
def get_tag(sha: str):
    """specific image:tag"""
    spec_image = session.query(Tag).filter(Tag.sha == sha).first()
    return spec_image.serialize(full=True)


@api_router.delete("/tags/{sha}", tags=['images'])
def delete_tag(sha: str):
    tag = session.query(Tag).filter(Tag.sha == sha).first()
    if tag:
        logger.info("deleting tag %s", sha)
        session.delete(tag)
        session.commit()
    return {}


@api_router.get("/vulnerabilities", tags=['vulnerabilities'])
def vulnerabilities(offset: int = 0, limit: int = 50):
    """vulnerabilities interface"""
    vulns = session.query(Vulnerability).all() #limit(limit).offset(offset).all()
    return [v.serialize(True) for v in vulns]


@api_router.get("/vulnerabilities/{cve_id}", tags=['vulnerabilities'])
def vulnerabilities(cve_id: int):
    """vulnerabilities interface"""
    vuln = session.query(Vulnerability).filter(
        Vulnerability.id == cve_id).first()
    if vuln:
        return vuln.serialize(True)
    raise HTTPException(status_code=404, detail="vulnerability does not exist")


@api_router.put("/vulnerabilities/{cve_id}", tags=['vulnerabilities'])
def set_vuln_notes(cve_id: int, vuln_def: VulnPut):
    """set notes and toggle active boolean for a vuln
    """
    vuln = session.query(Vulnerability).filter(
        Vulnerability.id == cve_id).first()
    if not vuln:
        raise HTTPException(
            status_code=404, detail="vulnerability does not exist")
    if vuln_def.notes is not None:
        vuln.notes = vuln_def.notes
    if vuln_def.active is not None:
        vuln.active = vuln_def.active
    session.add(vuln)
    session.commit()
    return {}


@api_router.get("/packages", tags=['packages'])
def packages(package_type: str | None = None, package_name: str | None = None, offset: int = 0, limit: int = 20):
    """returns all packages"""
    filters = {k: v for k, v in {"type": package_type,
                                 "name": package_name}.items() if v}
    dependencies = session.query(Package).all() #.limit(limit).offset(offset).all()
    return [d.serialize() for d in dependencies]


@api_router.put("/packages/{package_id}", tags=['packages'])
def set_packages_notes(package_id: int, package_def: PackagePut):
    """set minimum required version for a package
    """
    package = session.query(Package).filter(Package.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="id does not exists")
    if package_def.notes is not None:
        package.notes = package_def.notes
    if package_def.minimum_version:
        package.minimum_version = package_def.minimum_version

        # check for each version if they are now outdated
        for version in package.versions:
            version.outdated = version.is_outdated()
    session.add(package)
    session.commit()
    return {}


@api_router.get("/packages/{package_id}", tags=['packages'])
def get_specific_package_versions(package_id: int):
    """set minimum required version for a package
    """
    package = session.query(Package).filter(Package.id == package_id).first()
    if not package:
        return {}
    return package.serialize()


neptune_api = FastAPI(
    title="Neptune API",
    version="0.3.0",
    description="Containers SBOM & vulnerability management",
    redoc_url=None,
    docs_url="/api",
    openapi_url="/api/openapi.json"
)

neptune_api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

neptune_api.include_router(api_router)
neptune_api.mount(
    path="/",
    app=StaticFiles(directory="/app/dist", html=True),
    name="ui")
