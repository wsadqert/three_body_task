import configparser
from math import isnan, isinf

from constants import *
from modeling.body import Body


def read_data(parameters_body: list[str]) -> tuple[list[Body], list[float]]:
	data = configparser.ConfigParser()
	data.read(path_to_config)  # loading config file

	bodies: list[Body] = []
	general = data['General']

	for body_name in data.keys():
		if 'Body' not in body_name:  # Do not read the 'General' section
			continue

		params: list[float] = []
		body_dict = data[body_name]  # dict param-value for each body

		for i in parameters_body:  # Getting the parameters
			value = body_dict.get(i, None)
			try:
				"""
				Checking:
				- availability of all parameters;
				- possibility of converting values to floats.
				"""
				if i != 'fixed':
					value = float(value)

			except KeyError:
				raise KeyError(f"no parameter `{i}` found in section `{body_name}`")
			except ValueError:
				raise ValueError(f"parameter `{i} = {value}` in section `{body_name}` must be convertible to float")

			if i != 'fixed' and (isnan(value) or isinf(value)):  # checking for not-nan/inf
				raise ValueError(f"parameter `{i} = {value}` in section `{body_name}` must be not `±inf`, or `nan`")

			params.append(value)

		bodies.append(Body(*params))

	return bodies, [float(general[key]) for key in general.keys()]
