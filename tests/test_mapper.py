import unittest
from os import path
import sys

sys.path.append(path.join(".."))

from mapper import *
from .test_madmp import MADMP_EXAMPLE_PATH
from .test_rocrate import ROCRATE_EXAMPLE_PATH


class TestMapper(unittest.TestCase):

	def test_standard_detection(self):
		"""Check the abiliity of the mapper module to correcly identify maDMP and RO-Crate projects."""
		# maDMP
		mapper = Mapper(MADMP_EXAMPLE_PATH, ".")
		self.assertTrue(mapper.is_madmp() and not mapper.is_rocrate(), "Unbale to correcly identify maDMP project.")
		# RO-Crate
		mapper = Mapper(ROCRATE_EXAMPLE_PATH, ".")
		self.assertTrue(mapper.is_rocrate() and not mapper.is_madmp(), "Unbale to correcly identify RO-Crate project.")


if __name__ == '__main__':
	unittest.main()
