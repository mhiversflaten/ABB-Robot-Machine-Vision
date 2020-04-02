from requests.auth import HTTPDigestAuth
from requests import Session
import xml.etree.ElementTree as ET
import ast
import time
import json

# Address used to organize ET elements
namespace = '{http://www.w3.org/1999/xhtml}'


class RAPID:
    """Class for communicating with RobotWare through Robot Web Services (Rest API)"""

    def __init__(self, base_url='http://152.94.0.38', username='Default User', password='robotics'):
        """
        Initializes connection between Python and RobotWare (RAPID)

        :param base_url: the robots IP-address
        :param username: the robots username
        :param password: the robots password
        """

        self.base_url = base_url
        self.username = username
        self.password = password
        self.digest_auth = HTTPDigestAuth(self.username, self.password)
        # create persistent HTTP communication
        self.session = Session()

    def request_rmmp(self, timeout=5):
        """
        Request RMMP

        :param timeout: seconds before timeout (?) - ask markus
        :return: http response
        """
        t1 = time.time()
        resp = self.session.post(self.base_url + '/users/rmmp', auth=self.digest_auth, data={'privilege': 'modify'})

        return resp

    def cancel_rmmp(self):
        """
        Cancel RMMP

        :return: http response
        """
        resp = self.session.post(self.base_url + '/users/rmmp?action=cancel', auth=self.digest_auth)

        return resp

    def motors_on(self):
        """
        Turn motors on

        :return: printed message, *motors turned on* or *could not turn on motors*
        """
        payload = {'ctrl-state': 'motoron'}
        resp = self.session.post(self.base_url + "/rw/panel/ctrlstate?action=setctrlstate",
                                 auth=self.digest_auth, data=payload)

        if resp.status_code == 204:
            print("Robot motors turned on")
        else:
            print("Could not turn on motors. The controller might be in manual mode")

    def motors_off(self):
        """
        Turn motors off

        :return: printed message, *motors turned off* or *could not turn off motors*
        """
        payload = {'ctrl-state': 'motoroff'}
        resp = self.session.post(self.base_url + "/rw/panel/ctrlstate?action=setctrlstate",
                                 auth=self.digest_auth, data=payload)

        if resp.status_code == 204:
            print("Robot motors turned off")
        else:
            print("Could not turn off motors")

    def reset_pp(self):
        """
        Resets program pointer in RAPID

        :return: printed message, *program pointer reset to main* or *could not reset program pointer to main*
        """
        # Resets program pointer in RAPID
        resp = self.session.post(self.base_url + '/rw/rapid/execution?action=resetpp', auth=self.digest_auth)
        if resp.status_code == 204:
            print('Program pointer reset to main')
        else:
            print('Could not reset program pointer to main')

    def start_RAPID(self):
        """
        Resets program pointer to main and starts RAPID execution

        :return: printed message, *RAPID execution started* or *could not start RAPID*
        """
        self.reset_pp()
        payload = {'regain': 'continue', 'execmode': 'continue', 'cycle': 'once', 'condition': 'none',
                   'stopatbp': 'disabled', 'alltaskbytsp': 'false'}
        resp = self.session.post(self.base_url + "/rw/rapid/execution?action=start",
                                 auth=self.digest_auth, data=payload)
        if resp.status_code == 204:
            print("RAPID execution started")
        else:
            print("Could not start RAPID, maybe motors are turned off")

    def stop_RAPID(self):
        """
        Stops RAPID execution

        :return: printed message, *RAPID execution stopped* or *could not stop RAPID*
        """
        payload = {'stopmode': 'stop', 'usetsp': 'normal'}
        resp = self.session.post(self.base_url + "/rw/rapid/execution?action=stop", auth=self.digest_auth, data=payload)
        print(resp)
        if resp.status_code == 204:
            print('RAPID execution stopped')
        else:
            print('Could not stop RAPID execution')

    def get_execution_state(self):
        """
        GET request to receive execution state

        :return: execution state
        """
        resp = self.session.get(self.base_url + "/rw/rapid/execution?json=1", auth=self.digest_auth)
        json_string = resp.text
        _dict = json.loads(json_string)
        data = _dict["_embedded"]["_state"][0]["ctrlexecstate"]
        return data

    def is_running(self):
        """
        Check if execution state is running

        :return: boolean
        """
        execution_state = self.get_execution_state()
        if execution_state == "running":
            return True
        else:
            return False

    def set_speed_ratio(self, speed_ratio):
        """
        POST request to update/set the speed ratio

        :param speed_ratio: speed ratio wanted
        :return: printed message, *set speed ratio to ...* or *could not set speed ratio*
        """
        payload = {'speed-ratio': speed_ratio}
        resp = self.session.post(self.base_url + "/rw/panel/speedratio?action=setspeedratio", auth=self.digest_auth,
                                 data=payload)
        if resp.status_code == 204:
            print(f'Set speed ratio to {speed_ratio}%')
        else:
            print('Could not set speed ratio!')

    def set_zonedata(self, var, zonedata):
        """
        POST request to update/set the zone data

        :param var: variable name
        :param zonedata: zone data wanted
        :return: printed message, *set *var* zonedata to *zonedata** or *could not set zonedata*
        """
        if zonedata not in ['fine', 0, 1, 5, 10, 20, 30, 40, 50, 60, 80, 100, 150, 200]:
            print("You have entered false zonedata! Please try again")
            return
        else:
            if zonedata in [10, 20, 30, 40, 50, 60, 80, 100, 150, 200]:
                value = f'[FALSE, {zonedata}, {zonedata * 1.5}, {zonedata * 1.5}, {zonedata * 0.15}, ' \
                        f'{zonedata * 1.5}, {zonedata * 0.15}]'
            elif zonedata == 0:
                value = f'[FALSE, {zonedata + 0.3}, {zonedata + 0.3}, {zonedata + 0.3}, {zonedata + 0.03}, ' \
                        f'{zonedata + 0.3}, {zonedata + 0.03}]'
            elif zonedata == 1:
                value = f'[FALSE, {zonedata}, {zonedata}, {zonedata}, {zonedata * 0.1}, {zonedata}, {zonedata * 0.1}]'
            elif zonedata == 5:
                value = f'[FALSE, {zonedata}, {zonedata * 1.6}, {zonedata * 1.6}, {zonedata * 0.16}, ' \
                        f'{zonedata * 1.6}, {zonedata * 0.16}]'
            else:  # zonedata == 'fine':
                value = f'[TRUE, {0}, {0}, {0}, {0}, {0}, {0}]'

        resp = self.set_rapid_variable(var, value)
        if resp.status_code == 204:
            print(f'Set \"{var}\" zonedata to z{zonedata}')
        else:
            print('Could not set zonedata! Check that the variable name is correct')

    def set_speeddata(self, var, speeddata):
        """
        POST request to update/set the speed data

        :param var: variable name
        :param speeddata: speed data wanted
        :return: printed message, *set *var* speed data to *speeddata** or *could not set speeddata*
        """
        resp = self.set_rapid_variable(var, f'[{speeddata},500,5000,1000]')
        if resp.status_code == 204:
            print(f'Set \"{var}\" speeddata to v{speeddata}')
        else:
            print('Could not set speeddata. Check that the variable name is correct')

    def set_rapid_variable(self, var, value):
        """
        POST request to update variables in RAPID

        :param var: variable name
        :param value: value wanted
        :return: http response
        """
        payload = {'value': value}
        resp = self.session.post(self.base_url + '/rw/rapid/symbol/data/RAPID/T_ROB1/' + var + '?action=set',
                                 auth=self.digest_auth, data=payload)
        return resp

    def get_rapid_variable(self, var):
        """
        GET request to receive value from variable in RAPID

        :param var: variable name
        :return: the value of the specified variable
        """
        resp = self.session.get(self.base_url + '/rw/rapid/symbol/data/RAPID/T_ROB1/' + var + ';value?json=1',
                                auth=self.digest_auth)
        json_string = resp.text
        _dict = json.loads(json_string)
        value = _dict["_embedded"]["_state"][0]["value"]
        return value

    def set_robtarget_variables(self, var, trans):
        """
        Calls the function *set_rapid_variable*, manipulated to be able to update robtargets

        :param var: robtarget name
        :param trans: [x, y, z] coordinates
        :return: http response
        """
        resp = self.set_rapid_variable(var, "[[" + ','.join(
            [str(s) for s in trans]) + "],[0, 1, 0, 0],[-1,0,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]]")

        return resp

    def get_robtarget_variables(self, var):
        """
        GET request to receive value from robtarget in RAPID

        :param var: robtarget name
        :return: translation [x, y, z] and rotation [C, X*S, Y*S, Z*S]
        """
        resp = self.session.get(self.base_url + '/rw/rapid/symbol/data/RAPID/T_ROB1/' + var + ';value?json=1',
                                auth=self.digest_auth)
        json_string = resp.text
        _dict = json.loads(json_string)
        data = _dict["_embedded"]["_state"][0]["value"]
        data_list = ast.literal_eval(data)  # Convert the pure string from data to list
        trans = data_list[0]  # Get x,y,z from robtarget relative to work object (table)
        rot = data_list[1]  # Get orientation of robtarget
        
        return trans, rot

    def get_gripper_position(self):
        """
        GET request to receive gripper position

        :return: translation [x, y, z] and rotation [C, X*S, Y*S, Z*S] of the gripper tool
        """
        resp = self.session.get(self.base_url +
                                '/rw/motionsystem/mechunits/ROB_1/robtarget/?tool=tGripper&wobj=wobjTableN&coordinate=Wobj',
                                auth=self.digest_auth)

        root = ET.fromstring(resp.text)

        if root.findall(".//{0}li[@class='ms-robtargets']".format(namespace)):
            data = root.findall(".//{0}li[@class='ms-robtargets']/{0}span".format(namespace))
            # Extract translation data
            x = int(float(data[0].text))
            y = int(float(data[1].text))
            z = int(float(data[2].text))
            trans = [x, y, z]

            # Extract rotation data
            a = float(data[3].text)
            b = float(data[4].text)
            c = float(data[5].text)
            d = float(data[6].text)
            rot = [a, b, c, d]

            return trans, rot

    def get_gripper_height(self):
        """
        GET request to receive gripper height

        :return: gripper height
        """
        trans, rot = self.get_gripper_position()
        height = trans[2]

        return height

    def set_rapid_array(self, var, values):
        """
        Calls the function *set_rapid_variable*, manipulated to be able to update arrays

        :param var: array/variable name
        :param values: wanted values as array
        :return: http response
        """

        resp = self.set_rapid_variable(var, "[" + ','.join([str(s) for s in values]) + "]")

        return resp

    def wait_for_rapid(self):
        """
        Wait for RAPID to finish some instruction

        :return: nothing
        """
        while self.get_rapid_variable('ready_flag') == "FALSE" and self.is_running():
            time.sleep(0.1)
        self.set_rapid_variable('ready_flag', "FALSE")
