import numpy as np
import pandas as pd
from gears import *

lewis_factors = pd.read_excel('programdata.xlsx', 'lewis_factors', engine='openpyxl')

# Returns the Lewis Form Factor for given # of teeth
def lewis_factor(N: int) -> float:
    if N < 12 or N > 1000:
        raise Exception('N must be in the range of [12, 1000]')

    # Linear interpolation
    _N = [0, 0]
    _Y = [0, 0]

    for index, row in lewis_factors.iterrows():
        if row['N'] == N: return row['Y']
        
        _N[0] = _N[1]
        _N[1] = row['N']
        _Y[0] = _Y[1]
        _Y[1] = row['Y']
        
        if row['N'] > N: break

    Y = _Y[0] + (_Y[1] - _Y[0]) * (N - _N[0]) / (_N[1] - _N[0])
    return Y

def get_stress(gear: Gear) -> float:
    # Calculate dynamic effect coefficient
    V = gear.d * 1e-3 * np.pi * gear.rpm / 60    # Pitch-line velocity (m/s)
    Kv = (6.1 + V) / 6.1    # For cut or milled profile
    stress = (Kv * gear.W[0]) / (gear.F * gear.m * lewis_factor(gear.N) / 1000)
    return stress
