from invoke import task

@task
def run(c):
    c.run("python src/web_backend/app.py")

@task
def lint(c):
    c.run("flake8 src/")

@task
def lintfix(c):
    c.run("autopep8 --in-place --recursive --aggressive ./src/")