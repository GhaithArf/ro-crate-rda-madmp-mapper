from mapper import run
from os import listdir, makedirs, path
import logging


_MADMP_EXAMPLES_PATHS = [(path.join("examples", "madmp", d), d) for d in listdir(path.join("examples", "madmp"))]
_ROCRATE_EXAMPLES_PATHS = [(path.join("examples", "rocrate", d), d) for d in listdir(path.join("examples", "rocrate"))]


if __name__ == '__main__':

	# Transform all RDA maDMP examples to Ro-Crates
	for mpath, mname in _MADMP_EXAMPLES_PATHS:
		print("\n", "MADMP TO ROCRATE: Generating Rocrate for {}".format(mpath), sep="")
		run(mpath, path.join("demo_files", "generated_rocrates", mname))

	# Transform all Ro-Crates examples to RDA maDMP
	for rpath, rname in _ROCRATE_EXAMPLES_PATHS:
		print("\n", "ROCRATE TO MADMP: Generating MADMP for {}".format(rpath), sep="")
		target_path = path.join("demo_files", "generated_madmps", rname)
		try:
			makedirs(target_path)
		except FileExistsError:
			pass
		run(rpath, target_path)
