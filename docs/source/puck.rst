.. _Puck:

Puck Class
==========

.. py:class:: Puck(number, position, angle, height=30)

    .. py:method:: check_collision(puck_list)

        Finds an angle of rotation for the gripper which avoids
        collisions between the gripper and other pucks
        when sliding in to pick up a puck.

        :param Puck[] puck_list: List of all :py:class:`Puck` objects

        :return: Rotation which yields no collision
        :return: If puck should be gripped forward or backward
