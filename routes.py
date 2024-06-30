from aiohttp import web
from handlers import check_healthz

NAME = 'healthz'


def setup_routes(application: web.Application):
    application.router.add_get('/' + NAME, check_healthz.get_healthz, name=NAME)
    application.router.add_get('/' + NAME+'/', check_healthz.redirect_healthz)

