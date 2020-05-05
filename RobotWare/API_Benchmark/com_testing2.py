from locust import HttpLocust, TaskSequence, task, between, seq_task, constant
import random
from requests.auth import HTTPDigestAuth


class UserBehavior(TaskSequence):
    def on_start(self):
        pass

    def on_stop(self):
        pass

    @seq_task(1)
    def motorson(self):
        payload = {'ctrl-state': 'motoron'}
        self.client.post("/rw/panel/ctrlstate?action=setctrlstate",
                         auth=HTTPDigestAuth(username='Default User', password='robotics'), data=payload)

    @seq_task(2)
    def motorsoff(self):
        payload = {'ctrl-state': 'motoroff'}
        self.client.post("/rw/panel/ctrlstate?action=setctrlstate&",
                         auth=HTTPDigestAuth(username='Default User', password='robotics'), data=payload)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = constant(2)


"""locust -f RobotWare/API_Benchmark/com_testing.py"""
