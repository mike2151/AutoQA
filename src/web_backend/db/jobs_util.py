'''
File is responsible for handling the jobs table in the database.
'''

import random
import sqlite3

from flask import jsonify


def create_new_job():
    conn = sqlite3.connect('autoqa.db')
    cursor = conn.cursor()
    # create the jobs table if it doesn't exist yet
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs
                      (job_id INTEGER PRIMARY KEY,
                       status TEXT)''')
    job_id = random.randint(100000, 9999999)
    
    # insert a new row into the jobs table
    cursor.execute("INSERT INTO jobs (job_id, status) VALUES (?, 'pending')", (job_id,))
    conn.commit()
    conn.close()
    return jsonify({'job_id': job_id})