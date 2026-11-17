# -*- coding: utf-8 -*-
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Add explicit anchor for Section 1 and Section 7
if '## 1. Executive Summary & Defect Metrics Dashboard' in text and '<a id="1-executive-summary--defect-metrics-dashboard"></a>' not in text:
    text = text.replace(
        '## 1. Executive Summary & Defect Metrics Dashboard',
        '## 1. Executive Summary & Defect Metrics Dashboard\n\n<a id="1-executive-summary--defect-metrics-dashboard"></a>',
        1
    )

# Find Section 7
for line in text.split('\n'):
    if line.startswith('## 7.') or ('Verified Business Scenarios' in line and line.startswith('##')):
        print("Found Section 7 header:", line)
        if '<a id="7-verified-business-scenarios-confirmed-as-not-a-bug"></a>' not in text:
            text = text.replace(line, f"{line}\n\n<a id=\"7-verified-business-scenarios-confirmed-as-not-a-bug\"></a>", 1)
        break

with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated anchors in Defects/Attendance2_Master_Defect_Log.md")
