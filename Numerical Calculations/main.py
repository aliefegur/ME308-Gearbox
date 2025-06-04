import numpy as np
import pandas as pd
from interference import *
from gears import *
from stress_analyzer import get_stress

# Load program data resource from the excel table
print('Program data loading...')
standard_modules = pd.read_excel('programdata.xlsx', 'standard_modules', engine='openpyxl')
params = pd.read_excel('programdata.xlsx', 'params', engine='openpyxl')

E1 = params['e1'][0]
E2 = params['e2'][0]
POWER = params['H'][0]
RPM = params['ni'][0]
HANGLE = params['hangle'][0]
PANGLE = params['pangle'][0]
S_YT = params['S_yt'][0]
N_D = params['n_d'][0]

def calculate_possible_helical_properties():
    print('Possible helical gear properties are calculating...')
    e = E1   # Gear ratio

    # Minimum pinion teeth count to prevent interference
    min_pinion_teeth = minimum_helical_pinion(HANGLE, PANGLE, e, 1)

    # Minimum 12 teeth allowed because lewis factors table
    if min_pinion_teeth < 12:
        min_pinion_teeth = 12

    # Different module results
    element_data = []

    # Check for different pinion teeth count
    for N in range(min_pinion_teeth, min_pinion_teeth + 20):
        for module in standard_modules['modules'].values:
            face_width = 10 * module

            # Create pinion & gear
            pinion = HelicalGear(module, N, 25, 20, face_width)
            gear = HelicalGear(module, int(N / e), 25, 20, face_width)

            # Apply force
            pinion.apply_tangential_force((60000*POWER)/(np.pi * N * module * RPM))
            gear.apply_tangential_force(pinion.applied_force().x)

            # Set RPMs
            pinion.rpm = RPM
            gear.rpm = RPM * e

            # Stress calculation
            pinion_stress = get_stress(pinion)
            gear_stress = get_stress(gear)

            element_data.append({
                'N': N,
                'm': module,
                'N_p': pinion.N,
                'N_g': gear.N,
                'd_p': pinion.d,                        # mm
                'd_g': gear.d,                          # mm
                'W_p': pinion.applied_force().mag(),    # N
                'W_g': pinion.applied_force().mag(),    # N
                'stress_p': pinion_stress,              # MPa
                'stress_g': gear_stress,                # MPa
                'F': face_width,                        # mm
            })

    df = pd.DataFrame(element_data)
    return df

def calculate_possible_bevel_properties():
    print('Possible bevel gear properties are calculating...')
    e = E2              # Gear ratio
    gamma = np.atan(e)  # gamma angle of the couple

    min_pinion_teeth = minimum_bevel_pinion(20, e, 1)

    # Minimum 12 teeth allowed because lewis factors table
    if min_pinion_teeth < 12:
        min_pinion_teeth = 12

    # Different dimension results
    element_data = []

    for N in range(min_pinion_teeth, min_pinion_teeth + 20):
        for module in standard_modules['modules'].values:
            face_width = module * 10

            # Create pinion and gear
            pinion = BevelGear(module, N, 20, gamma, face_width)
            gear = BevelGear(module, N / e, 20, np.pi / 2 - gamma, face_width)
            
            pinion.apply_tangential_force((60000*POWER)/(np.pi*N*module*RPM*E1))
            gear.apply_tangential_force(pinion.applied_force().x)

            pinion.set_rpm(RPM)
            gear.set_rpm(RPM * e)

            pinion_stress = get_stress(pinion)
            gear_stress = get_stress(gear)

            element_data.append({
                'N': N,
                'm': module,
                'N_p': pinion.N,
                'N_g': gear.N,
                'd_p': pinion.d,
                'd_g': gear.d,
                'W_p': pinion.applied_force().mag(),
                'W_g': gear.applied_force().mag(),
                'stress_p': pinion_stress,
                'stress_g': gear_stress,
                'F': face_width
            })

    df = pd.DataFrame(element_data)
    return df

df1 = calculate_possible_helical_properties()
df2 = calculate_possible_bevel_properties()

# Filter all possible gear trains
helicals = df1[(df1['stress_p'] < (S_YT / N_D)) & (df1['d_p'] > 50) & (df1['d_g'] < 400) & (df1['N_p'] % 2 == 0) & (df1['N_g'] % 2 == 0)]
bevels = df2[(df2['stress_p'] < (S_YT / N_D)) & (df2['d_p'] > 50) & (df2['d_g'] < 400) & (df2['N_p'] % 2 == 0) & (df2['N_g'] % 2 == 0)]

print("\nPossible Helical Gear Couples:")
print(helicals)

print("\n\nPossible Bevel Gear Couples:")
print(bevels)
