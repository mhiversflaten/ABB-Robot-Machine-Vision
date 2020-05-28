.. _Puck:

Puck Class
==========

.. py:class:: Puck(number, position, angle, height=30)

    .. py:method:: set_position(position)

        Updates :py:class:`Puck` position.

        :param float[] position: New :py:class:`Puck` position [x,y]

    .. py:method:: set_angle(angle)

        Updates :py:class:`Puck` angle.

        :param float[] angle: New :py:class:`Puck` angle

    .. py:method:: set_height(height)

        Updates :py:class:`Puck` height.

        :param float[] height: New :py:class:`Puck` height

    .. py:method:: get_xyz()

        Gets true position of :py:class:`Puck` ([x,y,z] on the work object).

        :returns: :py:class:`Puck` position [x,y,z]

    .. py:method:: check_collision(puck_list)

        Finds an angle of rotation for the gripper which avoids
        collisions between the gripper and other pucks
        when sliding in to pick up a puck.

        :param Puck[] puck_list: List of all :py:class:`Puck` objects

        :return: Rotation which yields no collision
        :return: If puck should be gripped forward or backward
