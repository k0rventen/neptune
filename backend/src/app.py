"""main module"""
import threading

from uvicorn import Config

import api
from models import create_db
from tasks import tasks_thread
from utils import APIServer, Logger, grype_update,startup_logins

logger = Logger("main")

if __name__ == "__main__":
    logger.info('starting Neptune !')
    create_db()

    logger.info('Updating grype DB!')
    grype_update()
    startup_logins()

    threading.Thread(target=tasks_thread).start()
    server_config = Config(api.neptune_api, host="0.0.0.0", port=5000)
    server = APIServer(server_config)
    server.run()
