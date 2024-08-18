
from sqrl_python_interface.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket, GameInfo, GoalInfo, BoostPad, Touch, BoostPadState, BallInfo, Physics, PlayerInfo, Vector3, Rotator
from sqrl_python_interface.utils.structures.ball_prediction_struct import BallPrediction, Slice
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
        self.pipe_name = None
        self.python_interface = None
        self.renderer = Renderer()
        print("[PI] BaseAgent started")

    def set_vars(self, index, team, name, pipe_name):
        self.index = index
        self.team = team
        self.name = name
        self.pipe_name = pipe_name
        self.python_interface = PythonInterface(self.pipe_name)
        self.python_interface.start_connection()
        self.logger = print(f'[PI] Initialized bot | index: {index} | tea: {team} | name: {name} | pipe_name: {pipe_name}')

    def get_packet(self):
        d = self.python_interface.read()
        blue_car = PlayerInfo(Physics(Vector3(d[0], d[1], d[2]), Rotator(d[3], d[4], d[5]), Vector3(d[6], d[7], d[8]), Vector3(d[9], d[10], d[11])), d[12], d[13], d[14], d[15], d[16], d[17], d[18], "")
        orange_car = PlayerInfo(Physics(Vector3(d[19], d[20], d[21]), Rotator(d[22], d[23], d[24]), Vector3(d[25], d[26], d[27]), Vector3(d[28], d[29], d[30])), d[31], d[32], d[33], d[34], d[35], d[36], d[37], "")
        boost_pads = []
        for i in range(0, 68, 2):
            boost_pads.append(BoostPadState(d[38 + int(i/2)], d[39 + int(i/2)]))
        ball_info = BallInfo(Physics(Vector3(d[106], d[107], d[108]), Rotator(0, 0, 0), Vector3(d[109], d[110], d[111]), Vector3(d[112], d[113], d[114])), Touch(-1, -1))
        game_info = GameInfo(d[115], d[116], d[117], True, d[118], False, d[119])
        packet = GameTickPacket(
            (blue_car, orange_car),
            2,
            boost_pads,
            34,
            ball_info,
            game_info
        )
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
    
    def get_ball_prediction_struct(self) -> BallPrediction:


        return 0

    def send_controller(self, controller):
        self.python_interface.send(controller)
