# PayPilot


main
│
├── feature/data-extraction
├── feature/payroll-engine
├── feature/ml-models   ← You
└── feature/automation




# AI PayPilot 🚀

An AI-powered Payroll Management System designed specifically for **micro-businesses (1–10 employees)**. The platform simplifies payroll processing by automating salary prediction and aims to reduce manual effort, calculation errors, and processing time.

---

## 📌 Problem Statement

Micro-businesses often rely on Excel sheets or manual calculations to manage payroll. Every month, owners spend hours calculating:

- Employee Salaries
- Attendance
- Overtime
- Leave Deductions
- Bonuses
- Reimbursements
- Payroll Reports

Existing payroll software is often too expensive and too feature-heavy for businesses with only a handful of employees.

---

## 💡 Our Solution

AI PayPilot is a lightweight AI-powered payroll management system that automates payroll calculations while being affordable and easy to use for small businesses.

The platform includes:

- ✅ Payroll Cost Prediction (Implemented)
- 🔄 Overtime Prediction (Planned)
- 🔄 Absenteeism Risk Prediction (Planned)
- 🔄 Payroll Anomaly Detection (Planned)

---

## 🤖 Machine Learning

### Implemented Module

### Payroll Cost Prediction

Model Used:

- Random Forest Regressor

Input Features:

- Department
- Experience
- Base Salary
- Attendance Percentage
- Working Days
- Leave Days
- Overtime Hours
- Bonus
- Deductions
- Previous Payroll

Output:

- Predicted Payroll Cost (INR)

---

## 🛠 Tech Stack

### Machine Learning

- Python
- Google Colab
- Pandas
- NumPy
- Scikit-learn
- Joblib

### Prototype

- Figma

### Version Control

- Git
- GitHub

---

## 📂 Project Structure

```
AI-PayPilot/

├── dataset/
│   └── payroll_ml_dataset_5000.csv
│
├── notebooks/
│   └── payroll_prediction.ipynb
│
├── models/
│   └── payroll_forecast_model.pkl (Generated locally)
│
├── docs/
│   └── architecture.png
│
├── requirements.txt
│
└── README.md
```

---

## 📊 Dataset

The project uses a synthetic payroll dataset containing employee information such as:

- Employee ID
- Department
- Experience
- Attendance
- Working Days
- Leave Days
- Overtime Hours
- Bonus
- Deductions
- Previous Payroll
- Payroll Cost

---

## 🔮 Future Scope

- AI-based Overtime Prediction
- Employee Absenteeism Prediction
- Payroll Fraud Detection
- Salary Slip Generation
- WhatsApp Payslip Delivery
- GST & Tax Integration
- Dashboard Analytics
- Cloud Deployment

---

## 👥 Target Users

Micro-businesses with **1–10 employees**, including:

- Retail Shops
- Cafés
- Salons
- Tuition Centres
- Medical Shops
- Small Startups
- Local Businesses

---

## 🎯 Business Model

Subscription-based SaaS platform

- Basic Plan
- Professional Plan
- Enterprise Plan

---

## 📈 Current Status

- ✅ Problem Validation Completed
- ✅ Dataset Prepared
- ✅ Payroll Prediction Model Implemented
- ✅ GitHub Repository Created
- 🚧 Dashboard Prototype in Progress
- 🚧 Remaining AI Modules Planned

---

## 🚀 Future Development

The current implementation demonstrates the feasibility of AI-driven payroll prediction. Future versions will integrate the trained model into a web dashboard using a backend API (FastAPI/Flask) to provide real-time payroll predictions for business owners.

---

## 👨‍💻 Team

Developed as part of the E-Cell Startup Induction Project.

## PPT Presented :

https://www.canva.com/design/DAHRIYPztTQ/1ECM4WrH6F02OxHD0rH_ow/edit
