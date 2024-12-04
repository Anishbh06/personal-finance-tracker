import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import simpledialog
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    DATE_FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, 'a', newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully!")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.DATE_FORMAT)
        start_date = datetime.strptime(start_date, cls.DATE_FORMAT)
        end_date = datetime.strptime(end_date, cls.DATE_FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found")
        else:
            total_income = filtered_df[filtered_df["category"] == "income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "expense"]["amount"].sum()
            print(f"Total income: {total_income:.2f}")
            print(f"Total expense: {total_expense:.2f}")
            print(f"Net Savings: {total_income - total_expense:.2f}")
        return filtered_df

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        CSV.initialize_csv()  # Initialize CSV file if not already present

        # Create tabs
        self.tab_control = ttk.Notebook(root)
        self.add_transaction_tab = ttk.Frame(self.tab_control)
        self.view_summary_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.add_transaction_tab, text="Add Transaction")
        self.tab_control.add(self.view_summary_tab, text="View Summary")
        self.tab_control.pack(expand=1, fill="both")

        self.create_add_transaction_tab()
        self.create_view_summary_tab()

    def create_add_transaction_tab(self):
        ttk.Label(self.add_transaction_tab, text="Date (dd-mm-yyyy):").grid(column=0, row=0, padx=10, pady=10, sticky="w")
        self.date_entry = ttk.Entry(self.add_transaction_tab)
        self.date_entry.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(self.add_transaction_tab, text="Amount:").grid(column=0, row=1, padx=10, pady=10, sticky="w")
        self.amount_entry = ttk.Entry(self.add_transaction_tab)
        self.amount_entry.grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(self.add_transaction_tab, text="Category:").grid(column=0, row=2, padx=10, pady=10, sticky="w")
        self.category_entry = ttk.Entry(self.add_transaction_tab)
        self.category_entry.grid(column=1, row=2, padx=10, pady=10)

        ttk.Label(self.add_transaction_tab, text="Description:").grid(column=0, row=3, padx=10, pady=10, sticky="w")
        self.description_entry = ttk.Entry(self.add_transaction_tab)
        self.description_entry.grid(column=1, row=3, padx=10, pady=10)

        add_button = ttk.Button(self.add_transaction_tab, text="Add Transaction", command=self.add_transaction)
        add_button.grid(column=0, row=4, columnspan=2, pady=20)

    def create_view_summary_tab(self):
        ttk.Label(self.view_summary_tab, text="Start Date (dd-mm-yyyy):").grid(column=0, row=0, padx=10, pady=10, sticky="w")
        self.start_date_entry = ttk.Entry(self.view_summary_tab)
        self.start_date_entry.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(self.view_summary_tab, text="End Date (dd-mm-yyyy):").grid(column=0, row=1, padx=10, pady=10, sticky="w")
        self.end_date_entry = ttk.Entry(self.view_summary_tab)
        self.end_date_entry.grid(column=1, row=1, padx=10, pady=10)

        view_button = ttk.Button(self.view_summary_tab, text="View Summary", command=self.view_summary)
        view_button.grid(column=0, row=2, columnspan=2, pady=20)

        self.plot_frame = ttk.Frame(self.view_summary_tab)
        self.plot_frame.grid(column=0, row=3, columnspan=2, pady=20)

    def add_transaction(self):
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()

        if not date or not amount or not category or not description:
            messagebox.showerror("Input Error", "All fields are required")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number")
            return

        CSV.add_entry(date, amount, category, description)
        messagebox.showinfo("Success", "Transaction added successfully")

    def view_summary(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if not start_date or not end_date:
            messagebox.showerror("Input Error", "Both dates are required")
            return
        
        try:
            df = CSV.get_transactions(start_date, end_date)
            if df is not None:
                self.plot_transactions(df)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_transactions(self, df):
        self.clear_plot_frame()

        df.set_index("date", inplace=True)

        income_df = df[df["category"] == "income"].resample("D").sum().reindex(df.index, fill_value=0)
        expense_df = df[df["category"] == "expense"].resample("D").sum().reindex(df.index, fill_value=0)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(income_df.index, income_df["amount"], label="Income", color="g")
        ax.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount")
        ax.set_title("Income and Expenses over time")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def clear_plot_frame(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()