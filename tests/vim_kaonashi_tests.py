import unittest
import vim_kaonashi as sut


@unittest.skip("Don't forget to test!")
class VimKaonashiTests(unittest.TestCase):

    def test_example_fail(self):
        result = sut.vim_kaonashi_example()
        self.assertEqual("Happy Hacking", result)
