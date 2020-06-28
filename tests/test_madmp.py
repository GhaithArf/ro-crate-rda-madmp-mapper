from os import path
import unittest
import sys

sys.path.append(path.join(".."))

from madmp import *


MADMP_EXAMPLE_PATH = path.join("..", "examples", "madmp", "world-development-indicators")


class TestMADMP(unittest.TestCase):

	def test_load_madmp(self):
		"""Check that loading ma-DMPs works as expected."""
		# Test using existing project path
		try:
			MADMP(MADMP_EXAMPLE_PATH)
		except Exception as error:
			self.fail("Exception raised while instantiating ROCrate object using an existing path!")
		# Test using a broken path
		with self.assertRaises(Exception) as context:
			MADMP("badpath")
		self.assertTrue("Unable to locate the maDMP json file using the provided path." in str(context.exception))


if __name__ == '__main__':
	unittest.main()
