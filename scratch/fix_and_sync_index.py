# -*- coding: utf-8 -*-
import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
idx = wb['INDEX']

# Fix Row 19: User Scenarios (Add Here)
idx.cell(19, 8).value = "Custom QA Exploratory, Gaps, DTO, Fixed/Flexi Enums & Daily/Weekly Boundaries"
idx.cell(19, 9).value = 112
idx.cell(19, 10).value = 26
idx.cell(19, 11).value = 0
idx.cell(19, 12).value = 1.0 # 100%
idx.cell(19, 13).value = "✅ 100% Executed (81.2% Pass Rate)"

# Fix Row 20: Holiday Calendar - Test Cases
idx.cell(20, 8).value = "Complete Holiday Suite: DTO Validations, GUIDs, 5 Types, Combinations, Removals, CDWT Prerequisite, Publishing, Company Svc Sync & Location Auto-Assignment"
idx.cell(20, 9).value = 288
idx.cell(20, 10).value = 22
idx.cell(20, 11).value = 0
idx.cell(20, 12).value = 1.0 # 100%
idx.cell(20, 13).value = "🚀 100% Executed (92.9% Pass Rate)"

# Recalculate Row 21: TOTAL
tot_pass = 141 + 112 + 288 # 541
tot_fail = 9 + 26 + 22     # 57
tot_not_run = 1527 - (tot_pass + tot_fail) # 929
tot_exec = tot_pass + tot_fail # 598

idx.cell(21, 9).value = tot_pass
idx.cell(21, 10).value = tot_fail
idx.cell(21, 11).value = tot_not_run
idx.cell(21, 12).value = round(tot_exec / 1527, 3) # 39.2%
idx.cell(21, 13).value = f"🎯 {tot_exec} Executed ({tot_pass} Pass, {tot_fail} Fail — {tot_pass*100/tot_exec:.1f}% Pass Rate)"

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print(f"INDEX Updated Successfully!")
print(f"Row 19 (User Scenarios): Pass=112, Fail=26, Not-Run=0")
print(f"Row 20 (Holiday Calendar): Pass=288, Fail=22, Not-Run=0")
print(f"Row 21 (TOTAL): Total Executed={tot_exec}, Pass={tot_pass}, Fail={tot_fail}, Not-Run={tot_not_run}, Pass Rate={tot_pass*100/tot_exec:.1f}%")

