from app.data_loader import (
    load_employees,
    load_attendance,
    load_bonuses,
)

employees = load_employees()
attendance = load_attendance()
bonuses = load_bonuses()

def calculate_salary(employee_id: str):
    employee = employees[employees["Employee ID"] == employee_id].iloc[0]
    attendance_record = attendance[attendance["Employee ID"] == employee_id].iloc[0]
    bonus_record = bonuses[bonuses["Employee ID"] == employee_id]
    bonus = (
    bonus_record["Amount"].sum()
    if not bonus_record.empty
    else 0)

    basic_salary = employee["Basic Salary"]
    ot_rate = employee["OT Rate (per hr)"]
    working_days = attendance_record["Working Days"]
    absent_days = attendance_record["Absent Days"]
    half_days = attendance_record["Half Days"]
    ot_hours = attendance_record["Overtime Hours"]


#Calculations
    daily_salary = basic_salary / working_days
    leave_deduction = daily_salary * absent_days
    half_day_deduction = (
    daily_salary * 0.5 * half_days
)
    overtime_pay = ot_hours * ot_rate

    net_salary = (
    basic_salary
    + overtime_pay
    + bonus
    - leave_deduction
    - half_day_deduction
)

    return {
    "Employee ID": str(employee["Employee ID"]),
    "Name": str(employee["Name"]),
    "Email": str(employee["Email"]),
    "Month": str(attendance_record["Month"]),

    "Basic Salary": float(basic_salary),
    "OT Pay": float(overtime_pay),
    "Bonus": float(bonus),

    "Leave Deduction": float(round(leave_deduction, 2)),
    "Half Day Deduction": float(round(half_day_deduction, 2)),
    "Net Salary": float(round(net_salary, 2))
}

def generate_payroll():
    payroll = []

    for employee_id in employees["Employee ID"]:
        payroll.append(
        calculate_salary(employee_id)
        )

    return payroll