'''
File is responsible for handling the jobs table in the database.
'''

import random
import sqlite3

from flask import jsonify


def create_new_job(url, instructions):
    conn = sqlite3.connect('autoqa.db')
    cursor = conn.cursor()
    # create the jobs table if it doesn't exist yet
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs
                      (job_id INTEGER PRIMARY KEY,
                       url TEXT,
                       instructions TEXT,
                       status TEXT)''')
    
    # insert a new row into the jobs table
    job_id = random.randint(100000, 9999999) 
    cursor.execute("INSERT INTO jobs (job_id, url, instructions, status) VALUES (?, ?, ?, 'pending')",
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
        'status': job[3]
    }
    
    # return the job as a JSON response
    return jsonify(job_dict)