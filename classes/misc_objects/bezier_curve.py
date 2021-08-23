import math

class BezierCurve(object):
    start_pnt = 0
    start_ctrl = 0
    end_pnt = 0
    end_ctrl = 0

    t = 0
    t_increment = 0.0065

    prev_x = 0
    prev_y = 0
    prev_t = 0

    exit_bool = False

    def __init__(self, s_pnt, s_ctrl, e_pnt, e_ctrl):
        self.start_pnt = s_pnt
        self.start_ctrl = s_ctrl
        self.end_pnt = e_pnt
        self.end_ctrl = e_ctrl

    def __copy__(self):
        return BezierCurve(self.start_pnt, self.start_ctrl, self.end_pnt, self.end)

    def calculate_point(self):
        if self.t < 1:
            curr_point_x = math.pow((1-self.t), 3)*self.start_pnt[0] + 3*math.pow((1-self.t),2)*self.t*self.start_ctrl[0] + 3*(1-self.t)*math.pow(self.t,2)*self.end_pnt[0] + math.pow(self.t,3)*self.end_ctrl[0]
            curr_point_y = math.pow((1-self.t), 3)*self.start_pnt[1] + 3*math.pow((1-self.t),2)*self.t*self.start_ctrl[1] + 3*(1-self.t)*math.pow(self.t,2)*self.end_pnt[1] + math.pow(self.t,3)*self.end_ctrl[1]
            self.t += self.t_increment
            return [curr_point_x, curr_point_y]
        return [0, 0]

    def peek_calculated_point(self):
        if self.t < 1:
            curr_point_x = math.pow((1-self.t), 3)*self.start_pnt[0] + 3*math.pow((1-self.t),2)*self.t*self.start_ctrl[0] + 3*(1-self.t)*math.pow(self.t,2)*self.end_pnt[0] + math.pow(self.t,3)*self.end_ctrl[0]
            curr_point_y = math.pow((1-self.t), 3)*self.start_pnt[1] + 3*math.pow((1-self.t),2)*self.t*self.start_ctrl[1] + 3*(1-self.t)*math.pow(self.t,2)*self.end_pnt[1] + math.pow(self.t,3)*self.end_ctrl[1]
            return [curr_point_x, curr_point_y]
        return [0, 0]

    def increase_velocity(self):
        if not self.exit_bool:
            self.t_increment += 0.003
            self.exit_bool = True