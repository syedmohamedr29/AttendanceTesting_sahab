import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    text = f.read()

marker = 'To switch template types or update timings, ALWAYS use `PATCH`!**'
idx = text.find(marker)

if idx == -1:
    print("Marker not found!")
    sys.exit(1)

insert_pos = idx + len(marker)

insertion = """

> [!CAUTION] Critical Header Trap: First-Time Setup Lockout with Location Headers
> - **Do NOT pass `LocationId` or `X-Location-Id` in HTTP Request Headers** when creating the Company Default Work Template (`POST /fixed`, `POST /flexi`, or `POST /split`).
> - If an active `LocationId` is passed in headers when CDWT is not yet configured:
>   - The backend binds the request as a **Location Template creation**.
>   - Because CDWT does not exist yet, the system **STRICTLY BLOCKS CREATION** and throws **`HTTP 400 Bad Request: Cit.Attendance:1205 ('Company default is not available.')`**.
>   - This lockout applies uniformly across **Fixed**, **Flexible**, and **Split Shift** templates!
>   - **Rule:** CDWT creation MUST have `LocationId = 00000000-0000-0000-0000-000000000000` with headers and query strictly free of location identifiers."""

updated_text = text[:insert_pos] + insertion + text[insert_pos:]

with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'w', encoding='utf-8') as f:
    f.write(updated_text)

print("Successfully inserted Header Trap Caution into API Guide!")

