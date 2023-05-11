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
			try:
				"""
				Checking:
				- availability of all parameters;
				- possibility of converting values to floats.
				"""
				value = body_dict.get(i, None)
				if i != 'fixed':
					value = float(value)

			except KeyError:
				raise KeyError(f"no parameter `{i}` found in section `{body_name}`")
			except ValueError:
				raise ValueError(f"parameter `{i} = {value}` in section `{body_name}` must be convertible to float")

			if i != 'fixed' and (np.isnan((value, )) or np.isinf((value, ))):  # checking for not-nan/inf
				raise ValueError(f"parameter `{i} = {value}` in section `{body_name}` must be not `inf`, or `nan`")

			params.append(value)

		bodies.append(Body(*params))

	return bodies
