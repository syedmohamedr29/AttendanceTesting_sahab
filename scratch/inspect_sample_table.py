with open('reports/WORK_ASSIGNMENT_TEST_CASES.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'WA-CHK-001' in l:
        print(f"Around line {i}:")
        for j in range(max(0, i-5), min(len(lines), i+10)):
            print(f"{j}: {lines[j].rstrip()}")
        break
