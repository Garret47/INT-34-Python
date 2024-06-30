import uvicorn
from fastapi import FastAPI
from handlers import router
import logging

HOST = '0.0.0.0'
PORT = 8080

app = FastAPI(docs_url=None, redoc_url=None)
logging.basicConfig(level=logging.DEBUG, datefmt='%d.%m.%Y %H:%M:%S',
                    format='[%(asctime)s] #%(levelname)- 5s - %(name)s - %(message)s'
                    )
logger = logging.getLogger(__name__)


def setup_app(application: FastAPI):
    application.include_router(router=router)


if __name__ == '__main__':
    try:
        setup_app(app)
        logger.info('Server Start')
        uvicorn.run(app, host=HOST, port=PORT)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.critical(f'Server error: {e}')
    finally:
        logger.info('Server Stop')
