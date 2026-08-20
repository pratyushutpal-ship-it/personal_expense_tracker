"""
Personal Expense Tracker
========================
A command-line tool to record, manage, analyze, and visualize daily expenses.

Features:
1. Add, View, and Categorize Expenses.
2. File Handling using Python's `csv` module for persistent data storage.
3. Summary Reports (total expenditure, category breakdown, monthly spending, highest expense).
4. Data Visualization using `matplotlib` (Category Distribution Pie Chart & Bar Chart).
5. Comprehensive Error Handling for user inputs.
"""

import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FILE = os.path.join(BASE_DIR, "expenses.csv")

# Predefined standard categories for convenience
CATEGORIES = [
    "Food",
    "Transport",
    "Entertainment",
    "Utilities",
    "Rent",
    "Health",
    "Shopping",
    "Education",
    "Other"
]


# =====================================================================
# 1. FILE HANDLING FUNCTIONS
# =====================================================================

def load_expenses(filename=DEFAULT_FILE):
    """
    Loads expense records from a CSV file into a list of dictionaries.
    If the file does not exist, returns an empty list.
    """
    expenses = []
    if not os.path.exists(filename):
        return expenses

    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    expense = {
                        "date": row["date"].strip(),
                        "category": row["category"].strip(),
                        "amount": float(row["amount"].strip()),
                        "description": row.get("description", "").strip()
                    }
                    expenses.append(expense)
                except (ValueError, KeyError):
                    # Skip malformed lines gracefully
                    continue
    except Exception as e:
        print(f"\n[Warning] Could not read file '{filename}': {e}")

    return expenses


def save_expenses(expenses, filename=DEFAULT_FILE):
    """
    Saves the list of expense dictionaries to a CSV file.
    """
    fieldnames = ["date", "category", "amount", "description"]
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for exp in expenses:
                writer.writerow({
                    "date": exp["date"],
                    "category": exp["category"],
                    "amount": f"{exp['amount']:.2f}",
                    "description": exp.get("description", "")
                })
        print(f"\n[Success] Expenses successfully saved to '{filename}'.")
        return True
    except PermissionError:
        print(f"\n[Error] Permission Denied: Could not write to '{filename}'.")
        print("  -> Solution: If 'expenses.csv' is currently open in Microsoft Excel or another program, please close it and choose 'Save and Exit' or add an expense again.")
        return False
    except Exception as e:
        print(f"\n[Error] Failed to save expenses to '{filename}': {e}")
        return False


# =====================================================================
# 2. INPUT VALIDATION HELPERS
# =====================================================================

def get_valid_date():
    """
    Prompts the user for a date in YYYY-MM-DD format.
    Allows pressing Enter to default to the current date.
    """
    today_str = datetime.today().strftime("%Y-%m-%d")
    while True:
        user_input = input(f"Enter date (YYYY-MM-DD) [Press Enter for today: {today_str}]: ").strip()
        if not user_input:
            return today_str
        try:
            valid_date = datetime.strptime(user_input, "%Y-%m-%d")
            return valid_date.strftime("%Y-%m-%d")
        except ValueError:
            print("  [!] Invalid date format. Please use YYYY-MM-DD (e.g., 2024-10-15).")


def get_valid_amount():
    """
    Prompts the user for a numeric expense amount greater than 0.
    """
    while True:
        user_input = input("Enter amount ($): ").strip()
        try:
            amount = float(user_input)
            if amount <= 0:
                print("  [!] Expense amount must be greater than 0.")
                continue
            return round(amount, 2)
        except ValueError:
            print("  [!] Invalid input. Please enter a valid numerical value (e.g. 25.50).")


def get_valid_category():
    """
    Prompts user to select from predefined categories or input a custom one.
    """
    print("\nSelect Category:")
    for idx, cat in enumerate(CATEGORIES, start=1):
        print(f"  {idx}. {cat}")
    print(f"  {len(CATEGORIES) + 1}. Custom Category")

    while True:
        choice = input(f"Enter choice (1-{len(CATEGORIES) + 1}): ").strip()
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(CATEGORIES):
                return CATEGORIES[choice_num - 1]
            elif choice_num == len(CATEGORIES) + 1:
                custom_cat = input("Enter custom category name: ").strip().title()
                if custom_cat:
                    return custom_cat
                print("  [!] Category name cannot be blank.")
            else:
                print(f"  [!] Please enter a number between 1 and {len(CATEGORIES) + 1}.")
        else:
            print("  [!] Invalid selection. Please enter a number.")


