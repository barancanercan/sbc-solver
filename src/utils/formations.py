from enum import Enum
from typing import List


class Formations(Enum):
    # Common formations
    F4_4_2 = ["GK", "LB", "CB", "CB", "RB", "LM", "CM", "CM", "RM", "ST", "ST"]
    F4_1_3_2 = ["GK", "LB", "CB", "CB", "RB", "LM", "CM", "RM", "ST", "ST"]
    F4_1_2_1_2 = ["GK", "LB", "CB", "CB", "RB", "LM", "CM", "CM", "RM", "ST", "ST"]
    F4_2_3_1 = ["GK", "LB", "CB", "CB", "RB", "LM", "CM", "CM", "RM", "ST"]
    F4_3_3 = ["GK", "LB", "CB", "CB", "RB", "LM", "CM", "RM", "LW", "ST", "RW"]
    F3_5_2 = ["GK", "CB", "CB", "CB", "LM", "CM", "CM", "CM", "RM", "ST", "ST"]
    F5_3_2 = ["GK", "LB", "CB", "CB", "RB", "CB", "LM", "CM", "RM", "ST", "ST"]
    F5_4_1 = ["GK", "LB", "CB", "CB", "RB", "CB", "LM", "CM", "CM", "RM", "ST"]
    
    # FC 26 specific formations
    F4_2_2_2 = ["GK", "LB", "CB", "CB", "RB", "LM", "CM", "CM", "RM", "ST", "ST"]
    F4_1_4_1 = ["GK", "LB", "CB", "CB", "RB", "LM", "CM", "CM", "RM", "ST"]
    F3_4_3 = ["GK", "CB", "CB", "CB", "LM", "CM", "CM", "RM", "LW", "ST", "RW"]