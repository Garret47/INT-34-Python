from aiohttp import web
from handlers import check_healthz

REQUEST = '/healthz'


def setup_routes(application: web.Application):
    application.router.add_get(REQUEST, check_healthz.get_healthz, name='healthz')
    application.router.add_get(REQUEST+'/', check_healthz.redirect_healthz)
