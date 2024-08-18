
from dataclasses import dataclass
from typing import List, Tuple

from sqrl_python_interface.utils.structures.game_data_struct import Physics

@dataclass
class Slice:
    physics: Physics
    game_seconds: float

@dataclass
class BallPrediction:
    slices: Slice
    num_slices: int
