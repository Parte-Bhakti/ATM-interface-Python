import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class ATMApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ATM Interface")
        self.center_window(800, 600)
        self.master.config(bg="#1e293b")  # Dark slate background

        self.data_file = 'users.json'
        self.users = self.load_users()
        self.current_user = None

        self.login_screen()

    def center_window(self, width=800, height=600):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def load_users(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    # -------------------- Login Screen --------------------
    def login_screen(self):
        self.clear_window()
        self.master.title("ATM Login")

        header = tk.Label(self.master, text="💳 Welcome to ATM", bg="#4f46e5", fg="white",
                          font=("Helvetica", 24, "bold"), pady=20)
        header.pack(fill="x")

        tk.Label(self.master, text="Enter your 4-digit PIN", bg="#1e293b", fg="white",
                 font=("Arial", 16)).pack(pady=40)

        self.pin_entry = tk.Entry(self.master, show="*", font=("Arial", 18), width=15, justify='center')
        self.pin_entry.pack()

        tk.Button(self.master, text="Login / Register", font=("Arial", 14, "bold"),
                  bg="#22c55e", fg="white", relief="raised", borderwidth=4,
                  command=self.authenticate).pack(pady=30)

    def authenticate(self):
        pin = self.pin_entry.get()
        if not pin or len(pin) != 4 or not pin.isdigit():
            messagebox.showwarning("Invalid", "Enter a valid 4-digit PIN.")
            return

        if pin in self.users:
            self.current_user = pin
            self.dashboard()
        else:
            create = messagebox.askyesno("Create Account", "PIN not found. Create new account?")
            if create:
                self.users[pin] = {"balance": 0, "history": []}
                self.save_users()
                self.current_user = pin
                messagebox.showinfo("Account Created", "New account created!")
                self.dashboard()

    # -------------------- Dashboard --------------------
    def dashboard(self):
        self.clear_window()
        self.master.title("ATM Dashboard")

        tk.Label(self.master, text=f"Welcome, User {self.current_user}", bg="#4f46e5",
                 fg="white", font=("Helvetica", 20), pady=15).pack(fill="x")

        button_style = {
            "font": ("Arial", 14),
            "width": 25,
            "padx": 5,
            "pady": 5,
            "relief": "raised",
            "borderwidth": 4
        }

        actions = [
            ("💰 Check Balance", "#0ea5e9", self.check_balance),
            ("➕ Deposit Money", "#10b981", self.deposit),
            ("➖ Withdraw Money", "#f59e0b", self.withdraw),
            ("📄 Transaction History", "#6366f1", self.show_history),
            ("🔐 Change PIN", "#8b5cf6", self.change_pin),
            ("🗑️ Delete Account", "#ef4444", self.delete_account),
            ("🚪 Logout", "#334155", self.login_screen)
        ]

        for text, color, command in actions:
            tk.Button(self.master, text=text, bg=color, fg="white",
                      command=command, **button_style).pack(pady=10)

    # -------------------- ATM Functions --------------------
    def check_balance(self):
        balance = self.users[self.current_user]["balance"]
        messagebox.showinfo("Balance", f"Your current balance is ₹{balance}")

    def deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount and amount > 0:
            self.users[self.current_user]["balance"] += amount
            self.users[self.current_user]["history"].append(f"Deposited ₹{amount}")
            self.save_users()
            messagebox.showinfo("Success", f"₹{amount} deposited successfully!")
        else:
            messagebox.showwarning("Error", "Invalid deposit amount.")

    def withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount and 0 < amount <= self.users[self.current_user]["balance"]:
            self.users[self.current_user]["balance"] -= amount
            self.users[self.current_user]["history"].append(f"Withdrew ₹{amount}")
            self.save_users()
            messagebox.showinfo("Success", f"₹{amount} withdrawn successfully!")
        else:
            messagebox.showwarning("Error", "Invalid amount or insufficient balance.")

    def show_history(self):
        history = self.users[self.current_user]["history"]
        if history:
            history_text = "\n".join(history)
        else:
            history_text = "No transactions yet."
        messagebox.showinfo("Transaction History", history_text)

    def change_pin(self):
        new_pin = simpledialog.askstring("Change PIN", "Enter new 4-digit PIN:")
        if new_pin and new_pin.isdigit() and len(new_pin) == 4:
            if new_pin in self.users:
                messagebox.showwarning("Error", "PIN already in use.")
                return
            self.users[new_pin] = self.users.pop(self.current_user)
            self.current_user = new_pin
            self.save_users()
            messagebox.showinfo("PIN Changed", "Your PIN has been changed successfully.")
            self.dashboard()
        else:
            messagebox.showwarning("Invalid", "PIN must be 4 digits.")

    def delete_account(self):
        confirm = messagebox.askyesno("Delete Account", "Are you sure you want to delete your account?")
        if confirm:
            del self.users[self.current_user]
            self.save_users()
            self.current_user = None
            messagebox.showinfo("Account Deleted", "Your account has been deleted.")
            self.login_screen()

    # -------------------- Utility --------------------
    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# -------------------- Main --------------------
root = tk.Tk()
app = ATMApp(root)
root.mainloop()
