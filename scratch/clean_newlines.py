with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize text by splitting on any newline sequence and filtering extra blank lines if doubled
lines = text.splitlines()
print(f"Total lines: {len(lines)}")
# Check if every second line is blank
blanks = sum(1 for line in lines if line == '')
print(f"Blank lines: {blanks} / {len(lines)}")

# If every second line is empty:
if blanks > len(lines) * 0.4:
    collapsed = []
    prev_blank = False
    for line in lines:
        if line == '':
            if not prev_blank:
                collapsed.append(line)
                prev_blank = True
        else:
            collapsed.append(line)
            prev_blank = False
    print(f"Collapsed lines: {len(collapsed)}")
    with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(collapsed) + '\n')
    print("Rewritten cleaned file!")

