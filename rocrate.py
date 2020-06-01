import json
from os import listdir, walk
from os.path import isfile, join
import pprint
from utils import get_json_keys, load_rocrate_schema
import re


_ROCRATE_METADATA_FILENAME = "ro-crate-metadata.jsonld"
_ROCRATE_PREVIEW = "ro-crate-preview.html"


class ROCrate:

	# TODO: Use class methods
	# TODO: Create separate classes for preview and metadata???
	# TODO: GENERAL: Use prefixes for the different components of the framework when "logging"/stdout printing
	#		Example: [RO-Crate] log message
	#				 [maDMP] log message
	#		Look at log helper function in utils
	# TODO: Fix docstrings

	def __init__(self, path):
		self.root_folder = self.locate_root_folder(path)
		self.metadata = self.load_metadata()
		self.preview = self.load_preview()

	@staticmethod
	def locate_root_folder(path, check_name=True):
		"""Locate the root folder of the project based on the RO-Crate metadata file.

		:param path: path to crawl
		:param check_name: if True look for "ro-crate-metadata.jsonld", otherwise consider all "jsonld" files.
		:return: path of the root directory of the project
		"""
		# The RO-Crate Metadata File MUST be named ro-crate-metadata.jsonld and appear in the RO-Crate Root
		# This method will locate the first folder that contains metadata file and does not check for multiple
		# TODO: Consider the case where mutliple metadata files exist
		subdirs = [p[0] for p in walk(path)]
		for dir in subdirs:
			if check_name:
				if isfile(join(dir, _ROCRATE_METADATA_FILENAME)):
					return dir
			else:
				for file in listdir(dir):
					if file.lower().endswith('.jsonld'):
						return dir

	def load_metadata(self):
		"""Load the metadata file located at the root folder."""
		metadata_file = [file for file in listdir(self.root_folder) if file.endswith('.jsonld')]
		if metadata_file:
			with open("{}/{}".format(self.root_folder, metadata_file[0]), 'r') as file:
				if metadata_file != _ROCRATE_METADATA_FILENAME:
					print("Warning: Metadata file name: '{}' is different than {}".format(
						metadata_file, _ROCRATE_METADATA_FILENAME))
				print("Loading metadata file...")
				try:
					return json.loads(file.read())
				except json.JSONDecodeError:
					raise Exception("RO-Crate metadata file is not a valid JSON document.")
		else:
			raise Exception("Unable to locate metadata file.")

	def check_metadata_schema(self):
		"""Return True if the metadata schema matches the expected one, False otherwise."""
		# TODO: Consider all metadata attributes
		current_attributes = []
		get_json_keys(self.metadata, current_attributes)
		schema_attributes = []
		rocrate_schema = load_rocrate_schema()
		get_json_keys(rocrate_schema, schema_attributes)
		return set(current_attributes).issubset(set(schema_attributes))

	def load_preview(self, check_name=True, check_metadata=True):
		"""Return True if a RO-Crate website exists, False otherwise.

		:param check_name: if True look for "ro-crate-preview.html", otherwise consider all "html" files.
		"""
		# html file: MUST Contain a copy of the RO-Crate JSON-LD in a script element of the head element of the HTML
		# TODO: Clean and probably restructure (too many local variables)
		subdirs = [p[0] for p in walk(self.root_folder)]
		html_path = None
		for dir in subdirs:
			if check_name:
				if isfile(join(dir, _ROCRATE_PREVIEW)):
					html_path = join(dir, _ROCRATE_PREVIEW)
					break
			else:
				for file in listdir(dir):
					if file.endswith('.html'):
						html_path = join(dir, _ROCRATE_PREVIEW)
						break
		if html_path:
			print("Loading preview webpage...")
			html_file = open(html_path, 'r', encoding="utf-8")
			source_code = html_file.read()
			if check_metadata:
				# TODO: IMPROVE: use python native html parser instead of relyin on regex
				source_code_trimmed = source_code.replace("\n", "").replace('\r', '')
				search = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source_code_trimmed)
				if not json.loads((search[0])) == self.metadata:
					raise Exception("Preview webpage found, but does not contain a copy of the RO-Crate metadata.")
			return source_code
		else:
			print("Unable to locate preview webpage.")
			return None

	def has_preview_files(self):
		pass

	def has_dataset_payload(self):
		# The base RO-Crate specification makes no assumptions about the presence of any specific files or folders
		# beyond the reserved RO-Crate files described above. Payload files may appear directly in the RO-Crate Root
		# alongside the RO-Crate Metadata File, and/or appear in sub-directories of the RO-Crate Root. Each file and
		# directory MAY be represented as Data Entities in the RO-Crate Metadata File.
		pass

	def __repr__(self):
		return pprint.pformat(self.metadata)





