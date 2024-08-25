
from sqrl_python_interface.utils.structures.game_data_struct import FieldInfoPacket, BoostPad, GoalInfo, Vector3
from sqrl_python_interface.utils.python_connection import PythonInterface
from typing import List, Tuple

class SimpleControllerState:
    def __init__(self,
                 steer: float = 0.0,
                 throttle: float = 0.0,
                 pitch: float = 0.0,
                 yaw: float = 0.0,
                 roll: float = 0.0,
                 jump: bool = False,
                 boost: bool = False,
                 handbrake: bool = False,
                 use_item: bool = False):

        self.steer = steer
        self.throttle = throttle
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.jump = jump
        self.boost = boost
        self.handbrake = handbrake
        self.use_item = use_item

    def f(self):
        return [self.throttle, self.steer, self.pitch, self.yaw, self.roll]
    
    def b(self):
        return [self.jump, self.boost, self.handbrake]


class Renderer: # dummy renderer class, otherwise the bot will error
    def __init__(self):
        pass

    def begin_rendering(self):
        pass

    def end_rendering(self):
        pass

    def draw_line_3d(self, vec1, vec2, color):
        pass
    
    def draw_polyline_3d(self, vectors, color):
        pass
        
    def draw_rect_2d(self, x, y, width, height, filled, color):
        pass

    def draw_rect_3d(self, vec, width, height, filled, color, centered=False):
        pass

    def draw_string_2d(self, x, y, scale_x, scale_y, text, color):
        pass
    
    def draw_string_3d(self, vec, scale_x, scale_y, text, color):
        pass

    def create_color(self, alpha, red, green, blue):
        pass

    def black(self):
        pass

    def white(self):
        pass

    def gray(self):
        pass

    def grey(self):
        pass

    def blue(self):
        pass

    def red(self):
        pass

    def green(self):
        pass

    def lime(self):
        pass

    def yellow(self):
        pass

    def orange(self):
        pass

    def cyan(self):
        pass

    def pink(self):
        pass

    def purple(self):
        pass

    def teal(self):
        pass


class BaseAgent:
    def __init__(self):
        self.index = None
        self.team = None
        self.name = None
        self.match_id = None
        self.python_interface: PythonInterface = None
        self.renderer = Renderer()
        self.d = []
        print("[PI] BaseAgent started")

    def set_vars(self, index, team, name, match_id):
        self.index = index
        self.team = team
        self.name = name.replace('$', ' ')
        self.match_id = match_id
        self.python_interface = PythonInterface(self.match_id)
        print(f'[PI] Initialized bot | index: {self.index} | team: {self.team} | name: {self.name} | match_id: {self.match_id}')

    def get_packet(self):
        packet = self.python_interface.read()
        return packet

    def get_field_info(self):
        field_info = FieldInfoPacket([
            BoostPad(Vector3(0, -4240, 70), False),
            BoostPad(Vector3(-1792, -4184, 70), False),
            BoostPad(Vector3(1792, -4184, 70), False),
            BoostPad(Vector3(-3072, -4096, 73), True),
            BoostPad(Vector3(3072, -4096, 73), True),
            BoostPad(Vector3(-940, -3308, 70), False),
            BoostPad(Vector3(940, -3308, 70), False),
            BoostPad(Vector3(0, -2816, 70), False),
            BoostPad(Vector3(-3584, -2484, 70), False),
            BoostPad(Vector3(3584, -2484, 70), False),
            BoostPad(Vector3(-1788, -2300, 70), False),
            BoostPad(Vector3(1788, -2300, 70), False),
            BoostPad(Vector3(-2048, -1036, 70), False),
            BoostPad(Vector3(0, -1024, 70), False),
            BoostPad(Vector3(2048, -1036, 70), False),
            BoostPad(Vector3(-3584, 0, 73), True),
            BoostPad(Vector3(-1024, 0, 70), False),
            BoostPad(Vector3(1024, 0, 70), False),
            BoostPad(Vector3(3584, 0, 73), True),
            BoostPad(Vector3(-2048, 1036, 70), False),
            BoostPad(Vector3(0, 1024, 70), False),
            BoostPad(Vector3(2048, 1036, 70), False),
            BoostPad(Vector3(-1788, 2300, 70), False),
            BoostPad(Vector3(1788, 2300, 70), False),
            BoostPad(Vector3(-3584, 2484, 70), False),
            BoostPad(Vector3(3584, 2484, 70), False),
            BoostPad(Vector3(0, 2816, 70), False),
            BoostPad(Vector3(-940, 3308, 70), False),
            BoostPad(Vector3(940, 3308, 70), False),
            BoostPad(Vector3(-3072, 4096, 73), True),
            BoostPad(Vector3(3072, 4096, 73), True),
            BoostPad(Vector3(-1792, 4184, 70), False),
            BoostPad(Vector3(1792, 4184, 70), False),
            BoostPad(Vector3(0, 4240, 70), False)],
            34,
            [GoalInfo(0, Vector3(0, -5120, 0), 884, 642), GoalInfo(1, Vector3(0, 5120, 0), 884, 642)],
            2
        )
        return field_info
    
    def get_ball_prediction_struct(self):
        slices = self.python_interface.get_ball_prediction_struct()
        return slices

    def send_controller(self, team, controller):
        self.python_interface.send_controller(team, controller)

    def send_quick_chat(self, q, w):
        pass