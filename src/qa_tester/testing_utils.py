from web_backend.db.jobs_util import JobStatus, update_job_status, get_job, update_job_response
import os
import sys
import openai

# TODO: Hack until I figure out how the fuck Python imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


def process_request(job_id, url, instructions):
    job = get_job(job_id).json
    if job['status'] == JobStatus.PENDING.value:
        update_job_status(job_id, JobStatus.PLANNING_QA)
        # TODO: secure this
        openai.organization = os.environ.get("OPENAI_ORG")
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "assistant", "content": "Can you say the word hello?"}]
        )
        llm_response = chat.choices[0].message['content']
        update_job_response(job_id, llm_response)
        # once we get LLM response we can set to executing
        update_job_status(job_id, JobStatus.EXECUTING_QA)
