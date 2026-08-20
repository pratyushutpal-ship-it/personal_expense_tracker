"""
Demonstration Script for Personal Expense Tracker
Generates visual output and runs key operations to showcase CLI results.
"""

import matplotlib
matplotlib.use('Agg')  # Headless rendering

from expense_tracker import (
    load_expenses,
    view_expenses,
    generate_report,
    visualize_expenses,
    DEFAULT_FILE
)

def run_demonstration():
    print("=" * 60)
    print("  PERSONAL EXPENSE TRACKER - AUTOMATED DEMO & OUTPUT RUN")
    print("=" * 60)

    # 1. Load data
    expenses = load_expenses(DEFAULT_FILE)
    print(f"\n>> Step 1: Loaded {len(expenses)} existing expenses from '{DEFAULT_FILE}'.")

    # 2. View Expenses
    print("\n>> Step 2: Displaying All Expenses (Tabular View):")
    view_expenses(expenses)

    # 3. Generate Reports
    print("\n>> Step 3: Generating Financial Report & Summary Analytics:")
    generate_report(expenses)

    # 4. Generate Visualization
    print("\n>> Step 4: Generating Matplotlib Charts (Pie Chart & Monthly Bar Chart)...")
    visualize_expenses(expenses, save_path="expense_analytics.png", show_plot=False)
    print(">> Charts generated and saved as 'expense_analytics.png'!\n")

if __name__ == "__main__":
    run_demonstration()
