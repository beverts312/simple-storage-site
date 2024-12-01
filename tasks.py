import os

from invoke import task


def get_project_root():
    return os.path.dirname(os.path.realpath(__file__))


@task(aliases=["sd"])
def serve_docs(c):
    with c.cd(f"{get_project_root()}"):
        c.run("mkdocs serve")


@task(aliases=["f"])
def format(c):
    c.run("isort .")
    return c.run("black .")


@task(aliases=["cf"])
def check_format(c):
    return c.run("black . --check")


@task(aliases=["dev"])
def run_server(c):
    with c.cd(f"{get_project_root()}"):
        c.run("fastapi dev ./ssite/app.py")
