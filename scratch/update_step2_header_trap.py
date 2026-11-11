import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    text = f.read()

target = """> [!WARNING] Critical Rule: First-Time Setup Lockout (POST vs. PATCH)
- **`POST` is EXCLUSIVELY for first-time setup** when no default template exists for the company.
- Once a default work template exists (`IsDefault: true`), calling `POST /fixed`, `POST /flexi`, or `POST /split` will immediately throw **`HTTP 409 Conflict`** (*"A default work template already exists for this company. Please use PATCH to update or switch template types."*).
- **To switch template types or update timings, ALWAYS use `PATCH`!**"""

replacement = """> [!WARNING] Critical Rule: First-Time Setup Lockout (POST vs. PATCH)
- **`POST` is EXCLUSIVELY for first-time setup** when no default template exists for the company.
- Once a default work template exists (`IsDefault: true`), calling `POST /fixed`, `POST /flexi`, or `POST /split` will immediately throw **`HTTP 409 Conflict`** (*"A default work template already exists for this company. Please use PATCH to update or switch template types."*).
- **To switch template types or update timings, ALWAYS use `PATCH`!**

> [!CAUTION] Critical Header Trap: First-Time Setup Lockout with Location Headers
> - **Do NOT pass `LocationId` or `X-Location-Id` in HTTP Request Headers** when creating the Company Default Work Template (`POST /fixed`, `POST /flexi`, or `POST /split`).
> - If an active `LocationId` is passed in headers when CDWT is not yet configured:
>   - The backend binds the request as a **Location Template creation**.
>   - Because CDWT does not exist yet, the system **STRICTLY BLOCKS CREATION** and throws **`HTTP 400 Bad Request: Cit.Attendance:1205 ('Company default is not available.')`**.
>   - This lockout applies uniformly across **Fixed**, **Flexible**, and **Split Shift** templates!
>   - **Rule:** CDWT creation MUST have `LocationId = 00000000-0000-0000-0000-000000000000` with headers and query strictly free of location identifiers."""

if target in text:
    updated = text.replace(target, replacement, 1)
    with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'w', encoding='utf-8') as f:
        f.write(updated)
    print("Successfully added Header Trap warning to API Guide!")
else:
    print("Target string not found!")

