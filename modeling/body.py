class Body:
	def __init__(self, mass: float, x: float, y: float, vx: float, vy: float, fixed: bool = False):
		self.mass = mass
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.fixed = fixed

		if not self.fixed:
			self.fixed = False

		self.all = (mass, x, y, vx, vy, fixed)

	def __str__(self):
		return f"Body(mass={self.mass}, x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy}{', fixed' if self.fixed else ''})"

	def __repr__(self):
		return f"Body(mass={self.mass}, x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy}{', fixed' if self.fixed else ''}) with id={id(self)}"

	def __eq__(self, other):
		return self.all == other.all
