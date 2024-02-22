from astropy.constants import G  # noqa

from math import sqrt  # noqa
from numpy import abs  # noqa

G: float = G.value
t = 0.
t_last = 0.

path_to_config = './config.ini'

path_to_tmp = "R:/raw_data.dat"
path_to_output = "R:/output_data.dat"

path_to_solver = "%USERPROFILE%/source/repos/n-body_task/n-body_task.exe"
