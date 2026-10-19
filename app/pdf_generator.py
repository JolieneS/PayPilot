from pathlib import Path
from datetime import datetime

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from app.payroll import calculate_salary
from app.data_loader import load_employees


# ---------------------------------
# Fonts
# ---------------------------------

pdfmetrics.registerFont(
    TTFont("Arial", "C:/Windows/Fonts/arial.ttf")
)

pdfmetrics.registerFont(
    TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf")
)


# ---------------------------------
# Output Directory
# ---------------------------------

OUTPUT_DIR = Path(__file__).parent.parent / "generated_payslips"
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_payslip(employee_id: str):

    payroll = calculate_salary(employee_id)

    # Get employee information
    employees = load_employees()

    employee = employees[
        employees["Employee ID"] == employee_id
    ].iloc[0]

    # File name
    file_path = OUTPUT_DIR / (
        f"{employee_id}_{payroll['Month']}_payslip.pdf"
    )

    # Don't generate duplicate payslip
    if file_path.exists():
        return str(file_path)

    # ---------------------------------
    # PDF Setup
    # ---------------------------------

    doc = SimpleDocTemplate(
        str(file_path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()

    # ---------------------------------
    # Styles
    # ---------------------------------

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontName="Arial-Bold",
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Arial",
        fontSize=10,
        alignment=TA_CENTER,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Arial-Bold",
        fontSize=11,
        spaceBefore=8,
        spaceAfter=6,
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontName="Arial",
        fontSize=9,
    )

    elements = []

    # ---------------------------------
    # Header
    # ---------------------------------

    elements.append(
        Paragraph(
            "AI PAYROLL ASSISTANT",
            title_style
        )
    )

    elements.append(
        Paragraph(
            "SALARY PAYSLIP",
            subtitle_style
        )
    )

    elements.append(Spacer(1, 12))

    # ---------------------------------
    # Employee Information
    # ---------------------------------

    elements.append(
        Paragraph(
            "EMPLOYEE INFORMATION",
            section_style
        )
    )

    employee_data = [
        [
            Paragraph("<b>Employee ID</b>", normal_style),
            str(payroll["Employee ID"]),
            Paragraph("<b>Month</b>", normal_style),
            str(payroll["Month"]),
        ],
        [
            Paragraph("<b>Name</b>", normal_style),
            str(payroll["Name"]),
            Paragraph("<b>Email</b>", normal_style),
            str(payroll["Email"]),
        ],
        [
            Paragraph("<b>Department</b>", normal_style),
            str(employee["Department"]),
            Paragraph("<b>Designation</b>", normal_style),
            str(employee["Designation"]),
        ],
    ]

    employee_table = Table(
        employee_data,
        colWidths=[
            30 * mm,
            55 * mm,
            30 * mm,
            55 * mm,
        ],
    )

    employee_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

            ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
            ("BACKGROUND", (2, 0), (2, -1), colors.whitesmoke),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("FONTNAME", (0, 0), (-1, -1), "Arial"),

            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ])
    )

    elements.append(employee_table)

    # ---------------------------------
    # Salary Details
    # ---------------------------------

    elements.append(
        Paragraph(
            "SALARY DETAILS",
            section_style
        )
    )

    gross_salary = (
        payroll["Basic Salary"]
        + payroll["OT Pay"]
        + payroll["Bonus"]
    )

    total_deductions = (
        payroll["Leave Deduction"]
        + payroll["Half Day Deduction"]
    )

    earnings = [
        ["EARNINGS", "AMOUNT"],

        [
            "Basic Salary",
            f"₹ {payroll['Basic Salary']:,.2f}"
        ],

        [
            "Overtime Pay",
            f"₹ {payroll['OT Pay']:,.2f}"
        ],

        [
            "Bonus",
            f"₹ {payroll['Bonus']:,.2f}"
        ],

        [
            "Gross Salary",
            f"₹ {gross_salary:,.2f}"
        ],
    ]

    deductions = [
        ["DEDUCTIONS", "AMOUNT"],

        [
            "Leave Deduction",
            f"₹ {payroll['Leave Deduction']:,.2f}"
        ],

        [
            "Half Day Deduction",
            f"₹ {payroll['Half Day Deduction']:,.2f}"
        ],

        [
            "Total Deductions",
            f"₹ {total_deductions:,.2f}"
        ],
    ]

    # ---------------------------------
    # Earnings Table
    # ---------------------------------

    earnings_table = Table(
        earnings,
        colWidths=[
            50 * mm,
            35 * mm,
        ],
    )

    # ---------------------------------
    # Deductions Table
    # ---------------------------------

    deductions_table = Table(
        deductions,
        colWidths=[
            50 * mm,
            35 * mm,
        ],
    )

    table_style = TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

        ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Arial-Bold"),
        ("FONTNAME", (0, 1), (-1, -2), "Arial"),

        ("ALIGN", (1, 0), (1, -1), "RIGHT"),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ])

    earnings_table.setStyle(table_style)
    deductions_table.setStyle(table_style)

    # ---------------------------------
    # Combine Salary Tables
    # ---------------------------------

    salary_tables = Table(
        [
            [
                earnings_table,
                deductions_table
            ]
        ],
        colWidths=[
            85 * mm,
            85 * mm,
        ],
    )

    salary_tables.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ])
    )

    elements.append(salary_tables)

    elements.append(Spacer(1, 15))

    # ---------------------------------
    # Net Salary
    # ---------------------------------

    net_salary_table = Table(
        [
            [
                "NET SALARY",
                f"₹ {payroll['Net Salary']:,.2f}"
            ]
        ],
        colWidths=[
            85 * mm,
            85 * mm,
        ],
    )

    net_salary_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("FONTNAME", (0, 0), (-1, -1), "Arial-Bold"),

            ("FONTSIZE", (0, 0), (-1, -1), 14),

            ("ALIGN", (1, 0), (1, 0), "RIGHT"),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),

            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ])
    )

    elements.append(net_salary_table)

    elements.append(Spacer(1, 25))

    # ---------------------------------
    # Footer
    # ---------------------------------

    generated_date = datetime.now().strftime("%d-%m-%Y")

    footer_data = [
        [
            f"Payslip generated on: {generated_date}",
            "Computer-generated document",
        ]
    ]

    footer_table = Table(
        footer_data,
        colWidths=[
            85 * mm,
            85 * mm,
        ],
    )

    footer_table.setStyle(
        TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Arial"),

            ("FONTSIZE", (0, 0), (-1, -1), 8),

            ("TEXTCOLOR", (0, 0), (-1, -1), colors.grey),

            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ])
    )

    elements.append(footer_table)

    # ---------------------------------
    # Build PDF
    # ---------------------------------

    doc.build(elements)

    return str(file_path)


def generate_all_payslips():

    employees = load_employees()

    generated_files = []

    for employee_id in employees["Employee ID"]:

        file_path = generate_payslip(employee_id)

        generated_files.append(file_path)

    return generated_files