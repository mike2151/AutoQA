import os
import sys

# TODO: Hack until I figure out how the fuck Python imports work 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from web_backend.db.jobs_util import JobStatus, update_job_status


def process_request(job_id, url, instructions):
    update_job_status(job_id, JobStatus.PLANNING_QA)