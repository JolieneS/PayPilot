
from pathlib import Path
import pandas as pd
import joblib

PROJECT = Path(__file__).resolve().parents[2]
DATA = PROJECT / "data"
MODEL = PROJECT / "ml/models/payroll_isolation_forest.joblib"
OUTPUT = PROJECT / "ml/outputs/payroll_anomaly_results.csv"

def main():
    employees = pd.read_csv(DATA / "employees.csv")
    attendance = pd.read_csv(DATA / "attendance.csv")
    payroll = pd.read_csv(DATA / "payroll.csv")

    data = employees.merge(attendance, on="Employee ID", how="inner")

    payroll_data = payroll[[
        "Employee ID", "Month", "OT Pay", "Bonus",
        "Leave Deduction", "Half Day Deduction", "Net Salary"
    ]].rename(columns={"Net Salary": "Net Salary_payroll"})

    data = data.merge(
        payroll_data,
        on=["Employee ID", "Month"],
        how="inner"
    )

    feature_cols = [
        "Basic Salary", "Working Days", "Present Days",
        "Absent Days", "Half Days", "Overtime Hours",
        "OT Pay", "Bonus", "Leave Deduction",
        "Half Day Deduction", "Net Salary_payroll"
    ]

    X = data[feature_cols].apply(pd.to_numeric, errors="coerce")
    X = X.replace([float("inf"), float("-inf")], float("nan"))
    X = X.fillna(X.median()).fillna(0)

    model = joblib.load(MODEL)

    data["IsolationForest_Flag"] = [
        "Review" if value == -1 else "Not flagged"
        for value in model.predict(X)
    ]
    data["Anomaly_Score"] = -model.decision_function(X)

    data["Rule_Flags"] = ""

    def add_flag(mask, message):
        data.loc[mask, "Rule_Flags"] = data.loc[
            mask, "Rule_Flags"
        ].apply(lambda old: f"{old}; {message}".strip("; "))

    add_flag(data["Net Salary_payroll"] < 0, "Negative net salary")
    add_flag(
        data["Overtime Hours"] > data["Working Days"] * 4,
        "Unusually high overtime; review"
    )
    add_flag(
        data["Present Days"] + data["Absent Days"] > data["Working Days"],
        "Attendance totals exceed working days"
    )
    add_flag(
        data["Net Salary_payroll"] > 2 * data["Basic Salary"],
        "Net salary exceeds twice basic salary"
    )

    result = data[[
        "Employee ID", "Month", "Net Salary_payroll",
        "IsolationForest_Flag", "Anomaly_Score", "Rule_Flags"
    ]].rename(columns={"Net Salary_payroll": "Net Salary"})

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT, index=False)

    print("Payroll anomaly detection completed.")
    print(f"Results saved to: {OUTPUT}")
    print(result.to_string(index=False))

if __name__ == "__main__":
    main()
