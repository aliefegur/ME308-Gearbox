import numpy as np

class Gear:
  def __init__(self, m: float, N: int, pangle: float, F: float):
    self.m = m  # Module
    self.N = N  # Number of teeth
    self.d = m * N  # Pitch diameter
    self.p = np.pi * m 
    self.P = np.pi / self.p
    self.pangle = np.radians(pangle) # Pressure angle
    self.F = F # Face width
    self.W = [0, 0, 0]  # (tangential, radial, axial)
    self.rpm = 0

  def apply_force(self, W: float):
    self.W = [W, 0, 0]

  def applied_force(self):
    return np.sqrt(self.W[0]**2 + self.W[1]**2 + self.W[2]**2)
  
  def set_rpm(self, rpm: float):
    self.rpm = rpm

class HelicalGear(Gear):
  def __init__(self, m: float, N: int, hangle: float, pangle: float, F: float):
    super().__init__(m, N, pangle, F)
    self.hangle = np.radians(hangle)
  
  def phi_t(self) -> float:
    return np.atan(np.tan(self.pangle) / np.cos(self.hangle))
  
  def p_n(self) -> float:
    return self.p * np.cos(self.hangle)
  
  def p_x(self) -> float:
    return self.p / np.tan(self.hangle)
  
  def P_n(self) -> float:
    return np.pi / self.p_n()
  
  def apply_force(self, W: float):
    # (W_t, W_r, W_a)
    self.W = [
      W * np.sin(self.pangle),
      W * np.cos(self.pangle) * np.cos(self.hangle),
      W * np.cos(self.pangle) * np.sin(self.hangle)
    ]

class BevelGear(Gear):
  def __init__(self, m: float, N: int, pangle: float, gamma: float, F: float):
    super().__init__(m, N, pangle, F)
    self.gamma = np.radians(gamma)

  def apply_force(self, W: float):
    # (W_t, W_r, W_a)
    self.W = [
      W,
      W * np.tan(self.pangle) * np.cos(self.gamma),
      W * np.tan(self.pangle) * np.sin(self.gamma)
    ]

class GearCouple:
  def __init__(self, pinion: Gear, gear: Gear):
    self.pinion = pinion
    self.gear = gear
    self.gear.rpm = self.pinion.rpm * self.gear_ratio()

  def gear_ratio(self) -> float:
    return self.pinion.N / self.gear.N
  
  def input_rpm(self) -> float:
    return self.pinion.rpm
  
  def out_rpm(self) -> float:
    return self.gear.rpm
