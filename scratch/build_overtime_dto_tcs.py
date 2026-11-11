import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

def get_overtime_dto_cases():
    cases = []
    
    dto_specs = [
        ("POL-DTO-64", "isActive", "isActive string ('true')", '{"name": {"en": "DTO-01"}, "isActive": "true", "overtimeRule": "AfterShiftEnds", "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}', "HTTP 400 Bad Request", "P1", "The JSON value could not be converted to System.Boolean."),
        ("POL-DTO-65", "isActive", "isActive null", '{"name": {"en": "DTO-02"}, "isActive": null, "overtimeRule": "AfterShiftEnds", "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}', "HTTP 400 Bad Request", "P1", "isActive is required boolean."),
        ("POL-DTO-66", "hasBufferBeforeOvertime", "hasBufferBeforeOvertime string ('false')", '{"name": {"en": "DTO-03"}, "hasBufferBeforeOvertime": "false", "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}', "HTTP 400 Bad Request", "P1", "The JSON value could not be converted to System.Boolean."),
        ("POL-DTO-67", "hasBufferBeforeOvertime", "hasBufferBeforeOvertime null", '{"name": {"en": "DTO-04"}, "hasBufferBeforeOvertime": null, "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}', "HTTP 400 Bad Request", "P1", "hasBufferBeforeOvertime is required."),
        ("POL-DTO-68", "bufferMinutes", "bufferMinutes string ('15')", '{"name": {"en": "DTO-05"}, "bufferMinutes": "15", "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}', "HTTP 400 Bad Request", "P2", "The JSON value could not be converted to System.Int32."),
        ("POL-DTO-69", "bufferMinutes", "bufferMinutes decimal (1.5)", '{"name": {"en": "Decimal Buffer Test"}, "bufferMinutes": 1.5, "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}', "HTTP 400 Bad Request", "P1", "The JSON value could not be converted to System.Int32 (integer expected)."),
        ("POL-DTO-70", "bufferMinutes", "bufferMinutes null", '{"name": {"en": "DTO-07"}, "bufferMinutes": null, "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}', "HTTP 400 Bad Request", "P1", "bufferMinutes is required int32."),
        ("POL-DTO-71", "rates", "rates missing property", '{"name": {"en": "DTO-08"}, "overtimeRule": "AfterShiftEnds", "hasBufferBeforeOvertime": False, "bufferMinutes": 0}', "HTTP 400 Bad Request", "P1", "rates property is mandatory."),
        ("POL-DTO-72", "rates[0]", "rates[0] null", '{"name": {"en": "Null Rate Item Test"}, "rates": [null]}', "HTTP 400 Bad Request", "P1", "Rates array element cannot be null."),
        ("POL-DTO-73", "rates[0].rateFormula", "rates[0].rateFormula null", '{"name": {"en": "DTO-10"}, "rates": [{"dayRate": "WorkingDay", "rateFormula": null}]}', "HTTP 400 Bad Request", "P1", "rateFormula is required double."),
        ("POL-DTO-74", "name", "name string 'Overtime' instead of object", '{"name": "Overtime", "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]}', "HTTP 400 Bad Request", "P1", "The JSON value could not be converted to MultilingualString object."),
        ("POL-DTO-75", "rates", "rates object {} instead of array", '{"name": {"en": "DTO-12"}, "rates": {}}', "HTTP 400 Bad Request", "P1", "The JSON value could not be converted to System.Collections.Generic.List`1[OvertimeRate].")
    ]
    
    for tc_id, field, scenario, payload, exp_code, pri, err_msg in dto_specs:
        cases.append({
            "TC ID": tc_id,
            "Category": "5. Overtime Policy DTO",
            "Policy Type": "Overtime Policy",
            "Field Under Test": field,
            "Test Scenario / Edge Case": scenario,
            "HTTP Method": "POST",
            "Endpoint Route": "/api/companies/{companyId}/attpolicies/overtime",
            "Sample Request Payload (JSON)": payload,
            "Expected HTTP & Code": exp_code,
            "Pri": pri,
            "Automation Status": "Manual Only",
            "Manual Status": "Pass",
            "Actual HTTP Code": "400 Bad Request",
            "Actual Server Response / Notes": err_msg,
            "Known Defect / QA Reference": "DTO Serialization / Strict Validation"
        })
        
    return cases

print("Overtime DTO test cases defined successfully!")

