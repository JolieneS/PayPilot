from apscheduler.schedulers.background import BackgroundScheduler
from app.payroll_service import process_all_payslips


def run_scheduled_payroll():
    print("Running scheduled payroll process...")
    results = process_all_payslips()
    print(f"Payroll process completed: {len(results)} employees processed.")


scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(
        run_scheduled_payroll,
        "cron",
        day=28,
        hour=23,
        minute=59,
        id="monthly_payroll",
        replace_existing=True
    )

    scheduler.start()
    print("Payroll scheduler started.")