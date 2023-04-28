import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import configparser
from rich.traceback import install

from modeling.body import Body
from constants import *

install(show_locals=True, width=300)  # setting `rich.traceback` up  # noqa

data = configparser.ConfigParser()
data.read('./config.ini')  # loading config file

parameters_body = tuple(data['Body1'].keys())  # reading available parameters from section 'Body1'
bodies: list[Body] = [Body(*[float(data[body_name][i]) for i in parameters_body]) for body_name in data.keys() if 'Body' in body_name]  # loading bodies' data from config, checking if section name contain string 'Body' and creating and adding new Body object to list

n = len(bodies)  # number of bodies in simulation
dt, limx_min, limx_max, limy_min, limy_max = [float(data['General'][key]) for key in data['General'].keys()]

# --------CONFIGURING MATPLOTLIB--------

plt.style.use('dark_background') # noqa

fig = plt.figure()
ax: mpl.axes.Axes = plt.axes()

ax.set_xlim((limx_min, limx_max))
ax.set_ylim((limy_min, limy_max))

lines: list[mpl.lines.Line2D] = [ax.plot([], [])[0] for _ in range(n)]  # initializing list of lines showing paths of bodies
markers: list[mpl.lines.Line2D] = [ax.plot([], [], 'o', markersize=10, label=f"Body {i}")[0] for i in range(n)]  # initializing list of marker showing current position of bodies

lines_data_x: list[list[float]] = [[] for _ in range(n)]
lines_data_y: list[list[float]] = [[] for _ in range(n)]


def initialize():
	return lines+markers


# ----------BEGIN CALCULATIONS----------


# функция для расчёта ускорения
def acceleration(body_current: int) -> np.ndarray:
	ns = tuple(set(range(n)) - {body_current})

	body = bodies[body_current]
	bodies_other = [bodies[i] for i in ns]

	coords = np.array((body.x, body.y))
	coords_other = [np.array((b.x, b.y)) for b in bodies_other]

	rs: list[float] = [np.linalg.norm(coords - i) for i in coords_other]

	ax_sum = -G * sum([bodies_other[i].mass * (body.x - bodies_other[i].x) / rs[i] ** 3 for i in range(n-1)])
	ay_sum = -G * sum([bodies_other[i].mass * (body.y - bodies_other[i].y) / rs[i] ** 3 for i in range(n-1)])

	return np.array((ax_sum, ay_sum))


def animate(frame: int) -> list[mpl.lines.Line2D]:  # noqa
	global t

	t += dt
	for i in range(n):
		body = bodies[i]
		a = acceleration(i)

		body.x += body.vx * dt
		body.y += body.vy * dt

		body.vx += a[0] * dt
		body.vy += a[1] * dt

		lines_data_x[i].append(body.x)
		lines_data_y[i].append(body.y)

		lines[i].set_xdata(lines_data_x[i])
		lines[i].set_ydata(lines_data_y[i])
		markers[i].set_xdata((body.x,))
		markers[i].set_ydata((body.y,))

	return lines+markers


anim = animation.FuncAnimation(fig, animate, init_func=initialize, interval=0.01, blit=True, cache_frame_data=False)
ax.legend(loc="upper right")

plt.show()
