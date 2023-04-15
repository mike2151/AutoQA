from invoke import task

@task
def run(c):
    c.run("python src/web_backend/app.py")