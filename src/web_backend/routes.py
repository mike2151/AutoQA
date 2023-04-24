from flask import Blueprint, current_app
from db.jobs_util import create_new_job, get_job
import os
import sys
from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask.wrappers import Response

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from qa_tester.testing_utils import process_request  # noqa: E402
from qa_tester.job_queue_utils import JobQueue  # noqa: E402

bp = Blueprint('routes', __name__)
job_queue = JobQueue()
job_queue.start_workers()


@bp.route('/my_route')
def my_route():
    return 'Hello from my route!'


@bp.route('/', methods=['GET', 'POST'])
def hello() -> Response:
    if request.method == 'POST':
        url = request.form['url']
        instructions = request.form['instructions']
        job_res = create_new_job(url, instructions)
        job_id = job_res['job_id']
        job_queue.add_job(process_request, job_id, url, instructions)
        return redirect(url_for('routes.job', job_id=job_id))
    return render_template('index.html')


@bp.route('/job/<job_id>')
def job(job_id: str, methods=['GET']) -> Response:
    job_res = get_job(job_id)
    if 'error' in job_res:
        return render_template('error.html', error=job_res['error'])
    # get all screenshots for this job
    screenshot_directory = os.path.join(
        current_app.root_path, 'static/screenshots', job_id)
    image_urls = []
    if os.path.exists(screenshot_directory):
        png_files = sorted([f for f in os.listdir(
            screenshot_directory) if f.endswith('.png')])
        image_urls = [
            url_for(
                'routes.screenshots',
                job_id=job_id,
                filename=f) for f in png_files]
    return render_template('job.html', job=job_res, image_urls=image_urls)


@bp.route('/screenshots/<job_id>/<filename>')
def screenshots(job_id: str, filename: str) -> Response:
    directory = os.path.join(
        current_app.root_path,
        'static/screenshots',
        job_id)
    return send_from_directory(directory, filename)


def register_test_route(app):
    if app.config.get('TESTING', False):
        @app.route('/test')
        def test():
            return render_template('test/index.html')
