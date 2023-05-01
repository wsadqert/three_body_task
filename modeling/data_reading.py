from configparser import ConfigParser
from modeling.body import Body
import numpy as np


def read_data(data: ConfigParser, parameters_body: list[str]) -> list[Body]:
	bodies: list[Body] = []
	for body_name in data.keys():
		if 'Body' not in body_name:  # Do not read the 'General' section
			continue

		params: list[float] = []

		body_dict = data[body_name]  # dict name-value for each body
		for i in parameters_body:  # Getting the parameters
			try:  # checking availability of all parameters
				value: str = body_dict[i]
			except KeyError:
				if i == 'fixed':
					continue

				raise KeyError(f"no parameter `{i}` found in section `{body_name}`")

			try:  # checking possibility of converting values to floats
				float_value = float(value)
			except ValueError:
				if i != 'fixed':
					raise ValueError(f"parameter `{i} = {value}` in section `{body_name}` must be convertable to float")

			if np.isnan((float_value, )) or np.isinf((float_value, )):  # noqa  # checking for not-nan/inf
				raise ValueError(f"parameter `{i} = {value}` in section `{body_name}` must be not `inf`, or `nan`")

			params.append(float_value)

		bodies.append(Body(*params))

	return bodies
