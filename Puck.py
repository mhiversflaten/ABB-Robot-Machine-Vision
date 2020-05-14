import math
import sys


class Puck:

    """
    Puck class

    contains:
    puck number
    puck position (x,y)
    puck angle
    puck QR width
    puck height
    """

    def __init__(self, number, position, angle, qr_width, height=30):
        self.number = number
        self.set_number(number)
        self.set_position(position)
        self.set_angle(angle)
        self.qr_width = qr_width
        self.set_height(height)

    def __eq__(self, other):
        if not isinstance(other, Puck):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.number == other.number

    def __str__(self):
        return 'Puck #' + str(self.number)

    def set_position(self, position):
        try:
            position = list(position)
            if len(position) == 2:
                self.position = position
            else:
                raise TypeError
        except TypeError:
            print("Position has to be a list of [x, y]")

    def set_angle(self, angle):
        try:
            angle = float(angle)
            self.angle = angle
        except TypeError:
            print("Puck angle has to be a number")
        if angle > 180:
            self.angle -= 360
        elif angle < -180:
            self.angle += 360

    def set_height(self, height):
        try:
            height = int(height)
            self.height = height
        except TypeError:
            print("Puck height has to be an integer")

    def set_number(self, number):
        try:
            number = int(number)
            self.number = number
        except TypeError:
            print("Puck number has to be an integer")

    def get_xyz(self):
        return self.position + [self.height - 30]

    def check_collision(self, puck_list):
        """
        To pick up pucks, the gripper slides in towards them.
        This path must be clear of any other pucks, so that no collisions occur.

        Depending on the positions of all other pucks,
        this path is rotated around the puck until a clear path is found.
        """

        collision_list = [True]  # Assume there is collision before otherwise is proven
        rotation = 0  # Current rotation in degrees
        tries = 0  # Amount of tries to avoid collision
        retval = 0  # Rotation which will avoid collision
        forward_grip = True  # Slide in forward or backward toward puck

        # Collision area/path (rectangle):
        x1 = - 95
        x2 = 30
        y1 = - 67.5
        y2 = 67.5

        while True in collision_list:  # While there is still at least one collision

            collision_list.clear()

            for other_puck in puck_list:
                if self.number != other_puck.number:
                    puck_pos = self.position

                    # Rotate every puck around current puck (self)
                    # Instead of rotating the path in relation to the puck,
                    # the other pucks are rotated around the puck until they no longer appear inside the path.
                    # This means the rotation has to be equal and opposite.
                    rotated_position = rotate(other_puck.position, puck_pos, - rotation)

                    # Check if any pucks block the path
                    collision = (x1 + puck_pos[0] < rotated_position[0] < x2 + puck_pos[0]) \
                                and (y1 + puck_pos[1] < rotated_position[1] < y2 + puck_pos[1])

                    # Gather all results in list
                    collision_list.append(collision)

            # Maximum rotation is 180 degrees (+/-)
            if rotation > 180:
                retval = rotation - 360
            else:
                retval = rotation

            # If the gripper must rotate more than 90 degrees (+/-),
            # then it should instead slide in toward the puck backward.
            # This is done by doing a "180" with the gripper.
            if retval > 90:
                retval -= 180
                forward_grip = False  # Backward grip
            elif retval < -90:
                retval += 180
                forward_grip = False  # Backward grip

            rotation += 1
            tries += 1

            if tries > 360:  # Stop trying if every angle gives collision
                sys.exit(0)  # TODO: add better handling here
        return retval, forward_grip  # Return the value that gave no collision


def rotate(point, about_point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in degrees.
    """
    angle = math.radians(angle)

    ox, oy = about_point
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    rotated_point = (qx, qy)

    return rotated_point
