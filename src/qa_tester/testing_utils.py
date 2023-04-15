import re
import string
import requests
import os
import sys
import openai
# TODO: Hack until I figure out how the fuck Python imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from web_backend.db.jobs_util import JobStatus, update_job_status, get_job, update_job_response

def format_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        # URL already starts with http:// or https://, so return it as is
        return url
    else:
        # URL doesn't start with http:// or https://, so prepend http:// and return it
        return 'http://' + url

def extract_code_from_chat_gpt(prompt):
    pattern = r"```python(.+?)```"
    match = re.search(pattern, string, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None

def process_request(job_id, url, instructions):
    job = get_job(job_id).json
    if job['status'] == JobStatus.PENDING.value:
        update_job_status(job_id, JobStatus.PLANNING_QA)
        # TODO: secure this
        openai.organization = os.environ.get("OPENAI_ORG")
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        # TODO: (we will assume that we have one iteration of QA for now)
        properly_formed_url = format_url(url)
        response = requests.get(properly_formed_url)
        if response.status_code == 200:
            html = response.content
        else:
            # TODO: add error message to jobs table
            update_job_status(job_id, JobStatus.FAILED)
            return

        prompt = 'Write selenium code to "{}" from the page "{}" for the following HTML code: ```{}```'.format(instructions, url, html)

        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "assistant", "content": prompt}]
        )
        llm_response = chat.choices[0].message['content']
        update_job_response(job_id, llm_response)
        raw_code = extract_code_from_chat_gpt(llm_response)
        print(raw_code)
        # once we get selenium response we can set to executing
        update_job_status(job_id, JobStatus.EXECUTING_QA)
    
    job = get_job(job_id).json
    if job['status'] == JobStatus.EXECUTING_QA.value: 
        pass
