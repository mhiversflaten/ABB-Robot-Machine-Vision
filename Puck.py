import math


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
        while True in collision_list:
            print("While loop")
            collision_list.clear()
            for puck in puck_list:
                if self.number != puck.number:
                    puck_pos = self.position

                    # Collision area:
                    x1 = - 500
                    x2 = 0
                    y1 = - 150
                    y2 = 150
                    points = [(x1, y1), (x2, y2)]  # Rectangle

                    rotated_points = rotate(points=points, around_point=(0, 0), angle=rotation)
                    x1 = rotated_points[0][0]
                    x2 = rotated_points[1][0]
                    y1 = rotated_points[0][1]
                    y2 = rotated_points[1][1]
                    print(x1,x2,y1,y2)

                    collision = (x1 < puck.position[0] - puck_pos[0] < x2) \
                                and (y1 < puck.position[1] - puck_pos[1] < y2)
                    print("collision:", collision)
                    collision_list.append(collision)
            rotation += 180
            print(rotation)
            tries += 1
            if tries > 12:  # Stop trying if every angle gives collision
                return False
        if rotation > 180:
            rotation -= 360
        elif rotation < -180:
            rotation += 360
        return rotation - 30  # Return the value that gave no collision


def rotate(points, around_point, angle):
    """
    Rotate a list of point counterclockwise by a given angle around a given origin.

    The angle should be given in degrees.
    """
    rotated_points = []
    for point in points:
        angle = math.degrees(angle)
        ox, oy = around_point
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        rotated_points.append((qx, qy))
    return rotated_points
