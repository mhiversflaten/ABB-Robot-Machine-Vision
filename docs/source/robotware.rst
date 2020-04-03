RobotWare
=========

.. py:class:: RAPID(base_url, username, password)

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

        Resets RAPID program pointer to main procedure, and :warning:`starts RAPID execution`.
        Prints a message to the console stating whether or not the request was successful.

    .. py:method:: stop_RAPID(self)

        Stops RAPID execution.
        Prints a message to the console stating whether or not the request was successful.

    .. py:method:: set_zonedata(self, var, zonedata)

        Set the value for a zonedata variable in RAPID. Mastership is required.
        var: name of variable as declared in RAPID.
        zonedata: desired zonedata value [int].

    .. py:method:: set_speeddata(self, var, speeddata)

        Set the value [int] for a speeddata variable in RAPID. Mastership is required.

        :param str var: Name of variable as declared in RAPID.
        :param intspeeddata: Desired speeddata value [int].

    .. py:method:: set_speed_ratio(self, speed_ratio)

        Set the speed ratio of the robot. Mastership is required.
        speed_ratio: desired speed ratio in percent [1-100].

    .. py:method:: is_running(self)

        Uses :py:func:`get_execution_state` :py:synopsis:if RAPID execution is running or stopped.
        Returns True if running and False if stopped.

    .. py:method:: get_execution_state(self)

        Returns RAPID execution state ('running' / 'stopped')

    .. py:method:: get_execution_state(self)
        :classmethod:

        Testing difference






