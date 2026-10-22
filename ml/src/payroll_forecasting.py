
from pathlib import Path
import pandas as pd
import joblib

PROJECT = Path(__file__).resolve().parents[2]
DATA = PROJECT / "data"
MODEL = PROJECT / "ml/models/payroll_random_forest.joblib"
OUTPUT = PROJECT / "ml/outputs/payroll_predictions.csv"

def main():
    employees = pd.read_csv(DATA / "employees.csv")
    attendance = pd.read_csv(DATA / "attendance.csv")

    data = employees.merge(attendance, on="Employee ID", how="inner")

    numeric = [
        "Basic Salary", "OT Rate (per hr)", "Leave Balance",
        "Working Days", "Present Days", "Absent Days",
        "Half Days", "Overtime Hours"
    ]
    categorical = ["Department", "Designation", "Bonus Eligible"]

    X = data[numeric + categorical].copy()

    for col in numeric:
        X[col] = pd.to_numeric(X[col], errors="coerce")

    for col in categorical:
        X[col] = X[col].fillna("Unknown").astype(str)

    model = joblib.load(MODEL)
    data["Predicted Net Salary"] = model.predict(X)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result = data[["Employee ID", "Month", "Predicted Net Salary"]]
    result.to_csv(OUTPUT, index=False)

    print("Payroll forecasting completed.")
    print(f"Results saved to: {OUTPUT}")
    print(result.to_string(index=False))

if __name__ == "__main__":
    main()
