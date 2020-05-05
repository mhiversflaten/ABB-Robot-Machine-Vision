from locust import HttpLocust, TaskSet, task, between
import requests
from requests.auth import HTTPDigestAuth


class UserBehavior(TaskSet):
    def on_start(self):
        pass

    def on_stop(self):
        pass

    @task(1)
    def executionstate(self):
        self.client.get('/rw/rapid/execution?json=1', auth=HTTPDigestAuth(username='Default User', password='robotics'))

    @task(1)
    def startrapid(self):
        payload = {'ctrl-state': 'motoron'}
        self.client.post("/rw/panel/ctrlstate?action=setctrlstate",
                         auth=HTTPDigestAuth(username='Default User', password='robotics'), data=payload)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(0.05, 0.1)


"""locust -f RobotWare/API_Benchmark/com_testing.py"""
