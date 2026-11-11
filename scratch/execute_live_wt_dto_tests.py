import requests
import json
import time
import openpyxl
from openpyxl.styles import PatternFill, Font
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/target_company.json") as f:
    target = json.load(f)

with open("scratch/current_token.json") as f:
    token_data = json.load(f)

company_id = target["company_id"]
token = token_data["access_token"]
tenant = target["tenant"]

base_url = "https://attendance2.dev.zoolwork.com"
headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": tenant,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Standard valid 7-day fixed time slots helper
def get_valid_fixed_slots(shift_start="09:00", shift_end="17:00", duration=480):
    return [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": shift_start, "endTime": shift_end, "workDurationInMinutes": duration},
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": shift_start, "endTime": shift_end, "workDurationInMinutes": duration},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": shift_start, "endTime": shift_end, "workDurationInMinutes": duration},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": shift_start, "endTime": shift_end, "workDurationInMinutes": duration},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": shift_start, "endTime": shift_end, "workDurationInMinutes": duration},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": None, "endTime": None, "workDurationInMinutes": 0},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": None, "endTime": None, "workDurationInMinutes": 0}
    ]

# Standard valid 7-day flexi slots helper
def get_valid_flexi_slots(duration=480):
    return [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": duration},
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": duration},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": duration},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": duration},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": duration},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0}
    ]

