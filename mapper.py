from argparse import ArgumentParser

from rocrate import *
from madmp import *


class Mapper:

	# TODO: The user does not have to explicitally mention the desired operation (rocrate to madmp or madmp to rocrate)
	#  		Based on the provided path, identify the type of the input and perform the mapping
	# TODO: Mapping will be based on the content of the file "mapping.json"
	# TODO: Integrate "CalcyteJS: https://code.research.uts.edu.au/eresearch/CalcyteJS" within madmp_to_rocrate to
	# 		generate a preview web page after mapping.


	def __init__(self):
		pass

	def is_rocrate(self):
		pass

	def is_madmp(self):
		pass

	def rocrate_to_madmp(self):
		pass

	def madmp_to_rocrate(self, generate_preview=True):
		pass


def run(root_folder_path, output_path):
	pass


if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument("-r", "--root-folder", dest="root_folder_path", help="Path to the root folder corresponding "
																			 "to a maDMP or RO-Crate.")
	parser.add_argument("-o", "--output-path", dest="output_path", help="Path where to mapped data will be stored.")
	args = parser.parse_args()
	run(args.root_folder_path, args.output_path)
