from data_loader import (
    load_employees,
    load_attendance,
    load_leave_requests,
    load_bonuses,
    load_payroll,
)

employees = load_employees()
attendance = load_attendance()
leave_requests = load_leave_requests()
bonuses = load_bonuses()
payroll = load_payroll()

print(f"Employees: {len(employees)}")
print(f"Attendance Records: {len(attendance)}")
print(f"Leave Requests: {len(leave_requests)}")
print(f"Bonuses: {len(bonuses)}")
print(f"Payroll Records: {len(payroll)}")

print(employees.head())

from payroll import generate_payroll
import pprint

payroll = generate_payroll()

for employee in payroll:
    pprint.pprint(employee)

from app.payroll import generate_payroll

print(generate_payroll())