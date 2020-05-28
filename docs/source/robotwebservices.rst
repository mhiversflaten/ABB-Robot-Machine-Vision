.. _RobotWebServices:

Robot Web Services
==================

This section covers the communication between Python and *RobotWare*. A package, rwsuis_,
is pip installable and includes all functions provided in this section.

.. _rwsuis: https://pypi.org/project/rwsuis/

.. _RWS:

RWS Class
^^^^^^^^^

Take full control of ABB robots through HTTP requests, made easy with the RWS class.
Robot operating mode should be automatic.

::

    >>> robot = RWS.RWS(base_url='robot_IP', username='user', password='pass')
    >>> robot.request_mastership()
    >>> robot.motors_on()
    Robot motors turned on
    >>> robot.start_rapid()
    RAPID execution started from main

.. py:class:: RWS(base_url, username, password)

    .. py:method:: motors_on(self)

        Sends a request to turn the robot's motors on. Mastership is required.
        Prints a message to the console stating whether or not the motors were in fact turned on.

    .. py:method:: motors_off(self)

        Sends a request to turn the robot's motors off. Mastership is required.
        Prints a message to the console stating whether or not the motors were in fact turned off.

    .. py:method:: request_mastership(self)

        Requests mastership over controller in automatic mode.
        For mastership in manual mode, see :py:func:`request_rmmp`.

    .. py:method:: release_mastership(self)

        Releases mastership over controller.

    .. py:method:: request_rmmp(self)

        Requests RMMP (Request Manual Mode Privileges).
        The request needs to be accepted within 10 seconds on controller.
        For mastership in automatic mode, see :py:func:`request_mastership`.

    .. py:method:: cancel_rmmp(self)

        Cancels held or requested RMMP.

    .. py:method:: reset_pp(self)

        Resets RAPID program pointer to main procedure.
        Prints a message to the console stating whether or not the request was successful.

    .. py:method:: start_RAPID(self)

        Resets RAPID program pointer to main procedure, and starts RAPID execution.
        Prints a message to the console stating whether or not the request was successful.

    .. py:method:: stop_RAPID(self)

        Stops RAPID execution.
        Prints a message to the console stating whether or not the request was successful.

    .. py:method:: get_rapid_variable(self, var)

        Get the raw value of any variable in RAPID.

        :return: A number if RAPID variable is 'num'
        :return: A string if RAPID variable is not 'num'

    .. py:method:: set_rapid_variable(self, var, value)

        Sets the value of any variable in RAPID.
        Unless the variable is 'num', value has to be a string.

        :param str var: Name of variable as declared in RAPID
        :param value: Desired variable value
        :type value: int, float or str

    .. py:method:: set_robtarget_translation(self, var, trans)

        Sets only the translational data of a robtarget variable in RAPID.

        :param str var: Name of robtarget variable as declared in RAPID
        :param int[] trans: Translational data [x,y,z]

    .. py:method:: set_robtarget_rotation_z_degrees(self, var, rotation_z_degrees)

        Updates the orientation of a robtarget variable
        in RAPID by rotation about the z-axis in degrees.
        0 degrees gives the Quaternion [0,1,0,0].

        :param str var: Name of robtarget variable as declared in RAPID
        :param int rotation_z_degrees: Rotation in degrees

    .. py:method:: set_robtarget_rotation_quaternion(self, var, rotation_quaternion)

        Updates the orientation of a robtarget variable in RAPID by a Quaternion.

        :param str var: Name of robtarget variable as declared in RAPID
        :param tuple rotation_quaternion: Wanted robtarget orientation. Must be a Quaternion (tuple of length 4)

    .. py:method:: get_robtarget_variables(self, var)

        Gets translational and rotational data of a robtarget variable in RAPID

        :param str var: Name of robtarget variable as declared in RAPID

        :return: Translational data of robtarget [x,y,z]
        :return: Rotational data of robtarget (Quaternion: [w,x,y,z]).

    .. py:method:: get_gripper_position(self)

        Gets translational and rotational of the UiS tool 'tGripper'
        with respect to the work object 'wobjTableN'.

        :return: Translational data of gripper [x,y,z]
        :return: Rotational data of gripper (Quaternion: [w,x,y,z])

    .. py:method:: get_gripper_height(self)

        Uses :py:func:`get_gripper_position` to get the height of the UiS tool
        'tGripper' above the work object 'wobjTableN'.

    .. py:method:: set_rapid_array(self, var, value)

        Sets the values of a num array variable in RAPID.
        The length of the num array must match the length of the array from Python.

        :param str var: Name of variable as declared in RAPID.
        :param int[] value: Array to be sent to RAPID.

    .. py:method:: wait_for_rapid(self, var='ready_flag')

        Polls a boolean variable in RAPID every 0.1 seconds.
        When the variable is TRUE, Python resets it and continues.

        :param str var: Name of boolean variable as declared in RAPID.

    .. py:method:: set_zonedata(self, var, zonedata)

        Set the value for a zonedata variable in RAPID. Mastership is required.

        :param str var: Name of variable as declared in RAPID.
        :param int zonedata: desired zonedata value.

    .. py:method:: set_speeddata(self, var, speeddata)

        Set the value [int] for a speeddata variable in RAPID. Mastership is required.

        :param str var: Name of variable as declared in RAPID.
        :param int speeddata: Desired speeddata value.

    .. py:method:: set_speed_ratio(self, speed_ratio)

        Set the speed ratio of the robot. Mastership is required.
        speed_ratio: desired speed ratio in percent [1-100].

    .. py:method:: is_running(self)

        Uses :py:func:`get_execution_state` to check if RAPID execution is running or stopped.
        Returns True if running and False if stopped.

    .. py:method:: get_execution_state(self)

        Polls the RAPID execution state.

        :return: 'running' or 'stopped'







