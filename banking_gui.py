import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json, os
from datetime import datetime

DATA_FILE = "data.json"

# ---------------- Helper Functions ----------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def generate_account_number(data):
    if not data:
        return "1001"
    last_acc = max(int(acc) for acc in data.keys())
    return str(last_acc + 1)

# ---------------- Core Banking Logic ----------------

def create_account():
    name = simpledialog.askstring("Create Account", "Enter Full Name:")
    if not name:
        return
    pin = simpledialog.askstring("Create Account", "Set a 4-digit PIN:", show='*')
    if not pin or not pin.isdigit() or len(pin) != 4:
        messagebox.showerror("Error", "PIN must be a 4-digit number.")
        return

    data = load_data()
    acc_no = generate_account_number(data)
    data[acc_no] = {"name": name.title(), "pin": pin, "balance": 0.0, "transactions": []}
    save_data(data)

    messagebox.showinfo("Success", f"Account Created!\nAccount Number: {acc_no}")

def deposit_money():
    acc_no = simpledialog.askstring("Deposit", "Enter Account Number:")
    pin = simpledialog.askstring("Deposit", "Enter PIN:", show='*')
    amount = simpledialog.askfloat("Deposit", "Enter Amount:")

    data = load_data()
    if acc_no not in data or data[acc_no]["pin"] != pin:
        messagebox.showerror("Error", "Invalid account or PIN.")
        return

    if amount <= 0:
        messagebox.showerror("Error", "Invalid amount.")
        return

    data[acc_no]["balance"] += amount
    data[acc_no]["transactions"].append({
        "type": "Deposit", "amount": amount, "time": str(datetime.now())
    })
    save_data(data)
    messagebox.showinfo("Success", f"Deposited ₹{amount:.2f}")

def withdraw_money():
    acc_no = simpledialog.askstring("Withdraw", "Enter Account Number:")
    pin = simpledialog.askstring("Withdraw", "Enter PIN:", show='*')
    amount = simpledialog.askfloat("Withdraw", "Enter Amount:")

    data = load_data()
    if acc_no not in data or data[acc_no]["pin"] != pin:
        messagebox.showerror("Error", "Invalid account or PIN.")
        return

    if amount <= 0 or amount > data[acc_no]["balance"]:
        messagebox.showerror("Error", "Invalid amount or insufficient balance.")
        return

    data[acc_no]["balance"] -= amount
    data[acc_no]["transactions"].append({
        "type": "Withdraw", "amount": amount, "time": str(datetime.now())
    })
    save_data(data)
    messagebox.showinfo("Success", f"Withdrawn ₹{amount:.2f}")

def check_balance():
    acc_no = simpledialog.askstring("Balance", "Enter Account Number:")
    pin = simpledialog.askstring("Balance", "Enter PIN:", show='*')

    data = load_data()
    if acc_no not in data or data[acc_no]["pin"] != pin:
        messagebox.showerror("Error", "Invalid account or PIN.")
        return

    balance = data[acc_no]["balance"]
    messagebox.showinfo("Balance", f"💰 Current Balance: ₹{balance:.2f}")

def view_transactions():
    acc_no = simpledialog.askstring("Transactions", "Enter Account Number:")
    pin = simpledialog.askstring("Transactions", "Enter PIN:", show='*')

    data = load_data()
    if acc_no not in data or data[acc_no]["pin"] != pin:
        messagebox.showerror("Error", "Invalid account or PIN.")
        return

    transactions = data[acc_no]["transactions"]
    if not transactions:
        messagebox.showinfo("Transactions", "No transactions found.")
        return

    # Create a popup window to display the history
    win = tk.Toplevel(root)
    win.title("Transaction History")
    win.geometry("500x300")

    tree = ttk.Treeview(win, columns=("Time", "Type", "Amount"), show='headings')
    tree.heading("Time", text="Date & Time")
    tree.heading("Type", text="Type")
    tree.heading("Amount", text="Amount (₹)")
    tree.column("Time", width=220)
    tree.column("Type", width=80)
    tree.column("Amount", width=100)

    for t in transactions:
        tree.insert("", "end", values=(t["time"], t["type"], f"₹{t['amount']:.2f}"))

    tree.pack(fill="both", expand=True)

# ---------------- Tkinter GUI Setup ----------------

root = tk.Tk()
root.title("🏦 Banking Management System")
root.geometry("400x400")
root.resizable(False, False)

title_label = tk.Label(root, text="🏦 Banking Management System", font=("Arial", 16, "bold"), pady=15)
title_label.pack()

btn_create = tk.Button(root, text="Create Account", command=create_account, width=25, height=2, bg="#4CAF50", fg="white")
btn_create.pack(pady=5)

btn_deposit = tk.Button(root, text="Deposit Money", command=deposit_money, width=25, height=2, bg="#2196F3", fg="white")
btn_deposit.pack(pady=5)

btn_withdraw = tk.Button(root, text="Withdraw Money", command=withdraw_money, width=25, height=2, bg="#FF9800", fg="white")
btn_withdraw.pack(pady=5)

btn_balance = tk.Button(root, text="Check Balance", command=check_balance, width=25, height=2, bg="#9C27B0", fg="white")
btn_balance.pack(pady=5)

btn_transactions = tk.Button(root, text="View Transactions", command=view_transactions, width=25, height=2, bg="#795548", fg="white")
btn_transactions.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", command=root.quit, width=25, height=2, bg="#f44336", fg="white")
btn_exit.pack(pady=15)

root.mainloop()
