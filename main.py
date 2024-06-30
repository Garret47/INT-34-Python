import jinja2
from aiohttp import web
import aiohttp_jinja2
import logging
from routes import setup_routes

HOST = '0.0.0.0'
PORT = 8080
logging.basicConfig(level=logging.DEBUG, datefmt='%d.%m.%Y %H:%M:%S',
                    format='[%(asctime)s] #%(levelname)- 5s - %(name)s - %(message)s'
                    )
logger = logging.getLogger(__name__)


def setup_app(application: web.Application) -> None:
    setup_routes(application)
    aiohttp_jinja2.setup(application, loader=jinja2.FileSystemLoader('templates'))


if __name__ == '__main__':
    try:
        app = web.Application()
        setup_app(app)
        logger.info('Server Start')
        web.run_app(app, host=HOST, port=PORT)
        logger.info('Server Stop')
    except Exception as e:
        logger.critical(f'Server error: {e}')
