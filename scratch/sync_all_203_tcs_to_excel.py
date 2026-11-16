# -*- coding: utf-8 -*-
import openpyxl, re
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# 1. Parse all 203 TCs from reports/WORK_ASSIGNMENT_TEST_CASES.md
with open('reports/WORK_ASSIGNMENT_TEST_CASES.md', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
current_section = "General"
all_tcs = []

for line in lines:
    if line.startswith('### '):
        current_section = line.replace('### ', '').strip()
    elif line.startswith('## '):
        current_section = line.replace('## ', '').strip()
    
    if line.strip().startswith('|') and '`WA-' in line:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 6:
            tc_id = parts[1].replace('`', '').strip()
            if tc_id.startswith('WA-'):
                scenario = parts[2].strip()
                category = parts[3].strip() if len(parts) > 3 else ''
                params = parts[4].strip() if len(parts) > 4 else ''
                expected_http = parts[5].strip() if len(parts) > 5 else ''
                expected_resp = parts[6].strip() if len(parts) > 6 else ''
                
                # Determine priority
                if any(k in category.upper() for k in ['POS', 'BUS', 'FLOW']):
                    pri = 'P0'
                elif any(k in category.upper() for k in ['NEG', 'BVA']):
                    pri = 'P1'
                else:
                    pri = 'P2'
                
                # Determine type
                tc_type = category.lower() if category else 'functional'
                
                all_tcs.append({
                    'id': tc_id,
                    'section': current_section,
                    'scenario': scenario,
                    'params': params,
                    'expected': f"{expected_http} - {expected_resp}" if expected_resp else expected_http,
                    'pri': pri,
                    'type': tc_type,
                    'env': 'dev',
                    'status': 'Not-Run'
                })

print(f"Total TCs to sync: {len(all_tcs)}")

excel_files = [
    'AttendanceTestCases_Master_Consolidated.xlsx',
    'AttendanceTestCases.xlsx',
    'Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx'
]

header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
regular_font = Font(name="Calibri", size=10)
thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

headers = ['TC ID', 'Section', 'Test Scenario', 'Input / Preconditions', 'Expected Result', 'Pri', 'Type', 'Env', 'Status', 'QA Remarks', 'Source Origin']

for ef in excel_files:
    wb = openpyxl.load_workbook(ef)
    sheet_name = 'Work Assignments (Master 203)'
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]
    
    ws = wb.create_sheet(title=sheet_name)
    ws.append(headers)
    
    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
    
    for tc in all_tcs:
        row_data = [
            tc['id'],
            tc['section'],
            tc['scenario'],
            tc['params'],
            tc['expected'],
            tc['pri'],
            tc['type'],
            tc['env'],
            tc['status'],
            '',
            'Master Spec: WORK_ASSIGNMENT_TEST_CASES.md'
        ]
        ws.append(row_data)
        r = ws.max_row
        for c in range(1, len(row_data) + 1):
            cell = ws.cell(row=r, column=c)
            cell.font = regular_font
            cell.border = thin_border
            if c in [1, 6, 7, 8, 9]:
                cell.alignment = Alignment(horizontal="center", vertical="top")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    
    # Auto-fit column widths
    ws.column_dimensions['A'].width = 16
    ws.column_dimensions['B'].width = 35
    ws.column_dimensions['C'].width = 45
    ws.column_dimensions['D'].width = 40
    ws.column_dimensions['E'].width = 45
    ws.column_dimensions['F'].width = 8
    ws.column_dimensions['G'].width = 12
    ws.column_dimensions['H'].width = 8
    ws.column_dimensions['I'].width = 12
    ws.column_dimensions['J'].width = 20
    ws.column_dimensions['K'].width = 30
    
    wb.save(ef)
    print(f"Successfully added '{sheet_name}' with {len(all_tcs)} test cases to {ef}")
