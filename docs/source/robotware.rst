RobotWare
=========

.. py:function:: set_zonedata(self, var, zonedata)

    Set the value for a zonedata variable in RAPID. Mastership is required.
    var: name of variable as declared in RAPID.
    zonedata: desired zonedata value [int].

.. py:function:: set_speeddata(self, var, speeddata)

    |Set the value [int] for a speeddata variable in RAPID. Mastership is required.
    |var: name of variable as declared in RAPID.
    |speeddata: desired speeddata value [int].

.. py:function:: set_speed_ratio(self, speed_ratio)

    Set the speed ratio of the robot. Mastership is required.
    speed_ratio: desired speed ratio in percent [1-100].

.. py:function:: is_running(self)

    Uses get_execution_state if RAPID execution is running or stopped.
    Returns True if running and False if stopped.

.. py:function:: get_execution_state(self)

    Returns RAPID execution state ('running' / 'stopped')

.. py:classmethod:: get_execution_state(self)

    Testing difference






