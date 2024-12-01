import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTask

from sssite.providers import GCSProvider
from sssite.version import __version__

from .config import SsiteConfig

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(version=__version__, title="Simple Storage Site")
conf = SsiteConfig()
provider = GCSProvider(conf)
templates = Jinja2Templates(directory=conf.resource_dir)


@app.get("/version", description="Get version")
async def get_api_version():
    return __version__


@app.get("/", description="Build List", response_class=HTMLResponse)
async def load_index(request: Request):
    files = provider.list_files()
    return templates.TemplateResponse(
        request=request,
        name="index.html.j2",
        context={"name": conf.name, "pages": files},
    )


app.mount(
    "/static", StaticFiles(directory=conf.local_storage_path, html=True), name="static"
)


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: Exception):
    request_path = request.url.path
    if request_path.startswith("/static"):
        page_name = request_path.replace("/static", "")
        return templates.TemplateResponse(
            request=request,
            name="reloading-404.html.j2",
            context={"name": page_name},
            background=BackgroundTask(provider.sync, page_name),
        )
    return HTMLResponse("<h1>404 Page</h1>", status_code=404)
