from flask import Flask, redirect, render_template, request, url_for

from db.jobs_util import create_new_job, get_job

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        job_res = create_new_job(request.form['url'], request.form['instructions'])
        job_id = job_res.json['job_id']
        return redirect(url_for('job', job_id=job_id))
    return render_template('index.html')

@app.route('/job/<job_id>')
def job(job_id, methods=['GET']):
    job_res = get_job(job_id).json
    if 'error' in job_res:
        return render_template('error.html', error=job.json['error'])
    return render_template('job.html', job=job_res)

if __name__ == '__main__':
    app.run()