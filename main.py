import inspect
import time

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rcParams
from astropy.time import TimeDelta

from colorama import init as colorama_init, Fore

from rich.traceback import install

from modeling.body import Body
from modeling.read_data import read_data
from constants import *
from modeling.acceleration import acceleration

install(show_locals=True, width=300)  # initializing `rich.traceback`
colorama_init(autoreset=True)  # initializing `colorama`

parameters_body: list[str] = inspect.getfullargspec(Body).args[1:]
bodies, general = read_data(parameters_body)

n = len(bodies)  # number of bodies in simulation
dt, t_max, show_lines, output_rate, limx_min, limx_max, limy_min, limy_max = general

with open(path_to_tmp, 'w') as f:
	f.truncate(0)
	f.write(f"{n}\n")
	f.write(f"{dt}\n")
	f.write(f"{t_max}\n")
	for body in bodies:
		f.write(f"{body.x} {body.y} {body.vx} {body.vy} {int(body.fixed)}")

# --------CONFIGURING MATPLOTLIB--------

plt.style.use('dark_background')  # noqa

color_cycle = rcParams['axes.prop_cycle']()
colors_using: list[str] = [next(color_cycle)['color'] for _ in range(n)]


fig = plt.figure(figsize=(8, 8))
ax: mpl.axes.Axes = plt.axes()

ax.grid(True, ls='dashed', color='#333333')

ax.set_xlim((limx_min, limx_max))
ax.set_ylim((limy_min, limy_max))

if show_lines:
	lines: list[mpl.lines.Line2D] = [ax.plot([], [], color=colors_using[i])[0] for i in range(n)]  # initializing list of lines showing paths of bodies # noqa
	lines_data_x: list[list[float]] = [[] for _ in range(n)]
	lines_data_y: list[list[float]] = [[] for _ in range(n)]

markers: list[mpl.lines.Line2D] = [ax.plot([], [], 'o', markersize=10, label=f"Body {i}", color=colors_using[i])[0] for i in range(n)]  # initializing list of marker showing current position of bodies # noqa


# ----------BEGIN CALCULATIONS----------

def animate(frame: int) -> list[mpl.lines.Line2D]:  # noqa
	global t, t_last, t0  # noqa

	t += dt
	for i in range(n):
		body = bodies[i]

		if body.fixed:
			continue

		a = acceleration(bodies, i)

		body.x += body.vx * dt
		body.y += body.vy * dt

		body.vx += a[0] * dt
		body.vy += a[1] * dt

		if show_lines:
			lines_data_x[i].append(body.x)
			lines_data_y[i].append(body.y)

			lines[i].set_xdata(lines_data_x[i])
			lines[i].set_ydata(lines_data_y[i])

		markers[i].set_xdata((body.x,))
		markers[i].set_ydata((body.y,))

	if frame == 0:
		t0 = time.time()

	elif frame % output_rate == 0:
		t1 = time.time()

		print("\x1B[H\x1B[J")  # clearing console
		# it is better than `os.system('cls')`, bcos faster

		print('t =', TimeDelta(t, format='sec').datetime)
		print('fps =', round(output_rate / (t1 - t0), 2))
		print('tps =', TimeDelta((t - t_last) / (t1 - t0), format='sec').datetime)
		speed = round((t - t_last) / (t1 - t0))
		print('speed multiplier =', format(speed, ',').replace(',', ' '))  # do not refactor pls

		t_last = t
		t0 = time.time()

	ans = markers
	if show_lines:
		ans += lines

	return ans


anim = animation.FuncAnimation(fig, animate, interval=0.0001, blit=True, cache_frame_data=False)
ax.legend(loc="upper right")

try:
	plt.show()
except KeyboardInterrupt:
	print(f'{Fore.RED}Interrupted')
