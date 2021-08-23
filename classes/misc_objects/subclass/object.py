class Object(object):
    x = 0
    y = 0
    state = ""
    image = ""
    iter = 0

    def __init__(self):
        self.state = "Idle"
    
    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def get_pos(self):
        return (self.x, self.y)

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state