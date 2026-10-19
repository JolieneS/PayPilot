from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "data"

def load_employees():
    return pd.read_csv(DATA_DIR / "employees.csv")

def load_attendance():
    return pd.read_csv(DATA_DIR / "attendance.csv")

def load_leave_requests():
    return pd.read_csv(DATA_DIR / "leave_requests.csv")

def load_bonuses():
    return pd.read_csv(DATA_DIR / "bonuses.csv")

def load_payroll():
    return pd.read_csv(DATA_DIR / "payroll.csv")

def save_payroll(payroll):
    payroll.to_csv(DATA_DIR / "payroll.csv", index=False)