# =====================================================================
# 3. CORE OPERATIONS: ADD & VIEW
# =====================================================================

def add_expense(expenses):
    """
    Guides the user to input a new expense and adds it to the list.
    """
    print("\n" + "=" * 40)
    print("           ADD NEW EXPENSE")
    print("=" * 40)

    amount = get_valid_amount()
    category = get_valid_category()
    date = get_valid_date()
    description = input("Enter brief description/note (optional): ").strip()

    new_expense = {
        "date": date,
        "category": category,
        "amount": amount,
        "description": description
    }

    expenses.append(new_expense)
    print(f"\n[+] Added Expense: ${amount:.2f} for '{category}' on {date}.")


def view_expenses(expenses):
    """
    Displays all recorded expenses in a formatted table.
    """
    print("\n" + "=" * 70)
    print("                        ALL EXPENSES")
    print("=" * 70)

    if not expenses:
        print("No expenses recorded yet.")
        print("=" * 70)
        return

    # Table Header
    print(f"{'#':<4} {'Date':<12} {'Category':<16} {'Amount ($)':<12} {'Description'}")
    print("-" * 70)

    total = 0.0
    for idx, exp in enumerate(expenses, start=1):
        desc = exp.get("description", "")
        print(f"{idx:<4} {exp['date']:<12} {exp['category']:<16} ${exp['amount']:<11.2f} {desc}")
        total += exp['amount']

    print("-" * 70)
    print(f"{'TOTAL:':<33} ${total:.2f}")
    print("=" * 70)


# =====================================================================
# 4. REPORTS AND CALCULATIONS
# =====================================================================

def calculate_summary(expenses):
    """
    Calculates summary statistics from the list of expenses.
    Returns: total_spent, category_totals, monthly_totals, highest_expense, avg_expense
    """
    if not expenses:
        return 0, {}, {}, None, 0

    total_spent = sum(e["amount"] for e in expenses)
    category_totals = {}
    monthly_totals = {}
    highest_expense = expenses[0]

    for exp in expenses:
        # Category totals
        cat = exp["category"]
        category_totals[cat] = category_totals.get(cat, 0.0) + exp["amount"]

        # Monthly totals (YYYY-MM)
        month_key = exp["date"][:7] if len(exp["date"]) >= 7 else "Unknown"
        monthly_totals[month_key] = monthly_totals.get(month_key, 0.0) + exp["amount"]

        # Highest expense
        if exp["amount"] > highest_expense["amount"]:
            highest_expense = exp

    avg_expense = total_spent / len(expenses)

    return total_spent, category_totals, monthly_totals, highest_expense, avg_expense


def generate_report(expenses):
    """
    Generates and prints a detailed financial report.
    """
    print("\n" + "=" * 50)
    print("              EXPENSE REPORT")
    print("=" * 50)

    if not expenses:
        print("No expenses recorded yet to generate report.")
        print("=" * 50)
        return

    total_spent, category_totals, monthly_totals, highest_expense, avg_expense = calculate_summary(expenses)

    print(f"Total Number of Expenses : {len(expenses)}")
    print(f"Total Amount Spent       : ${total_spent:,.2f}")
    print(f"Average Expense Amount   : ${avg_expense:,.2f}")
    print(f"Highest Single Expense   : ${highest_expense['amount']:,.2f} ({highest_expense['category']} on {highest_expense['date']})")

    # Spending by Category
    print("\n" + "-" * 50)
    print(" SPENDING BY CATEGORY")
    print("-" * 50)
    print(f"{'Category':<20} {'Amount ($)':<15} {'Percentage'}")
    print("-" * 50)
    # Sorted by spending descending
    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    for cat, amt in sorted_cats:
        pct = (amt / total_spent) * 100 if total_spent > 0 else 0
        print(f"{cat:<20} ${amt:<14.2f} {pct:>6.1f}%")

    # Spending by Month
    print("\n" + "-" * 50)
    print(" MONTHLY SPENDING SUMMARY")
    print("-" * 50)
    print(f"{'Month (YYYY-MM)':<20} {'Amount ($)'}")
    print("-" * 50)
    for month in sorted(monthly_totals.keys()):
        print(f"{month:<20} ${monthly_totals[month]:,.2f}")

    print("=" * 50)


