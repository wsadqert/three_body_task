import inspect
import os
import time

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from astropy.time import TimeDelta
from matplotlib import rcParams
import numpy as np

import configparser
from rich.traceback import install

from modeling.body import Body
from constants import *
from modeling.data_reading import read_data

install(show_locals=True, width=300)  # setting `rich.traceback` up  # noqa

data = configparser.ConfigParser()
data.read('./config.ini')  # loading config file

parameters_body: list[str] = inspect.getfullargspec(Body).args[1:]
bodies: list[Body] = read_data(data, parameters_body)

n = len(bodies)  # number of bodies in simulation
dt, limx_min, limx_max, limy_min, limy_max = [float(data['General'][key]) for key in data['General'].keys()]

# --------CONFIGURING MATPLOTLIB--------

plt.style.use('dark_background')  # noqa

color_cycle = rcParams['axes.prop_cycle']()
colors_using: list[str] = [next(color_cycle) for _ in range(n)]


fig = plt.figure()
ax: mpl.axes.Axes = plt.axes()

ax.grid(True, ls='dashed', color='#333333')

ax.set_xlim((limx_min, limx_max))
ax.set_ylim((limy_min, limy_max))

# lines: list[mpl.lines.Line2D] = [ax.plot([], [], color=colors_using[i]['color'])[0] for i in range(n)]  # initializing list of lines showing paths of bodies  # noqa
markers: list[mpl.lines.Line2D] = [ax.plot([], [], 'o', markersize=10, label=f"Body {i}", color=colors_using[i]['color'])[0] for i in range(n)]  # initializing list of marker showing current position of bodies  # noqa

# lines_data_x: list[list[float]] = [[] for _ in range(n)]
# lines_data_y: list[list[float]] = [[] for _ in range(n)]


def initialize():
	return markers  # + lines


# ----------BEGIN CALCULATIONS----------

# функция для расчёта ускорения
def acceleration(body_current: int) -> np.ndarray:
	ns = tuple(set(range(n)) - {body_current})

	body = bodies[body_current]
	bodies_other = [bodies[i] for i in ns]

	coords = np.array((body.x, body.y))
	coords_other = [np.array((b.x, b.y)) for b in bodies_other]

	rs: list[float] = [np.linalg.norm(coords - i) for i in coords_other]
	ax_sum = -G * sum([bodies_other[i].mass * (body.x - bodies_other[i].x) / rs[i] ** 3 for i in range(n - 1)])
	ay_sum = -G * sum([bodies_other[i].mass * (body.y - bodies_other[i].y) / rs[i] ** 3 for i in range(n - 1)])

	return np.array((ax_sum, ay_sum))


def animate(frame: int) -> list[mpl.lines.Line2D]:  # noqa
	global t, t_last, t0  # noqa

	t += dt
	for i in range(n):
		body = bodies[i]

		if body.fixed:
			continue

		a = acceleration(i)

		body.x += body.vx * dt
		body.y += body.vy * dt

		body.vx += a[0] * dt
		body.vy += a[1] * dt

		# lines_data_x[i].append(body.x)
		# lines_data_y[i].append(body.y)

		# lines[i].set_xdata(lines_data_x[i])
		# lines[i].set_ydata(lines_data_y[i])
		markers[i].set_xdata((body.x,))
		markers[i].set_ydata((body.y,))

	if frame == 0:
		t0 = time.time()

	elif frame % output_rate == 0:
		t1 = time.time()

		os.system('cls')

		print('t =', TimeDelta(t, format='sec').datetime)  # noqa
		print('fps =', round(output_rate / (t1 - t0), 2))  # noqa
		print('tps =', TimeDelta((t - t_last) / (t1 - t0), format='sec').datetime)  # noqa
		speed = round((t - t_last) / (t1 - t0))
		print('speed multiplier =', format(speed, ',').replace(',', ' '))

		t_last = t
		t0 = time.time()

	return markers  # + lines


anim = animation.FuncAnimation(fig, animate, init_func=initialize, interval=0.0001, blit=True, cache_frame_data=False)
ax.legend(loc="upper right")

try:
	plt.show()
except KeyboardInterrupt:
	print('Interrupted')
