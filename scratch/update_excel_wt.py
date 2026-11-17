import openpyxl

wb_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(wb_path)

if 'WT - Company Default' in wb.sheetnames:
    ws = wb['WT - Company Default']
    
    # Rows 5, 6, 89, 90
    updates = {
        5: "HTTP 200 (Cross-tenant leak: __tenant header ignored; returned company templates) | Re-verified 16-Nov-2026: Still Failing / Not Fixed (DEFECT-20261104-01). Synced to Confluence.",
        6: "HTTP 200 (Cross-company scoping fallback: returned 200 [] instead of 400 Cit.Attendance:9001) | Re-verified 16-Nov-2026: Still Failing / Not Fixed (DEFECT-20261028-04). Synced to Confluence.",
        89: "HTTP 200 (Tenant isolation failure: __tenant header bypassed; cross-tenant template access allowed) | Re-verified 16-Nov-2026: Still Failing / Not Fixed (DEFECT-20261104-01). Synced to Confluence.",
        90: "HTTP 200 (Company scoping fallback: foreign company returns HTTP 200 [] instead of 400 Cit.Attendance:9001) | Re-verified 16-Nov-2026: Still Failing / Not Fixed (DEFECT-20261028-04). Synced to Confluence."
    }
    
    for row_idx, note in updates.items():
        ws.cell(row=row_idx, column=10).value = note
        print(f"Updated row {row_idx}: {ws.cell(row=row_idx, column=1).value} -> {note[:60]}...")
    
    wb.save(wb_path)
    print("Successfully updated AttendanceTestCases_Master_Consolidated.xlsx!")
else:
    print("Sheet 'WT - Company Default' not found!")
