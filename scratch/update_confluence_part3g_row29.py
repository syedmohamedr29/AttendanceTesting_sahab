import json
import requests
import html

CONFIG_FILE = 'scratch/confluence_config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']
page_id = cfg['page_id']

# 1. Fetch current page details
r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version,space", auth=auth)
if r.status_code != 200:
    raise RuntimeError(f"Failed to fetch page {page_id}: {r.text}")

page_data = r.json()
current_version = page_data['version']['number']
title = page_data['title']
space_key = page_data['space']['key']

print(f"Current Page: '{title}', Version: {current_version}")

# Rows 1 to 28 (Existing) + Row 29 (Part 3G Work Template Module Live Compass Verification)
rows_data = [
    # Rows 1 - 4: Core User Scenarios & Multi-Tenancy Architecture
    {
        "sno": "1",
        "defect_id": "DEFECT-20261026-01 (USER-01 / USER-128)",
        "module": "Part 3 User Scenarios / Company Checklist",
        "type": "API / Integration",
        "description": "<p><strong>Company Checklist Sync Failure:</strong> Newly created company is not marked in Company Checklist upon Attendance template creation (<code>WorkSchedulesCreated</code> remains false).</p>",
        "screenshot": "evidence_02_companiesmaster_checklist_false.png",
        "remarks": "<p><strong>Endpoint:</strong> <code>POST /worktemplates/fixed</code></p><p><strong>Status:</strong> Not marked in <code>CompaniesMaster</code>.</p><p><strong>Note:</strong> Need to be helped with Ravi sir need to fix the issue.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Checklist in <code>CompaniesMaster</code> remains false. Cross-service event synchronization between CompanySvc and AttendanceSvc missing.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "2",
        "defect_id": "DEFECT-20261028-05 (USER-02 / USER-129 / DEFECT-20261026-02)",
        "module": "Part 3 (28-Oct) / Multi-Tenancy Architecture",
        "type": "API / DB",
        "description": "<p><strong>Empty TenantName Object in MongoDB:</strong> <code>TenantName</code> persists as an empty BSON object <code>{}</code> in MongoDB across all Work Templates collections.</p>",
        "screenshot": "evidence_06_tenantname_empty_object_compass.png",
        "remarks": "<p><strong>Database:</strong> <code>Sahab.ERP.Attendance.WorkTemplates</code></p><p><code>\"TenantName\": { }</code> in MongoDB Compass.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Inspection of MongoDB Compass confirms <code>TenantName</code> persists as <code>Object (empty) {}</code> across all seeded templates.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "3",
        "defect_id": "DEFECT-20261026-03 (USER-03 / USER-130)",
        "module": "Part 3 User Scenarios / Audit Trail & Identity",
        "type": "API / DB",
        "description": "<p><strong>Plain Email in CreatedBy:</strong> Audit field <code>CreatedBy</code> persists as a plain email string instead of composite user identity object <code>{ id, email, name }</code>.</p>",
        "screenshot": "evidence_05_createdby_plain_email_highlighted.png",
        "remarks": "<p><strong>Database:</strong> <code>Sahab.ERP.Attendance.WorkTemplates</code></p><p><code>\"CreatedBy\": \"admin@zoolwork.com\"</code> (string).</p>",
        "priority": "P2",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Plain string email persists instead of composite user identity document, breaking ERP audit identity invariants.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "4",
        "defect_id": "DEFECT-20261028-06 (USER-04 / USER-122 / USER-131 / DEFECT-20261026-04)",
        "module": "Part 3 (28-Oct) / API Contracts & DTOs",
        "type": "API",
        "description": "<p><strong>DTO Pollution & Client Spoofing:</strong> Server-side internal field <code>tenantName</code> is exposed in OpenAPI request body DTOs and accepts client spoofing with <code>200 OK</code> across 26 POST/PATCH routes.</p>",
        "screenshot": "evidence_07_swagger_tenantname_still_present.png",
        "remarks": "<p><strong>Endpoint:</strong> <code>POST /worktemplates/*</code> &amp; <code>PATCH</code></p><p>Exposes <code>tenantName</code> in OpenAPI schema.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Swagger UI schemas expose <code>tenantName</code> in request DTOs; client-supplied spoofed names are accepted with HTTP 200 OK.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    # Rows 5 - 9: WT - Company Default Failed Issues
    {
        "sno": "5",
        "defect_id": "DEFECT-20261104-01 (DOC-A-04 / ROOT-E-05)",
        "module": "WT - Company Default / Multi-Tenancy Scoping",
        "type": "API",
        "description": "<p><strong>Multi-Tenancy Scoping Leak:</strong> <code>__tenant</code> header ignored; cross-tenant company default work template access allowed with HTTP 200 OK.</p>",
        "screenshot": "evidence_39_companyname_empty_object_compass.jpg",
        "remarks": "<p><strong>Request:</strong> <code>GET /api/companies/{companyId}/worktemplates</code></p><p><strong>Header:</strong> <code>__tenant: foreign-tenant-id</code></p><p><strong>Response:</strong> <code>HTTP 200 OK</code> (Templates leaked)</p>",
        "priority": "P0",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. ABP multi-tenancy filter is bypassed on company template routes; cross-tenant data leaked with HTTP 200 OK instead of 403 Forbidden.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "6",
        "defect_id": "DEFECT-20261028-04 (DOC-A-05 / ROOT-E-06)",
        "module": "Part 3 (28-Oct) / WT - Company Scoping",
        "type": "API",
        "description": "<p><strong>Cross-Company Scoping Fallback:</strong> Querying another company's template returns <code>HTTP 200 []</code> instead of throwing <code>400 Cit.Attendance:9001</code> or 404.</p>",
        "screenshot": "evidence_39_companyname_empty_object_compass.jpg",
        "remarks": "<p><strong>Request:</strong> <code>GET /api/companies/{CompanyB}/worktemplates?id={CompanyA_TemplateId}</code></p><p><strong>Response:</strong> <code>HTTP 200 []</code> (Empty array fallback)</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Foreign company route silently falls back to <code>HTTP 200 []</code>, masking unauthorized cross-company scoping probing.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "7",
        "defect_id": "DEFECT-20261105-01",
        "module": "WT - Company Default / Master Data Resolution",
        "type": "API / DB",
        "description": "<p><strong>CompanyName Persists as Empty Object:</strong> <code>CompanyName</code> persists as <code>Object (empty) {}</code> in MongoDB upon CDWT creation due to missing metadata resolution from <code>CompanySvc</code>.</p>",
        "screenshot": "evidence_39_companyname_empty_object_compass.jpg",
        "remarks": "<p><strong>Trigger:</strong> <code>POST /api/companies/{companyId}/worktemplates/fixed</code></p><p><strong>MongoDB Compass:</strong> <code>\"CompanyName\": { }</code></p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. MongoDB Compass inspection confirms <code>CompanyName</code> field remains <code>{}</code> empty document across all seeded CDWTs.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "8",
        "defect_id": "DEFECT-20261110-01",
        "module": "WT - Company Default / Auto-Provisioning & Localization",
        "type": "API / DB",
        "description": "<p><strong>Missing Arabic Name in Seeded Location Template:</strong> Auto-seeded Location Default Work Template created with blank Arabic name (<code>WorkTemplateName.ar: \"\"</code>) in MongoDB.</p>",
        "screenshot": "evidence_51_location_default_worktemplate_ar_name_empty_compass.png",
        "remarks": "<p><strong>Trigger:</strong> CDWT auto-provisioning cascade</p><p><strong>MongoDB Compass:</strong> <code>WorkTemplateName: { en: \"Location Default\", ar: \"\" }</code></p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Arabic name remains empty string in auto-provisioned location work templates, causing blank template headers in Arabic UI.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "9",
        "defect_id": "DEFECT-20261103-16",
        "module": "WT - Company Default / Location Sync Architecture",
        "type": "Architecture / Sync",
        "description": "<p><strong>Architecture Integration Gap:</strong> Newly created location ('Delhi') NOT auto-assigned Company Default Work Template upon creation in Company Service.</p>",
        "screenshot": "evidence_37_cdwt_compass_only_4_templates_missing_delhi.jpg",
        "remarks": "<p><strong>Trigger:</strong> Add new location in CompanySvc after CDWT creation</p><p><strong>MongoDB:</strong> 0 templates or plans created for Delhi.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. No distributed domain event listener exists between <code>CompanySvc</code> and <code>AttendanceSvc</code>; new locations remain unprovisioned.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    # Rows 10 - 14: Part 3B Holiday Calendar Failed Issues
    {
        "sno": "10",
        "defect_id": "DEFECT-20261103-08 (HC-DTO-145)",
        "module": "Part 3B / Holiday Calendar DTO Validations",
        "type": "API / DB",
        "description": "<p><strong>Invalid calendarType Enum Coerced to Default:</strong> Sending invalid <code>\"calendarType\": 999</code> is silently accepted, coerced to <code>1 (CompanyDefault)</code> in MongoDB, and triggers <code>Cit.Attendance:1713</code> conflict instead of returning HTTP 400 DTO enum validation.</p>",
        "screenshot": "evidence_26_holiday_calendar_invalid_calendartype_999_stored_as_default_1.png",
        "remarks": "<p><strong>Payload:</strong> <code>{\"calendarType\": 999}</code></p><p><strong>MongoDB Compass:</strong> Stored with <code>CalendarType: 1</code>.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. DTO model binder lacks Enum range validation; silently mutates invalid enum to 1 and corrupts database invariants.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "11",
        "defect_id": "DEFECT-20261103-15 (HC-PUB-01 / HC-PUB-18)",
        "module": "Part 3B / Holiday Calendar Publishing Lifecycle",
        "type": "API / Business Guard",
        "description": "<p><strong>Empty Holiday Calendar Published (0 Holidays):</strong> <code>PublishHolidayCalendarCommandHandler</code> lacks defense-in-depth guard; calling <code>POST /holidaylist/publish/2026</code> on a calendar with 0 holidays succeeds with <code>HTTP 200 OK</code> and marks <code>IsPublished: true</code>.</p>",
        "screenshot": "evidence_34_holiday_publish_empty_calendar_compass_proof.jpg",
        "remarks": "<p><strong>Endpoint:</strong> <code>POST /api/companies/{companyId}/holidaylist/publish/2026</code></p><p><strong>Impact:</strong> Empty calendar pushed live to locations.</p>",
        "priority": "P0",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Calling publish endpoint on 0-holiday calendar returns 200 OK without asserting that at least one holiday exists.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "12",
        "defect_id": "DEFECT-20261103-03",
        "module": "Part 3B / Holiday Calendar State Management",
        "type": "API / DB",
        "description": "<p><strong>isActive: false Overwritten:</strong> Submitting <code>\"isActive\": false</code> in request payload is completely ignored by the backend handler and persisted as <code>IsActive: true</code> in MongoDB.</p>",
        "screenshot": "evidence_20_holiday_calendar_isactive_false_ignored_stored_true.jpg",
        "remarks": "<p><strong>Endpoint:</strong> <code>POST /holidaylist</code> with <code>\"isActive\": false</code></p><p><strong>MongoDB:</strong> Persisted as <code>IsActive: true</code>.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Command handler unconditionally sets <code>IsActive = true</code>, ignoring client payload configuration.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "13",
        "defect_id": "HC-DTO-01 / HC-DTO-74 / HC-DTO-127 / HC-DTO-129",
        "module": "Part 3B / API Routing & Error Standards",
        "type": "API / Routing",
        "description": "<p><strong>Route Constraint Mismatch (HTTP 404 Instead of HTTP 400):</strong> ASP.NET Core route constraints (<code>{companyId:guid}</code>, <code>{year:int}</code>) reject malformed route parameters before reaching the controller, returning <code>HTTP 404 Not Found</code> instead of RFC 9110 <code>HTTP 400 Bad Request</code>.</p>",
        "screenshot": "evidence_26_holiday_calendar_invalid_calendartype_999_stored_as_default_1.png",
        "remarks": "<p><strong>Affected Endpoints:</strong> <code>POST /holidaylist</code>, <code>PATCH /{id}/{year}</code></p><p>Malformed GUID / non-numeric year returns 404.</p>",
        "priority": "P2",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Framework route constraints short-circuit request pipeline without structured 400 ProblemDetails.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "14",
        "defect_id": "HC-PUB-16 (DEFECT-20261026-01)",
        "module": "Part 3B / Cross-Service Checklist Sync",
        "type": "API / Integration",
        "description": "<p><strong>Publish Does Not Synchronize Checklist:</strong> Publishing a holiday calendar does not update <code>CompanyChecklist.HolidayCalendarPublished</code> in <code>SP.CompanySvc</code>; remains <code>false</code>.</p>",
        "screenshot": "evidence_02_companiesmaster_checklist_false.png",
        "remarks": "<p><strong>Trigger:</strong> <code>POST /holidaylist/publish/2026</code></p><p><strong>Impact:</strong> Checklist wizard remains blocked in Company Service.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Event integration between AttendanceSvc and CompanySvc is missing for publishing events.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    # Rows 15 - 16: Part 3C Security & Swagger Architecture Issues
    {
        "sno": "15",
        "defect_id": "DEFECT-20261029-01",
        "module": "Part 3C / Security & Authentication Architecture",
        "type": "API / Security",
        "description": "<p><strong>Critical JWT Validation Bypass:</strong> <code>SP.AttendanceSvc</code> accepts expired JWT tokens (tested 10 days past expiration) and forged / tampered signatures (<code>AAAA...</code>), returning <code>HTTP 200 OK</code> and live company data instead of <code>HTTP 401 Unauthorized</code>.</p>",
        "screenshot": "evidence_16_attendance_swagger_missing_oauth2.png",
        "remarks": "<p><strong>Vulnerability:</strong> <code>ValidateLifetime = false</code> &amp; <code>ValidateIssuerSigningKey = false</code> in Kestrel Auth pipeline.</p><p><strong>Note:</strong> Need to be helped with Ravi sir need to fix the issue.</p>",
        "priority": "P0",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Expired and tampered signature tokens are accepted with HTTP 200 OK. Critical security blocker.</p><p><strong>Note:</strong> Need to be helped with Ravi sir need to fix the issue.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "16",
        "defect_id": "DEFECT-20261029-02",
        "module": "Part 3C / Swagger & OpenAPI Architecture",
        "type": "Swagger / DX",
        "description": "<p><strong>Swagger Missing OAuth2 (<code>authorizationCode</code>) Flow:</strong> Unlike <code>SP.CompanySvc</code> which implements <code>oauth2 (authorizationCode)</code> with <code>WebGateway_Swagger</code> client, Attendance Swagger only offers raw <code>Bearer (http, Bearer)</code>, blocking seamless SSO login.</p>",
        "screenshot": "evidence_16_attendance_swagger_missing_oauth2.png",
        "remarks": "<p><strong>Endpoint:</strong> <code>/swagger/index.html</code></p><p>Missing OpenIddict OAuth2 authorizationCode configuration.</p><p><strong>Note:</strong> Need to be helped with Ravi sir need to fix the issue.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Attendance Swagger UI still only provides manual Bearer text input, breaking unified SSO testing flow.</p><p><strong>Note:</strong> Need to be helped with Ravi sir need to fix the issue.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    # Rows 17 - 26: Part 3D Work Template DTO Validations, Invariants & Architecture Issues
    {
        "sno": "17",
        "defect_id": "DEFECT-20261102-10",
        "module": "Part 3D / Work Template Temporal Invariants",
        "type": "API / Temporal Invariant",
        "description": "<p><strong>Inverted Shift Timings Accepted (endTime &lt; startTime):</strong> Single-day fixed shift with <code>startTime: \"10:00:00\"</code> and <code>endTime: \"09:00:00\"</code> accepted with <code>HTTP 200 OK</code> without requiring an overnight shift flag, producing negative shift durations in MongoDB.</p>",
        "screenshot": "evidence_09_split_overlap_500_validation_exception.png",
        "remarks": "<p><strong>Payload:</strong> <code>{\"startTime\": \"10:00:00\", \"endTime\": \"09:00:00\", \"isOvernight\": false}</code></p><p><strong>Impact:</strong> Negative work duration crashes daily attendance calculation.</p>",
        "priority": "P0",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Kestrel and FluentValidation lack chronological timing assertion (<code>RuleFor(x =&gt; x).Must(s =&gt; s.IsOvernight || s.EndTime &gt; s.StartTime)</code>).</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "18",
        "defect_id": "DEFECT-20261102-01",
        "module": "Part 3D / Work Template Localization & Data Integrity",
        "type": "API / Localization",
        "description": "<p><strong>Missing Mandatory English Template Name (<code>templateName.en</code>):</strong> Creating or updating work templates with only Arabic name (<code>\"templateName\": {\"ar\": \"دوام\"}</code>) succeeds with <code>HTTP 200 OK</code>, persisting <code>WorkTemplateName.en: null</code> in MongoDB.</p>",
        "screenshot": "evidence_01_worktemplates_created_with_placeholder.png",
        "remarks": "<p><strong>Endpoint:</strong> <code>POST/PATCH /api/companies/{companyId}/worktemplates/{fixed|flexi|split}</code></p><p><strong>Impact:</strong> Blank template headers in English UI sessions.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Validator only asserts <code>templateName</code> object existence, but omits mandatory check on <code>templateName.en</code>.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "19",
        "defect_id": "DEFECT-20261102-03 / DEFECT-20261102-04",
        "module": "Part 3D / Work Template DTO Contracts",
        "type": "API / Contract",
        "description": "<p><strong><code>shortCode</code> Length &amp; Character Boundaries Bypassed:</strong> Single-character codes (<code>\"A\"</code>) and codes exceeding 7 characters (<code>\"CDWT12345\"</code>) or with special characters (<code>\"CDW@#99\"</code>) accepted with <code>HTTP 200 OK</code> instead of enforcing <code>^[A-Za-z0-9]{2,7}$</code>.</p>",
        "screenshot": "evidence_14_att4_patch_shortcode_locked_1107.png",
        "remarks": "<p><strong>Endpoint:</strong> <code>POST /api/companies/{companyId}/worktemplates/*</code></p><p><strong>Violation:</strong> Length boundaries &lt; 2 and &gt; 7 bypassed.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Boundary checks for shortCode length (&gt;= 2 and &lt;= 7) and alphanumeric regex are missing in DTO validators.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "20",
        "defect_id": "DEFECT-20261102-06",
        "module": "Part 3D / Work Template Business Invariants",
        "type": "API / Validation",
        "description": "<p><strong><code>totalWorkDurationInMinutes</code> Missing Validation (Zero / Negative):</strong> Submitting <code>totalWorkDurationInMinutes: 0</code> or negative values (<code>-480</code>) accepted with <code>HTTP 200 OK</code> on templates with active working days.</p>",
        "screenshot": "evidence_08_negative_grace_accepted_200.png",
        "remarks": "<p><strong>Payload:</strong> <code>{\"totalWorkDurationInMinutes\": 0}</code> on 6-day template.</p><p><strong>Impact:</strong> Corrupts weekly required working hours calculations in payroll.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Total weekly duration accepted as zero/negative without validation.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "21",
        "defect_id": "DEFECT-20261102-07",
        "module": "Part 3D / Work Template Robustness & Exception Handling",
        "type": "API / Server Error",
        "description": "<p><strong>Omitting <code>totalWorkingDays</code> / <code>totalDaysOff</code> Triggers HTTP 500 Crash:</strong> Omitting working/off days from create payload throws unhandled <code>NullReferenceException</code> / HTTP 500 server crash instead of RFC 9110 HTTP 400 Bad Request.</p>",
        "screenshot": "evidence_15_att4_patch_empty_payload_500.png",
        "remarks": "<p><strong>Endpoint:</strong> <code>POST /api/companies/{companyId}/worktemplates</code></p><p><strong>Response:</strong> Raw HTTP 500 stack trace leaked.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Handler lacks null-safety guard for omitted integer properties prior to calculation.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "22",
        "defect_id": "DEFECT-20261102-08",
        "module": "Part 3D / Work Template Slot Validation",
        "type": "API / Business Rule",
        "description": "<p><strong>Daily <code>workDurationInMinutes</code> Accepts Zero or Negative on Active Days:</strong> Configuring an active working day (<code>isWorkingDay: true</code>) with <code>workDurationInMinutes: 0</code> or negative minutes accepted with <code>HTTP 200 OK</code>.</p>",
        "screenshot": "evidence_08_negative_grace_accepted_200.png",
        "remarks": "<p><strong>Invariant:</strong> Active days must have positive work duration.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Time slot validator does not assert <code>WorkDurationInMinutes &gt; 0</code> when <code>IsWorkingDay == true</code>.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "23",
        "defect_id": "DEFECT-20261102-11",
        "module": "Part 3D / Work Template Mathematical Invariants",
        "type": "API / Math Invariant",
        "description": "<p><strong>Slot Duration Mathematical Invariant Violation:</strong> Shift from 09:00 to 17:00 (480 min elapsed) with declared <code>workDurationInMinutes: 120</code> accepted with <code>HTTP 200 OK</code> without asserting mathematical equality.</p>",
        "screenshot": "evidence_10_negative_break_accepted_200.png",
        "remarks": "<p><strong>Payload:</strong> 09:00-17:00 with 120m duration.</p><p><strong>Impact:</strong> Inconsistent shift durations stored in database.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Slot duration math invariant check is not enforced between timings and duration.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "24",
        "defect_id": "DEFECT-20261102-12",
        "module": "Part 3D / Work Template Calendar Invariants",
        "type": "API / Calendar Invariant",
        "description": "<p><strong>Contradictory Off-Day Configuration Accepted:</strong> Days marked with <code>isWorkingDay: false</code> allowed to carry active start/end timings and positive duration, and total working days sum does not match active slots.</p>",
        "screenshot": "evidence_12_calendar_sum_not_7_500_validation_exception.png",
        "remarks": "<p><strong>Invariant:</strong> Non-working days must have 0 duration and no active timings.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Off-day contradiction allowed without validation error.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "25",
        "defect_id": "DEFECT-20261102-13",
        "module": "Part 3D / Work Template Domain Guards & Immutability",
        "type": "API / Domain Guard",
        "description": "<p><strong>Template Type Mutability via PATCH:</strong> Modifying <code>templateType</code> across incompatible categories (e.g. Fixed to Flexi or Roster) via PATCH is allowed or corrupts polymorphic document schema in MongoDB.</p>",
        "screenshot": "evidence_14_att4_patch_shortcode_locked_1107.png",
        "remarks": "<p><strong>Invariant:</strong> <code>templateType</code> is immutable after creation.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. PATCH handler lacks immutability guard for <code>templateType</code>.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "26",
        "defect_id": "DEFECT-20261102-18",
        "module": "Part 3D / Split Shift Functional Invariants",
        "type": "API / Robustness",
        "description": "<p><strong>Split Shift Empty Interval Array (<code>timeSlots: []</code>):</strong> Submitting an empty interval array on Split Work Template creation lacks domain guard requiring at least 2 non-overlapping intervals.</p>",
        "screenshot": "evidence_09_split_overlap_500_validation_exception.png",
        "remarks": "<p><strong>Endpoint:</strong> <code>POST /api/companies/{companyId}/worktemplates/split</code></p><p><strong>Violation:</strong> Empty intervals accepted.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Split shift validator does not enforce minimum 2 intervals requirement.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    # Rows 27 - 28: Part 3F Holiday Calendar Live Compass Proofs (Audit Identity & TenantName Persistence)
    {
        "sno": "27",
        "defect_id": "DEFECT-20261103-01",
        "module": "Part 3F / Holiday Calendar Audit Trail",
        "type": "API / DB",
        "description": "<p><strong>Audit Field <code>CreatedBy</code> Stores Plain Email String:</strong> Audit field <code>CreatedBy</code> persists as plain email string (<code>\"syed.mohamed@comm-it.in\"</code>) instead of composite user identity document <code>{ userId, loginId, name, email }</code> in <code>ERP.Attendance.HolidayCalendars</code>.</p>",
        "screenshot": "evidence_18_holiday_calendar_createdby_email_tenantname_empty.jpg",
        "remarks": "<p><strong>Database:</strong> <code>ERP.Attendance.HolidayCalendars</code></p><p>Document: <code>82830d41-a933-4610-a591-13b8ea6e6caf</code></p><p><code>CreatedBy: \"syed.mohamed@comm-it.in\"</code> (string).</p>",
        "priority": "P2",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. MongoDB Compass inspection confirms plain email string persists instead of structured composite <code>AuditUser</code> document, breaking ERP audit identity invariants.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "28",
        "defect_id": "DEFECT-20261103-02",
        "module": "Part 3F / Holiday Calendar Multi-Tenancy",
        "type": "API / DB",
        "description": "<p><strong><code>TenantName</code> Persists as <code>Object (empty)</code> <code>{}</code>:</strong> When creating or updating a holiday calendar, <code>TenantName</code> persists as an empty BSON object <code>{}</code> in MongoDB despite <code>CompanyName</code> being properly populated.</p>",
        "screenshot": "evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg",
        "remarks": "<p><strong>Database:</strong> <code>ERP.Attendance.HolidayCalendars</code></p><p><code>TenantName: Object (empty) {}</code> highlighted in Compass.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. MongoDB Compass inspection confirms <code>TenantName</code> persists as <code>Object (empty) {}</code> across all holiday calendar documents in <code>ERP.Attendance.HolidayCalendars</code>.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    # Row 29: Part 3G Defects Identified on 05 November 2026 — Work Template Module (Live MongoDB Compass Verification)
    {
        "sno": "29",
        "defect_id": "DEFECT-20261105-01",
        "module": "Part 3G: Defects Identified on 05 November 2026 — Work Template Module (Live MongoDB Compass Verification)",
        "type": "API / DB",
        "description": "<p><strong><code>CompanyName</code> Persists as <code>Object (empty)</code> <code>{}</code> in MongoDB:</strong> During fresh company onboarding and CDWT creation on Company <strong>Attendance 9</strong> (<code>3a249872-2d69-f931-41f6-d8db086b09b8</code>), document <code>d5abe5c4-d51f-4287-9baf-38e2e4f547c8</code> stores <code>CompanyId</code> but leaves <code>CompanyName</code> as an unpopulated empty object <code>{}</code>. <code>SP.AttendanceSvc</code> never queries <code>SP.CompanySvc</code> to resolve localized names (<code>{\"en\": \"Attendance 9\", \"ar\": \"الحضور 9\"}</code>), causing blank company names in API responses (<code>\"companyName\": {}</code>) and UI.</p>",
        "screenshot": "evidence_39_companyname_empty_object_compass.jpg",
        "remarks": "<p><strong>Database:</strong> <code>Sahab.ERP.Attendance.WorkTemplates</code></p><p><strong>Document ID:</strong> <code>d5abe5c4-d51f-4287-9baf-38e2e4f547c8</code></p><p><strong>Endpoint:</strong> <code>POST /api/companies/{companyId}/worktemplates/fixed</code></p><p><code>\"CompanyName\": { }</code> highlighted in Compass.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Inspection of MongoDB Compass confirms <code>CompanyName</code> remains <code>Object (empty) {}</code> across all seeded templates in <code>Sahab.ERP.Attendance.WorkTemplates</code>. Upstream metadata resolution from <code>SP.CompanySvc</code> missing.</p>",
        "testing_status": "Failed – Not Fixed"
    }
]

# Generate storage HTML matching the Leave Balance format with an executive summary macro
table_html = """<p><strong>Attendance 2 Microservice &mdash; Consolidated Defect Verification &amp; Fixes Register</strong></p>

<ac:structured-macro ac:name="info" ac:schema-version="1">
  <ac:rich-text-body>
    <p><strong>Defect Verification &amp; Re-Test Execution Summary (Updated 16-Nov-2026):</strong></p>
    <ul>
      <li><strong>Part 3 (28-Oct) User Scenarios &amp; Core Defects:</strong> 138 User Scenarios + 7 Core Defects. <strong>4 Fixed</strong> (<code>DEFECT-20261028-01</code>, <code>02</code>, <code>03</code>, <code>07</code>) | <strong>3 Core Backlogs Not Fixed</strong> (<code>DEFECT-20261028-04</code>, <code>05</code>, <code>06</code> + <code>USER-01</code>, <code>USER-03</code>).</li>
      <li><strong>WT - Company Default (Module 2):</strong> 150 Scenarios. <strong>146 Passed</strong> | <strong>5 Failed Issues Not Fixed</strong> (<code>DOC-A-04</code>/<code>ROOT-E-05</code>, <code>DOC-A-05</code>/<code>ROOT-E-06</code>, <code>DEFECT-20261105-01</code>, <code>DEFECT-20261110-01</code>, <code>DEFECT-20261103-16</code>).</li>
      <li><strong>Part 3B: Holiday Calendar Suite (313 Test Cases):</strong> 100% Executed. <strong>305 Passed (97.4%)</strong> | <strong>8 Failed Scenarios Not Fixed (2.6%)</strong> (<code>DEFECT-20261103-08</code>, <code>DEFECT-20261103-15</code>, <code>DEFECT-20261103-03</code>, Route Constraints <code>HC-DTO-01/74/127/129</code>, and Checklist Sync <code>HC-PUB-16</code>).</li>
      <li><strong>Part 3C: Security &amp; Swagger Architecture (29-Oct):</strong> 2 Critical Architecture Issues. <strong>0 Fixed | 2 NOT FIXED</strong> (<code>DEFECT-20261029-01</code> JWT validation bypass &amp; <code>DEFECT-20261029-02</code> Swagger OAuth2 missing). <em>Note: Need to be helped with Ravi sir need to fix the issue.</em></li>
      <li><strong>Part 3D: Work Template DTO Validations &amp; Invariants (02-Nov):</strong> 13 Core Validations &amp; Invariants. <strong>1 Resolved / Mitigated</strong> (<code>DEFECT-20261102-09</code> 500 crash mapped to 400) | <strong>10 Failed Invariants NOT FIXED</strong> (<code>DEFECT-20261102-10</code>, <code>DEFECT-20261102-01</code>, <code>DEFECT-20261102-03/04</code>, <code>DEFECT-20261102-06</code>, <code>DEFECT-20261102-07</code>, <code>DEFECT-20261102-08</code>, <code>DEFECT-20261102-11</code>, <code>DEFECT-20261102-12</code>, <code>DEFECT-20261102-13</code>, <code>DEFECT-20261102-18</code>).</li>
      <li><strong>Part 3F: Holiday Calendar Live Compass Proofs (03-Nov):</strong> 2 Core Audit &amp; Multi-Tenancy Defects. <strong>0 Fixed | 2 NOT FIXED</strong> (<code>DEFECT-20261103-01</code> plain email string in <code>CreatedBy</code> &amp; <code>DEFECT-20261103-02</code> empty <code>TenantName: {}</code> object &mdash; Rows 27-28).</li>
      <li><strong>Part 3G: Work Template Module Live Compass Proofs (05-Nov):</strong> 1 Critical Master Data Defect. <strong>0 Fixed | 1 NOT FIXED</strong> (<code>DEFECT-20261105-01</code> empty <code>CompanyName: {}</code> object in MongoDB across all seeded templates &mdash; <strong>Row 29</strong>).</li>
    </ul>
  </ac:rich-text-body>
</ac:structured-macro>

<table data-table-width="1800" data-layout="default">
  <colgroup>
    <col style="width: 70.0px;" />
    <col style="width: 200.0px;" />
    <col style="width: 110.0px;" />
    <col style="width: 260.0px;" />
    <col style="width: 220.0px;" />
    <col style="width: 260.0px;" />
    <col style="width: 90.0px;" />
    <col style="width: 110.0px;" />
    <col style="width: 280.0px;" />
    <col style="width: 140.0px;" />
  </colgroup>
  <tbody>
    <tr>
      <th data-highlight-colour="#f0f1f2"><p><strong>S.no</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>Module</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>FE / API</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>description</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>Screenshot</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>Remarks</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>Priority</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>Dev Status</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>QA Remarks</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>Testing Status</strong></p></th>
    </tr>
"""

for row in rows_data:
    table_html += f"""    <tr>
      <td><p><strong>{row['sno']}</strong></p><p><small>{html.escape(row['defect_id'])}</small></p></td>
      <td><p><strong>{html.escape(row['module'])}</strong></p></td>
      <td><p>{html.escape(row['type'])}</p></td>
      <td>{row['description']}</td>
      <td>
        <ac:image ac:align="center" ac:layout="center" ac:custom-width="true" ac:width="190">
          <ri:attachment ri:filename="{row['screenshot']}" />
        </ac:image>
      </td>
      <td>{row['remarks']}</td>
      <td><p><strong>{row['priority']}</strong></p></td>
      <td><p><strong>{row['dev_status']}</strong></p></td>
      <td>{row['qa_remarks']}</td>
      <td><p><strong>{row['testing_status']}</strong></p></td>
    </tr>
"""

table_html += """  </tbody>
</table>
"""

# Publish update to Confluence
update_payload = {
    "id": page_id,
    "type": "page",
    "title": title,
    "space": {"key": space_key},
    "body": {
        "storage": {
            "value": table_html,
            "representation": "storage"
        }
    },
    "version": {
        "number": current_version + 1,
        "message": "Added Part 3G Defects Identified on 05 November 2026 - Work Template Module (Live MongoDB Compass Verification) as Row 29."
    }
}

print(f"Publishing updated table to Confluence (Version {current_version + 1})...")
put_res = requests.put(
    f"{base_url}/rest/api/content/{page_id}",
    auth=auth,
    headers={"Content-Type": "application/json"},
    data=json.dumps(update_payload)
)

print(f"Response status: {put_res.status_code}")
if put_res.status_code == 200:
    res_data = put_res.json()
    new_v = res_data.get('version', {}).get('number')
    print(f"SUCCESS: Page '{title}' updated to version {new_v} with 29 rows!")
else:
    print(f"FAILURE: {put_res.status_code}")
    print(put_res.text[:500])
