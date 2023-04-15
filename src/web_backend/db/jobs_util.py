'''
File is responsible for handling the jobs table in the database.
'''

import enum
import random
import sqlite3


class JobStatus(enum.Enum):
    PENDING = 'pending'
    PLANNING_QA = 'planning_qa'
    EXECUTING_QA = 'executing_qa'
    COMPLETED = 'completed'
    FAILED = 'failed'


def create_new_job(url: str, instructions: str) -> dict:
    conn = sqlite3.connect('autoqa.db')
    cursor = conn.cursor()
    # create the jobs table if it doesn't exist yet
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs
                      (job_id INTEGER PRIMARY KEY,
                       url TEXT,
                       instructions TEXT,
                       status TEXT,
                       llm_response TEXT,
                       selenium_code TEXT,
                       selenium_output TEXT)''')

    # insert a new row into the jobs table
    job_id = random.randint(100000, 9999999)
    cursor.execute("INSERT INTO jobs (job_id, url, instructions, status, llm_response, selenium_code, selenium_output) VALUES (?, ?, ?, 'pending', '', '', '')",
                   (job_id, url, instructions))
    conn.commit()
    conn.close()
    return {'job_id': str(job_id)}


def get_job(job_id: str) -> dict:
    conn = sqlite3.connect('autoqa.db')
    cursor = conn.cursor()

    # fetch the job with the given job_id from the jobs table
    cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
    job = cursor.fetchone()
    conn.close()

    if not job:
        return {'error': 'Job not found'}

    return {
        'job_id': str(job[0]),
        'url': job[1],
        'instructions': job[2],
        'status': job[3],
        'llm_response': job[4] if job[4] else '',
        'selenium_code': job[5] if job[5] else ''
    }


def update_job_status(job_id: str, new_status: JobStatus) -> None:
    conn = sqlite3.connect('autoqa.db')
    c = conn.cursor()

    # update the status of the job with the given ID
    c.execute("UPDATE jobs SET status = ? WHERE job_id = ?",
              (new_status.value, job_id))

    conn.commit()
    conn.close()


def update_job_response(job_id: str, llm_response: JobStatus) -> None:
    conn = sqlite3.connect('autoqa.db')
    cursor = conn.cursor()

    # update the llm_response column of the job with the given job_id
    cursor.execute(
        "UPDATE jobs SET llm_response=? WHERE job_id=?",
        (llm_response,
         job_id))

    conn.commit()
    conn.close()


def update_job_selenium_code(job_id: str, selenium_code: str) -> None:
    conn = sqlite3.connect('autoqa.db')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE jobs SET selenium_code = ? WHERE job_id = ?",
        (selenium_code,
         job_id))
    conn.commit()
    conn.close()


def update_selenium_output(job_id: str, output: str) -> None:
    conn = sqlite3.connect('autoqa.db')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE jobs SET selenium_output = ? WHERE job_id = ?", (output, job_id))
    conn.commit()
    conn.close()
