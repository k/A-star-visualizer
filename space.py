class Type(object):
    blocked = '0'
    regular = '1'
    rough = '2'
    highway_regular = 'A'
    highway_rough = 'B'
    highways = [highway_regular, highway_rough]


class Space(object):
    def __init__(self, coords, space_type='1'):
        self.coords = coords    # Should never change
        self.type = space_type  # Mutable

    def movement(self):
        # TODO: fill in rest of movement
        return 1.0

    def is_regular(self):
        return self.type is Type.regular

    def is_rough(self):
        return self.type is Type.rough

    def is_highway(self):
        return self.type in Type.highways

    def is_blocked(self):
        return self.type is Type.blocked

    def set_rough(self):
        self.type = Type.rough

    def set_blocked(self):
        self.type = Type.blocked

    def set_highway(self):
        if self.is_highway():
            raise Exception('There is already a highway here')
        elif self.is_blocked():
            raise Exception('Cannot build highway on blocked tile')
        elif self.is_rough():
            self.type = Type.highway_rough
        else:
            self.type = Type.highway_regular
