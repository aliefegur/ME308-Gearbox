import numpy as np

class Gear:
  def __init__(self, m, N, pangle):
    self.d = m * N
    self.p = np.pi * m
    self.P = np.pi / self.p
    self.pangle = np.radians(pangle)
    self.W = [0, 0, 0]  # (tangential, radial, axial)

  def apply_force(F):
    pass

class HelicalGear(Gear):
  def __init__(self, m, N, hangle, pangle):
    Gear.__init__(self, m, N, pangle)
    self.hangle = np.radians(hangle)
  
  def phi_t(self):
    return np.atan(np.tan(self.pangle) / np.cos(self.hangle))
  
  def p_n(self):
    return self.p * np.cos(self.hangle)
  
  def p_x(self):
    return self.p / np.tan(self.hangle)
  
  def P_n(self):
    return np.pi / self.p_n()
  
  def apply_force(self, F):
    # (W_t, W_r, W_a)
    self.W = [
      F * np.sin(self.pangle),
      F * np.cos(self.pangle) * np.cos(self.hangle),
      F * np.cos(self.pangle) * np.sin(self.hangle)
    ]
