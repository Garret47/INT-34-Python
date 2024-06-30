from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(prefix='/healthz')
templates = Jinja2Templates(directory='templates')


@router.get('', response_class=HTMLResponse)
async def get_healthz(request: Request):
    return templates.TemplateResponse(request=request, name='index.html', context={'msg': 'OK'})
