import inspect
# import torch
import random

import numpy as np

from types import MethodType, FunctionType
from pathlib import Path
from enum import Enum


class OptimizationTarget(Enum):
    
    # Dominating Set Problem
    DSP = 1
    # Roman Domination Problem
    RDP = 2
    # Independent Roman Domination Problem
    IRDP = 3
    # Restrained Double Roman Domination Problem
    RDRDP = 4

class GraphType(Enum):
    
    # Random Graph
    RANDOM = 1
    # Split Graph
    SPLIT = 2
    # Erdos Renyi Graph
    ER = 3
    # Barabasi Albert Graph
    BA = 4
    # Regular Graph
    REGULAR = 5
    # Watts Strogatz Graph
    WS = 6

# def enable_grad_for_hf_llm(func: MethodType | FunctionType) -> MethodType | FunctionType:
#     return func.__closure__[1].cell_contents


def get_script_name() -> str:
    caller_frame_record = inspect.stack()[1]
    module_path = caller_frame_record.filename
    return Path(module_path).stem
