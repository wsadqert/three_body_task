import numpy as np
from constants import *
from modeling.body import Body
from typing import Sequence


def acceleration(bodies: Sequence[Body], body_current: int) -> np.ndarray:
	n = len(bodies)

	ns = tuple(set(range(n)) - {body_current})

	body = bodies[body_current]
	bodies_other = [bodies[i] for i in ns]

	coords = np.array((body.x, body.y))
	coords_other = [np.array((b.x, b.y)) for b in bodies_other]

	rs: list[float] = [np.linalg.norm(coords - i) for i in coords_other]
	ax_sum = -G * sum([bodies_other[i].mass * (body.x - bodies_other[i].x) / rs[i] ** 3 for i in range(n - 1)])
	ay_sum = -G * sum([bodies_other[i].mass * (body.y - bodies_other[i].y) / rs[i] ** 3 for i in range(n - 1)])

	return np.array((ax_sum, ay_sum))