# =====================================================================
# 5. DATA VISUALIZATION
# =====================================================================

def visualize_expenses(expenses, save_path=None, show_plot=True):
    """
    Generates Matplotlib charts:
    - Pie Chart: Spending Breakdown by Category
    - Bar Chart: Monthly Spending Comparison
    """
    if not expenses:
        print("\n[!] No expenses available to visualize.")
        return

    total_spent, category_totals, monthly_totals, _, _ = calculate_summary(expenses)

    if not category_totals:
        print("\n[!] Insufficient data for visualization.")
        return

    # Create figure with 2 subplots side-by-side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Personal Expense Tracker - Visual Analytics", fontsize=16, fontweight='bold')

    # 1. Pie Chart: Category Distribution
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())
    colors = plt.cm.Set3.colors[:len(categories)]

    wedges, texts, autotexts = ax1.pie(
        amounts,
        labels=categories,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        textprops=dict(color="black")
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_weight("bold")
    ax1.set_title("Spending by Category", fontsize=13, fontweight='bold')

    # 2. Bar Chart: Monthly or Category Spending
    if len(monthly_totals) > 1:
        months = sorted(monthly_totals.keys())
        month_amts = [monthly_totals[m] for m in months]
        bars = ax2.bar(months, month_amts, color="#4C72B0", edgecolor="black")
        ax2.set_title("Monthly Spending Comparison", fontsize=13, fontweight='bold')
        ax2.set_xlabel("Month (YYYY-MM)", fontsize=11)
        ax2.set_ylabel("Total Spending ($)", fontsize=11)
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        for bar in bars:
            height = bar.get_height()
            ax2.annotate(f"${height:,.0f}",
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=9)
    else:
        bars = ax2.bar(categories, amounts, color="#55A868", edgecolor="black")
        ax2.set_title("Category Spending Comparison", fontsize=13, fontweight='bold')
        ax2.set_xlabel("Category", fontsize=11)
        ax2.set_ylabel("Amount ($)", fontsize=11)
        ax2.tick_params(axis='x', rotation=30)
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        for bar in bars:
            height = bar.get_height()
            ax2.annotate(f"${height:,.0f}",
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=9)

    plt.tight_layout()

    # Save chart if requested or default filename
    target_img = save_path or os.path.join(BASE_DIR, "expense_analytics.png")
    try:
        plt.savefig(target_img, dpi=300)
        print(f"\n[Success] Chart saved as '{target_img}'.")
    except Exception as e:
        print(f"\n[Error] Could not save chart image: {e}")

    if show_plot:
        try:
            plt.show()
        except Exception:
            pass


# =====================================================================
# 6. MAIN MENU AND CONTROL FLOW
# =====================================================================

def display_menu():
    """
    Displays the primary interactive menu.
    """
    print("\n" + "=" * 40)
    print("   Personal Expense Tracker")
    print("=" * 40)
    print("1. Add an Expense")
    print("2. View All Expenses")
    print("3. Generate Report")
    print("4. Visualize Expenses (Charts)")
    print("5. Save and Exit")
    print("=" * 40)


def main():
    """
    Main entry point for the Expense Tracker program.
    """
    print("=" * 50)
    print("  Welcome to Personal Expense Tracker!")
    print("=" * 50)

    # Load existing expenses from CSV on startup
    expenses = load_expenses(DEFAULT_FILE)
    print(f"Loaded {len(expenses)} expense record(s) from '{DEFAULT_FILE}'.")

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)
            # Automatically save changes
            save_expenses(expenses, DEFAULT_FILE)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            generate_report(expenses)

        elif choice == "4":
            print("\nGenerating spending charts...")
            visualize_expenses(expenses)

        elif choice == "5":
            save_expenses(expenses, DEFAULT_FILE)
            print("\nThank you for using Personal Expense Tracker! Goodbye.\n")
            break

        else:
            print("\n[!] Invalid selection. Please enter a valid number (1-5).")


if __name__ == "__main__":
    main()
