import aiohttp.web_request
import aiohttp_jinja2
from aiohttp import web
import logging

loger = logging.getLogger(__name__)


async def redirect_healthz(request: aiohttp.web_request.Request):
    location = request.app.router['healthz'].url_for()
    return web.HTTPFound(location=location)


@aiohttp_jinja2.template('index.html')
async def get_healthz(request: aiohttp.web_request.Request):
    loger.debug(f'request method: {request.method}, message: {request.message}')
    return {'msg': 'OK'}
