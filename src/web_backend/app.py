from db.jobs_util import create_new_job, get_job
import os
import sys
from flask import Flask
from routes import bp
from web_backend.routes import register_test_route

# TODO: Hack until I figure out how the fuck Python imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from qa_tester.testing_utils import process_request  # noqa: E402
from qa_tester.job_queue_utils import JobQueue  # noqa: E402


def create_app(testing=False):
    app = Flask(__name__)
    app.config['TESTING'] = testing
    app.register_blueprint(bp)
    register_test_route(app)
    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        app.run(debug=True)
