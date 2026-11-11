with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    content = f.read()

target_step3 = """### Step 3: Company Holiday Calendar
* **Goal:** Create public holidays per year. Auto-fanout inherited copies to locations. Stage and publish changes.
* **Microservice:** **`SP.AttendanceSvc`**

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |
|---|:---:|---|---|---|---|---|---|
| **3.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/holidaylist` | *(No `locationId`)* | `shortCode: "HC-2027"`<br>`yearlyCalendar: {year: 2027, holidayLists: [...]}` | **HTTP 200**: Company Default created (`CalendarType: 1`). **Auto-fans out** read-only inherited copies (`IsInherited: true`) to all active locations. | `ERP.Attendance.HolidayCalendars` |
| **3.2** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{id}/{year}` | `{id}`, `{year}` | Modified `holidayLists` | **HTTP 200**: Staged edit: sets `IsPublished = false`. Locations are untouched until publish. | `ERP.Attendance.HolidayCalendars` |
| **3.3** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{id}/remove/{holidayId}/{year}` | `{id}`, `{holidayId}`, `{year}` | None | **HTTP 200**: Removes holiday from staged list | `ERP.Attendance.HolidayCalendars` |
| **3.4** | `POST` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/publish/{year}` | `{year}` | None | **HTTP 200**: **Publish:** Overwrites all locations where `IsInherited == true`. Sets `LastPublishedOn`. | `ERP.Attendance.HolidayCalendars` |
| **3.5** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{locationCalendarId}/customise` | `{locationCalendarId}` | None | **HTTP 200**: **Customise (Detach):** Sets `IsInherited = false`. Protects location from future company publishes. | `ERP.Attendance.HolidayCalendars` |
| **3.6** | `GET` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{year}` | `?locationId={locId}` | None | **HTTP 200**: Returns active calendar applicable to location | `ERP.Attendance.HolidayCalendars` |"""

replacement_step3 = """### Step 3: Company Holiday Calendar & Publishing Lifecycle
* **Goal:** Create public holidays per year across 5 enum types. Enforce From Date Only mandatory rule. Stage changes, validate Work Template & compulsory $\ge 1$ holiday prerequisites, publish to overwrite inheriting locations, synchronize Company Service checklist, handle post-publish mutations, and re-publish round 2.
* **Microservices:** **`SP.AttendanceSvc`** (Port 5001 / Dev: `attendance2.dev.zoolwork.com`) & **`SP.CompanySvc`** (Port 5000 / Dev: `company8.dev.zoolwork.com`)

#### Key Business & Validation Rules:
1. **5 Holiday Types Dropdown:** `Public Holiday` (1), `Religious Holiday` (2), `National Holiday` (3), `Bank Holiday` (4), `Gazette Holiday` (5).
2. **From Date Only Rule:** Only `StartDate` is mandatory. If `EndDate` is null or omitted, backend auto-assigns `EndDate = StartDate` and `TotalDays = 1`.
3. **End Date Boundary:** If `EndDate < StartDate`, backend rejects with HTTP 400 Bad Request, code `Cit.Attendance:1705`.
4. **Publishing Prerequisites:**
   - **Compulsory $\ge 1$ Holiday:** Cannot publish empty list (`holidayLists: []`). Rejects with HTTP 400 Bad Request, code `Cit.Attendance:1704`.
   - **Mandatory Work Template:** Company Default Work Template (CDWT) must exist and be active before publishing holidays.
5. **Pre-Publish Staging:** `POST /holidaylist`, `PATCH /holidaylist/{id}/{year}` (Add/Edit), and `PATCH /remove/{holidayId}` update company default in staged mode (`IsPublished = false`). Inherited locations are NOT touched until published.
6. **Publish Execution:** `POST /publish/{year}` sets `IsPublished = true`, sets `LastPublishedOn = UTC now`, overwrites all active locations where `IsInherited == true`, and updates Company Service `CompaniesMaster.CompanyChecklist.HolidayCalendarPublished = true`.
7. **Post-Publish Mutations & Re-Publish (Round 2):** Any addition, edit, or removal after initial publish reverts `IsPublished = false` (Unpublished Changes flag). Re-publishing (`POST /publish/{year}`) re-syncs round-2 changes to inheriting locations and refreshes Company Service status.
8. **Location Isolation:** Detached locations (`IsInherited = false`) remain 100% immune across initial publish and all subsequent re-publish rounds.

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | Target DB & Field Updates |
|---|:---:|---|---|---|---|---|---|
| **3.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/holidaylist` | *(No `locationId`)* | `shortCode: "HC-2026"`<br>`yearlyCalendar: {year: 2026, holidayLists: [...]}` | **HTTP 200**: Creates Company Default (`CalendarType: 1`, `IsPublished: false`). **Auto-fans out** read-only inherited copies (`IsInherited: true`) to all active locations. | `ERP.Attendance.HolidayCalendars`<br>`IsPublished: false` |
| **3.2** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{id}/{year}` | `{id}`, `{year}` | Modified `holidayLists` (Add or Edit) | **HTTP 200**: Staged edit: sets `IsPublished = false`. Locations are untouched until publish. | `ERP.Attendance.HolidayCalendars`<br>`IsPublished: false` |
| **3.3** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{id}/remove/{holidayId}/{year}` | `{id}`, `{holidayId}`, `{year}` | None | **HTTP 200**: Removes holiday from staged list; `IsPublished = false`. Past holidays rejected (`1709`). | `ERP.Attendance.HolidayCalendars`<br>`Pull from HolidayLists` |
| **3.4** | `POST` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/publish/{year}` | `{year}` | None | **HTTP 200**: **Publish:** Validates CDWT + list $\ge 1$. Overwrites inheriting locations (`IsInherited: true`). Sets `LastPublishedOn`. | Attendance: `IsPublished: true`<br>Company Svc: `CompanyChecklist` sync |
| **3.5** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{locationCalendarId}/customise` | `{locationCalendarId}` | None | **HTTP 200**: **Customise (Detach):** Sets `IsInherited = false`. Protects location from future company publishes. | `ERP.Attendance.HolidayCalendars`<br>`IsInherited: false` |
| **3.6** | `GET` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{year}` | `?locationId={locId}` | None | **HTTP 200**: Returns active calendar applicable to location. Confirms `isPublished` state. | `ERP.Attendance.HolidayCalendars` |
| **3.7** | `GET` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{id}` | `{id}` | None | **HTTP 200**: Returns specific holiday calendar document details. | `ERP.Attendance.HolidayCalendars` |
| **3.8** | `POST` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/publish/{year}` | `{year}` | None | **HTTP 200**: **Re-Publish (Round 2):** Syncs post-publish additions, edits, and removals to locations. | Attendance & Company Svc |"""

content_norm = content.replace('\r\n', '\n')
target_norm = target_step3.replace('\r\n', '\n')
replacement_norm = replacement_step3.replace('\r\n', '\n')

if target_norm in content_norm:
    content_norm = content_norm.replace(target_norm, replacement_norm)
    with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(content_norm.replace('\n', '\r\n'))
    print("Successfully updated Step 3 in guide!")
else:
    print("Target Step 3 not found!")

