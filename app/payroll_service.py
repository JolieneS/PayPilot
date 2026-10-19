from app.data_loader import load_employees, load_payroll, save_payroll
from app.payroll import calculate_salary
from app.pdf_generator import generate_payslip
from app.email_service import send_payslip_email


def process_all_payslips():
    employees = load_employees()
    payroll_data = load_payroll()

    results = []

    for employee_id in employees["Employee ID"]:

        payroll_record = payroll_data[
            payroll_data["Employee ID"] == employee_id
        ]

        if payroll_record.empty:
            continue

        index = payroll_record.index[0]

        # Skip if email was already sent
        if str(payroll_data.loc[index, "Email Sent"]).strip().lower() == "yes":
            results.append({
                "employee_id": employee_id,
                "status": "skipped",
                "reason": "Email already sent"
            })
            continue

        # Calculate salary
        payroll = calculate_salary(employee_id)

        # Generate payslip
        payslip_path = generate_payslip(employee_id)

        # Send email
        result = send_payslip_email(
            employee_name=payroll["Name"],
            employee_email=payroll["Email"],
            month=payroll["Month"],
            net_salary=payroll["Net Salary"],
            payslip_path=payslip_path,
        )

        # Update payroll.csv
        payroll_data.loc[index, "Basic Salary"] = payroll["Basic Salary"]
        payroll_data.loc[index, "OT Pay"] = payroll["OT Pay"]
        payroll_data.loc[index, "Bonus"] = payroll["Bonus"]
        payroll_data.loc[index, "Leave Deduction"] = payroll["Leave Deduction"]
        payroll_data.loc[index, "Half Day Deduction"] = payroll["Half Day Deduction"]
        payroll_data.loc[index, "Net Salary"] = payroll["Net Salary"]
        payroll_data.loc[index, "Payslip Generated"] = "Yes"
        payroll_data.loc[index, "Email Sent"] = "Yes"

        save_payroll(payroll_data)

        results.append(result)

    return results