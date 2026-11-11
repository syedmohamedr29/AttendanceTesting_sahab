import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Step 3 & Step 4 in Part 2
idx_step3 = text.find('### Step 3: Company Holiday Calendar')
idx_step5 = text.find('### Step 5: Location Custom Holidays')
if idx_step5 == -1:
    idx_step5 = text.find('### Step 5:')
print("=== Step 3 & 4 (Lifecycle) ===")
print(text[idx_step3:idx_step3+2500])

# 2. Module 5 in Part 3
idx_mod5 = text.find('### Module 5: Holiday Calendars')
idx_mod6 = text.find('### Module 6:')
print("\n=== Module 5 (Catalog) ===")
print(text[idx_mod5:idx_mod6])

# 3. Collection detail in Part 4
idx_coll = text.find('#### 2. `ERP.Attendance.HolidayCalendars`')
idx_coll_next = text.find('#### 3. `ERP.Attendance.WorkPlans`')
print("\n=== Collection Architecture ===")
print(text[idx_coll:idx_coll_next])

