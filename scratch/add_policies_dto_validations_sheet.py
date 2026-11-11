import sys
import json
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

DTO_HEADERS = [
    "TC ID",
    "Category",
    "Policy Type",
    "Field Under Test",
    "Test Scenario / Edge Case",
    "HTTP Method",
    "Endpoint Route",
    "Sample Request Payload (JSON)",
    "Expected HTTP & Code",
    "Pri",
    "Automation Status",
    "Manual Status",
    "Actual HTTP Code",
    "Actual Server Response / Notes",
    "Known Defect / QA Reference"
]

def get_dto_test_cases():
    cases = []
    
    # -------------------------------------------------------------------------
    # 1. Route & Security DTO Validations (8 TCs)
    # -------------------------------------------------------------------------
    cases.append({
        "TC ID": "POL-DTO-01",
        "Category": "1. Route & Security",
        "Policy Type": "All Types",
        "Field Under Test": "Authorization",
        "Test Scenario / Edge Case": "Missing Authorization header in request",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Break Test"}, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 401 Unauthorized",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "401 Unauthorized",
        "Actual Server Response / Notes": "Request blocked at API gateway / Auth middleware.",
        "Known Defect / QA Reference": "Core Security Invariant"
    })
    
    cases.append({
        "TC ID": "POL-DTO-02",
        "Category": "1. Route & Security",
        "Policy Type": "All Types",
        "Field Under Test": "Authorization",
        "Test Scenario / Edge Case": "Expired or forged Bearer token",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Grace Test"}, "lateCheckInGraceMinutes": 15}',
        "Expected HTTP & Code": "HTTP 401 Unauthorized",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "401 Unauthorized",
        "Actual Server Response / Notes": "JWT token signature validation failed.",
        "Known Defect / QA Reference": "Core Security Invariant"
    })

    cases.append({
        "TC ID": "POL-DTO-03",
        "Category": "1. Route & Security",
        "Policy Type": "All Types",
        "Field Under Test": "__tenant",
        "Test Scenario / Edge Case": "JWT token missing tenant claim",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "Overtime Test"}, "overtimeRule": "AfterShiftEnds"}',
        "Expected HTTP & Code": "HTTP 401 / 403 SbpAuthorizationException",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "401 / 403",
        "Actual Server Response / Notes": "Tenant ID was not resolved.",
        "Known Defect / QA Reference": "Multi-Tenant Isolation"
    })

    cases.append({
        "TC ID": "POL-DTO-04",
        "Category": "1. Route & Security",
        "Policy Type": "All Types",
        "Field Under Test": "Roles",
        "Test Scenario / Edge Case": "User role is not TenantAdmin (e.g. Employee)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Employee Break"}, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 403 Forbidden",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "403 Forbidden",
        "Actual Server Response / Notes": "[Authorize(Roles = 'TenantAdmin')] strictly blocks non-admins.",
        "Known Defect / QA Reference": "RBAC Policy Gate"
    })

    cases.append({
        "TC ID": "POL-DTO-05",
        "Category": "1. Route & Security",
        "Policy Type": "All Types",
        "Field Under Test": "companyId",
        "Test Scenario / Edge Case": "Malformed companyId GUID in route parameter (e.g. invalid-uuid-12345)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/invalid-uuid-12345/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Test"}, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Route parameter companyId is not a valid GUID.",
        "Known Defect / QA Reference": "ASP.NET Route Constraint"
    })

    cases.append({
        "TC ID": "POL-DTO-06",
        "Category": "1. Route & Security",
        "Policy Type": "All Types",
        "Field Under Test": "companyId",
        "Test Scenario / Edge Case": "Guid.Empty all-zeros companyId in route parameter",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/00000000-0000-0000-0000-000000000000/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Test"}, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 400 / 404 Not Found",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 / 404",
        "Actual Server Response / Notes": "Company does not exist.",
        "Known Defect / QA Reference": "Entity Scope Check"
    })

    cases.append({
        "TC ID": "POL-DTO-07",
        "Category": "1. Route & Security",
        "Policy Type": "All Types",
        "Field Under Test": "policyId",
        "Test Scenario / Edge Case": "Malformed policyId GUID on PATCH /delete route parameter",
        "HTTP Method": "PATCH",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/malformed-policy-guid/delete",
        "Sample Request Payload (JSON)": "{}",
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Route parameter policyId is not a valid GUID.",
        "Known Defect / QA Reference": "ASP.NET Route Constraint"
    })

    cases.append({
        "TC ID": "POL-DTO-08",
        "Category": "1. Route & Security",
        "Policy Type": "All Types",
        "Field Under Test": "policyId",
        "Test Scenario / Edge Case": "Guid.Empty all-zeros policyId on PATCH /delete route parameter",
        "HTTP Method": "PATCH",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/00000000-0000-0000-0000-000000000000/delete",
        "Sample Request Payload (JSON)": "{}",
        "Expected HTTP & Code": "HTTP 400 / 404 Not Found",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 / 404",
        "Actual Server Response / Notes": "Cit.Attendance:1501 Policy not found.",
        "Known Defect / QA Reference": "Entity Scope Check"
    })

    # -------------------------------------------------------------------------
    # 2. Common Policy Headers, Name & State DTO Validations (10 TCs)
    # -------------------------------------------------------------------------
    cases.append({
        "TC ID": "POL-DTO-09",
        "Category": "2. Common Policy DTO",
        "Policy Type": "All Types",
        "Field Under Test": "name",
        "Test Scenario / Edge Case": "Missing 'name' property entirely from request body",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Name is required for the policy.",
        "Known Defect / QA Reference": "FluentValidation Layer 1"
    })

    cases.append({
        "TC ID": "POL-DTO-10",
        "Category": "2. Common Policy DTO",
        "Policy Type": "All Types",
        "Field Under Test": "name",
        "Test Scenario / Edge Case": "'name' property is explicitly null in request payload",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": null, "lateCheckInGraceMinutes": 15}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Name is required for the policy.",
        "Known Defect / QA Reference": "FluentValidation Layer 1"
    })

    cases.append({
        "TC ID": "POL-DTO-11",
        "Category": "2. Common Policy DTO",
        "Policy Type": "All Types",
        "Field Under Test": "name",
        "Test Scenario / Edge Case": "'name' property is an empty JSON dictionary {}",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {}, "overtimeRule": "AfterShiftEnds", "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Name is required for the policy.",
        "Known Defect / QA Reference": "FluentValidation Layer 1"
    })

    cases.append({
        "TC ID": "POL-DTO-12",
        "Category": "2. Common Policy DTO",
        "Policy Type": "All Types",
        "Field Under Test": "name.en",
        "Test Scenario / Edge Case": "'name.en' localized string is empty ''",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": ""}, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Policy name cannot be empty.",
        "Known Defect / QA Reference": "String NullOrWhiteSpace Rule"
    })

    cases.append({
        "TC ID": "POL-DTO-13",
        "Category": "2. Common Policy DTO",
        "Policy Type": "All Types",
        "Field Under Test": "name.en",
        "Test Scenario / Edge Case": "'name.en' contains only spaces/whitespace '    '",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "    "}, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Policy name cannot be whitespace.",
        "Known Defect / QA Reference": "String NullOrWhiteSpace Rule"
    })

    cases.append({
        "TC ID": "POL-DTO-14",
        "Category": "2. Common Policy DTO",
        "Policy Type": "All Types",
        "Field Under Test": "name",
        "Test Scenario / Edge Case": "'name' passed as primitive string 'Standard' instead of dictionary",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": "Standard String Name", "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to Dictionary<string, string>.",
        "Known Defect / QA Reference": "System.Text.Json Type Safety"
    })

    cases.append({
        "TC ID": "POL-DTO-15",
        "Category": "2. Common Policy DTO",
        "Policy Type": "All Types",
        "Field Under Test": "name.en",
        "Test Scenario / Edge Case": "'name.en' exceeding max string length (>255 chars)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "' + ('A' * 300) + '"}, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P2",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Name length cannot exceed maximum allowed limit.",
        "Known Defect / QA Reference": "MaxLength Boundary Guard"
    })

    cases.append({
        "TC ID": "POL-DTO-16",
        "Category": "2. Common Policy DTO",
        "Policy Type": "All Types",
        "Field Under Test": "isActive",
        "Test Scenario / Edge Case": "'isActive' passed as string 'true' or 'yes' instead of boolean",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Active String"}, "isActive": "yes", "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P2",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to System.Boolean.",
        "Known Defect / QA Reference": "BSON Boolean Schema"
    })

    cases.append({
        "TC ID": "POL-DTO-17",
        "Category": "2. Common Policy DTO",
        "Policy Type": "All Types",
        "Field Under Test": "id",
        "Test Scenario / Edge Case": "Client supplies custom 'id' GUID in POST body",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"id": "11111111-2222-3333-4444-555555555555", "name": {"en": "Client ID Policy"}, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 200 / 201 (Client ID ignored)",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "200 / 201",
        "Actual Server Response / Notes": "Backend assigns server-generated UUIDv4; client value ignored.",
        "Known Defect / QA Reference": "Server-Side ID Generation"
    })

    cases.append({
        "TC ID": "POL-DTO-18",
        "Category": "2. Common Policy DTO",
        "Policy Type": "All Types",
        "Field Under Test": "tenantId / companyId",
        "Test Scenario / Edge Case": "Client supplies tenantId or companyId in JSON payload",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"tenantId": "00000000-0000-0000-0000-000000000000", "companyId": "00000000-0000-0000-0000-000000000000", "name": {"en": "Spoof"}, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 200 / 201 (Payload IDs ignored)",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "200 / 201",
        "Actual Server Response / Notes": "TenantId and CompanyId stamped from JWT and route context.",
        "Known Defect / QA Reference": "Security Scoping Guard"
    })

    # -------------------------------------------------------------------------
    # 3. Break Policy DTO Validations (14 TCs)
    # -------------------------------------------------------------------------
    cases.append({
        "TC ID": "POL-DTO-19",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "breaks",
        "Test Scenario / Edge Case": "Missing 'breaks' property entirely from BreakPolicyDto",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "No Breaks Policy"}}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Breaks list cannot be null or empty.",
        "Known Defect / QA Reference": "FluentValidation Layer 1"
    })

    cases.append({
        "TC ID": "POL-DTO-20",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "breaks",
        "Test Scenario / Edge Case": "'breaks' property explicitly set to null",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Null Breaks Policy"}, "breaks": null}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Breaks list cannot be null or empty.",
        "Known Defect / QA Reference": "FluentValidation Layer 1"
    })

    cases.append({
        "TC ID": "POL-DTO-21",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "breaks",
        "Test Scenario / Edge Case": "'breaks' is an empty array []",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Empty Array Policy"}, "breaks": []}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Breaks list cannot be empty.",
        "Known Defect / QA Reference": "FluentValidation Layer 1"
    })

    cases.append({
        "TC ID": "POL-DTO-22",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "breaks",
        "Test Scenario / Edge Case": "'breaks' passed as non-array object instead of array of BreakItem",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Object Breaks"}, "breaks": {"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to List<BreakItem>.",
        "Known Defect / QA Reference": "System.Text.Json Type Safety"
    })

    cases.append({
        "TC ID": "POL-DTO-23",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "BreakItem.name",
        "Test Scenario / Edge Case": "BreakItem missing 'name' property entirely",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Nameless Break Item"}, "breaks": [{"type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Break item name is required.",
        "Known Defect / QA Reference": "Child DTO Validation"
    })

    cases.append({
        "TC ID": "POL-DTO-24",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "BreakItem.name",
        "Test Scenario / Edge Case": "BreakItem 'name' is empty string '' or whitespace '   '",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Whitespace Item Name"}, "breaks": [{"name": "   ", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Break item name cannot be whitespace.",
        "Known Defect / QA Reference": "Child DTO Validation"
    })

    cases.append({
        "TC ID": "POL-DTO-25",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "BreakItem.type",
        "Test Scenario / Edge Case": "BreakItem 'type' is missing or null",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "No Type Break"}, "breaks": [{"name": "Lunch", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Break type is required.",
        "Known Defect / QA Reference": "Enum Validation"
    })

    cases.append({
        "TC ID": "POL-DTO-26",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "BreakItem.type",
        "Test Scenario / Edge Case": "BreakItem 'type' invalid string enum (e.g. 'VoluntaryBreak' or 'Coffee')",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Invalid Enum Break"}, "breaks": [{"name": "Lunch", "type": "VoluntaryBreak", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to BreakType.",
        "Known Defect / QA Reference": "Enum Constraint [Paid=1, Unpaid=2]"
    })

    cases.append({
        "TC ID": "POL-DTO-27",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "BreakItem.type",
        "Test Scenario / Edge Case": "BreakItem 'type' invalid integer enum (e.g. 99, -1)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Invalid Int Enum"}, "breaks": [{"name": "Lunch", "type": 99, "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to BreakType.",
        "Known Defect / QA Reference": "Enum Constraint"
    })

    cases.append({
        "TC ID": "POL-DTO-28",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "BreakItem.durationMinutes",
        "Test Scenario / Edge Case": "BreakItem 'durationMinutes' = 0",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Zero Duration Break"}, "breaks": [{"name": "Pause", "type": "Paid", "durationMinutes": 0}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Duration must be greater than 0.",
        "Known Defect / QA Reference": "Duration > 0 Boundary Rule"
    })

    cases.append({
        "TC ID": "POL-DTO-29",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "BreakItem.durationMinutes",
        "Test Scenario / Edge Case": "BreakItem 'durationMinutes' negative integer (-15, -60)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Negative Duration Break"}, "breaks": [{"name": "Pause", "type": "Unpaid", "durationMinutes": -15}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Duration must be greater than 0.",
        "Known Defect / QA Reference": "Duration > 0 Boundary Rule"
    })

    cases.append({
        "TC ID": "POL-DTO-30",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "BreakItem.durationMinutes",
        "Test Scenario / Edge Case": "BreakItem 'durationMinutes' decimal / float value (15.5)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Decimal Break"}, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 15.5}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P2",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to System.Int32.",
        "Known Defect / QA Reference": "Int32 Strict Serialization"
    })

    cases.append({
        "TC ID": "POL-DTO-31",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "BreakItem.durationMinutes",
        "Test Scenario / Edge Case": "BreakItem 'durationMinutes' exceeds 1440 minutes (e.g. 1441)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Exceeding Break"}, "breaks": [{"name": "Full Day", "type": "Unpaid", "durationMinutes": 1441}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P2",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Break duration cannot exceed 1440 minutes (24 hours).",
        "Known Defect / QA Reference": "24-Hour Shift Guard"
    })

    cases.append({
        "TC ID": "POL-DTO-32",
        "Category": "3. Break Policy DTO",
        "Policy Type": "Break Policy",
        "Field Under Test": "totalBreakDurationInMinutes",
        "Test Scenario / Edge Case": "Client supplies fake totalBreakDurationInMinutes in body (e.g. 999)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Fake Total Break"}, "totalBreakDurationInMinutes": 999, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 200 / 201 (Client total overridden)",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "200 / 201",
        "Actual Server Response / Notes": "TotalBreakDuration recalculated as 60; fake 999 ignored.",
        "Known Defect / QA Reference": "Business Calculation Invariant"
    })

    # -------------------------------------------------------------------------
    # 4. Grace Period Policy DTO Validations (14 TCs)
    # -------------------------------------------------------------------------
    cases.append({
        "TC ID": "POL-DTO-33",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "lateCheckInGraceMinutes",
        "Test Scenario / Edge Case": "lateCheckInGraceMinutes negative integer (-15)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Negative Late Grace"}, "lateCheckInGraceMinutes": -15}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Grace period minutes cannot be negative.",
        "Known Defect / QA Reference": "FluentValidation Rule >= 0"
    })

    cases.append({
        "TC ID": "POL-DTO-34",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "lateCheckInGraceMinutes",
        "Test Scenario / Edge Case": "lateCheckInGraceMinutes non-numeric string ('fifteen')",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "String Late Grace"}, "lateCheckInGraceMinutes": "fifteen"}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to System.Int32.",
        "Known Defect / QA Reference": "Int32 Strict Serialization"
    })

    cases.append({
        "TC ID": "POL-DTO-35",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "lateCheckInGraceMinutes",
        "Test Scenario / Edge Case": "lateCheckInGraceMinutes decimal / float value (15.5)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Decimal Late Grace"}, "lateCheckInGraceMinutes": 15.5}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P2",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to System.Int32.",
        "Known Defect / QA Reference": "Int32 Strict Serialization"
    })

    cases.append({
        "TC ID": "POL-DTO-36",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "earlyCheckOutGraceMinutes",
        "Test Scenario / Edge Case": "earlyCheckOutGraceMinutes negative integer (-10)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Negative Early Grace"}, "earlyCheckOutGraceMinutes": -10}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Grace period minutes cannot be negative.",
        "Known Defect / QA Reference": "FluentValidation Rule >= 0"
    })

    cases.append({
        "TC ID": "POL-DTO-37",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "deviationThreshold",
        "Test Scenario / Edge Case": "deviationThreshold = 0 occurrences",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Zero Threshold Grace"}, "deviationThreshold": 0}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Deviation threshold must be greater than 0.",
        "Known Defect / QA Reference": "Threshold >= 1 Boundary"
    })

    cases.append({
        "TC ID": "POL-DTO-38",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "deviationThreshold",
        "Test Scenario / Edge Case": "deviationThreshold negative integer (-1, -3)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Negative Threshold Grace"}, "deviationThreshold": -1}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Deviation threshold must be greater than 0.",
        "Known Defect / QA Reference": "Threshold >= 1 Boundary"
    })

    cases.append({
        "TC ID": "POL-DTO-39",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "deviationPeriod",
        "Test Scenario / Edge Case": "deviationPeriod invalid string enum ('Quarterly' or 'Yearly')",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Invalid Period Grace"}, "deviationPeriod": "Quarterly"}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to GracePeriodDeviationPeriod.",
        "Known Defect / QA Reference": "Enum [Weekly=1, BiWeekly=2, Monthly=3]"
    })

    cases.append({
        "TC ID": "POL-DTO-40",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "deviationPeriod",
        "Test Scenario / Edge Case": "deviationPeriod invalid integer enum (99, -1)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Invalid Period Int"}, "deviationPeriod": 99}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to GracePeriodDeviationPeriod.",
        "Known Defect / QA Reference": "Enum Constraint"
    })

    cases.append({
        "TC ID": "POL-DTO-41",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "deductLeaveFrom",
        "Test Scenario / Edge Case": "deductLeaveFrom invalid string enum ('MaternityLeave' or 'CompOff')",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Invalid Leave Enum"}, "deductLeaveFrom": "MaternityLeave"}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to GracePeriodLeaveDeductionType.",
        "Known Defect / QA Reference": "Enum [Annual=1, Casual=2, Sick=3]"
    })

    cases.append({
        "TC ID": "POL-DTO-42",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "deductLeaveFrom",
        "Test Scenario / Edge Case": "deductLeaveFrom invalid integer enum (99, -1)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Invalid Leave Int"}, "deductLeaveFrom": 99}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to GracePeriodLeaveDeductionType.",
        "Known Defect / QA Reference": "Enum Constraint"
    })

    cases.append({
        "TC ID": "POL-DTO-43",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "deductionDays",
        "Test Scenario / Edge Case": "deductionDays negative double (-0.5, -1.0)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Negative Deduction"}, "deductionDays": -0.5}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Deduction days cannot be negative.",
        "Known Defect / QA Reference": "FluentValidation Rule >= 0"
    })

    cases.append({
        "TC ID": "POL-DTO-44",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "deductionDays",
        "Test Scenario / Edge Case": "deductionDays non-numeric string ('half-day')",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "String Deduction"}, "deductionDays": "half-day"}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to System.Double.",
        "Known Defect / QA Reference": "Double Strict Serialization"
    })

    cases.append({
        "TC ID": "POL-DTO-45",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "deductionDays",
        "Test Scenario / Edge Case": "Valid fractional deductionDays (0.25, 0.5, 1.0)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Quarter Day Grace"}, "deductionDays": 0.25, "lateCheckInGraceMinutes": 15}',
        "Expected HTTP & Code": "HTTP 200 / 201 Created",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "200 / 201",
        "Actual Server Response / Notes": "DeductionDays stored as 0.25 double precision.",
        "Known Defect / QA Reference": "BVA Valid Fractional"
    })

    cases.append({
        "TC ID": "POL-DTO-46",
        "Category": "4. Grace Period DTO",
        "Policy Type": "Grace Period Policy",
        "Field Under Test": "lateCheckInGraceMinutes & earlyCheckOutGraceMinutes",
        "Test Scenario / Edge Case": "Zero tolerance valid boundary: late = 0, early = 0",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Zero Grace Policy"}, "lateCheckInGraceMinutes": 0, "earlyCheckOutGraceMinutes": 0}',
        "Expected HTTP & Code": "HTTP 200 / 201 Created",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "200 / 201",
        "Actual Server Response / Notes": "0 minutes accepted as valid minimum boundary.",
        "Known Defect / QA Reference": "BVA Valid Minimum Boundary"
    })

    # -------------------------------------------------------------------------
    # 5. Overtime Policy DTO Validations (14 TCs)
    # -------------------------------------------------------------------------
    cases.append({
        "TC ID": "POL-DTO-47",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "overtimeRule",
        "Test Scenario / Edge Case": "overtimeRule invalid string enum ('WeekendOnly' or 'CustomRule')",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "Invalid Rule"}, "overtimeRule": "WeekendOnly", "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to OvertimeRule.",
        "Known Defect / QA Reference": "Enum [AllExtraTime=1, BeforeShift=2, AfterShift=3]"
    })

    cases.append({
        "TC ID": "POL-DTO-48",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "overtimeRule",
        "Test Scenario / Edge Case": "overtimeRule invalid integer enum (99, -1)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "Invalid Rule Int"}, "overtimeRule": 99, "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to OvertimeRule.",
        "Known Defect / QA Reference": "Enum Constraint"
    })

    cases.append({
        "TC ID": "POL-DTO-49",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "hasBufferBeforeOvertime",
        "Test Scenario / Edge Case": "hasBufferBeforeOvertime non-boolean string ('enabled' or '1')",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "String Buffer Flag"}, "hasBufferBeforeOvertime": "enabled", "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P2",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to System.Boolean.",
        "Known Defect / QA Reference": "Boolean Deserialization"
    })

    cases.append({
        "TC ID": "POL-DTO-50",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "bufferMinutes",
        "Test Scenario / Edge Case": "bufferMinutes negative integer (-30)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "Negative Buffer"}, "bufferMinutes": -30, "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Buffer minutes cannot be negative.",
        "Known Defect / QA Reference": "FluentValidation Rule >= 0"
    })

    cases.append({
        "TC ID": "POL-DTO-51",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "bufferMinutes",
        "Test Scenario / Edge Case": "bufferMinutes non-numeric string ('thirty')",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "String Buffer"}, "bufferMinutes": "thirty", "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P2",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to System.Int32.",
        "Known Defect / QA Reference": "Int32 Strict Serialization"
    })

    cases.append({
        "TC ID": "POL-DTO-52",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "rates",
        "Test Scenario / Edge Case": "'rates' property explicitly set to null",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "Null Rates Overtime"}, "overtimeRule": "AfterShiftEnds", "rates": null}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Rates list cannot be null or empty.",
        "Known Defect / QA Reference": "FluentValidation Layer 1"
    })

    cases.append({
        "TC ID": "POL-DTO-53",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "rates",
        "Test Scenario / Edge Case": "'rates' is an empty array []",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "Empty Rates Overtime"}, "overtimeRule": "AfterShiftEnds", "rates": []}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Rates list cannot be empty.",
        "Known Defect / QA Reference": "FluentValidation Layer 1"
    })

    cases.append({
        "TC ID": "POL-DTO-54",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "rates",
        "Test Scenario / Edge Case": "'rates' passed as non-array object instead of array of OvertimeRate",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "Object Rates"}, "overtimeRule": "AfterShiftEnds", "rates": {"dayRate": "WorkingDay", "rateFormula": 1.5}}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to List<OvertimeRate>.",
        "Known Defect / QA Reference": "System.Text.Json Type Safety"
    })

    cases.append({
        "TC ID": "POL-DTO-55",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "OvertimeRate.dayRate",
        "Test Scenario / Edge Case": "OvertimeRate 'dayRate' invalid string enum ('RestDay' or 'Sunday')",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "Invalid DayRate"}, "rates": [{"dayRate": "RestDay", "rateFormula": 1.5}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to OvertimeDayRate.",
        "Known Defect / QA Reference": "Enum [WorkingDay=1, DayOff=2, Holiday=3]"
    })

    cases.append({
        "TC ID": "POL-DTO-56",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "OvertimeRate.dayRate",
        "Test Scenario / Edge Case": "OvertimeRate 'dayRate' invalid integer enum (99, -1)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "Invalid DayRate Int"}, "rates": [{"dayRate": 99, "rateFormula": 1.5}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to OvertimeDayRate.",
        "Known Defect / QA Reference": "Enum Constraint"
    })

    cases.append({
        "TC ID": "POL-DTO-57",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "OvertimeRate.rateFormula",
        "Test Scenario / Edge Case": "OvertimeRate 'rateFormula' = 0.0x multiplier",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "Zero Multiplier"}, "rates": [{"dayRate": "WorkingDay", "rateFormula": 0.0}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Rate formula multiplier must be greater than 0.",
        "Known Defect / QA Reference": "Multiplier > 0 Rule"
    })

    cases.append({
        "TC ID": "POL-DTO-58",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "OvertimeRate.rateFormula",
        "Test Scenario / Edge Case": "OvertimeRate 'rateFormula' negative double (-1.5)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "Negative Multiplier"}, "rates": [{"dayRate": "WorkingDay", "rateFormula": -1.5}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Rate formula multiplier must be greater than 0.",
        "Known Defect / QA Reference": "Payroll Math Violation"
    })

    cases.append({
        "TC ID": "POL-DTO-59",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "OvertimeRate.rateFormula",
        "Test Scenario / Edge Case": "OvertimeRate 'rateFormula' non-numeric string ('double')",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "String Formula"}, "rates": [{"dayRate": "WorkingDay", "rateFormula": "double"}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P2",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "The JSON value could not be converted to System.Double.",
        "Known Defect / QA Reference": "Double Strict Serialization"
    })

    cases.append({
        "TC ID": "POL-DTO-60",
        "Category": "5. Overtime Policy DTO",
        "Policy Type": "Overtime Policy",
        "Field Under Test": "rates",
        "Test Scenario / Edge Case": "'rates' array contains duplicate DayRate entries (e.g. two WorkingDay rates)",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
        "Sample Request Payload (JSON)": '{"name": {"en": "Duplicate Rate"}, "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}, {"dayRate": "WorkingDay", "rateFormula": 2.0}]}',
        "Expected HTTP & Code": "HTTP 400 Bad Request",
        "Pri": "P1",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "400 Bad Request",
        "Actual Server Response / Notes": "Duplicate day rate entries are not allowed.",
        "Known Defect / QA Reference": "Unique DayRate Invariant"
    })

    return cases

