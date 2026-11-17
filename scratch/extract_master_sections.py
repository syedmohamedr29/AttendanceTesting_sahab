# -*- coding: utf-8 -*-

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    master_text = f.read()

# 1. Extract Section 1 (Executive Summary) up to Section 2
s1_start = master_text.find('## 1. Executive Summary & Defect Metrics Dashboard')
s2_start = master_text.find('## 2. Master Defect Quick-Reference Matrix')
s3_start = master_text.find('## 3. Module 1: Holiday Calendar Module')

assert s1_start != -1, "s1 not found"
assert s2_start != -1, "s2 not found"
assert s3_start != -1, "s3 not found"

exec_summary_and_matrix = master_text[s1_start:s3_start]
print("Length of Exec Summary + Quick-Ref Matrix:", len(exec_summary_and_matrix))

# 2. Extract PART X (Defects 64 to 74)
part_x_start = master_text.find('# PART X: SHIFT ROTATION WORK PLAN DEFECTS & ARCHITECTURAL GAPS (LIVE ATTENDANCE 11 AUDIT)')
part_x_end = master_text.find('### 📊 Master Re-Verification & Deduplication Summary', part_x_start)

assert part_x_start != -1, "part_x_start not found"
assert part_x_end != -1, "part_x_end not found"

part_x_full = master_text[part_x_start:part_x_end]
print("Length of PART X (Defects 64 to 74):", len(part_x_full))