# Standard valid 7-day split slots helper
def get_valid_split_slots():
    return [
        {
            "dayEnum": 1,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "noOfInterval": 2,
            "timeSlots": [
                {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
                {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 2,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "noOfInterval": 2,
            "timeSlots": [
                {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
                {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 3,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "noOfInterval": 2,
            "timeSlots": [
                {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
                {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 4,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "noOfInterval": 2,
            "timeSlots": [
                {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
                {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 5,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "noOfInterval": 2,
            "timeSlots": [
                {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
                {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 6,
            "isWorkingDay": False,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 0,
            "noOfInterval": 0,
            "timeSlots": []
        },
        {
            "dayEnum": 7,
            "isWorkingDay": False,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 0,
            "noOfInterval": 0,
            "timeSlots": []
        }
    ]

# Define Test Matrix
test_matrix = [
    # --- Sheet: WT - Company Default (Layer 1 Command Validation) ---
    {
        "sheet": "WT - Company Default",
        "row": 54,
        "tc_id": "ROOT-A-01",
        "desc": "Any required header field missing (Missing Authorization / __tenant)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/fixed",
        "custom_headers": {"Content-Type": "application/json"}, # Missing Auth & tenant
        "payload": {
            "templateName": {"en": "Missing Auth Test"},
            "shortCode": "NOAUTH1",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "fixedTimeSlots": get_valid_fixed_slots()
        },
        "expected_status": 401,
        "rule": "Missing Authorization header must return 401 Unauthorized"
    },
    {
        "sheet": "WT - Company Default",
        "row": 55,
        "tc_id": "ROOT-A-02",
        "desc": "ShortCode boundary — not exactly 7 chars (8 chars)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "Invalid Short Code Length"},
            "shortCode": "TOOLONG1",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "fixedTimeSlots": get_valid_fixed_slots()
        },
        "expected_status": 400,
        "rule": "shortCode must be exactly 7 characters"
    },
    {
        "sheet": "WT - Company Default",
        "row": 56,
        "tc_id": "ROOT-A-03",
        "desc": "ShortCode non-alphanumeric (@#$%)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "Special Char ShortCode"},
            "shortCode": "FX@#123",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "fixedTimeSlots": get_valid_fixed_slots()
        },
        "expected_status": 400,
        "rule": "shortCode must be uppercase alphanumeric only"
    },

    # --- Sheet: User Scenarios (Add Here) - Fixed WT Validations ---
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 15,
        "tc_id": "USER-14",
        "desc": "Fixed WT - Reject Working Day payload contradiction (isWorkingDay=false with non-zero duration/times)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "Contradiction Day Off"},
            "shortCode": "FXCON01",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "fixedTimeSlots": [
                {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}, # Contradiction!
                {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": None, "endTime": None, "workDurationInMinutes": 0}
            ]
        },
        "expected_status": 400,
        "rule": "Day off cannot contain non-zero duration or active shift times"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 18,
        "tc_id": "USER-17",
        "desc": "Fixed WT - Reject invalid / out of range dayEnum (e.g. 0 or 8)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "Invalid DayEnum Range"},
            "shortCode": "FXDAY01",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "fixedTimeSlots": [
                {"dayEnum": 8, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": None, "endTime": None, "workDurationInMinutes": 0},
                {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": None, "endTime": None, "workDurationInMinutes": 0}
            ]
        },
        "expected_status": 400,
        "rule": "DayEnum must be between 1 (Sunday) and 7 (Saturday)"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 67,
        "tc_id": "USER-66",
        "desc": "Mandatory Validation - Template Name omitted / empty object {}",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {},
            "shortCode": "FXNAM01",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "fixedTimeSlots": get_valid_fixed_slots()
        },
        "expected_status": 400,
        "rule": "templateName must contain valid 'en' name string"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 68,
        "tc_id": "USER-67",
        "desc": "Boundary Validation - Template Name Length > 100 characters",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "A" * 105},
            "shortCode": "FXNAM02",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "fixedTimeSlots": get_valid_fixed_slots()
        },
        "expected_status": 400,
        "rule": "templateName length cannot exceed 100 characters"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 69,
        "tc_id": "USER-68",
        "desc": "Format & Length Validation - Short Code Under 7 Chars (5 chars)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "Short Code 5 Chars"},
            "shortCode": "FXSH5",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "fixedTimeSlots": get_valid_fixed_slots()
        },
        "expected_status": 400,
        "rule": "shortCode must be exactly 7 characters"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 71,
        "tc_id": "USER-70",
        "desc": "Array Completeness - Incomplete 7-Day Slot Array (Only 5 Days)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "5 Days Slots Only"},
            "shortCode": "FXINC01",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "fixedTimeSlots": get_valid_fixed_slots()[:5]
        },
        "expected_status": 400,
        "rule": "fixedTimeSlots array must contain exactly 7 daily slots"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 72,
        "tc_id": "USER-71",
        "desc": "Array Integrity - Duplicate DayEnum in Time Slots Array (Two Sunday entries)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "Duplicate DayEnum"},
            "shortCode": "FXDUP01",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "fixedTimeSlots": [
                {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}, # Duplicate!
                {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": None, "endTime": None, "workDurationInMinutes": 0},
                {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": None, "endTime": None, "workDurationInMinutes": 0}
            ]
        },
        "expected_status": 400,
        "rule": "All 7 days of the week must be defined, each day once"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 73,
        "tc_id": "USER-72",
        "desc": "Fixed Shift Boundary - Inverted Shift Times (shiftEnd <= shiftStart)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "Inverted Timings"},
            "shortCode": "FXINV01",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "fixedTimeSlots": [
                {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "17:00", "endTime": "09:00", "workDurationInMinutes": 480}, # Inverted!
                {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
                {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": None, "endTime": None, "workDurationInMinutes": 0},
                {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": None, "endTime": None, "workDurationInMinutes": 0}
            ]
        },
        "expected_status": 400,
        "rule": "shiftEnd must be after shiftStart"
    },

    # --- Flexible Work Template DTO Validations ---
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 34,
        "tc_id": "USER-33",
        "desc": "Flexi WT - Reject daily work duration exceeding 24 hours (1500 mins / 25h)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/flexi",
        "payload": {
            "templateName": {"en": "Flexi Daily Exceed 24h"},
            "shortCode": "FLX2401",
            "totalWorkDurationInMinutes": 1500,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "flexibleType": 1, # Daily
            "flexiTimeSlots": [
                {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 1500},
                {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
                {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
                {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
                {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
                {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
                {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0}
            ]
        },
        "expected_status": 400,
        "rule": "Daily work duration cannot exceed 1440 minutes (24 hours)"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 35,
        "tc_id": "USER-34",
        "desc": "Flexi WT - Reject weekly work duration exceeding total hours in a week (11000 mins > 10080 mins)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/flexi",
        "payload": {
            "templateName": {"en": "Flexi Weekly Exceed 168h"},
            "shortCode": "FLXWK01",
            "totalWorkDurationInMinutes": 11000,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "flexibleType": 2, # Weekly
            "flexiTimeSlots": get_valid_flexi_slots()
        },
        "expected_status": 400,
        "rule": "Total weekly work duration cannot exceed 10080 minutes (168 hours)"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 36,
        "tc_id": "USER-35",
        "desc": "Flexi WT - Reject active working day configured with 0 hours in Daily Flexible mode",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/flexi",
        "payload": {
            "templateName": {"en": "Flexi Daily Zero Hours"},
            "shortCode": "FLXZR01",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "flexibleType": 1, # Daily
            "flexiTimeSlots": [
                {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0}, # 0 hours on active day!
                {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
                {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
                {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
                {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
                {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
                {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0}
            ]
        },
        "expected_status": 400,
        "rule": "Active working day must have duration > 0 minutes"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 37,
        "tc_id": "USER-36",
        "desc": "Flexi WT - Reject negative work duration (< 0 mins)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/flexi",
        "payload": {
            "templateName": {"en": "Flexi Negative Duration"},
            "shortCode": "FLXNEG1",
            "totalWorkDurationInMinutes": -480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "flexibleType": 1,
            "flexiTimeSlots": [
                {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": -480},
                {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
                {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
                {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
                {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
                {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
                {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0}
            ]
        },
        "expected_status": 400,
        "rule": "workDurationInMinutes must be greater than 0"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 38,
        "tc_id": "USER-37",
        "desc": "Enum Validation - FlexibleType invalid value (e.g. 99)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/flexi",
        "payload": {
            "templateName": {"en": "Invalid FlexibleType"},
            "shortCode": "FLXEN01",
            "totalWorkDurationInMinutes": 2400,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "flexibleType": 99, # Invalid enum
            "flexiTimeSlots": get_valid_flexi_slots()
        },
        "expected_status": 400,
        "rule": "FlexibleType must be 1 (Daily) or 2 (Weekly)"
    },

    # --- Split Shift Work Template DTO Validations ---
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 60,
        "tc_id": "USER-59",
        "desc": "Split Negative - Overlapping Intervals within Same Day (08:00-12:00 & 11:00-15:00)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/split",
        "payload": {
            "templateName": {"en": "Split Overlap Intervals"},
            "shortCode": "SPOVL01",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "splitTimeSlots": [
                {
                    "dayEnum": 1,
                    "isWorkingDay": True,
                    "recurrenceOfMonth": [1, 2, 3, 4, 5],
                    "workDurationInMinutes": 480,
                    "noOfInterval": 2,
                    "timeSlots": [
                        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
                        {"startTime": "11:00", "endTime": "15:00", "workDurationInMinutes": 240} # Overlaps with 08:00-12:00!
                    ]
                },
                {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []},
                {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []}
            ]
        },
        "expected_status": 400,
        "rule": "Intervals within the same day cannot overlap"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 61,
        "tc_id": "USER-60",
        "desc": "Split Negative - Zero Gap Between Intervals (Contiguous 08:00-12:00 & 12:00-16:00)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/split",
        "payload": {
            "templateName": {"en": "Split Zero Gap"},
            "shortCode": "SPGAP01",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "splitTimeSlots": [
                {
                    "dayEnum": 1,
                    "isWorkingDay": True,
                    "recurrenceOfMonth": [1, 2, 3, 4, 5],
                    "workDurationInMinutes": 480,
                    "noOfInterval": 2,
                    "timeSlots": [
                        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
                        {"startTime": "12:00", "endTime": "16:00", "workDurationInMinutes": 240} # 0 gap!
                    ]
                },
                {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []},
                {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []}
            ]
        },
        "expected_status": 400,
        "rule": "Split shift must have break gap > 0 between intervals"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 62,
        "tc_id": "USER-61",
        "desc": "Split Negative - Inverted Start/End Timings in an Interval (12:00 to 08:00)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/split",
        "payload": {
            "templateName": {"en": "Split Inverted Timing"},
            "shortCode": "SPINV01",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "splitTimeSlots": [
                {
                    "dayEnum": 1,
                    "isWorkingDay": True,
                    "recurrenceOfMonth": [1, 2, 3, 4, 5],
                    "workDurationInMinutes": 480,
                    "noOfInterval": 2,
                    "timeSlots": [
                        {"startTime": "12:00", "endTime": "08:00", "workDurationInMinutes": 240}, # Inverted!
                        {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}
                    ]
                },
                {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []},
                {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []}
            ]
        },
        "expected_status": 400,
        "rule": "endTime must be after startTime within interval"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 63,
        "tc_id": "USER-62",
        "desc": "Split Negative - Single Interval Configured on Active Day (< 2 Intervals)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/split",
        "payload": {
            "templateName": {"en": "Split Single Interval Day"},
            "shortCode": "SPSNG01",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "splitTimeSlots": [
                {
                    "dayEnum": 1,
                    "isWorkingDay": True,
                    "recurrenceOfMonth": [1, 2, 3, 4, 5],
                    "workDurationInMinutes": 240,
                    "noOfInterval": 1, # Only 1 interval on active day!
                    "timeSlots": [
                        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}
                    ]
                },
                {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []},
                {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []}
            ]
        },
        "expected_status": 400,
        "rule": "Split shift requires at least 2 distinct intervals per active day"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 64,
        "tc_id": "USER-63",
        "desc": "Split Negative - Active Time Slots Configured on Day Off (Friday isWorkingDay=false with intervals)",
        "method": "POST",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/split",
        "payload": {
            "templateName": {"en": "Split Intervals on OffDay"},
            "shortCode": "SPOFF01",
            "totalWorkDurationInMinutes": 480,
            "totalWorkingDays": 5,
            "totalDaysOff": 2,
            "splitTimeSlots": [
                {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
                {
                    "dayEnum": 6,
                    "isWorkingDay": False, # Day off with active intervals!
                    "recurrenceOfMonth": [1, 2, 3, 4, 5],
                    "workDurationInMinutes": 240,
                    "noOfInterval": 1,
                    "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}]
                },
                {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []}
            ]
        },
        "expected_status": 400,
        "rule": "Day off cannot contain active time slots"
    },
    {
        "sheet": "User Scenarios (Add Here)",
        "row": 91,
        "tc_id": "USER-90",
        "desc": "PATCH Negative - Empty Request Body {} (Nothing to Update)",
        "method": "PATCH",
        "url": f"{base_url}/api/companies/{company_id}/worktemplates/fixed/00000000-0000-0000-0000-000000000001",
        "payload": {},
        "expected_status": 400,
        "rule": "Empty PATCH request body must be rejected"
    }
]

print(f"=== Starting Execution of {len(test_matrix)} DTO Validation Test Cases ===")
print(f"Company: Attendance 2 ({company_id}) | Tenant: {tenant}")

results = []
pass_count = 0
fail_count = 0

for idx, tc in enumerate(test_matrix, 1):
    req_headers = tc.get("custom_headers") if tc.get("custom_headers") is not None else headers
    method = tc["method"]
    url = tc["url"]
    payload = tc["payload"]
    expected_status = tc["expected_status"]
    
    start_time = time.time()
    try:
        if method == "POST":
            r = requests.post(url, json=payload, headers=req_headers, timeout=15)
        elif method == "PATCH":
            r = requests.patch(url, json=payload, headers=req_headers, timeout=15)
        latency_ms = int((time.time() - start_time) * 1000)
        
        status_code = r.status_code
        try:
            resp_body = r.json()
        except:
            resp_body = r.text
            
    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)
        status_code = 0
        resp_body = str(e)

    # Analyze Pass / Fail
    # Note: If validation error was triggered (e.g. ValidationException), the rule was enforced.
    # However, if HTTP status is 500 instead of 400, it's a defect in error handling!
    is_rule_enforced = False
    validation_err_msg = ""
    
    if isinstance(resp_body, dict) and "error" in resp_body:
        err = resp_body["error"]
        err_code = err.get("code")
        err_msg = err.get("message", "")
        validation_err_msg = f"{err_code}: {err_msg[:120].strip()}"
        if err_code in ["ValidationException", "Cit.Attendance:1701", "Cit.Attendance:1702", "Cit.Attendance:1703", "Cit.Attendance:1704", "Cit.Attendance:1705"]:
            is_rule_enforced = True
    elif status_code in [400, 401, 403, 404, 422]:
        is_rule_enforced = True
        validation_err_msg = str(resp_body)[:120]

    # Status judgment:
    # If expected 400, but got 500 (even with ValidationException), we record as FAIL (HTTP 500 Defect)
    # If expected 401 and got 401 -> PASS
    if status_code == expected_status:
        result_status = "Pass"
        pass_count += 1
    elif status_code == 500 and "ValidationException" in str(resp_body):
        # Rule caught by FluentValidation, but unhandled exception middleware returns 500!
        result_status = "Fail"
        fail_count += 1
    else:
        result_status = "Fail"
        fail_count += 1

    actual_remark = f"HTTP {status_code} | {validation_err_msg} | Latency: {latency_ms}ms"
    if status_code == 500 and "ValidationException" in str(resp_body):
        actual_remark = f"HTTP 500 (DEFECT: ValidationException returned 500 instead of 400) | {validation_err_msg} | Latency: {latency_ms}ms"

    print(f"\n[{idx:02d}/{len(test_matrix):02d}] {tc['tc_id']} ({tc['sheet']}) -> {result_status.upper()}")
    print(f"  Scenario: {tc['desc']}")
    print(f"  Expected: HTTP {expected_status} | Actual: HTTP {status_code} ({latency_ms}ms)")
    print(f"  Remarks:  {actual_remark[:120]}")

    results.append({
        "sheet": tc["sheet"],
        "row": tc["row"],
        "tc_id": tc["tc_id"],
        "desc": tc["desc"],
        "method": method,
        "url": url,
        "payload": payload,
        "expected_status": expected_status,
        "actual_status": status_code,
        "latency_ms": latency_ms,
        "response": resp_body,
        "result_status": result_status,
        "qa_remark": actual_remark
    })

# Save results JSON
with open("scratch/live_cdwt_dto_results.json", "w", encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n==================== EXECUTION SUMMARY ====================")
print(f"Total Test Cases Executed: {len(test_matrix)}")
print(f"Passed: {pass_count}")
print(f"Failed: {fail_count} (Detailed defect analysis generated)")
print(f"Results saved to scratch/live_cdwt_dto_results.json")

