import requests
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load target company and auth token
with open("scratch/target_company.json") as f:
    target = json.load(f)

with open("scratch/current_token.json") as f:
    token_data = json.load(f)

company_id = target["company_id"]
company_name = target["company_name"]
token = token_data["access_token"]
tenant = target["tenant"]

base_url = "https://attendance2.dev.zoolwork.com"

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": tenant,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Define the DTO validation test cases for Company Default Work Template (Fixed, Flexi, Split)
dto_test_cases = [
    {
        "id": "CDWT-DTO-01",
        "section": "Template Name Validations",
        "scenario": "Template Name Missing / Empty Object",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {},
            "shortCode": "FXDT001",
            "weeklyOffDays": [5, 6],
            "fixedTimeSlots": []
        },
        "expected_code": 400,
        "validation_rule": "templateName must contain at least 'en' name"
    },
    {
        "id": "CDWT-DTO-02",
        "section": "Template Name Validations",
        "scenario": "Template Name 'en' Empty String",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": ""},
            "shortCode": "FXDT002",
            "weeklyOffDays": [5, 6],
            "fixedTimeSlots": []
        },
        "expected_code": 400,
        "validation_rule": "templateName.en cannot be empty"
    },
    {
        "id": "CDWT-DTO-03",
        "section": "Template Name Validations",
        "scenario": "Template Name Exceeds Max Length (101 characters)",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "A" * 101},
            "shortCode": "FXDT003",
            "weeklyOffDays": [5, 6],
            "fixedTimeSlots": []
        },
        "expected_code": 400,
        "validation_rule": "templateName length <= 100 characters"
    },
    {
        "id": "CDWT-DTO-04",
        "section": "Short Code Validations",
        "scenario": "Short Code Exceeds Exactly 7 Characters (8 chars)",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "Invalid ShortCode Length"},
            "shortCode": "FXDTO001", # 8 chars
            "weeklyOffDays": [5, 6],
            "fixedTimeSlots": []
        },
        "expected_code": 400,
        "validation_rule": "shortCode must be exactly 7 alphanumeric characters"
    },
    {
        "id": "CDWT-DTO-05",
        "section": "Short Code Validations",
        "scenario": "Short Code Under 7 Characters (6 chars)",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "ShortCode Under 7"},
            "shortCode": "FXDT01", # 6 chars
            "weeklyOffDays": [5, 6],
            "fixedTimeSlots": []
        },
        "expected_code": 400,
        "validation_rule": "shortCode must be exactly 7 alphanumeric characters"
    },
    {
        "id": "CDWT-DTO-06",
        "section": "Short Code Validations",
        "scenario": "Short Code Special Characters (@#$%)",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "ShortCode Special Chars"},
            "shortCode": "FX@#123",
            "weeklyOffDays": [5, 6],
            "fixedTimeSlots": []
        },
        "expected_code": 400,
        "validation_rule": "shortCode must be uppercase alphanumeric only"
    },
    {
        "id": "CDWT-DTO-07",
        "section": "7-Day Slots Structure Validations",
        "scenario": "Empty fixedTimeSlots Array",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "Empty Slots Array"},
            "shortCode": "FXDT007",
            "weeklyOffDays": [5, 6],
            "fixedTimeSlots": []
        },
        "expected_code": 400,
        "validation_rule": "fixedTimeSlots array must contain exactly 7 daily slots"
    },
    {
        "id": "CDWT-DTO-08",
        "section": "7-Day Slots Structure Validations",
        "scenario": "Incomplete Slots Array (Only 5 Days Provided)",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "5 Days Slots Only"},
            "shortCode": "FXDT008",
            "weeklyOffDays": [],
            "fixedTimeSlots": [
                {"day": 1, "isDayOff": False, "shiftStart": "09:00", "shiftEnd": "17:00", "totalWorkDurationInMinutes": 480},
                {"day": 2, "isDayOff": False, "shiftStart": "09:00", "shiftEnd": "17:00", "totalWorkDurationInMinutes": 480},
                {"day": 3, "isDayOff": False, "shiftStart": "09:00", "shiftEnd": "17:00", "totalWorkDurationInMinutes": 480},
                {"day": 4, "isDayOff": False, "shiftStart": "09:00", "shiftEnd": "17:00", "totalWorkDurationInMinutes": 480},
                {"day": 5, "isDayOff": True, "shiftStart": None, "shiftEnd": None, "totalWorkDurationInMinutes": 0}
            ]
        },
        "expected_code": 400,
        "validation_rule": "Must supply all 7 calendar days (Sun=1 to Sat=7)"
    },
    {
        "id": "CDWT-DTO-09",
        "section": "Day Enum Validations",
        "scenario": "Invalid DayEnum (Day 0 and Day 8)",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "Invalid DayEnum"},
            "shortCode": "FXDT009",
            "weeklyOffDays": [],
            "fixedTimeSlots": [
                {"day": 0, "isDayOff": True, "shiftStart": None, "shiftEnd": None, "totalWorkDurationInMinutes": 0},
                {"day": 8, "isDayOff": True, "shiftStart": None, "shiftEnd": None, "totalWorkDurationInMinutes": 0}
            ]
        },
        "expected_code": 400,
        "validation_rule": "DayEnum must be between 1 and 7"
    },
    {
        "id": "CDWT-DTO-10",
        "section": "Time Slot Boundary Validations",
        "scenario": "Inverted Shift Timings (shiftEnd < shiftStart on same day)",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "Inverted Shift Timings"},
            "shortCode": "FXDT010",
            "weeklyOffDays": [5, 6],
            "fixedTimeSlots": [
                {"day": 1, "isDayOff": False, "shiftStart": "17:00", "shiftEnd": "09:00", "totalWorkDurationInMinutes": 480},
                {"day": 2, "isDayOff": False, "shiftStart": "09:00", "shiftEnd": "17:00", "totalWorkDurationInMinutes": 480},
                {"day": 3, "isDayOff": False, "shiftStart": "09:00", "shiftEnd": "17:00", "totalWorkDurationInMinutes": 480},
                {"day": 4, "isDayOff": False, "shiftStart": "09:00", "shiftEnd": "17:00", "totalWorkDurationInMinutes": 480},
                {"day": 5, "isDayOff": False, "shiftStart": "09:00", "shiftEnd": "17:00", "totalWorkDurationInMinutes": 480},
                {"day": 6, "isDayOff": True, "shiftStart": None, "shiftEnd": None, "totalWorkDurationInMinutes": 0},
                {"day": 7, "isDayOff": True, "shiftStart": None, "shiftEnd": None, "totalWorkDurationInMinutes": 0}
            ]
        },
        "expected_code": 400,
        "validation_rule": "shiftEnd must be after shiftStart for day shift"
    },
    {
        "id": "CDWT-DTO-11",
        "section": "Mathematical Consistency Validations",
        "scenario": "TotalWorkDuration Mismatch with shiftStart/shiftEnd",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/fixed",
        "payload": {
            "templateName": {"en": "Math Duration Mismatch"},
            "shortCode": "FXDT011",
            "weeklyOffDays": [6, 7],
            "fixedTimeSlots": [
                {"day": 1, "isDayOff": False, "shiftStart": "09:00", "shiftEnd": "17:00", "totalWorkDurationInMinutes": 200}, # 8 hours = 480 mins, but passed 200
                {"day": 2, "isDayOff": False, "shiftStart": "09:00", "shiftEnd": "17:00", "totalWorkDurationInMinutes": 480},
                {"day": 3, "isDayOff": False, "shiftStart": "09:00", "shiftEnd": "17:00", "totalWorkDurationInMinutes": 480},
                {"day": 4, "isDayOff": False, "shiftStart": "09:00", "shiftEnd": "17:00", "totalWorkDurationInMinutes": 480},
                {"day": 5, "isDayOff": False, "shiftStart": "09:00", "shiftEnd": "17:00", "totalWorkDurationInMinutes": 480},
                {"day": 6, "isDayOff": True, "shiftStart": None, "shiftEnd": None, "totalWorkDurationInMinutes": 0},
                {"day": 7, "isDayOff": True, "shiftStart": None, "shiftEnd": None, "totalWorkDurationInMinutes": 0}
            ]
        },
        "expected_code": 400,
        "validation_rule": "totalWorkDurationInMinutes must match (shiftEnd - shiftStart - breaks)"
    },
    {
        "id": "CDWT-DTO-12",
        "section": "Flexi Work Template Validations",
        "scenario": "Flexi Daily Limit Exceeds 24 Hours (1500 minutes)",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/flexi",
        "payload": {
            "templateName": {"en": "Flexi Daily Over 24h"},
            "shortCode": "FLDT012",
            "flexibleType": 1, # Daily
            "dailyWorkDurationInMinutes": 1500, # 25 hours
            "weeklyOffDays": [6, 7]
        },
        "expected_code": 400,
        "validation_rule": "dailyWorkDurationInMinutes must be <= 1440 (24h)"
    },
    {
        "id": "CDWT-DTO-13",
        "section": "Flexi Work Template Validations",
        "scenario": "Flexi Weekly Limit Exceeds 168 Hours (11000 minutes)",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/flexi",
        "payload": {
            "templateName": {"en": "Flexi Weekly Over 168h"},
            "shortCode": "FLDT013",
            "flexibleType": 2, # Weekly
            "weeklyWorkDurationInMinutes": 11000, # > 10080
            "weeklyOffDays": [6, 7]
        },
        "expected_code": 400,
        "validation_rule": "weeklyWorkDurationInMinutes must be <= 10080 (168h)"
    },
    {
        "id": "CDWT-DTO-14",
        "section": "Split Shift Validations",
        "scenario": "Split Shift with Single Interval (< 2 intervals)",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/split",
        "payload": {
            "templateName": {"en": "Split Single Interval"},
            "shortCode": "SPDT014",
            "weeklyOffDays": [6, 7],
            "splitTimeSlots": [
                {
                    "day": 1,
                    "isDayOff": False,
                    "intervals": [
                        {"intervalNumber": 1, "shiftStart": "08:00", "shiftEnd": "12:00", "durationInMinutes": 240}
                    ]
                }
            ]
        },
        "expected_code": 400,
        "validation_rule": "Split shift requires at least 2 distinct working intervals per working day"
    },
    {
        "id": "CDWT-DTO-15",
        "section": "Split Shift Validations",
        "scenario": "Split Shift with Overlapping Intervals (08:00-12:00 and 11:00-15:00)",
        "method": "POST",
        "endpoint": f"/api/companies/{company_id}/worktemplates/split",
        "payload": {
            "templateName": {"en": "Split Overlap"},
            "shortCode": "SPDT015",
            "weeklyOffDays": [6, 7],
            "splitTimeSlots": [
                {
                    "day": 1,
                    "isDayOff": False,
                    "intervals": [
                        {"intervalNumber": 1, "shiftStart": "08:00", "shiftEnd": "12:00", "durationInMinutes": 240},
                        {"intervalNumber": 2, "shiftStart": "11:00", "shiftEnd": "15:00", "durationInMinutes": 240}
                    ]
                }
            ]
        },
        "expected_code": 400,
        "validation_rule": "Intervals within the same day cannot overlap"
    }
]

print(f"=== READY: {len(dto_test_cases)} DTO Validation Test Cases Configured ===")
print(f"Target Company: {company_name} ({company_id})")
print(f"Tenant: {tenant}")
print("Status: Prerequisite configuration COMPLETE. Ready for execution on user command.")

