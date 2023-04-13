class Body:
	def __init__(self, mass: float, x: float, y: float, vx: float, vy: float):
		self.mass = mass
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy

	def __str__(self):
		return f"Body(mass={self.mass}, x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy})"
