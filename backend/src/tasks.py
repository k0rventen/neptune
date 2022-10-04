import time

from schedule import every, repeat, run_pending

from utils import (Logger, cleanup_images, database_housekeeping, grype_update,
                   startup_logins, stop_flag)

tasks_logger = Logger("tasks")


def tasks_thread():
    tasks_logger.info("Starting background tasks thread")
    startup_logins()
    while not stop_flag.is_set():
        run_pending()
        time.sleep(1)
    tasks_logger.info("exiting")


@repeat(every().day.at("00:00"))
def daily_image_cleanup():
    tasks_logger.info("Cleaning up images !")
    cleanup_images()


@repeat(every().day.at("23:00"))
def daily_database_housekeeping():
    tasks_logger.info("Cleaning up database !")
    database_housekeeping()


@repeat(every().day.at("22:00"))
def daily_gryp_db_update():
    tasks_logger.info("Updating grype !")
    ok, msg = grype_update()
    if not ok:
        tasks_logger.error('Unable to update grype: %s', msg)
    else:
        tasks_logger.info("Grype updated !")
