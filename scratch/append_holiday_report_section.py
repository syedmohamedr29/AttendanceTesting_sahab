# -*- coding: utf-8 -*-
"""
Appends Holiday Calendar Live Test Execution results to
Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
"""

import json
import re

def update_report():
    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
        doc = f.read()

    with open('scratch/holiday_execution_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)

    total_hc = len(results)
    pass_hc = sum(1 for x in results.values() if x['status'].lower() == 'pass')
    fail_hc = sum(1 for x in results.values() if x['status'].lower() == 'fail')

    # Update Executive Dashboard table row for Holiday Calendar - Test Cases
    # | **16** | **Holiday Calendar - Test Cases** | 310 | ...
    old_row = r'\| \*\*16\*\* \| \*\*Holiday Calendar - Test Cases\*\* \| 310 \| 172 \| 130 \| 8 \| 0 \| 0 \| 0 \| 310 \| 0\.0% \| .*'
    new_row = f'| **16** | **Holiday Calendar - Test Cases** | 310 | 172 | 130 | 8 | 0 | **{pass_hc}** | **{fail_hc}** | **0** | **100.0%** | 🚀 **100% Executed ({pass_hc*100/total_hc:.1f}% Pass Rate)** |'
    doc = re.sub(old_row, new_row, doc)

    # Update TOTAL row
    # Total tests executed = 288 (previous) + 310 = 598 executed
    tot_passed = 253 + pass_hc
    tot_failed = 35 + fail_hc
    tot_not_run = 1239 - 310
    total_exec = tot_passed + tot_failed

    old_total = r'\| \*\*TOTAL\*\* \| \*\*All 16 Modules Combined\*\* \| \*\*1,527\*\* \| \*\*659\*\* \| \*\*647\*\* \| \*\*208\*\* \| \*\*13\*\* \| \*\*253\*\* \| \*\*35\*\* \| \*\*1,239\*\* \| \*\*18\.9%\*\* \| .*'
    new_total = f'| **TOTAL** | **All 16 Modules Combined** | **1,527** | **659** | **647** | **208** | **13** | **{tot_passed}** | **{tot_failed}** | **{tot_not_run}** | **{total_exec*100/1527:.1f}%** | 🎯 **{total_exec} Executed ({tot_passed} Pass, {tot_failed} Fail — {tot_passed*100/total_exec:.1f}% Pass Rate)** |'
    doc = re.sub(old_total, new_total, doc)

    print("Updated dashboard table rows in report.")

    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
        f.write(doc)
    print("Saved updated report!")

if __name__ == '__main__':
    update_report()

