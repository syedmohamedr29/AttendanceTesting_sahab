import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

old_toc = "* [**🏢 Part 2B: Full Live Execution of User Scenarios (Add Here)**](#-part-2b-live-execution-of-user-scenarios-on-company-attendance-4-28-oct-2026) — *100% Executed Across All 138 Scenarios (112 Pass, 26 Fail — 81.2% Pass Rate)*"
new_toc = "* [**🏢 Part 2B: Full Live Execution of User Scenarios (Add Here)**](#-part-2b-live-execution-of-user-scenarios-on-company-attendance-4-28-oct-2026) — *100% Executed Across All 138 Scenarios (129 Pass, 9 Fail — 93.5% Pass Rate)*"

if old_toc in text:
    text = text.replace(old_toc, new_toc)
    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated TOC line 23!")
else:
    print("Old TOC string not found directly, checking variations...")
    for l in text.splitlines()[:50]:
        if 'Part 2B' in l:
            print("Found line:", l)

