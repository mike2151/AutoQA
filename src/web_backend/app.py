import random
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        # todo: hook this up to a backend but for now we do a temporary redirect
        job_id = random.randint(0, 1000000)
        return redirect(url_for('job', job_id=job_id))
    return render_template('index.html')

@app.route('/job/<job_id>')
def job(job_id):
    return render_template('job.html', job_id=job_id)

if __name__ == '__main__':
    app.run()