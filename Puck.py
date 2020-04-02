class Puck:
    """
    Puck class

    contains:
    puck number
    puck position
    puck angle
    puck height
    TEST
    """

    def __init__(self, number, position, angle, height=0):
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
        return self.position + [self.height]
