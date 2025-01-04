import unittest
from returns_backend import get_product_returns

class TestReturns(unittest.TestCase):

    def test_product_returns(self):
        result = get_product_returns()
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0][0], "Produit A")

if _name_ == '_main_':
    unittest.main()