from requests.auth import HTTPDigestAuth
from RobotWebServices import RWS

"""Script to easily turn the motors off, on Norbert"""

norbert = RWS.RWS()

norbert_url = 'http://152.94.0.38'
digest_auth = HTTPDigestAuth('Default User', 'robotics')

payload = {'ctrl-state': 'motoroff'}
resp = norbert.session.post(norbert_url + "/rw/panel/ctrlstate?action=setctrlstate", auth=digest_auth, data=payload)

if resp.status_code == 204:
    print("Robot motors turned off")
else:
    print("Could not turn off motors")