if __name__ == "__main__":
    dto_cases = get_dto_test_cases()
print(f"Total DTO test cases defined: {len(dto_cases)}")

# Open master workbook and write sheet
wb_path = "AttendanceTestCases_Master_Consolidated.xlsx"
wb = openpyxl.load_workbook(wb_path)

sheet_name = "Policies - Manual DTO Validations"
if sheet_name in wb.sheetnames:
    print(f"Replacing existing sheet: {sheet_name}...")
    del wb[sheet_name]

ws = wb.create_sheet(title=sheet_name)
ws.views.sheetView[0].showGridLines = True
ws.row_dimensions[1].height = 30

# Header styling matching CDWT DTO sheet
hdr_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
hdr_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
hdr_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

thin_side = Side(border_style="thin", color="CBD5E1")
cell_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

data_font = Font(name="Calibri", size=9, color="1E293B")
data_font_bold = Font(name="Calibri", size=9, bold=True, color="1E293B")

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

# Priority fills
p0_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
p0_font = Font(name="Calibri", size=9, bold=True, color="991B1B")
p1_fill = PatternFill(start_color="FFEDD5", end_color="FFEDD5", fill_type="solid")
p1_font = Font(name="Calibri", size=9, bold=True, color="C2410C")
p2_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
p2_font = Font(name="Calibri", size=9, bold=True, color="92400E")

