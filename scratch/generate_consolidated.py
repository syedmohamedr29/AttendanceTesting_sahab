import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb_out = openpyxl.Workbook()
wb_out.remove(wb_out.active)

# Load existing files
wb1 = openpyxl.load_workbook(r'AttendanceTestCases.xlsx', data_only=True)
wb2 = openpyxl.load_workbook(r'document (Enum and db collection)\AttendanceTestCases.xlsx', data_only=True)

header_fill = PatternFill(start_color='1E3A8A', end_color='1E3A8A', fill_type='solid')
header_font = Font(name='Calibri', size=11, bold=True, color='FFFFFF')

section_fill = PatternFill(start_color='F1F5F9', end_color='F1F5F9', fill_type='solid')
section_font = Font(name='Calibri', size=10, bold=True, color='0F172A')

data_font = Font(name='Calibri', size=10, color='1E293B')
border_thin = Border(
    left=Side(style='thin', color='E2E8F0'),
    right=Side(style='thin', color='E2E8F0'),
    top=Side(style='thin', color='E2E8F0'),
    bottom=Side(style='thin', color='E2E8F0')
)

p0_fill = PatternFill(start_color='FEE2E2', end_color='FEE2E2', fill_type='solid')
p0_font = Font(name='Calibri', size=10, bold=True, color='991B1B')

p1_fill = PatternFill(start_color='FEF3C7', end_color='FEF3C7', fill_type='solid')
p1_font = Font(name='Calibri', size=10, bold=True, color='92400E')

p2_fill = PatternFill(start_color='E0F2FE', end_color='E0F2FE', fill_type='solid')
p2_font = Font(name='Calibri', size=10, color='0369A1')

p3_fill = PatternFill(start_color='F3F4F6', end_color='F3F4F6', fill_type='solid')
p3_font = Font(name='Calibri', size=10, color='4B5563')

def extract_doc_rows(sheetname):
    if sheetname not in wb2.sheetnames: return []
    ws = wb2[sheetname]
    rows = []
    for r in ws.iter_rows(values_only=True):
        if r and r[0] and any(str(r[0]).strip().startswith(p) for p in ['A-', 'B-', 'C-', 'D-', 'E-', 'F-', 'G-', 'H-', 'I-', 'J-']):
            rows.append({
                'tc': f'DOC-{str(r[0]).strip()}',
                'section': str(r[1]).strip() if len(r)>1 and r[1] else '',
                'test': str(r[2]).strip() if len(r)>2 and r[2] else '',
                'detail': str(r[3]).strip() if len(r)>3 and r[3] else '',
                'expected': str(r[4]).strip() if len(r)>4 and r[4] else '',
                'pri': str(r[5]).strip() if len(r)>5 and r[5] else 'P1',
                'type': str(r[6]).strip() if len(r)>6 and r[6] else 'functional',
                'env': str(r[7]).strip() if len(r)>7 and r[7] else 'dev',
                'status': str(r[8]).strip() if len(r)>8 and r[8] else 'Not-Run',
                'remarks': str(r[9]).strip() if len(r)>9 and r[9] else '',
                'source': f'Doc: {sheetname}'
            })
    return rows

def extract_root_rows(sheetname):
    if sheetname not in wb1.sheetnames: return []
    ws = wb1[sheetname]
    rows = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r and len(r)>1 and r[1] and any(str(r[1]).strip().startswith(p) for p in ['A-', 'B-', 'C-', 'D-', 'E-', 'F-', 'G-', 'H-', 'I-', 'J-', 'K-', 'L-', 'M-', 'N-', 'O-']):
            rows.append({
                'tc': f'ROOT-{str(r[1]).strip()}',
                'section': str(r[2]).strip() if len(r)>2 and r[2] else '',
                'test': str(r[3]).strip() if len(r)>3 and r[3] else '',
                'detail': str(r[4]).strip() if len(r)>4 and r[4] else '',
                'expected': str(r[5]).strip() if len(r)>5 and r[5] else '',
                'pri': str(r[6]).strip() if len(r)>6 and r[6] else 'P1',
                'type': str(r[7]).strip() if len(r)>7 and r[7] else 'functional',
                'env': str(r[8]).strip() if len(r)>8 and r[8] else 'dev',
                'status': str(r[9]).strip() if len(r)>9 and r[9] else 'Not-Run',
                'remarks': '',
                'source': f'Root: {sheetname}'
            })
    return rows

