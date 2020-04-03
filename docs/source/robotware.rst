RobotWare
=========

.. py:class:: RAPID(base_url, username, password)

    .. py:method:: motors_on(self)

        Turns the robot's motors on.

    .. py:method:: set_zonedata(self, var, zonedata)

        Set the value for a zonedata variable in RAPID. Mastership is required.
        var: name of variable as declared in RAPID.
        zonedata: desired zonedata value [int].

    .. py:method:: set_speeddata(self, var, speeddata)

        Set the value [int] for a speeddata variable in RAPID. Mastership is required.\
        var: name of variable as declared in RAPID.\
        speeddata: desired speeddata value [int].

    .. py:method:: set_speed_ratio(self, speed_ratio)

        :py:synopsis:`Set the speed ratio of the robot. Mastership is required.`
        speed_ratio: desired speed ratio in percent [1-100].

    .. py:method:: is_running(self)

        :py:synopsis:`Uses` :py:func:`get_execution_state` :py:synopsis:`if RAPID execution is running or stopped.`
        Returns True if running and False if stopped.

    .. py:method:: get_execution_state(self)

        :py:synopsis:`Returns RAPID execution state ('running' / 'stopped')`

    .. py:method:: get_execution_state(self)
        :classmethod:

        Testing difference






