import re, sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
master_path = "Defects/Attendance2_Master_Defect_Log.md"

# Read apply_defects_15_to_18.py to get defect_entries_report and defect_entries_master
import importlib.util
spec = importlib.util.spec_from_file_location("mod", "scratch/apply_defects_15_to_18.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

with open(report_path, "r", encoding="utf-8") as f:
    text_r = f.read()

if "#### Defect `DEFECT-20261110-15`" not in text_r:
    m = re.search(r'#### Defect `DEFECT-20261110-10`', text_r)
    if m:
        idx = m.start()
        text_r = text_r[:idx] + mod.defect_entries_report.strip() + "\n\n---\n\n" + text_r[idx:]
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(text_r)
        print("Report MD: Detail sections 15-18 inserted!")
    else:
        print("Report MD: Anchor not found!")
else:
    print("Report MD: Already contains DEFECT-20261110-15.")

with open(master_path, "r", encoding="utf-8") as f:
    text_m = f.read()

if "### <a id=\"defect-20261110-15\"></a>" not in text_m:
    m2 = re.search(r'### <a id="defect-20261110-10"></a>', text_m)
    if m2:
        idx2 = m2.start()
        text_m = text_m[:idx2] + mod.defect_entries_master.strip() + "\n\n---\n\n" + text_m[idx2:]
        with open(master_path, "w", encoding="utf-8") as f:
            f.write(text_m)
        print("Master Log: Detail sections 15-18 inserted!")
    else:
        print("Master Log: Anchor not found!")
else:
    print("Master Log: Already contains DEFECT-20261110-15.")
