from locust import HttpLocust, TaskSequence, task, between, seq_task, constant
import random
from requests.auth import HTTPDigestAuth


class UserBehavior(TaskSequence):
    """Used for testing communication between Python and RAPID (RobotWare) through the use of RobotWebServices
    and REST API"""

    def on_start(self):
        pass

    def on_stop(self):
        pass

    @seq_task(1)
    def motorson(self):
        """Turns the motors on"""
        payload = {'ctrl-state': 'motoron'}
        self.client.post("/rw/panel/ctrlstate?action=setctrlstate",
                         auth=HTTPDigestAuth(username='Default User', password='robotics'), data=payload)

    @seq_task(2)
    def motorsoff(self):
        """Turns the motors off"""
        payload = {'ctrl-state': 'motoroff'}
        self.client.post("/rw/panel/ctrlstate?action=setctrlstate&",
                         auth=HTTPDigestAuth(username='Default User', password='robotics'), data=payload)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior

    # Wait time between requests
    wait_time = constant(2)


"""To run the test, type the following in console: locust -f RobotWebServices/API_Benchmark/com_testing2.py
Open localhost:8089 to get to the http page to spawn users and decide spawn rate and address"""