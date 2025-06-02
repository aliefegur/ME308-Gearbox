import numpy as np
import pandas as pd
from interference import *

# Load program data resource from the excel table
standard_modules = pd.read_excel('programdata.xlsx', 'standard_modules', engine='openpyxl')

def calculate_helical_properties():
    e = 1/7     # Gear ratio
    POWER = 4   # 4 kW power
    RPM = 1350  # 1350 rpm input

    # Minimum pinion teeth count to prevent interference
    min_pinion_teeth = minimum_helical_pinion(25, 20, e, 1)

    # Different module results
    element_data = []
    for module in standard_modules['modules'].values:
        # Pinion diameter
        d_p = module * min_pinion_teeth

        # Force Analysis
        W_t = (60000*POWER)/(np.pi * d_p * RPM) # Targential force
        T = W_t * d_p / 2                       # Torque

        element_data.append({
            'm': module,
            'N_p': min_pinion_teeth,
            'N_g': min_pinion_teeth / e,
            'd_p': d_p,
            'd_g': d_p / e,
            'W_t': W_t,
            'T': T,
        })

    df = pd.DataFrame(element_data)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)

# Operation entry point
if __name__ == '__main__':
    calculate_helical_properties()
