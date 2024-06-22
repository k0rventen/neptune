"""ressources management endpoints (tags, vulns, packages)"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from models import (
    HistoricalStatistics,
    Package,
    RegistryConfig,
    Tag,
    Vulnerability,
    get_db,
)
from pydantic import BaseModel
from sqlalchemy.orm import Session
from utils import (
    Logger,
    create_statistics,
    database_housekeeping,
    mem_cache,
    paginate_query,
    skopeo_login,
)


class RegistryConfigRequest(BaseModel):
    registry: str
    user: str
    password: str


class RegistryConfigDelete(BaseModel):
    registry: str


class VulnPut(BaseModel):
    notes: str | None = None
    active: bool | None = None


class PackagePut(BaseModel):
    notes: str | None = None
    minimum_version: str | None = None

logger = Logger("api")

api_router = APIRouter(prefix='/api')

@api_router.post("/registries", tags=['config'])
def post_config(new_config: RegistryConfigRequest, session: Session = Depends(get_db)):
    """add a new registry login for skopeo"""
    auth_ok, message = skopeo_login(
        new_config.registry, new_config.user, new_config.password)
    if auth_ok:
        registry_conf = session.query(RegistryConfig).filter(
            RegistryConfig.url == new_config.registry).one_or_none()
        if registry_conf:
            registry_conf.url = new_config.registry
            registry_conf.user = new_config.user
            registry_conf.password = new_config.password
        else:
            registry_conf = RegistryConfig(
                url=new_config.registry, user=new_config.user, password=new_config.password)
        session.add(registry_conf)
        return registry_conf.serialize()
        #return {"message": message}
    raise HTTPException(status_code=400, detail=message)


@api_router.delete("/registries", tags=['config'])
def delete_config(registry: RegistryConfigDelete, session: Session = Depends(get_db)):
    """get the current registries configs"""
    registry_config = session.query(RegistryConfig).filter(
        RegistryConfig.url == registry.registry).one_or_none()
    if registry_config:
        session.delete(registry_config)
    return JSONResponse(content={}, status_code=204)


@api_router.get("/registries", tags=['config'])
def get_config(session: Session = Depends(get_db)):
    """get the current registries configs"""
    registry_configs = session.query(RegistryConfig).all()
    return [c.serialize() for c in registry_configs]


@api_router.get("/statistics", tags=['ui'])
def statistics(session: Session = Depends(get_db), current: bool = False):
    """statistics about the inventory
    if current is True, only returns the last element
    """
    base_query = session.query(HistoricalStatistics)
    if current:
        last_stats = base_query.order_by(HistoricalStatistics.timestamp.desc()).first()
        return last_stats.serialize() if last_stats else None

    stats = base_query.order_by(HistoricalStatistics.timestamp.asc()).all()
    stats = [s.serialize() for s in stats]
    return stats


@api_router.get("/tags", tags=['images'])
def get_all_tags(session: Session = Depends(get_db), name_filter: str = None, tag_filter: str = None,distro_filter: str = None, has_vuln: bool = None, page: int = 1, per_page: int = 20):
    """list of tags"""
    filters = []
    if tag_filter:
        filters.append(Tag.tag.ilike(f"%{tag_filter}%"))
    if name_filter:
        filters.append(Tag.image.ilike(f"%{name_filter}%"))
    if distro_filter:
        filters.append(Tag.distro.ilike(f"%{distro_filter}%"))
    if has_vuln is not None:
        filters.append(Tag.has_vulnerabilities== has_vuln)
    query = session.query(Tag).order_by(Tag.date_added.desc()).filter(*filters)
    return paginate_query(query, page, per_page)


@api_router.get("/tags/featured", tags=['images'])
def get_featured_tags(session: Session = Depends(get_db)):
    """returns a curated list of 5 tags:
       ["active_vulnerabilities", "vulnerabilities", "outdated_packages", "packages","most_recent"]
    """
    if cached := mem_cache.cached('featured'):
        return cached
    response = {"most_vulnerabilities": {}, "most_packages": {},
                "most_outdated_packages": {}, "most_active_vulnerabilities": {},"most_recent":{}}
    all_tags = session.query(Tag).all()
    most_recent_tag = session.query(Tag).order_by(Tag.date_added.desc()).first()
    most_recent_tag_serialized = most_recent_tag.serialize()
    for t in all_tags:
        tag = t.serialize()
        for feature in ["active_vulnerabilities", "vulnerabilities", "outdated_packages", "packages"]:
            if tag[feature] > response["most_"+feature].get(feature, -1):
                response["most_"+feature] = tag
    response["most_recent"] = most_recent_tag_serialized
    mem_cache.cache('featured',response,600)
    return response


@api_router.get("/tags/{sha}", tags=['images'])
def get_tag(sha: str, session: Session = Depends(get_db)):
    """specific image:tag"""
    spec_image = session.query(Tag).filter(Tag.sha == sha).first()
    if spec_image:
        return spec_image.serialize(full=True)
    return HTTPException(status_code=404, detail="sha does not exist")

@api_router.delete("/tags/{sha}", tags=['images'])
def delete_tag(sha: str, session: Session = Depends(get_db)):
    tag = session.query(Tag).filter(Tag.sha == sha).first()
    if tag:
        session.delete(tag)
        database_housekeeping()
        create_statistics()
    return {}


@api_router.get("/vulnerabilities", tags=['vulnerabilities'])
def all_vulnerabilities(session: Session = Depends(get_db), name_filter: str = None, severity_filter: str = None, notes_filter: str = None, active_filter: bool = None, scan_filter: bool = None, page: int = 1, per_page: int = 20):
    """vulnerabilities interface"""
    filters = []
    if name_filter:
        filters.append(Vulnerability.name.ilike(f"%{name_filter}%"))
    if severity_filter:
        filters.append(Vulnerability.severity.ilike(f"%{severity_filter}%"))
    if notes_filter:
        filters.append(Vulnerability.notes.ilike(f"%{notes_filter}%"))
    if active_filter is not None:
        filters.append(Vulnerability.active.is_(active_filter))
    if scan_filter is not None:
        filters.append(Vulnerability.discovered_during_rescan.is_(scan_filter))
    query = session.query(Vulnerability).filter(*filters)
    return paginate_query(query, page, per_page, full_serialize=True)


@api_router.get("/vulnerabilities/{cve_id}", tags=['vulnerabilities'])
def vulnerabilities(cve_id: int, session: Session = Depends(get_db)):
    """vulnerabilities interface"""
    vuln = session.query(Vulnerability).filter(
        Vulnerability.id == cve_id).first()
    if vuln:
        return vuln.serialize(True)
    raise HTTPException(status_code=404, detail="vulnerability does not exist")


@api_router.put("/vulnerabilities/{cve_id}", tags=['vulnerabilities'])
def set_vuln_notes(cve_id: int, vuln_def: VulnPut, session: Session = Depends(get_db)):
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
    return {}


@api_router.get("/packages", tags=['packages'])
def packages(session: Session = Depends(get_db), name_filter: str = None, type_filter: str = None, with_outdated_versions: bool = None,with_vulnerable_versions: bool = None,page: int = 1, per_page: int = 20):
    """returns all packages that match the filters"""
    filters = []
    if name_filter:
        filters.append(Package.name.ilike(f"%{name_filter}%"))
    if type_filter:
        filters.append(Package.type.ilike(f"%{type_filter}%"))
    if with_outdated_versions is not None:
        filters.append(Package.has_outdated_packages == with_outdated_versions)
    if with_vulnerable_versions is not None:
        filters.append(Package.has_vulnerable_versions == with_vulnerable_versions)
    query = session.query(Package).filter(*filters)
    return paginate_query(query, page, per_page)


@api_router.put("/packages/{package_id}", tags=['packages'])
def set_packages_notes(package_id: int, package_def: PackagePut, session: Session = Depends(get_db)):
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
    return {}


@api_router.get("/packages/{package_id}", tags=['packages'])
def get_specific_package_versions(package_id: int, session: Session = Depends(get_db)):
    """set minimum required version for a package
    """
    package = session.query(Package).filter(Package.id == package_id).first()
    if not package:
        return {}
    return package.serialize()