pass_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
pass_font = Font(name="Calibri", size=9, bold=True, color="166534")

# Write headers
for c_idx, h in enumerate(DTO_HEADERS, 1):
    c = ws.cell(1, c_idx, h)
    c.fill = hdr_fill
    c.font = hdr_font
    c.alignment = hdr_align
    c.border = cell_border

# Write rows
for r_idx, tc in enumerate(dto_cases, 2):
    ws.row_dimensions[r_idx].height = 24
    fill = zebra_fill if (r_idx % 2 == 0) else white_fill
    
    for c_idx, h in enumerate(DTO_HEADERS, 1):
        val = tc.get(h, "")
        cell = ws.cell(r_idx, c_idx, val)
        cell.fill = fill
        cell.font = data_font
        cell.border = cell_border
        
        if c_idx in [1, 3, 6, 9, 10, 11, 12, 13]:
            cell.alignment = align_center
            if c_idx == 1:
                cell.font = data_font_bold
        else:
            cell.alignment = align_left
            
        if h == "Pri":
            p = str(val).strip().upper()
            if p == "P0":
                cell.fill = p0_fill
                cell.font = p0_font
            elif p == "P1":
                cell.fill = p1_fill
                cell.font = p1_font
            elif p == "P2":
                cell.fill = p2_fill
                cell.font = p2_font
                
        if h in ["Automation Status", "Manual Status"] and str(val).strip().lower() in ["pass", "ready"]:
            cell.fill = pass_fill
            cell.font = pass_font

