import time

from schedule import every, repeat, run_pending

from utils import (Logger, cleanup_images, database_housekeeping, grype_update, create_statistics,
                   startup_logins, stop_flag)

tasks_logger = Logger("tasks")


def tasks_thread():
    tasks_logger.info("Starting background tasks thread")
    startup_logins()
    while not stop_flag.is_set():
        run_pending()
        time.sleep(1)
    tasks_logger.info("exiting")


@repeat(every(1).minute)
def daily_statistics():
    create_statistics()


@repeat(every().day.at("23:00"))
def daily_housekeeping():
    database_housekeeping()
    cleanup_images()


@repeat(every().day.at("22:00"))
def daily_grype_db_update():
    grype_update()

def 