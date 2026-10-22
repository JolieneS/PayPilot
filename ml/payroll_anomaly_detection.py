import pandas as pd


def detect_payroll_anomalies(attendance_path, employees_path, payroll_path,
                             output_path="payroll_anomaly_report.csv"):
    attendance = pd.read_csv(attendance_path)
    employees = pd.read_csv(employees_path)
    payroll = pd.read_csv(payroll_path)

    data = attendance.merge(employees, on="Employee ID", how="left")
    data = data.merge(
        payroll.drop(columns=["Basic Salary"], errors="ignore"),
        on=["Employee ID", "Month"],
        how="left"
    )

    results = data[
        [
            "Employee ID", "Month", "Basic Salary", "Net Salary",
            "Overtime Hours", "Working Days", "Present Days",
            "Absent Days", "Half Days"
        ]
    ].copy()

    def find_flags(row):
        flags = []

        if row["Net Salary"] < 0:
            flags.append("Negative net salary")

        if row["Overtime Hours"] > row["Working Days"] * 4:
            flags.append("Unusually high overtime")

        recorded_days = (
            row["Present Days"] + row["Absent Days"] + row["Half Days"]
        )
        if recorded_days != row["Working Days"]:
            flags.append("Attendance totals need checking")

        if row["Net Salary"] > row["Basic Salary"] * 2:
            flags.append("Net salary unusually high compared with basic salary")

        return "; ".join(flags) if flags else "No rule-based flags"

    results["Flags"] = results.apply(find_flags, axis=1)
    results.to_csv(output_path, index=False)
    return results


if __name__ == "__main__":
    result = detect_payroll_anomalies(
        "../../data/attendance.csv",
        "../../data/employees.csv",
        "../../data/payroll.csv"
    )
    print(result[["Employee ID", "Net Salary", "Flags"]])