# Column widths
DTO_COL_WIDTHS = {
    1: 16, 2: 24, 3: 20, 4: 25, 5: 45, 6: 12, 7: 42,
    8: 48, 9: 25, 10: 10, 11: 18, 12: 15, 13: 18, 14: 40, 15: 28
}
for c_idx, w in DTO_COL_WIDTHS.items():
    ws.column_dimensions[get_column_letter(c_idx)].width = w

# Autofilter & freeze
ws.auto_filter.ref = f"A1:{get_column_letter(len(DTO_HEADERS))}{len(dto_cases)+1}"
ws.freeze_panes = "A2"

# Update INDEX sheet
if "INDEX" in wb.sheetnames:
    idx_ws = wb["INDEX"]
    # Check if 'Policies - Manual DTO Validations' already exists in INDEX
    found = False
    for r in range(5, idx_ws.max_row + 1):
        val = idx_ws.cell(r, 2).value
        if val and "policies - manual dto validations" in str(val).lower():
            found = True
            idx_ws.cell(r, 3, len(dto_cases))
            idx_ws.cell(r, 4, sum(1 for t in dto_cases if t["Pri"] == "P0"))
            idx_ws.cell(r, 5, sum(1 for t in dto_cases if t["Pri"] == "P1"))
            idx_ws.cell(r, 6, sum(1 for t in dto_cases if t["Pri"] == "P2"))
            break
            
    if not found:
        # Find where to insert (before TOTAL row)
        total_row = None
        for r in range(5, idx_ws.max_row + 1):
            val = str(idx_ws.cell(r, 1).value or "").strip().upper()
            if "TOTAL" in val:
                total_row = r
                break
                
        if total_row:
            idx_ws.insert_rows(total_row)
            item_num = total_row - 4 # e.g. 18
            idx_ws.cell(total_row, 1, item_num)
            idx_ws.cell(total_row, 2, "Policies - Manual DTO Validations")
            idx_ws.cell(total_row, 3, len(dto_cases))
            idx_ws.cell(total_row, 4, sum(1 for t in dto_cases if t["Pri"] == "P0"))
            idx_ws.cell(total_row, 5, sum(1 for t in dto_cases if t["Pri"] == "P1"))
            idx_ws.cell(total_row, 6, sum(1 for t in dto_cases if t["Pri"] == "P2"))
            
            # Recalculate totals on total_row + 1
            new_tot_row = total_row + 1
            tot_tcs = sum(idx_ws.cell(r, 3).value or 0 for r in range(5, new_tot_row))
            tot_p0 = sum(idx_ws.cell(r, 4).value or 0 for r in range(5, new_tot_row))
            tot_p1 = sum(idx_ws.cell(r, 5).value or 0 for r in range(5, new_tot_row))
            tot_p2 = sum(idx_ws.cell(r, 6).value or 0 for r in range(5, new_tot_row))
            idx_ws.cell(new_tot_row, 3, tot_tcs)
            idx_ws.cell(new_tot_row, 4, tot_p0)
            idx_ws.cell(new_tot_row, 5, tot_p1)
            idx_ws.cell(new_tot_row, 6, tot_p2)
            idx_ws.cell(new_tot_row, 2, f"All {item_num} Modules Combined")

wb.save(wb_path)
print(f"Updated {wb_path} with new sheet 'Policies - Manual DTO Validations' and updated INDEX successfully!")

