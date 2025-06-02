import numpy as np

# Returns the helical pinion's minimum number of teeth to prevent interference
def minimum_helical_pinion(hangle, pangle, gear_ratio, k):
	psi = np.radians(hangle)
	phi = np.radians(pangle)

	num = 2 * k * np.cos(psi)
	den = (1 + 2*gear_ratio) * np.sin(phi)**2
	bracket = gear_ratio + np.sqrt(gear_ratio**2 + (1 + 2 * gear_ratio) * np.sin(phi)**2)

	return np.ceil((num / den) * bracket)

# Returns the bevel pinion's minimum number of teeth to prevent interference
def minimum_bevel_pinion(pangle, gear_ratio, k):
	phi = np.radians(pangle)

	num = 2 * k
	den = (1 + 2 * gear_ratio) * np.sin(phi)**2
	bracket = gear_ratio + np.sqrt(gear_ratio**2 + (1 + 2 * gear_ratio) * np.sin(phi)**2)

	return np.ceil((num / den) * bracket)