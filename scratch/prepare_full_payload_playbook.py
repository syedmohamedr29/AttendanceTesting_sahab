# -*- coding: utf-8 -*-
"""
Rebuilds CDWT_Manual_Testing_Playbook.md with 100% complete, fully formatted,
copy-pasteable Request Body JSON payloads for EVERY test case.
No shortcuts, no placeholders, no tables. Pure text with full JSON blocks.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

# We will generate comprehensive test cases with full JSON bodies
script_code = '''# -*- coding: utf-8 -*-
import json

base_fixed_slots = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 6, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480}]},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []}
]

base_flexi_slots = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0}
]

base_split_slots = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}]},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}]},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}]},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}]},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}]},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "timeSlots": []}
]

# Write full file
'''

