'''
Comprehensive integration test for the entire flow of the application.
Will mock out Chat GPT. Tests on a basic webserver
'''
import multiprocessing
import os
import sys
import time
from unittest.mock import patch

from flask import url_for
from werkzeug.test import Client
from flask_testing import LiveServerTestCase

# TODO: Hack until I figure out how the fuck Python imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
web_backend_dir = os.path.join(parent_dir, 'web_backend')
qa_tester_dir = os.path.join(parent_dir, 'qa_tester')
sys.path.append(parent_dir)
sys.path.append(web_backend_dir)
sys.path.append(qa_tester_dir)
from web_backend.app import create_app  # noqa: E402
from web_backend.db.jobs_util import JobStatus, get_job  # noqa: E402

# needed for OSX
multiprocessing.set_start_method("fork")


class TestE2EFlow(LiveServerTestCase):
    def create_app(self):
        app = create_app(testing=True)
        self.client = Client(app, app.response_class)
        return app

    def get_mocked_llm_response(*args, **kwargs):
        url = args[2]
        url = url.replace('localhost', '127.0.0.1')
        return """```
# Test Output
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up options for headless mode
options = Options()
options.add_argument('--headless')

# Create a WebDriver instance with the options
driver = webdriver.Chrome(options=options)

# Navigate to the page
driver.get('{}')

# Find the link element using the By module
link = driver.find_element(By.XPATH, '//a[contains(text(), "Other")]')

# Click the link
link.click()

# Wait for the next page to load
driver.implicitly_wait(2)
driver.quit()```
        """.format(url)

    def test_my_function(self):
        with patch('qa_tester.testing_utils.get_llm_response', autospec=True, side_effect=self.get_mocked_llm_response):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertTrue("Auto QA" in response.data.decode('utf-8'))
            response = self.client.get('/test')
            self.assertEqual(response.status_code, 200)
            self.assertTrue("Other" in response.data.decode('utf-8'))

            test_route_url = self.get_server_url() + url_for('test')
            self.assertIsNotNone(test_route_url)
            test_instructions = 'Click the link on the page which takes you to the next page'

            response = self.client.post(
                '/',
                data={
                    "url": test_route_url,
                    "instructions": test_instructions},
                follow_redirects=False)
            redirect_url = response.headers['Location']
            self.assertTrue('job/' in redirect_url)

            # wait two seconds for the job to finish planning
            time.sleep(2)

            # get the job and check the selenium code planned
            job_id = redirect_url.split('/')[-1]
            job_res = get_job(job_id)
            self.assertTrue('Test Output' in job_res['llm_response'])

            # wait for selenium to finish
            time.sleep(4)
            job_res = get_job(job_id)

            self.assertEqual(job_res['status'], JobStatus.COMPLETED.value)

    def tearDown(self):
        super(TestE2EFlow, self).tearDown()


if __name__ == '__main__':
    LiveServerTestCase.main()
