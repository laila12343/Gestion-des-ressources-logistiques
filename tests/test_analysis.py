import unittest
import json
from src.backend.analysis import get_top_selling_products

class TestAnalysis(unittest.TestCase):
    def test_get_top_selling_products(self):
        sales = [{"product": "A", "quantity": 10}, {"product": "B", "quantity": 5}]
        with open('data/sales.json', 'w') as f:
            json.dump(sales, f)
        result = get_top_selling_products()
        self.assertEqual(result[0][0], "A")