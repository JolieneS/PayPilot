from fastapi import FastAPI
from app.payroll import generate_payroll, calculate_salary
from app.pdf_generator import generate_payslip, generate_all_payslips
from app.email_service import send_payslip_email
from app.data_loader import load_employees, load_payroll, save_payroll
from app.payroll_service import process_all_payslips
from app.scheduler import start_scheduler

app = FastAPI(
    title="AI Payroll Assistant"
)
start_scheduler()

@app.get("/")
def root():
    return {"message": "AI Payroll Assistant API is Running"}

@app.get("/payroll/{employee_id}")
def get_employee_payroll(employee_id: str):
    return calculate_salary(employee_id)

@app.get("/payroll")
def get_all_payroll():
    return generate_payroll()

@app.get("/payslip/{employee_id}")
def create_payslip(employee_id: str):
    return {
        "message": "Payslip generated successfully",
        "file": generate_payslip(employee_id)
    }

@app.get("/payslips")
def create_all_payslips():
    return {
        "message": "All payslips generated successfully",
        "files": generate_all_payslips()
    }

@app.post("/test-email/{employee_id}")
def test_email(employee_id: str):

    payroll = calculate_salary(employee_id)

    payslip_path = generate_payslip(employee_id)

    result = send_payslip_email(
        employee_name=payroll["Name"],
        employee_email=payroll["Email"],
        month=payroll["Month"],
        net_salary=payroll["Net Salary"],
        payslip_path=payslip_path,
    )

    return result

@app.post("/send-all-payslips")
def send_all_payslips():

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

        payroll = calculate_salary(employee_id)

        payslip_path = generate_payslip(employee_id)

        result = send_payslip_email(
            employee_name=payroll["Name"],
            employee_email=payroll["Email"],
            month=payroll["Month"],
            net_salary=payroll["Net Salary"],
            payslip_path=payslip_path,
        )

        # Update payroll CSV
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

    return {
        "message": "Payroll email process completed",
        "results": results
    }

@app.post("/send-one-payslip/{employee_id}")
def send_one_payslip(employee_id: str):

    employees = load_employees()
    payroll_data = load_payroll()

    payroll_record = payroll_data[
        payroll_data["Employee ID"] == employee_id
    ]

    if payroll_record.empty:
        return {
            "status": "error",
            "message": "Employee not found in payroll.csv"
        }

    index = payroll_record.index[0]

    # Check duplicate
    if str(payroll_data.loc[index, "Email Sent"]).strip().lower() == "yes":
        return {
            "status": "skipped",
            "employee_id": employee_id,
            "message": "Email already sent"
        }

    payroll = calculate_salary(employee_id)

    payslip_path = generate_payslip(employee_id)

    result = send_payslip_email(
        employee_name=payroll["Name"],
        employee_email=payroll["Email"],
        month=payroll["Month"],
        net_salary=payroll["Net Salary"],
        payslip_path=payslip_path,
    )

    # Update payroll record
    payroll_data.loc[index, "Basic Salary"] = payroll["Basic Salary"]
    payroll_data.loc[index, "OT Pay"] = payroll["OT Pay"]
    payroll_data.loc[index, "Bonus"] = payroll["Bonus"]
    payroll_data.loc[index, "Leave Deduction"] = payroll["Leave Deduction"]
    payroll_data.loc[index, "Half Day Deduction"] = payroll["Half Day Deduction"]
    payroll_data.loc[index, "Net Salary"] = payroll["Net Salary"]
    payroll_data.loc[index, "Payslip Generated"] = "Yes"
    payroll_data.loc[index, "Email Sent"] = "Yes"

    save_payroll(payroll_data)

    return result

@app.post("/send-all-payslips")
def send_all_payslips():
    results = process_all_payslips()

    return {
        "message": "Payroll email process completed",
        "results": results
    }