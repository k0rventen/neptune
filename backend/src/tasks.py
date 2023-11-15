"""background tasks for async processing
"""
import time

from schedule import every, repeat, run_pending, run_all

from utils import (Logger, cleanup_images, create_statistics,
                   database_housekeeping, db_sbom_rescan, grype_update,
                   startup_logins, stop_flag)

tasks_logger = Logger("tasks")


def tasks_thread():
    tasks_logger.info("Starting background tasks thread")
    while not stop_flag.is_set():
        run_pending()
        time.sleep(1)
    tasks_logger.info("exiting")


@repeat(every().day.at("20:00"))
def daily_rescan():
    tasks_logger.info("starting complete inventory rescan..")
    grype_update()
    db_sbom_rescan()

@repeat(every().day.at("23:00"))
def daily_housekeeping():
    tasks_logger.info("starting housekeeping chores..")
    database_housekeeping()
    cleanup_images()
    create_statistics()
