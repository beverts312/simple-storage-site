import logging

from fastapi import FastAPI

from ssite.version import __version__

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(version=__version__, title="Simple Storage Site")


@app.get("/version", description="Get version")
async def get_api_version():
    return __version__
