# PayPilot — Machine Learning Modules

## Overview

PayPilot is an AI-assisted payroll management system designed for micro-businesses with approximately 1–10 employees. It aims to simplify payroll operations by combining payroll calculations, employee data, attendance records, and machine learning techniques.

This branch, `feature/ml-models`, contains the initial implementations of two modules:

1. **Payroll Cost Estimation**
2. **Payroll Anomaly Detection**

These modules are intended to complement PayPilot's payroll engine. The payroll engine should remain responsible for calculating salaries according to confirmed business rules, while the ML modules provide estimates and identify records that may need further review.

## Modules

### 1. Payroll Cost Estimation

**File:** `src/payroll_forecasting.py`

This module provides a baseline estimate of employee net salary using employee and attendance information.

**Inputs include:**
- Basic salary
- Overtime rate per hour
- Overtime hours
- Working days
- Present days
- Absent days
- Half days
- Leave balance

**Current approach:**

The initial implementation calculates an estimated net salary using basic salary, estimated overtime pay, and a simplified absence deduction.

The estimate is intended as a prototype for exploring payroll cost estimation. It is not yet a trained or validated machine learning forecasting model.

**Potential future improvements:**
- Collect historical payroll records across multiple months.
- Define the exact prediction target, such as total monthly payroll expense.
- Confirm overtime, leave deduction, bonus, and half-day rules.
- Train and evaluate suitable regression models.
- Compare predictions with actual payroll outcomes using MAE and RMSE.

### 2. Payroll Anomaly Detection

**File:** `src/payroll_anomaly_detection.py`

This module identifies payroll records that meet predefined review conditions.

**Current checks include:**
- Negative net salary.
- Unusually high overtime relative to working days.
- Attendance totals that do not match working days.
- Net salary unusually high relative to basic salary.

**Current approach:**

The implementation uses transparent, rule-based checks. Each record receives a flag describing the condition that may require investigation.

An anomaly flag does not prove fraud or an incorrect payment. It indicates that the record should be reviewed by an authorised person.

**Potential future improvements:**
- Add payroll-specific validation rules.
- Compare payroll values with historical employee records.
- Evaluate anomaly detection techniques such as Isolation Forest when sufficient data is available.
- Allow configurable thresholds based on the organisation's payroll policies.

## Project Structure

```text
PayPilot/
├── data/
│   ├── employees.csv
│   ├── attendance.csv
│   ├── payroll.csv
│   ├── bonuses.csv
│   └── leave_requests.csv
├── ml/
│   
│── payroll_forecasting.py
│── payroll_anomaly_detection.py
│  
└── requirements.txt
 └── README.md
```

The CSV files are expected to be supplied by the shared PayPilot project. Do not commit employee names, email addresses, or other sensitive personal information to a public repository.

## Requirements

- Python 3.10 or later
- pandas
- numpy

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Modules

Run these commands from the `ml/` directory, assuming the shared `data/` directory is at the repository root.

### Payroll Cost Estimation

```bash
python src/payroll_forecasting.py
```

### Payroll Anomaly Detection

```bash
python src/payroll_anomaly_detection.py
```

The modules read the employee, attendance, and payroll CSV files and generate output CSV reports in the working directory.

## Data Requirements

The current implementation expects these files:

| File | Purpose |
|---|---|
| `employees.csv` | Employee salary information and overtime rates |
| `attendance.csv` | Working days, attendance and overtime hours |
| `payroll.csv` | Recorded salary components and net salary |

The expected column names must match those used in the Python modules.

## Current Limitations

- The prototype has been developed using a small sample containing 10 employee records for one month.
- A single month's data is insufficient to establish reliable future payroll forecasting performance.
- The cost estimation uses simplified assumptions and must not be treated as the official salary calculation.
- Payroll deduction and overtime rules must be confirmed before the estimates are used operationally.
- The anomaly detector currently uses fixed rules rather than a trained anomaly detection model.
- Model performance has not yet been established through robust evaluation on unseen historical data.

## Future Scope

- Integrate the modules with PayPilot's backend and payroll engine.
- Support historical, multi-month payroll data.
- Develop and evaluate a genuine regression model for payroll cost forecasting.
- Introduce configurable anomaly thresholds and historical comparisons.
- Add automated tests, data validation, and structured logging.
- Produce reports that can be reviewed by payroll administrators.

## Branch Information

**Branch:** `feature/ml-models`

**Status:** Initial prototype

This branch focuses on developing the machine learning and data-analysis components of PayPilot. Integration with the wider application should be performed in coordination with the team.
