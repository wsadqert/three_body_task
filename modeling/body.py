class Body:
	def __init__(self, mass: float, x: float, y: float, vx: float, vy: float, fixed: bool = False):
		self.mass = mass
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.fixed = fixed

	def __str__(self):
		return f"Body(mass={self.mass}, x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy}{', fixed' if self.fixed else ''})"

	def __eq__(self, other):
		return self.mass == other.mass and \
			self.x == other.x and \
			self.y == other.y and \
			self.vx == other.vx and \
			self.vy == other.vy and \
			self.fixed == other.fixed
