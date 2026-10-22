import pandas as pd


def estimate_payroll_cost(attendance_path, employees_path, payroll_path,
                          output_path="payroll_cost_estimates.csv"):
    attendance = pd.read_csv(attendance_path)
    employees = pd.read_csv(employees_path)
    payroll = pd.read_csv(payroll_path)

    data = attendance.merge(employees, on="Employee ID", how="left")
    data = data.merge(
        payroll.drop(columns=["Basic Salary"], errors="ignore"),
        on=["Employee ID", "Month"],
        how="left"
    )

    daily_salary = (
        data["Basic Salary"] / data["Working Days"].replace(0, float("nan"))
    )

    # Simplified baseline only; confirm the real payroll rules before use.
    data["Estimated Net Salary"] = (
        data["Basic Salary"]
        + data["Overtime Hours"] * data["OT Rate (per hr)"]
        - daily_salary.fillna(0) * data["Absent Days"]
    )

    data.to_csv(output_path, index=False)
    return data


if __name__ == "__main__":
    result = estimate_payroll_cost(
        "../../data/attendance.csv",
        "../../data/employees.csv",
        "../../data/payroll.csv"
    )
    print(result[["Employee ID", "Month", "Estimated Net Salary"]])