module_configs = [
    {
        'title': 'WT - Company Default',
        'tab_color': '2563EB',
        'doc_sheets': ['Work Template - Company'],
        'root_sheets': ['Work Template - Company', 'Work Template - Versioning']
    },
    {
        'title': 'WT - Location Shifts',
        'tab_color': '2563EB',
        'doc_sheets': ['Work Template - Location'],
        'root_sheets': ['Work Template - Location']
    },
    {
        'title': 'WT - Roster & Rotation',
        'tab_color': '2563EB',
        'doc_sheets': ['Work Template - Roster+Rotation'],
        'root_sheets': []
    },
    {
        'title': 'Holiday Calendar - Company',
        'tab_color': '2563EB',
        'doc_sheets': ['Holiday Calendar - Company'],
        'root_sheets': ['Holiday Calendar - Company']
    },
    {
        'title': 'Holiday Calendar - Location',
        'tab_color': '2563EB',
        'doc_sheets': ['Holiday Calendar - Location'],
        'root_sheets': ['Holiday Calendar - Location']
    },
    {
        'title': 'Attendance Policies',
        'tab_color': '2563EB',
        'doc_sheets': ['Policy - Create & Edit', 'Policy - Delete, Lists & Usage'],
        'root_sheets': ['Policy (Break-Grace-Overtime)']
    },
    {
        'title': 'Work Plans',
        'tab_color': '16A34A',
        'doc_sheets': ['Work Plan - Regular', 'Work Plan - Lists & Employees', 'Work Plan - Roster Shift'],
        'root_sheets': ['Work Plan']
    },
    {
        'title': 'Work Assignments',
        'tab_color': '16A34A',
        'doc_sheets': ['Work Assignment - Assign', 'Work Assignment - Edit & Move', 'Work Assignment - Queries'],
        'root_sheets': ['Work Assignment (+ Map)']
    },
    {
        'title': 'Attendance Exemptions',
        'tab_color': '16A34A',
        'doc_sheets': [],
        'root_sheets': ['Attendance Config (Exemptions)']
    },
    {
        'title': 'Att Log - Upload (KT)',
        'tab_color': 'E11D48',
        'doc_sheets': [],
        'root_sheets': ['Att Log - Upload & Import']
    },
    {
        'title': 'Att Log - Finalise (KT)',
        'tab_color': 'E11D48',
        'doc_sheets': [],
        'root_sheets': ['Att Log - Processing Finalise']
    },
    {
        'title': 'Att Log - Edits (KT)',
        'tab_color': 'E11D48',
        'doc_sheets': [],
        'root_sheets': ['Att Log - Edit & Refinalise']
    },
    {
        'title': 'Att Log - Issues (KT)',
        'tab_color': 'E11D48',
        'doc_sheets': [],
        'root_sheets': ['Att Log - Issues']
    },
    {
        'title': 'Att Log - Monthly L4-L5 (KT)',
        'tab_color': 'E11D48',
        'doc_sheets': [],
        'root_sheets': ['Att Log - L4-L5 Data']
    }
]

headers = ['TC ID', 'Section', 'Test Scenario', 'Input / Preconditions', 'Expected Result', 'Pri', 'Type', 'Env', 'Status', 'QA Remarks', 'Source Origin']

# Build module sheets
sheet_stats = []

for cfg in module_configs:
    ws = wb_out.create_sheet(title=cfg['title'])
    ws.sheet_properties.tabColor = cfg['tab_color']
    ws.views.sheetView[0].showGridLines = True
    
    # Write header
    ws.append(headers)
    ws.row_dimensions[1].height = 26
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    
    all_rows = []
    for ds in cfg['doc_sheets']:
        all_rows.extend(extract_doc_rows(ds))
    for rs in cfg['root_sheets']:
        all_rows.extend(extract_root_rows(rs))
    
    p0_c, p1_c, p2_c, p3_c = 0, 0, 0, 0
    row_num = 2
    for r in all_rows:
        pri = r['pri'].upper()
        if 'P0' in pri: p0_c += 1
        elif 'P1' in pri: p1_c += 1
        elif 'P2' in pri: p2_c += 1
        else: p3_c += 1
        
        ws.append([
            r['tc'], r['section'], r['test'], r['detail'], r['expected'],
            r['pri'], r['type'], r['env'], r['status'], r['remarks'], r['source']
        ])
        
        # Style cells
        for c_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=row_num, column=c_idx)
            cell.font = data_font
            cell.border = border_thin
            cell.alignment = Alignment(vertical='top', wrap_text=True)
        
        # Priority chip style
        pri_cell = ws.cell(row=row_num, column=6)
        pri_cell.alignment = Alignment(horizontal='center', vertical='top')
        if 'P0' in pri:
            pri_cell.fill = p0_fill; pri_cell.font = p0_font
        elif 'P1' in pri:
            pri_cell.fill = p1_fill; pri_cell.font = p1_font
        elif 'P2' in pri:
            pri_cell.fill = p2_fill; pri_cell.font = p2_font
        else:
            pri_cell.fill = p3_fill; pri_cell.font = p3_font
            
        row_num += 1
    
    sheet_stats.append({
        'title': cfg['title'],
        'total': len(all_rows),
        'p0': p0_c,
        'p1': p1_c,
        'p2': p2_c,
        'p3': p3_c
    })

