# Personal Expense Tracker

A command-line Python application to record, categorize, analyze, and visualize daily expenses.

---

## 📌 Features

1. **Add & Categorize Expenses**: Record expenses with amount, category (e.g. Food, Transport, Entertainment, etc.), date (`YYYY-MM-DD`), and optional description.
2. **View Expenses**: Formatted tabular view displaying all expense entries and grand total.
3. **Financial Reports & Analytics**:
   - Total expenditures & average expense amount.
   - Highest single expense.
   - Category-wise spending breakdown with percentage shares.
   - Monthly spending summary.
4. **Data Visualization (`matplotlib`)**:
   - Category-wise spending distribution pie chart.
   - Monthly / category spending comparison bar chart.
   - Automatically saved as `expense_analytics.png`.
5. **Persistent CSV File Storage**: Automatically loads on launch and saves updates to `expenses.csv` using Python's standard `csv` library.
6. **Robust Input Validation & Error Handling**: `try-except` blocks protect against invalid numerical inputs, malformed dates, and missing files.

---

## 🚀 How to Run

### 1. Prerequisites
Make sure Python 3.x and `matplotlib` are installed:
```bash
pip install matplotlib
```

### 2. Launch the Application
Run the interactive CLI tracker:
```bash
python expense_tracker.py
```

### 3. Run Automated Tests
```bash
python test_tracker.py
```

### 4. Run Demonstration
```bash
python run_demo.py
```

---

## 📁 Project Structure

```
personal_expense_tracker/
├── expense_tracker.py       # Main CLI application source code
├── expenses.csv             # CSV data storage
├── test_tracker.py          # Unit & integration tests
├── run_demo.py              # Automated demo script
├── expense_analytics.png    # Exported charts & analytics
└── README.md                # Project documentation
```
