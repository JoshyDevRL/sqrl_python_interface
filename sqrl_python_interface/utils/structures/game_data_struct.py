
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Vector3:
    x: float
    y: float
    z: float

@dataclass
class Rotator:
    pitch: float
    yaw: float
    roll: float

@dataclass
class Physics:
    location: Vector3
    rotation: Rotator
    velocity: Vector3
    angular_velocity: Vector3

@dataclass
class BoxShape:
    length: float
    width: float
    height: float

@dataclass
class ScoreInfo:
    score: int
    goals: int
    own_goals: int
    assists: int
    saves: int
    shots: int
    demolitions: int

@dataclass
class PlayerInfo:
    physics: Physics
    hitbox: BoxShape
    hitbox_offset: Vector3
    boost: float
    score_info: ScoreInfo
    team: int
    is_demolished: bool
    has_wheel_contact: bool
    is_super_sonic: bool
    jumped: bool
    double_jumped: bool
    name: str

@dataclass
class Touch:
    time_seconds: float
    hit_location: Vector3
    hit_normal: Vector3
    team: int
    player_index: int

@dataclass
class BallInfo:
    physics: Physics
    latest_touch: Touch

@dataclass
class BoostPadState:
    is_active: bool
    timer: float

@dataclass
class GameInfo:
    seconds_elapsed: float
    game_time_remaining: float
    is_overtime: bool
    is_round_active: bool
    is_kickoff_pause: bool
    is_match_ended: bool
    frame_num: int

@dataclass
class GameTickPacket:
    game_cars: Tuple[PlayerInfo, PlayerInfo]
    num_cars: int
    game_boosts: List[BoostPadState]
    num_boost: int
    game_ball: BallInfo
    game_info: GameInfo

@dataclass
class BoostPad:
    location: Vector3
    is_full_boost: bool

@dataclass
class GoalInfo:
    team_num: int
    location: Vector3
    width: float
    height: float

@dataclass
class FieldInfoPacket:
    boost_pads: List[BoostPad]
    num_boosts: int
    goals: Tuple[GoalInfo, GoalInfo]
    num_goals: int

