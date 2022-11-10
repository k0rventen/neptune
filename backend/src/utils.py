"""functions that interacts with locally installed binaries and other utils"""
import logging
import os
import subprocess
import threading
import json
import uvicorn

from models import (Image, Tag, Package, PackageVersion, RegistryConfig,  Vulnerability, HistoricalStatistics,
                    create_session)

stop_flag = threading.Event()
scan_mutex = threading.Lock()


class APIServer(uvicorn.Server):
    """custom uvicorn server

    when receiving a sigterm, it will toggle our stop flag for the task threads
    """

    def handle_exit(self, sig: int, frame) -> None:
        stop_flag.set()
        return super().handle_exit(sig, frame)


def Logger(name, level='INFO'):
    # Create a custom logger
    log = logging.getLogger(name)
    if log.hasHandlers():
        return log
    log.propagate = False

    # add a streamhandler for stdout
    stdout_handler = logging.StreamHandler()
    stdout_format = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s',
                                      "%Y-%m-%d %H:%M:%S")
    stdout_handler.setFormatter(stdout_format)
    log.addHandler(stdout_handler)
    log.setLevel(level)

    return log


def human_readable_time(time_s: int) -> str:
    timestr = ""
    for timeunit in [(3600, "h"), (60, "m"), (1, "s")]:
        quot, rem = divmod(time_s, timeunit[0])
        timestr += "{}{}".format(quot, timeunit[1]) if quot > 0 else ""
        time_s = rem
    return timestr


def human_readable_size(size_s: int) -> str:
    sizestr = ""
    for sizeunit in [(1000000000, "Go"), (1000000, "Mo")]:
        quot, rem = divmod(size_s, sizeunit[0])
        sizestr += "{}{}".format(quot, sizeunit[1]) if quot > 0 else ""
        size_s = rem
    return sizestr


def cleanup_images():
    """deletes images in the images dir
    """
    cleanup = Logger("cleanup")
    cleanup.info("Cleaning up images..")
    for image in os.listdir("/tmp"):
        os.remove("/tmp/{}".format(image))


def database_housekeeping():
    session = create_session()
    housekeeping_logger = Logger("housekeeping")
    housekeeping_logger.info("Cleaning up the base")
    # delete package version with no tags
    no_tags_packages = [p for p in session.query(
        PackageVersion).all() if len(p.tags) == 0]
    for p in no_tags_packages:
        for v in p.vulnerabilities:
            housekeeping_logger.info("deleting vulnerability %s", v.name)
            session.delete(v)
        housekeeping_logger.info(
            "deleting packageversion %s==%s", p.package.name, p.version)
        session.delete(p)

    # now delete the remaining images & packages
    no_versions_packages = [p for p in session.query(
        Package).all() if len(p.versions) == 0]
    no_tags_images = [i for i in session.query(
        Image).all() if len(i.tags) == 0]
    for p in no_versions_packages:
        housekeeping_logger.info("deleting package %s", p.name)
        session.delete(p)
    for i in no_tags_images:
        housekeeping_logger.info("deleting image %s", i.name)
        session.delete(i)
    housekeeping_logger.info("commiting !")
    session.commit()


def create_statistics():
    session = create_session()

    all_tags = session.query(Tag).all()

    today_stats = HistoricalStatistics(
        tags_total_count=len(all_tags),
        vulnerable_tags_count=len(
            [tag for tag in all_tags if tag.has_vulnerabilities()]),
        outdated_tags_count=len(
            [tag for tag in all_tags if tag.has_outdated_packages()]),
        packages_total_count=session.query(PackageVersion).count(),
        outdated_packages_count=session.query(PackageVersion).filter(
            PackageVersion.outdated == True).count(),
        vulnerable_packages_count=session.query(PackageVersion).filter(
            PackageVersion.vulnerabilities.any()).count(),
        vulnerabilities_total_count=session.query(Vulnerability).count(),
        active_vulnerabilities_count=session.query(
            Vulnerability).filter(Vulnerability.active == True).count(),
        low_vulnerabilities_count=session.query(Vulnerability).filter(
            Vulnerability.active == True, Vulnerability.severity == "Low").count(),
        medium_vulnerabilities_count=session.query(Vulnerability).filter(
            Vulnerability.active == True, Vulnerability.severity == "Medium").count(),
        high_vulnerabilities_count=session.query(Vulnerability).filter(
            Vulnerability.active == True, Vulnerability.severity == "High").count(),
        critical_vulnerabilities_count=session.query(Vulnerability).filter(Vulnerability.active == True, Vulnerability.severity == "Critical").count())
    session.add(today_stats)
    session.commit()


def startup_logins():
    """tries to login to every registered registry
    """
    app_session = create_session()
    startup_logger = Logger("registry_login")
    registries = app_session.query(RegistryConfig).all()
    for registry in registries:
        ok, err = skopeo_login(registry.url, registry.user, registry.password)
        if ok:
            startup_logger.info(
                "skopeo successfully logged into registry %s!", registry.url)
        else:
            startup_logger.error(
                "Failed to log into registry %s : %s", registry.url, err)


def skopeo_login(registry, user, passwd):
    """tries to login against a registry using the provided creds

    Args:
        registry (str): registry url
        user (str): username
        passwd (str): password

    Returns:
        tuple: (bool,str)
    """
    login = subprocess.run(
        ["skopeo", "login", registry, "-u", user, "-p", passwd], capture_output=True)
    if login.returncode == 0:
        return True, login.stdout.decode()
    return False, login.stdout.decode()+login.stderr.decode()


def skopeo_pull(url, local_path):
    """pull a given image

    Args:
        url (str): url to pull
        local_path (str): relative path to store the image to

    Returns:
        tuple: (bool,str)
    """
    pull = subprocess.run(["skopeo", "copy", "docker://{}".format(url),
                          "docker-archive:/tmp/{}".format(local_path)], capture_output=True)
    if pull.returncode == 0:
        return True, pull.stdout.decode()
    return False, pull.stdout.decode()+pull.stderr.decode()


def grype_update():
    grype = subprocess.run(["grype", "db", "update"], capture_output=True)
    if grype.returncode == 0:
        return True, grype.stdout.decode()
    return False, grype.stdout.decode()+grype.stderr.decode()


def grype_report(syft_report_path):
    """reports vulnerabilities for a given local image

    Args:
        syft_report_path (str): local image path

    Returns:
        tuple: (bool,str)
    """
    grype = subprocess.run(["grype", "-q", "-o", "json",
                           "sbom:{}".format(syft_report_path)], capture_output=True)
    if grype.returncode == 0:
        return True, json.loads(grype.stdout.decode())
    return False, grype.stdout.decode()+grype.stderr.decode()


def syft_report(local_image_path):
    """returns a SBOM for a given image

    Args:
        local_image_path (str): local path

    Returns:
        tuple: (bool,str)
    """
    syft_report_path = f"/tmp/{local_image_path}_syft.json"
    syft = subprocess.run(["syft", "-q", "-o", "json", "--file", syft_report_path,
                          "docker-archive:/tmp/{}".format(local_image_path)], capture_output=True)
    if syft.returncode == 0:
        with open(syft_report_path) as f:
            return syft_report_path, json.load(f)
    return False, syft.stdout.decode()+syft.stderr.decode()
