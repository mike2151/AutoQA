'''
File is responsible for handling the jobs table in the database.
'''

import enum
import random
import sqlite3

from flask import jsonify

class JobStatus(enum.Enum):
    PENDING = 'pending'
    PLANNING_QA = 'planning_qa'
    EXECUTING_QA = 'executing_qa'
    COMPLETED = 'completed'
    FAILED = 'failed'


def create_new_job(url, instructions):
    conn = sqlite3.connect('autoqa.db')
    cursor = conn.cursor()
    # create the jobs table if it doesn't exist yet
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs
                      (job_id INTEGER PRIMARY KEY,
                       url TEXT,
                       instructions TEXT,
                       status TEXT,
                       llm_response TEXT)''')
    
    # insert a new row into the jobs table
    job_id = random.randint(100000, 9999999) 
    cursor.execute("INSERT INTO jobs (job_id, url, instructions, status, llm_response) VALUES (?, ?, ?, 'pending', '')",
                   (job_id, url, instructions))
    conn.commit()
    conn.close()
    return jsonify({'job_id': job_id})

def get_job(job_id):
    conn = sqlite3.connect('autoqa.db')
    cursor = conn.cursor()
    
    # fetch the job with the given job_id from the jobs table
    cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
    job = cursor.fetchone()
    conn.close()
    
    if not job:
        return jsonify({'error': 'Job not found'})
    
    # create a dictionary to hold the job data
    job_dict = {
        'job_id': job[0],
        'url': job[1],
        'instructions': job[2],
        'status': job[3],
        'llm_response': job[4] if job[4] else ''
    }
    
    # return the job as a JSON response
    return jsonify(job_dict)

def update_job_status(job_id, new_status : JobStatus):
    conn = sqlite3.connect('autoqa.db')
    c = conn.cursor()
    
    # update the status of the job with the given ID
    c.execute("UPDATE jobs SET status = ? WHERE job_id = ?", (new_status.value, job_id))
    
    conn.commit()
    conn.close()

def update_job_response(job_id, llm_response):
    conn = sqlite3.connect('autoqa.db')
    cursor = conn.cursor()

    # update the llm_response column of the job with the given job_id
    cursor.execute("UPDATE jobs SET llm_response=? WHERE job_id=?", (llm_response, job_id))

    conn.commit()
    conn.close()