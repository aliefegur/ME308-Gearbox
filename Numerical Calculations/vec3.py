import numpy as np

class vec3:
  def __init__(self, x: float, y: float, z: float):
    self.x = x
    self.y = y
    self.z = z
  
  def mag(self) -> float:
    return np.sqrt(self.x**2 + self.y**2 + self.z**2)
  
  def to_string(self) -> str:
    return f"({self.x}, {self.y}, {self.z})"
  