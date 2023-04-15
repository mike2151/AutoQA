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

@task
def test(c) -> None:
    c.run("python -m unittest discover -s src/tests")