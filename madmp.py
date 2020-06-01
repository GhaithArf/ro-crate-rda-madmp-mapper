import json
from os import listdir
from os.path import isfile, isdir, join
import pprint

from utils import log


class MADMP:

	# TODO: Should the user provide the path to the json file or to the project?
	#		1 to many in the assignment means we only have one file for maDMP
	#		Support both file path and project path?

	def __init__(self, path):
		# TODO: json file path or project path? look in subfolders?
		self.path = path
		self.madmp = self.load_madmp()

	def load_madmp(self):
		"""Load the metadata file from the given path"""
		# TODO: cleanup
		json_path = ""
		if isfile(self.path) and self.path.lower().endswith(".json"):
			json_path = self.path
		elif isdir(self.path):
			# Look in the root path only! Do not look in subfolders since dataset itself may include json files
			for file in listdir(self.path):
				if file.lower().endswith('.json'):
					json_path = join(self.path, file)
					print("Successfully located the maDMP json file within the provided path.")
					setattr(self, "path", json_path) # Update path accordingly
					print("The maDMP path is set to {}".format(json_path))
		if not json_path:
			raise Exception("Unable to locate the maDMP json file using the provided path.")
		try:
			with open(json_path, 'r') as file:
				print("Loading maDMP file...")
				try:
					return json.loads(file.read())
				except json.JSONDecodeError:
					raise Exception("maDMP file is not a valid JSON document.")
		except FileNotFoundError:
			raise Exception("Unable to open the json maDMP file.")

	def __repr__(self):
		return pprint.pformat(self.madmp)


