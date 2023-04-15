'''
The purpose of this file is to provide a set of functions
 that can be used to manage a queue of jobs 
'''
import queue
import threading

class JobQueue:
    def __init__(self):
        self.job_queue = queue.Queue()
        self.workers = []

    def start_workers(self, num_workers=3):
        for i in range(num_workers):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            self.workers.append(t)

    def add_job(self, func, *args, **kwargs):
        job = (func, args, kwargs)
        self.job_queue.put(job)

    def worker(self):
        while True:
            job = self.job_queue.get()
            self.process_job(*job)
            self.job_queue.task_done()

    def process_job(self, func, args, kwargs):
        func(*args, **kwargs)

    def get_queue_size(self):
        return self.job_queue.qsize()

    def get_pending_jobs(self):
        return list(self.job_queue.queue)