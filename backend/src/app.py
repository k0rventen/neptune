"""main module"""
import threading

from uvicorn import Config

import api
from models import create_db
from tasks import tasks_thread
from utils import APIServer, Logger, grype_update,startup_logins, DEV_MODE
import uvicorn

logger = Logger("main")

if __name__ == "__main__":
    logger.info(f'starting Neptune  {"(dev mode)" if DEV_MODE else ""} !')
    create_db()

    logger.info('Updating grype DB..')
    grype_update()

    logger.info('login in known registries..')
    startup_logins()

    threading.Thread(target=tasks_thread).start()
    if DEV_MODE:
        uvicorn.run("app:api.neptune_api", host="0.0.0.0", port=5000,reload=True)
    else:
        server_config = Config(api.neptune_api, host="0.0.0.0", port=5000)
        server = APIServer(server_config)
        server.run()
