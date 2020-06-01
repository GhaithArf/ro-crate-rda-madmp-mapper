import json
import requests


ROCRATE_CURRENT_VERSION = 1.0
_SCHEMA_URL = "https://researchobject.github.io/ro-crate/{}/context.jsonld".format(ROCRATE_CURRENT_VERSION)
_LOG_PREFIX_ROCRATE = "[RO-Crate]"
_LOG_PREFIX_MADMP= "[MADMP]"
_LOG_PREFIX_MAPPER= "[MAPPER]"


def load_rocrate_schema():
	"""Retrieve the RO-Crate JSON-LD Context and parse its content

	:return: dict including the content of rocrate context
	"""
	try:
		response = requests.get(_SCHEMA_URL)
		response.raise_for_status()
		return json.loads(response.text)
	except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
		raise Exception("Unable to connect to the RO-Crate JSON-LD Context url!")


def get_json_keys(dictonary, keys_list):
	"""Add all keys from a nested dict structure to a list.

	:param dictonary: dict object
	:param keys_list: list where keys will be added
	"""
	if isinstance(dictonary, dict):
		for k, v in dictonary.items():
			keys_list.append(k)
			get_json_keys(v, keys_list)
	elif isinstance(dictonary, list):
		for i in dictonary:
			get_json_keys(i, keys_list)


def log(msg):
	"""Add prefix to the provided message and print the result.

	:param msg: message to be printed.
	"""
	# TODO: Implement this
	# Dynamically identify the module where the function was called, add prefix accordignly and print
	module = ""
	if "mapper" in module.lower():
		print("{}: {}".format(_LOG_PREFIX_MAPPER, msg))
	elif "rocrate" in module.lower():
		print("{}: {}".format(_LOG_PREFIX_ROCRATE, msg))
	elif "madmp" in module.lower():
		print("{}: {}".format(_LOG_PREFIX_MADMP, msg))
