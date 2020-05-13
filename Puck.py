import math
import sys


class Puck:
    """
    Puck class

    contains:
    puck number
    puck position (x,y)
    puck angle
    puck height
    """

    def __init__(self, number, position, angle, height=30):
        self.number = number
        self.set_number(number)
        self.set_position(position)
        self.set_angle(angle)
        self.set_height(height)


    def __eq__(self, other):
        if not isinstance(other, Puck):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.number == other.number

    def __str__(self):
        return 'puck #' + str(self.number)

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
        # Assume there is collision before otherwise is proven
        collision_list = [True]
        rotation = 0
        tries = 0
        retval = 0
        while True in collision_list:
            print("While loop")
            collision_list.clear()

            # Collision area:
            x1 = - 150
            x2 = 10
            y1 = - 67.5
            y2 = 67.5

            for puck in puck_list:
                if self.number != puck.number:
                    puck_pos = self.position
                    rotated_position = rotate(puck.position, puck_pos, - rotation)

                    collision = (x1 + puck_pos[0] < rotated_position[0] < x2 + puck_pos[0]) \
                                and (y1 + puck_pos[1] < rotated_position[1] < y2 + puck_pos[1])
                    print("collision:", collision)
                    collision_list.append(collision)
            if rotation > 180:
                retval = rotation - 360
            else:
                retval = rotation
            print("retval:", retval)

            rotation += 1
            print(rotation)
            tries += 1
            if tries > 360:  # Stop trying if every angle gives collision
                sys.exit(0)
        return retval  # Return the value that gave no collision


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
