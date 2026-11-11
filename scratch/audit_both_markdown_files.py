import re

file1 = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
file2 = "Defects/Attendance2_Master_Defect_Log.md"

with open(file1, "r", encoding="utf-8") as f:
    text1 = f.read()

with open(file2, "r", encoding="utf-8") as f:
    text2 = f.read()

def extract_defects(text):
    return set(re.findall(r'DEFECT-\d{8}-\d{2}', text))

defects1 = extract_defects(text1)
defects2 = extract_defects(text2)

print("=== 1. DEFECT ID AUDIT ===")
print(f"File 1 ({file1}) unique defects count: {len(defects1)}")
print(f"File 2 ({file2}) unique defects count: {len(defects2)}")

diff1_2 = defects1 - defects2
diff2_1 = defects2 - defects1

print(f"Defects in File 1 but NOT in File 2: {diff1_2 if diff1_2 else 'None (Clean Match)'}")
print(f"Defects in File 2 but NOT in File 1: {diff2_1 if diff2_1 else 'None (Clean Match)'}")

print("\n=== 2. RECENT DEFECTS AUDIT (05 & 06 NOV) ===")
recent = [
    "DEFECT-20261105-01",
    "DEFECT-20261105-02",
    "DEFECT-20261105-03",
    "DEFECT-20261105-04",
    "DEFECT-20261106-01",
    "DEFECT-20261106-02",
    "DEFECT-20261106-03",
    "DEFECT-20261106-04",
    "DEFECT-20261106-05",
    "DEFECT-20261106-06",
    "DEFECT-20261106-07"
]
for d in recent:
    c1 = text1.count(d)
    c2 = text2.count(d)
    print(f"{d:<20} | In Report: {c1:2d} times | In Master Defect Log: {c2:2d} times")

print("\n=== 3. VISUAL EVIDENCE AUDIT (Evidence 40 to 47) ===")
for ev in ["evidence_40", "evidence_41", "evidence_42", "evidence_43", "evidence_44", "evidence_45", "evidence_46", "evidence_47"]:
    c1 = text1.count(ev)
    c2 = text2.count(ev)
    print(f"{ev:<20} | In Report: {c1:2d} times | In Master Defect Log: {c2:2d} times")

print("\n=== 4. SEVERITY & METRIC COUNTERS AUDIT ===")
metrics1 = re.findall(r'Total Tracked Defects:\s*\*\*\d+\*\*|Total Defects:\s*\*\*\d+\*\*|P1 Critical:\s*\*\*\d+\*\*|P0 Blocker:\s*\*\*\d+\*\*|P2 Major:\s*\*\*\d+\*\*', text1)
metrics2 = re.findall(r'Total Tracked Defects:\s*\*\*\d+\*\*|Total Defects:\s*\*\*\d+\*\*|P1 Critical:\s*\*\*\d+\*\*|P0 Blocker:\s*\*\*\d+\*\*|P2 Major:\s*\*\*\d+\*\*', text2)

print("Metrics in Report:")
for m in set(metrics1):
    print(" ", m)

print("Metrics in Master Defect Log:")
for m in set(metrics2):
    print(" ", m)
