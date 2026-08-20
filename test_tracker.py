"""
Unit and Integration Tests for Personal Expense Tracker
"""

import os
import unittest
import tempfile
import matplotlib
matplotlib.use('Agg')  # Headless backend for automated test/image rendering

from expense_tracker import (
    load_expenses,
    save_expenses,
    calculate_summary,
    visualize_expenses
)

class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        self.sample_expenses = [
            {"date": "2024-10-13", "category": "Food", "amount": 50.0, "description": "Groceries"},
            {"date": "2024-10-12", "category": "Transport", "amount": 20.0, "description": "Bus"},
            {"date": "2024-10-10", "category": "Entertainment", "amount": 35.5, "description": "Movies"},
            {"date": "2024-09-28", "category": "Shopping", "amount": 120.0, "description": "Clothes"},
        ]

    def test_calculate_summary(self):
        total, cat_totals, month_totals, highest, avg = calculate_summary(self.sample_expenses)
        
        self.assertEqual(total, 225.5)
        self.assertEqual(cat_totals["Food"], 50.0)
        self.assertEqual(cat_totals["Transport"], 20.0)
        self.assertEqual(cat_totals["Entertainment"], 35.5)
        self.assertEqual(cat_totals["Shopping"], 120.0)
        
        self.assertEqual(month_totals["2024-10"], 105.5)
        self.assertEqual(month_totals["2024-09"], 120.0)
        
        self.assertEqual(highest["amount"], 120.0)
        self.assertEqual(highest["category"], "Shopping")
        self.assertEqual(avg, 225.5 / 4)

    def test_save_and_load_csv(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tf:
            temp_path = tf.name

        try:
            # Save
            success = save_expenses(self.sample_expenses, temp_path)
            self.assertTrue(success)

            # Load
            loaded = load_expenses(temp_path)
            self.assertEqual(len(loaded), 4)
            self.assertEqual(loaded[0]["amount"], 50.0)
            self.assertEqual(loaded[0]["category"], "Food")
            self.assertEqual(loaded[3]["description"], "Clothes")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_visualize_expenses(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            img_path = tf.name

        try:
            visualize_expenses(self.sample_expenses, save_path=img_path, show_plot=False)
            self.assertTrue(os.path.exists(img_path))
            self.assertGreater(os.path.getsize(img_path), 1000)
        finally:
            if os.path.exists(img_path):
                os.remove(img_path)

if __name__ == "__main__":
    unittest.main()
