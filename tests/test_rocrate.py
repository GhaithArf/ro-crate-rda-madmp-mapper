import unittest

from rocrate import *


class TestROCrate(unittest.TestCase):

	def test_load_rocrate(self):
		"""Check that loading RO-Crate files works as expected."""
		# Test using existing project path
		try:
			ROCrate("../examples/rocrate/GTM")
		except Exception as error:
			self.fail("Exception raised while instantiating ROCrate object using an existing path!")
		# Test using a broken path
		with self.assertRaises(Exception) as context:
			ROCrate("badpath")
		self.assertTrue("Unable to locate metadata file." in str(context.exception))


if __name__ == '__main__':
	unittest.main()
