
from sqrl_python_interface.utils.structures.game_data_struct import GameTickPacket, GameInfo, Touch, BoostPadState, BallInfo, Physics, PlayerInfo, ScoreInfo, BoxShape, Vector3, Rotator
from sqrl_python_interface.utils.structures.ball_prediction_struct import BallPrediction, Slice

import ctypes
import numpy as np
import struct
import mmap

def modf(buffer, offset, value):
    struct.pack_into('f', buffer, offset, value)

def modi(buffer, offset, value):
    struct.pack_into('i', buffer, offset, value)

def modb(buffer, offset, value):
    struct.pack_into('b', buffer, offset, value)

def vec(buffer, offset):
    x, y, z = struct.unpack_from('fff', buffer, offset)
    return Vector3(x, y, z), offset + 3 * 4

def rot(buffer, offset):
    pitch, yaw, roll = struct.unpack_from('fff', buffer, offset)
    return Rotator(pitch, yaw, roll), offset + 3 * 4

def f(buffer, offset):
    value = struct.unpack_from('f', buffer, offset)[0]
    return value, offset + 4

def i(buffer, offset):
    value = struct.unpack_from('i', buffer, offset)[0]
    return value, offset + 4

def b(buffer, offset):
    value = struct.unpack_from('?', buffer, offset)[0]
    return value, offset + 1

def car(buf, offset):
    bcp, offset = vec(buf, offset)
    bcr, offset = rot(buf, offset)
    bcv, offset = vec(buf, offset)
    bca, offset = vec(buf, offset)
    bch, offset = vec(buf, offset)
    bco, offset = vec(buf, offset)
    bcb, offset = f(buf, offset)
    bcscore, offset = i(buf, offset)
    bcgoal, offset = i(buf, offset)
    bcown, offset = i(buf, offset)
    bcass, offset = i(buf, offset)
    bcsave, offset = i(buf, offset)
    bcshot, offset = i(buf, offset)
    bcdemo, offset = i(buf, offset) 
    bct, offset = i(buf, offset)
    bcd, offset = b(buf, offset)
    bcg, offset = b(buf, offset)
    bcs, offset = b(buf, offset)
    bcj, offset = b(buf, offset)
    bcdj, offset = b(buf, offset)
    phys = Physics(bcp, bcr, bcv, bca)
    box = BoxShape(bch.x, bch.y, bch.z)
    score = ScoreInfo(bcscore, bcgoal, bcown, bcass, bcsave, bcshot, bcdemo)
    car_info = PlayerInfo(phys, box, bco, bcb, score, bct, bcd, bcg, bcs, bcj, bcdj, "")
    return car_info, offset

def boosts(buf, offset):
    boosts = []
    for n in range(34):
        ba, offset = b(buf, offset)
        bt, offset = f(buf, offset)
        boosts.append(BoostPadState(ba, bt))
    return boosts, offset

def ball(buf, offset):
    bp, offset = vec(buf, offset)
    bv, offset = vec(buf, offset)
    ba, offset = vec(buf, offset)
    bh, offset = vec(buf, offset)
    bn, offset = vec(buf, offset)
    btime, offset = f(buf, offset)
    bteam, offset = i(buf, offset)
    bidx, offset = i(buf, offset)
    phys = Physics(bp, Rotator(0, 0, 0), bv, ba)
    touch = Touch(btime, bh, bn, bteam, bidx)
    ball_info = BallInfo(phys, touch)
    return ball_info, offset

def game(buf, offset):
    t, offset = f(buf, offset)
    r, offset = f(buf, offset)
    o, offset = b(buf, offset)
    k, offset = b(buf, offset)
    e, offset = b(buf, offset)
    c, offset = i(buf, offset)
    game_info = GameInfo(t, r, o, True, k, e, c)
    return game_info, offset


class PythonInterface:
    def __init__(self, match_id):
        self.shm_name = f"Local\\SQRL_Python_{match_id}"
        self.size = 14952
        self.__packet: GameTickPacket = None
        self.__ball_pred: BallPrediction = None
        
    def read(self):
        with mmap.mmap(-1, self.size, tagname=self.shm_name) as buf:
            offset = 0
            blue_car, offset = car(buf, offset)
            orange_car, offset = car(buf, offset)
            boost_pads, offset = boosts(buf, offset)
            ball_info, offset = ball(buf, offset)
            game_info, offset = game(buf, offset)
            num_cars, offset = i(buf, 14945)
            slices = []
            offset = 483
            for n in range(0, 360):
                p, offset = vec(buf, offset)
                v, offset = vec(buf, offset)
                a, offset = vec(buf, offset)
                t, offset = f(buf, offset)
                phys = Physics(p, Rotator(0, 0, 0), v, a)
                slices.append(Slice(phys, t))
            offset = 14883
            n, offset = i(buf, offset)
            if num_cars == 0 or n == 0:
                exit()
        self.__packet = GameTickPacket((blue_car, orange_car), num_cars, boost_pads, 34, ball_info, game_info)
        self.__ball_pred = BallPrediction(slices, n)
        return self.__packet
    
    def get_ball_prediction_struct(self):
        return self.__ball_pred

    def send_controller(self, team, controller):
        with mmap.mmap(-1, self.size, tagname=self.shm_name) as buf:
            if team == 0:
                modi(buf, 14891, self.__packet.game_info.frame_num)
                modf(buf, 14895, controller.throttle)
                modf(buf, 14899, controller.steer)
                modf(buf, 14903, controller.pitch)
                modf(buf, 14907, controller.yaw)
                modf(buf, 14911, controller.roll)
                modb(buf, 14915, controller.jump)
                modb(buf, 14916, controller.boost)
                modb(buf, 14917, controller.handbrake)

            else:
                modi(buf, 14918, self.__packet.game_info.frame_num)
                modf(buf, 14922, controller.throttle)
                modf(buf, 14926, controller.steer)
                modf(buf, 14930, controller.pitch)
                modf(buf, 14934, controller.yaw)
                modf(buf, 14938, controller.roll)
                modb(buf, 14942, controller.jump)
                modb(buf, 14943, controller.boost)
                modb(buf, 14944, controller.handbrake)


