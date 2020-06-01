import unittest

from madmp import *

class TestMADMP(unittest.TestCase):

	def test_load_madmp(self):
		"""Check that loading ma-DMPs works as expected."""
		# Test using existing project path
		try:
			MADMP("../examples/madmp/world_development_indicators_visualization_madmp.json")
		except Exception as error:
			self.fail("Exception raised while instantiating ROCrate object using an existing path!")
		# Test using a broken path
		with self.assertRaises(Exception) as context:
			MADMP("badpath")
		self.assertTrue("Unable to locate the maDMP json file using the provided path." in str(context.exception))

if __name__ == '__main__':
	unittest.main()