# Add User Scenarios Sheet
ws_user = wb_out.create_sheet(title='User Scenarios (Add Here)', index=0)
ws_user.sheet_properties.tabColor = 'D97706'
ws_user.views.sheetView[0].showGridLines = True
ws_user.append(headers)
ws_user.row_dimensions[1].height = 26
for col_idx in range(1, len(headers) + 1):
    cell = ws_user.cell(row=1, column=col_idx)
    cell.fill = PatternFill(start_color='D97706', end_color='D97706', fill_type='solid')
    cell.font = header_font
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

# Add 30 pre-formatted empty rows for user entry
for r_idx in range(2, 32):
    ws_user.append([f'USER-{r_idx-1:02d}', '', '', '', '', 'P1', 'functional', 'dev', 'Not-Run', '', 'User Custom'])
    for c_idx in range(1, len(headers) + 1):
        c = ws_user.cell(row=r_idx, column=c_idx)
        c.font = data_font
        c.border = border_thin
        c.alignment = Alignment(vertical='top', wrap_text=True)

# Add INDEX Sheet at position 0
ws_idx = wb_out.create_sheet(title='INDEX', index=0)
ws_idx.sheet_properties.tabColor = '0F172A'
ws_idx.views.sheetView[0].showGridLines = True

# Title block
ws_idx.append(['Attendance 2 - Master Consolidated Test Suite'])
ws_idx.cell(row=1, column=1).font = Font(name='Calibri', size=16, bold=True, color='1E3A8A')
ws_idx.append(['Consolidated from Root AttendanceTestCases.xlsx & document/AttendanceTestCases.xlsx | Release dev300-1.0.2'])
ws_idx.cell(row=2, column=1).font = Font(name='Calibri', size=10, italic=True, color='64748B')
ws_idx.append([])

idx_headers = ['#', 'Module / Sheet', 'Total TCs', 'P0 (Blocker)', 'P1 (Must Work)', 'P2 (Should)', 'P3 (Nice)', 'Testing Scope / Notes']
ws_idx.append(idx_headers)
ws_idx.row_dimensions[4].height = 24
for col_idx in range(1, len(idx_headers) + 1):
    c = ws_idx.cell(row=4, column=col_idx)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal='center', vertical='center')

total_tc, total_p0, total_p1, total_p2, total_p3 = 0, 0, 0, 0, 0

for i, st in enumerate(sheet_stats, start=1):
    total_tc += st['total']
    total_p0 += st['p0']
    total_p1 += st['p1']
    total_p2 += st['p2']
    total_p3 += st['p3']
    
    note = 'Core Active Testing'
    if '(KT)' in st['title']:
        note = 'Testing Deferred (Pending KT)'
    
    ws_idx.append([i, st['title'], st['total'], st['p0'], st['p1'], st['p2'], st['p3'], note])
    r_curr = ws_idx.max_row
    for c_idx in range(1, len(idx_headers) + 1):
        c = ws_idx.cell(row=r_curr, column=c_idx)
        c.font = data_font
        c.border = border_thin
        if c_idx in [1, 3, 4, 5, 6, 7]:
            c.alignment = Alignment(horizontal='center')

# Summary Total Row
ws_idx.append(['TOTAL', 'All 14 Modules Combined', total_tc, total_p0, total_p1, total_p2, total_p3, 'Master Consolidated Suite'])
r_tot = ws_idx.max_row
for c_idx in range(1, len(idx_headers) + 1):
    c = ws_idx.cell(row=r_tot, column=c_idx)
    c.font = Font(name='Calibri', size=11, bold=True, color='0F172A')
    c.fill = PatternFill(start_color='E2E8F0', end_color='E2E8F0', fill_type='solid')
    c.border = border_thin
    if c_idx in [1, 3, 4, 5, 6, 7]:
        c.alignment = Alignment(horizontal='center')

# Auto-adjust column widths across all sheets
col_widths = {
    'TC ID': 15, 'Section': 32, 'Test Scenario': 38, 'Input / Preconditions': 45,
    'Expected Result': 45, 'Pri': 10, 'Type': 14, 'Env': 12, 'Status': 14,
    'QA Remarks': 25, 'Source Origin': 28
}

for sheet in wb_out.worksheets:
    if sheet.title == 'INDEX':
        sheet.column_dimensions['A'].width = 6
        sheet.column_dimensions['B'].width = 34
        sheet.column_dimensions['C'].width = 14
        sheet.column_dimensions['D'].width = 14
        sheet.column_dimensions['E'].width = 14
        sheet.column_dimensions['F'].width = 14
        sheet.column_dimensions['G'].width = 14
        sheet.column_dimensions['H'].width = 32
        continue
    for c_idx, h in enumerate(headers, start=1):
        letter = get_column_letter(c_idx)
        sheet.column_dimensions[letter].width = col_widths.get(h, 20)

out_file = r'D:\Code\Attendance Testing\AttendanceTestCases_Master_Consolidated.xlsx'
wb_out.save(out_file)
print(f'Master Consolidated Workbook successfully saved: {out_file}')
print(f'Total Test Cases: {total_tc} (P0: {total_p0}, P1: {total_p1}, P2: {total_p2}, P3: {total_p3})')

