import os
import sys
from flask import Flask, redirect, render_template, request, url_for
import threading

from db.jobs_util import create_new_job, get_job

# TODO: Hack until I figure out how the fuck Python imports work 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from qa_tester.testing_utils import process_request

app = Flask(__name__)

def process_request_wrapper(job_id,url,instructions): 
     with app.app_context():
         process_request(job_id, url, instructions)
         

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        url = request.form['url']
        instructions = request.form['instructions']
        job_res = create_new_job(url, instructions)
        job_id = job_res.json['job_id']
        # TODO: start the QA in the background - this should be on a queue but just for MVP purposes
        threading.Thread(target=process_request_wrapper, args=(job_id, url, instructions)).start()
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