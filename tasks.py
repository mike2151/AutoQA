from invoke import task

@task
def run(c) -> None:
    c.run("python src/web_backend/app.py")

@task
def lint(c) -> None:
    c.run("flake8 src/")

@task
def lintfix(c) -> None:
    c.run("autopep8 --in-place --recursive --aggressive ./src/")
    c.run("python3 tidy_html.py ./src")

@task
def test(c) -> None:
    c.run("pytest")

@task
def clean(c) -> None:
    c.run("rm -rf src/web_backend/static/screenshots")
    c.run("rm ./autoqa.db")
    c.run("find . -type d -name '__pycache__' -exec rm -r {} +")