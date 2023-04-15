from flask import Flask, redirect, render_template, request, url_for

from db.jobs_util import create_new_job

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        job_res = create_new_job(request.form['url'], request.form['instructions'])
        job_id = job_res.json['job_id']
        return redirect(url_for('job', job_id=job_id))
    return render_template('index.html')

@app.route('/job/<job_id>')
def job(job_id):
    return render_template('job.html', job_id=job_id)

if __name__ == '__main__':
    app.run()