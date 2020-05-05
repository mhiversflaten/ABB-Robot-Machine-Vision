from locust import HttpLocust, TaskSet, task, between
import random
from requests.auth import HTTPDigestAuth


class UserBehavior(TaskSet):
    def on_start(self):
        pass

    def on_stop(self):
        pass

    @task(1)
    def executionstate(self):
        self.client.get('/rw/rapid/execution?json=1', auth=HTTPDigestAuth(username='Default User', password='robotics'))

    """"@task(1)
    def motorson(self):
        payload = {'ctrl-state': 'motoron'}
        self.client.post("/rw/panel/ctrlstate?action=setctrlstate",
                         auth=HTTPDigestAuth(username='Default User', password='robotics'), data=payload)

    @task(1)
    def motorsoff(self):
        payload = {'ctrl-state': 'motoroff'}
        self.client.post("/rw/panel/ctrlstate?action=setctrlstate",
                         auth=HTTPDigestAuth(username='Default User', password='robotics'), data=payload)"""

    @task(1)
    def setrapidvariable(self):
        # TODO: test with both a set variable and also with a random variable, see any difference in timings?
        value = random.randint(0,100)
        locustvar = "locustvar"
        payload = {'value': value}
        self.client.post('/rw/rapid/symbol/data/RAPID/T_ROB1/' + locustvar + '?action=set',
                         auth=HTTPDigestAuth(username='Default User', password='robotics'), data=payload)

    @task(1)
    def getrapidvariable(self):
        locustvar = "locustvar"
        payload = {'value': 6}
        self.client.get('/rw/rapid/symbol/data/RAPID/T_ROB1/' + locustvar + ';value?json=1',
                        auth=HTTPDigestAuth(username='Default User', password='robotics'), data=payload)

    @task(1)
    def getgripperpos(self):
        self.client.get('/rw/motionsystem/mechunits/ROB_1/robtarget/?tool=tGripper&wobj=wobjTableN&coordinate=Wobj',
                        auth=HTTPDigestAuth(username='Default User', password='robotics'))

    @task(1)
    def setrobtarget(self):
        locustrobtarg = "locustrobtarg"
        payload = {'value': "[[0,0,100],[0,1,0,0],[-1,0,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]]"}
        self.client.post('/rw/rapid/symbol/data/RAPID/T_ROB1/' + locustrobtarg + '?action=set',
                         auth=HTTPDigestAuth(username='Default User', password='robotics'), data=payload)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(0.01, 0.015)


"""locust -f RobotWare/API_Benchmark/com_testing.py"""
