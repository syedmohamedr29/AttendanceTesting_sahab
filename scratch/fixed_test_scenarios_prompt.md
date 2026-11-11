<USER_REQUEST>
https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614


now you run the test all the validation based above prompt


# Fixed Work Template API – Complete Test Scenarios

I have used the Fixed Work Template structure from your previous `Sahab.ERP.Attendance.WorkTemplates.json` data and the earlier Fixed-to-Flexible testing discussion.

The stored Fixed template uses:

- `TemplateType: 1`
- `FixedTimeSlots`
- `DayEnum`: Sunday = 1 through Saturday = 7
- `RecurrenceOfMonth`: First = 1 through Fifth = 5
- Working-day slots with start/end times and work duration
- Off-day slots with zero duration, midnight times, and an empty recurrence list

The saved document also contains totals, status, version, company/location information, and template flags. These database fields are not necessarily all POST/PATCH request fields.&#x20;

## 1. API endpoints

| Method | Endpoint                                              | Purpose               |
| ------ | ----------------------------------------------------- | --------------------- |
| POST   | `/api/companies/{companyId}/worktemplates/fixed`      | Create Fixed template |
| PATCH  | `/api/companies/{companyId}/worktemplates/fixed/{id}` | Update Fixed template |

## 2. Request fields and enum values

| Field                        | Meaning                 | Known value/example            |
| ---------------------------- | ----------------------- | ------------------------------ |
| `templateName`               | Localized template name | `{ "en": "...", "ar": "..." }` |
| `shortCode`                  | Template short code     | `"FIX001"`                     |
| `templateType`               | Fixed template type     | `1`                            |
| `totalWorkDurationInMinutes` | Total work duration     | `2700`                         |
| `totalWorkingDays`           | Number of working days  | `5`                            |
| `totalDaysOff`               | Number of days off      | `2`                            |
| `timeZoneId`                 | Time zone               | `"Asia/Riyadh"`                |
| `fixedTimeSlots`             | Weekly schedule         | Array of slots                 |

Day enum

| Day       | Numeric value |
| --------- | ------------- |
| Sunday    | 1             |
| Monday    | 2             |
| Tuesday   | 3             |
| Wednesday | 4             |
| Thursday  | 5             |
| Friday    | 6             |
| Saturday  | 7             |

Monthly recurrence enum

| Recurrence | Numeric value |
| ---------- | ------------- |
| First      | 1             |
| Second     | 2             |
| Third      | 3             |
| Fourth     | 4             |
| Fifth      | 5             |

Fixed slot structure

```
{
  "workDurationInMinutes": 540,
  "dayEnum": 2,
  "isWorkingDay": true,
  "recurrenceOfMonth": [1, 2, 3, 4, 5],
  "startTime": "08:00:00",
  "endTime": "17:00:00"
}
```

For an off-day slot, the stored example uses:

```
{
  "workDurationInMinutes": 0,
  "dayEnum": 6,
  "isWorkingDay": false,
  "recurrenceOfMonth": [],
  "startTime": "00:00:00",
  "endTime": "00:00:00"
}
```

The payloads below use these known fields. I have not added unconfirmed fields such as `locationId`, `tenantId`, or `companyName` to the request.

## 3. Standard baseline payload

Use this as the baseline for POST and PATCH testing.

```
{
  "templateName": {
    "en": "Standard Fixed Work Template",
    "ar": "قالب العمل الثابت القياسي"
  },
  "shortCode": "FIX001",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    }
  ]
}
```

The 5 × 540-minute total is 2700 minutes (45 hours). The slot array covers all seven days.

## 4. POST – Positive scenarios

Endpoint: `POST /api/companies/{companyId}/worktemplates/fixed`

For each create test, use a unique `shortCode` and template name unless specifically testing duplicate validation.

### P01 – Create standard five-day working template

Use the baseline payload above.

Expected:

- Template created successfully.
- `TemplateType` saved as `1`.
- Five working days and two days off.
- Total duration matches the working slots.

### P02 – Create six-day working template

```
{
  "templateName": {
    "en": "Six Days Fixed Template",
    "ar": "قالب عمل ثابت لستة أيام"
  },
  "shortCode": "FIX002",
  "templateType": 1,
  "totalWorkDurationInMinutes": 3240,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    }
  ]
}
```

### P03 – Create four-day working template

Use four working slots and three off-day slots.

Expected: Verify working-day count, off-day count, and duration calculation.

### P04 – Create template with different working hours per day

Use a full seven-day array with working durations such as 480, 540, and 600 minutes. Ensure the totals equal the sum of the working slots.

### P05 – Create with different start and end times

Use `09:00:00` to `18:00:00` for all five working days, with 540 minutes per day.

Expected: Verify the saved start/end time and calculated duration.

### P06 – Create with 30-minute shorter working duration

Use `08:00:00` to `16:30:00`, with `workDurationInMinutes: 510` for each working day.

Expected: Verify that duration and time range are consistent.

### P07 – Create with all five monthly recurrences

Use `[1,2,3,4,5]` for working days.

Expected: All five recurrence values are saved correctly.

### P08 – Create with selected monthly recurrences

Use `[1,3,5]` for a working day.

Expected: The day applies only to the selected occurrences, if supported by the application.

### P09 – Create English and Arabic names

Use valid English and Arabic `templateName` values.

Expected: Both languages are persisted correctly.

### P10 – Create with a different time zone

Use a valid supported timezone such as `"Asia/Kolkata"`.

Expected: The timezone is saved and displayed correctly.

### P11 – Create with one working day and six days off

Use one working slot with 540 minutes and six off-day slots.

Expected: Verify whether this schedule is allowed by business rules.

### P12 – Create with zero working duration on off-days

Use zero duration, midnight start/end, empty recurrence on every off-day.

Expected: Off-day information should be persisted consistently.

## 5. POST – Negative validation scenarios

For each negative case, keep the remaining fields valid and change only the field being tested.

### N01 – Empty request body

```
{}
```

Expected: Request validation failure.

### N02 – Missing template name

```
{
  "shortCode": "FIXN02",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": []
}
```

Expected: Reject missing required template name.

### N03 – Null template name

```
{
  "templateName": null,
  "shortCode": "FIXN03",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": []
}
```

### N04 – Empty English name

```
{
  "templateName": {
    "en": "",
    "ar": "قالب العمل الثابت"
  },
  "shortCode": "FIXN04",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": []
}
```

### N05 – Missing short code

```
{
  "templateName": {
    "en": "Missing Short Code",
    "ar": "قالب بدون رمز"
  },
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": []
}
```

### N06 – Empty short code

```
{
  "templateName": {
    "en": "Empty Short Code",
    "ar": "رمز فارغ"
  },
  "shortCode": "",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": []
}
```

### N07 – Duplicate short code

Use an already-existing short code in the same company.

Expected: Verify duplicate validation and company-level uniqueness.

### N08 – Invalid template type

```
{
  "templateName": {
    "en": "Invalid Template Type",
    "ar": "نوع قالب غير صالح"
  },
  "shortCode": "FIXN08",
  "templateType": 999,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": []
}
```

### N09 – Null fixed time slots

```
{
  "templateName": {
    "en": "Null Slots",
    "ar": "فترات زمنية فارغة"
  },
  "shortCode": "FIXN09",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": null
}
```

### N10 – Empty fixed time slots

```
{
  "templateName": {
    "en": "Empty Slots",
    "ar": "قالب بدون فترات"
  },
  "shortCode": "FIXN10",
  "templateType": 1,
  "totalWorkDurationInMinutes": 0,
  "totalWorkingDays": 0,
  "totalDaysOff": 7,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": []
}
```

Expected: Verify whether an empty schedule is rejected.

### N11 – Invalid day enum

```
{
  "templateName": {
    "en": "Invalid Day Enum",
    "ar": "يوم غير صالح"
  },
  "shortCode": "FIXN11",
  "templateType": 1,
  "totalWorkDurationInMinutes": 540,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 8,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    }
  ]
}
```

### N12 – Day enum below minimum

```
{
  "templateName": {
    "en": "Day Enum Below Minimum",
    "ar": "يوم أقل من الحد الأدنى"
  },
  "shortCode": "FIXN12",
  "templateType": 1,
  "totalWorkDurationInMinutes": 540,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 0,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    }
  ]
}
```

### N13 – Invalid recurrence value

```
{
  "templateName": {
    "en": "Invalid Recurrence",
    "ar": "تكرار غير صالح"
  },
  "shortCode": "FIXN13",
  "templateType": 1,
  "totalWorkDurationInMinutes": 540,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 6],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    }
  ]
}
```

### N14 – Recurrence below minimum

```
{
  "templateName": {
    "en": "Recurrence Below Minimum",
    "ar": "تكرار أقل من الحد الأدنى"
  },
  "shortCode": "FIXN14",
  "templateType": 1,
  "totalWorkDurationInMinutes": 540,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [0],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    }
  ]
}
```

### N15 – Negative work duration

```
{
  "templateName": {
    "en": "Negative Work Duration",
    "ar": "مدة عمل سالبة"
  },
  "shortCode": "FIXN15",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": -1,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    }
  ]
}
```

### N16 – Decimal work duration

```
{
  "templateName": {
    "en": "Decimal Work Duration",
    "ar": "مدة عمل عشرية"
  },
  "shortCode": "FIXN16",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540.5,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    }
  ]
}
```

### N17 – Start time later than end time

```
{
  "templateName": {
    "en": "Invalid Time Range",
    "ar": "نطاق وقت غير صالح"
  },
  "shortCode": "FIXN17",
  "templateType": 1,
  "totalWorkDurationInMinutes": 540,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "17:00:00",
      "endTime": "08:00:00"
    }
  ]
}
```

### N18 – Invalid start time format

```
{
  "templateName": {
    "en": "Invalid Start Time",
    "ar": "وقت بداية غير صالح"
  },
  "shortCode": "FIXN18",
  "templateType": 1,
  "totalWorkDurationInMinutes": 540,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "25:70:00",
      "endTime": "17:00:00"
    }
  ]
}
```

### N19 – Invalid end time format

```
{
  "templateName": {
    "en": "Invalid End Time",
    "ar": "وقت نهاية غير صالح"
  },
  "shortCode": "FIXN19",
  "templateType": 1,
  "totalWorkDurationInMinutes": 540,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "25:70:00"
    }
  ]
}
```

### N20 – Wrong working-day data type

```
{
  "templateName": {
    "en": "Invalid Working Day Type",
    "ar": "نوع يوم عمل غير صالح"
  },
  "shortCode": "FIXN20",
  "templateType": 1,
  "totalWorkDurationInMinutes": 540,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": "true",
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    }
  ]
}
```

### N21 – Wrong time data type

```
{
  "templateName": {
    "en": "Invalid Time Data Type",
    "ar": "نوع وقت غير صالح"
  },
  "shortCode": "FIXN21",
  "templateType": 1,
  "totalWorkDurationInMinutes": 540,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": 800,
      "endTime": 1700
    }
  ]
}
```

### N22 – Invalid timezone

```
{
  "templateName": {
    "en": "Invalid Time Zone",
    "ar": "منطقة زمنية غير صالحة"
  },
  "shortCode": "FIXN22",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Invalid/TimeZone",
  "fixedTimeSlots": []
}
```

### N23 – Working day with zero duration

```
{
  "templateName": {
    "en": "Working Day Zero Duration",
    "ar": "يوم عمل بدون مدة"
  },
  "shortCode": "FIXN23",
  "templateType": 1,
  "totalWorkDurationInMinutes": 0,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 0,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    }
  ]
}
```

### N24 – Off-day with non-zero duration

```
{
  "templateName": {
    "en": "Off Day Nonzero Duration",
    "ar": "يوم عطلة بمدة غير صفرية"
  },
  "shortCode": "FIXN24",
  "templateType": 1,
  "totalWorkDurationInMinutes": 540,
  "totalWorkingDays": 0,
  "totalDaysOff": 1,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    }
  ]
}
```

Note on N23 and N24: These are business-consistency probes. The earlier saved data shows off-days represented with zero duration and midnight times, but it does not establish every server-side validation rule. Do not mark them as confirmed failures until the API behavior is checked.

### N25 – Duplicate day with overlapping recurrence

```
{
  "templateName": {
    "en": "Duplicate Day Overlap",
    "ar": "يوم مكرر بتكرار متداخل"
  },
  "shortCode": "FIXN25",
  "templateType": 1,
  "totalWorkDurationInMinutes": 1080,
  "totalWorkingDays": 2,
  "totalDaysOff": 0,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [3, 4, 5],
      "startTime": "09:00:00",
      "endTime": "18:00:00"
    }
  ]
}
```

Expected: Verify duplicate day handling. Your earlier test established that duplicate `dayEnum` values can be accepted when recurrence sets are disjoint. Overlapping recurrence values such as `3` should be checked for rejection or conflict handling.

### N26 – Duplicate recurrence values inside one slot

```
{
  "templateName": {
    "en": "Duplicate Recurrence Values",
    "ar": "قيم تكرار مكررة"
  },
  "shortCode": "FIXN26",
  "templateType": 1,
  "totalWorkDurationInMinutes": 540,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 1, 2, 3, 4, 5],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    }
  ]
}
```

Expected: Verify whether duplicate recurrence values are rejected or normalized.

## 6. POST – Boundary Value Analysis

These values are test candidates. The actual permitted maximums are not confirmed by the saved document.

### A. `workDurationInMinutes`

| Test ID | Value      | Purpose                    |
| ------- | ---------- | -------------------------- |
| BVA-01  | -1         | Below zero                 |
| BVA-02  | 0          | Zero boundary / off-day    |
| BVA-03  | 1          | Minimum positive candidate |
| BVA-04  | 30         | Short duration             |
| BVA-05  | 60         | One hour                   |
| BVA-06  | 480        | Eight hours                |
| BVA-07  | 510        | Eight and a half hours     |
| BVA-08  | 540        | Baseline nine hours        |
| BVA-09  | 600        | Ten hours                  |
| BVA-10  | 720        | Twelve hours               |
| BVA-11  | 1440       | Twenty-four hours          |
| BVA-12  | 2147483647 | Large integer              |
| BVA-13  | 2147483648 | Integer overflow candidate |

### B. `dayEnum`

| Test ID | Value | Expected  |
| ------- | ----- | --------- |
| BVA-14  | 0     | Invalid   |
| BVA-15  | 1     | Sunday    |
| BVA-16  | 2     | Monday    |
| BVA-17  | 3     | Tuesday   |
| BVA-18  | 4     | Wednesday |
| BVA-19  | 5     | Thursday  |
| BVA-20  | 6     | Friday    |
| BVA-21  | 7     | Saturday  |
| BVA-22  | 8     | Invalid   |

### C. `recurrenceOfMonth`

| Test ID | Value         | Expected                           |
| ------- | ------------- | ---------------------------------- |
| BVA-23  | `[]`          | Valid for off-day in saved example |
| BVA-24  | `[1]`         | First                              |
| BVA-25  | `[1,2]`       | First and second                   |
| BVA-26  | `[1,2,3]`     | First to third                     |
| BVA-27  | `[1,2,3,4]`   | First to fourth                    |
| BVA-28  | `[1,2,3,4,5]` | All five                           |
| BVA-29  | `[0]`         | Invalid candidate                  |
| BVA-30  | `[6]`         | Invalid candidate                  |
| BVA-31  | `[-1]`        | Invalid candidate                  |
| BVA-32  | `[1,1,2]`     | Duplicate recurrence candidate     |
| BVA-33  | `[5,4,3,2,1]` | Reverse ordering candidate         |

### D. Total duration and day counts

| Field                        | Test values                                     |
| ---------------------------- | ----------------------------------------------- |
| `totalWorkDurationInMinutes` | -1, 0, 1, 540, 2700, 3240, 10080, large integer |
| `totalWorkingDays`           | -1, 0, 1, 5, 6, 7, 8                            |
| `totalDaysOff`               | -1, 0, 1, 2, 6, 7, 8                            |

Test the relationship between all three totals:

\\[ \text{TotalWorkingDays}+\text{TotalDaysOff}=7 \\]

For the standard weekly example:

\\[ 5 \times 540 = 2700 \text{ minutes} \\]

Check whether the API calculates these totals itself or validates the values supplied by the client.

### E. Time values

| Test ID | Start time | End time   | Scenario                           |
| ------- | ---------- | ---------- | ---------------------------------- |
| BVA-34  | `00:00:00` | `00:01:00` | Minimum time interval candidate    |
| BVA-35  | `08:00:00` | `08:01:00` | One-minute slot                    |
| BVA-36  | `08:00:00` | `17:00:00` | Standard                           |
| BVA-37  | `09:00:00` | `18:00:00` | Alternative shift                  |
| BVA-38  | `00:00:00` | `23:59:00` | Nearly full day                    |
| BVA-39  | `23:00:00` | `23:59:00` | Late shift                         |
| BVA-40  | `17:00:00` | `08:00:00` | Overnight/cross-midnight candidate |
| BVA-41  | `24:00:00` | `25:00:00` | Invalid time                       |

For a Fixed template, verify whether overnight shifts are supported before treating a start time later than the end time as invalid.

## 7. PATCH – Positive scenarios

Endpoint: `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}`

Use an existing Fixed template ID returned from POST. The following payloads use the same request structure as the baseline.

### P01 – Update template name

Change:

```
{
  "templateName": {
    "en": "Updated Fixed Template",
    "ar": "قالب العمل الثابت المحدث"
  },
  "shortCode": "FIX001"
}
```

Keep all other baseline fields and slots unchanged.

### P02 – Update working hours

Change all five working slots from `08:00–17:00` to `09:00–18:00`, maintaining 540 minutes per day.

Expected: Verify all slot times and totals.

### P03 – Change five working days to six

Update Friday (`dayEnum: 6`) from off-day to working day.

Expected:

- `totalWorkingDays: 6`
- `totalDaysOff: 1`
- Recalculate `totalWorkDurationInMinutes` according to all working slots.

### P04 – Change five working days to four

Change one working day to an off-day.

Expected:

- `totalWorkingDays: 4`
- `totalDaysOff: 3`
- Update duration and slot information.

### P05 – Change off-day configuration

Move the off-day from Friday to Sunday.

Expected: Verify `dayEnum`, `isWorkingDay`, recurrence, and duration for both affected slots.

### P06 – Change recurrence

Change Monday recurrence from `[1,2,3,4,5]` to `[1,3,5]`.

Expected: Verify recurrence is updated without changing other days.

### P07 – Update one day's duration

Change Monday's duration from 540 to 480 minutes and update its end time to `16:00:00`.

Expected: Verify the new total duration.

### P08 – Update multiple day schedules

Change:

- Monday: 480 minutes
- Tuesday: 510 minutes
- Wednesday: 540 minutes
- Thursday: 570 minutes
- Friday: 600 minutes

Expected total: 2700 minutes, if all five are working days.

### P09 – Update time zone

Change:

```
"timeZoneId": "Asia/Kolkata"
```

Expected: Verify the timezone is saved and used correctly when displaying the schedule.

### P10 – Update all template fields

Update name, short code, all working slots, recurrence, working-day count, off-day count, total duration, and timezone together.

Expected: Every requested field should be reflected in the updated document.

### P11 – Update template with disjoint recurrence slots

Use two slots for the same `dayEnum`, with disjoint recurrence values:

```
{
  "templateName": {
    "en": "Disjoint Recurrence Fixed Template",
    "ar": "قالب بتكرار منفصل"
  },
  "shortCode": "FIX011",
  "templateType": 1,
  "totalWorkDurationInMinutes": 540,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [3, 4, 5],
      "startTime": "09:00:00",
      "endTime": "18:00:00"
    }
  ]
}
```

Expected: Verify the disjoint recurrence behavior already observed in your previous testing.

## 8. PATCH – Negative scenarios

Use a valid existing policy ID, except where the scenario specifically tests an invalid ID.

| Test ID | Scenario                                                   | Expected result to verify                 |
| ------- | ---------------------------------------------------------- | ----------------------------------------- |
| PN01    | Empty request body                                         | Validation failure or documented behavior |
| PN02    | Missing template name                                      | Reject if required                        |
| PN03    | Null template name                                         | Validation failure                        |
| PN04    | Empty English name                                         | Validation failure                        |
| PN05    | Missing short code                                         | Validation failure if required            |
| PN06    | Empty short code                                           | Validation failure                        |
| PN07    | Duplicate short code                                       | Duplicate validation                      |
| PN08    | Invalid template type                                      | Reject unsupported template type          |
| PN09    | Null fixedTimeSlots                                        | Reject if required                        |
| PN10    | Empty fixedTimeSlots                                       | Check empty schedule behavior             |
| PN11    | Invalid day enum 8                                         | Reject                                    |
| PN12    | Day enum 0                                                 | Reject                                    |
| PN13    | Recurrence 0                                               | Reject invalid recurrence                 |
| PN14    | Recurrence 6                                               | Reject invalid recurrence                 |
| PN15    | Negative work duration                                     | Reject                                    |
| PN16    | Decimal work duration                                      | Reject if integer required                |
| PN17    | Start time after end time                                  | Verify overnight support                  |
| PN18    | Invalid time format                                        | Reject                                    |
| PN19    | Invalid timezone                                           | Reject unsupported timezone               |
| PN20    | Wrong `isWorkingDay` type                                  | Reject                                    |
| PN21    | Duplicate overlapping day slots                            | Verify overlap validation                 |
| PN22    | Duplicate recurrence values                                | Verify validation                         |
| PN23    | Working day with zero duration                             | Business validation                       |
| PN24    | Off-day with positive duration                             | Business validation                       |
| PN25    | Incorrect total duration                                   | Verify total consistency                  |
| PN26    | Incorrect working-day count                                | Verify total consistency                  |
| PN27    | Incorrect days-off count                                   | Verify total consistency                  |
| PN28    | Non-existing template ID                                   | Not found                                 |
| PN29    | Invalid template ID format                                 | Route validation                          |
| PN30    | Template ID from another company                           | Company isolation                         |
| PN31    | Attempt to update Flexible template through Fixed endpoint | Reject or prevent cross-type update       |
| PN32    | Attempt to update deleted/superseded template              | Verify lifecycle restrictions             |
| PN33    | Attempt to update non-editable template                    | Verify edit permission                    |
| PN34    | Attempt to update default template                         | Verify default-template restrictions      |

### Important PATCH-specific checks

You previously observed a Fixed template update where:

- Version changed from `1.0` to `2.0`.
- Schedule changed.
- `_id` appeared to change.
- `LocationId` changed to a zero GUID.
- `LocationName` changed to null.

These are important regression checks.&#x20;

For every PATCH, verify:

1. Whether the existing `_id` remains stable or whether a new version document is intentionally created.
2. Version increments correctly.
3. `TenantId` and `CompanyId` remain associated with the correct tenant/company.
4. `LocationId` and `LocationName` are preserved when not changed in the request.
5. `IsDefault` is not unintentionally changed.
6. `IsSuperseded` and `Status` reflect the intended version lifecycle.
7. Old versions remain available if versioning is expected.

## 9. PATCH – Boundary Value Analysis

| Field                        | Values to test                                                     |
| ---------------------------- | ------------------------------------------------------------------ |
| `workDurationInMinutes`      | -1, 0, 1, 30, 60, 480, 540, 600, 720, 1440, 2147483647, 2147483648 |
| `dayEnum`                    | -1, 0, 1, 2, 6, 7, 8                                               |
| `recurrenceOfMonth`          | `[]`, `[1]`, `[1,2]`, `[1,2,3,4,5]`, `[0]`, `[6]`, `[-1]`          |
| `totalWorkDurationInMinutes` | -1, 0, 1, 2700, 3240, 10080, large integer                         |
| `totalWorkingDays`           | -1, 0, 1, 5, 6, 7, 8                                               |
| `totalDaysOff`               | -1, 0, 1, 2, 6, 7, 8                                               |
| `startTime`                  | `00:00:00`, `00:00:01`, `08:00:00`, `23:59:59`, invalid            |
| `endTime`                    | `00:00:00`, `00:00:01`, `17:00:00`, `23:59:59`, invalid            |
| `shortCode`                  | Empty, 1 character, normal length, maximum candidate + 1           |
| `templateName`               | Empty, one character, normal length, maximum candidate + 1         |

For `shortCode` and `templateName`, the actual maximum character lengths must be obtained from DTO validation or product requirements.

## 10. Additional business logic validation

| ID   | Business scenario                                          | Expected behavior                                    |
| ---- | ---------------------------------------------------------- | ---------------------------------------------------- |
| BL01 | All seven days working                                     | Verify if allowed                                    |
| BL02 | All seven days off                                         | Verify if allowed                                    |
| BL03 | Five working and two off                                   | Counts and totals should match                       |
| BL04 | Six working and one off                                    | Counts and totals should match                       |
| BL05 | Four working and three off                                 | Counts and totals should match                       |
| BL06 | Working duration equals time difference                    | Verify consistency                                   |
| BL07 | Working duration less than time difference                 | Verify break deduction rules                         |
| BL08 | Working duration greater than time difference              | Verify validation                                    |
| BL09 | Duplicate day with disjoint recurrence                     | Confirm accepted behavior                            |
| BL10 | Duplicate day with overlapping recurrence                  | Confirm conflict behavior                            |
| BL11 | Same start and end time                                    | Verify zero-duration handling                        |
| BL12 | Shift crosses midnight                                     | Verify overnight support                             |
| BL13 | Working slot recurrence empty                              | Verify validation                                    |
| BL14 | Off-day recurrence populated                               | Verify validation                                    |
| BL15 | Total duration does not match slot durations               | Verify server-side calculation/validation            |
| BL16 | Total working days do not match slots                      | Verify server-side calculation/validation            |
| BL17 | Total days off do not match slots                          | Verify server-side calculation/validation            |
| BL18 | Same short code in another company                         | Verify company-level uniqueness                      |
| BL19 | Same name with different short code                        | Verify duplicate-name behavior                       |
| BL20 | Update company default template                            | Verify default location seeding behavior             |
| BL21 | Update default template duration                           | Verify company default location data is synchronized |
| BL22 | Change Fixed template to Flexible through another endpoint | Verify correct subtype and slot data handling        |

## 11. MongoDB verification

Collection:

`ERP.Attendance.WorkTemplates`

### A. Find Fixed templates for a company

```
db.getCollection("ERP.Attendance.WorkTemplates").find({
    CompanyId: UUID("YOUR_COMPANY_ID"),
    TemplateType: 1,
    _t: "FixedWorkTemplate"
}).pretty()
```

### B. Find one template by ID

```
db.getCollection("ERP.Attendance.WorkTemplates").findOne({
    _id: UUID("YOUR_TEMPLATE_ID"),
    CompanyId: UUID("YOUR_COMPANY_ID")
})
```

### C. Verify complete schedule and totals

```
db.getCollection("ERP.Attendance.WorkTemplates").aggregate([
    {
        $match: {
            _id: UUID("YOUR_TEMPLATE_ID"),
            CompanyId: UUID("YOUR_COMPANY_ID")
        }
    },
    {
        $project: {
            _id: 1,
            _t: 1,
            TenantId: 1,
            CompanyId: 1,
            CompanyName: 1,
            LocationId: 1,
            LocationName: 1,
            WorkTemplateName: 1,
            ShortCode: 1,
            TemplateType: 1,
            TotalWorkDurationInMinutes: 1,
            TotalWorkingDays: 1,
            TotalDaysOff: 1,
            TimeZoneId: 1,
            Status: 1,
            Version: 1,
            IsDefault: 1,
            IsEditable: 1,
            IsDeleted: 1,
            IsSuperseded: 1,
            FixedTimeSlots: 1
        }
    }
])
```

### D. Verify working and off-day counts

```
db.getCollection("ERP.Attendance.WorkTemplates").aggregate([
    {
        $match: {
            _id: UUID("YOUR_TEMPLATE_ID"),
            CompanyId: UUID("YOUR_COMPANY_ID")
        }
    },
    {
        $unwind: "$FixedTimeSlots"
    },
    {
        $group: {
            _id: "$_id",
            WorkingSlots: {
                $sum: {
                    $cond: ["$FixedTimeSlots.IsWorkingDay", 1, 0]
                }
            },
            OffDaySlots: {
                $sum: {
                    $cond: ["$FixedTimeSlots.IsWorkingDay", 0, 1]
                }
            },
            CalculatedDuration: {
                $sum: "$FixedTimeSlots.WorkDurationInMinutes"
            }
        }
    }
])
```

### E. API-to-Mongo mapping

| API field                                | MongoDB field                            |
| ---------------------------------------- | ---------------------------------------- |
| `templateName`                           | `WorkTemplateName`                       |
| `shortCode`                              | `ShortCode`                              |
| `templateType`                           | `TemplateType`                           |
| `totalWorkDurationInMinutes`             | `TotalWorkDurationInMinutes`             |
| `totalWorkingDays`                       | `TotalWorkingDays`                       |
| `totalDaysOff`                           | `TotalDaysOff`                           |
| `timeZoneId`                             | `TimeZoneId`                             |
| `fixedTimeSlots`                         | `FixedTimeSlots`                         |
| `fixedTimeSlots[].workDurationInMinutes` | `FixedTimeSlots[].WorkDurationInMinutes` |
| `fixedTimeSlots[].dayEnum`               | `FixedTimeSlots[].DayEnum`               |
| `fixedTimeSlots[].isWorkingDay`          | `FixedTimeSlots[].IsWorkingDay`          |
| `fixedTimeSlots[].recurrenceOfMonth`     | `FixedTimeSlots[].RecurrenceOfMonth`     |
| `fixedTimeSlots[].startTime`             | `FixedTimeSlots[].StartTime`             |
| `fixedTimeSlots[].endTime`               | `FixedTimeSlots[].EndTime`               |

## 12. Test execution checklist

Fixed Work Template test progress

# 0/76

POST – Positive

Create standard five-day template

Create six-day working template

Create four-day working template

Different working hours per day

Different start and end times

Shorter working duration

All five recurrences

Selected recurrences

English and Arabic names

Different timezone

One working day and six off-days

Correct off-day configuration

POST – Negative

Empty body

Missing/null template name

Empty template name

Missing/empty short code

Duplicate short code

Invalid template type

Null fixed slots

Empty fixed slots

Invalid day enum

Invalid recurrence

Negative/decimal duration

Invalid time format

Start time after end time

Invalid timezone

Wrong isWorkingDay type

Working day with zero duration

Off-day with positive duration

Duplicate overlapping day slots

Duplicate recurrence values

PATCH – Positive

Update template name

Update working hours

Change five days to six

Change five days to four

Change off-day configuration

Update recurrence

Update one day's duration

Update multiple day schedules

Update timezone

Update all fields

Disjoint recurrence slots

PATCH – Negative

Empty body

Missing/null name

Invalid short code

Duplicate short code

Invalid template type

Null/empty fixed slots

Invalid day enum

Invalid recurrence

Negative/decimal duration

Invalid time format

Invalid timezone

Wrong working-day type

Overlapping duplicate slots

Incorrect totals

Non-existing ID

Invalid ID format

Another company's template

Flexible template through Fixed endpoint

Deleted/superseded template

Non-editable template

Default template restrictions

MongoDB and regression

Verify template subtype

Verify TemplateType = 1

Verify all fixed time slots

Verify total duration

Verify working and off-day counts

Verify recurrence values

Verify timezone

Verify company and tenant IDs

Verify location ID and name

Verify version behavior

Verify default status

Verify superseded status

Verify no unintended data changes

Reset checklist

## 13. Important validations to prioritize

For your Fixed Work Template API, I recommend prioritizing these five areas:

1. Schedule consistency: `workDurationInMinutes` must be consistent with start/end times and applicable break deductions.
2. Weekly totals: Working days + days off, and the total duration, must be consistent with the actual schedule.
3. Day and recurrence validation: Validate all seven day enum values, all five recurrence values, and duplicate/overlapping day combinations.
4. Fixed/Flexible subtype protection: A Fixed endpoint must not accidentally create or update a Flexible template.
5. Update integrity: Check versioning, IDs, company defaults, location IDs, location names, and superseded records after PATCH.

One limitation: The previous MongoDB JSON gives us the persisted Fixed template structure, but not the complete Swagger request DTO. The test payloads above are built from the known request fields; verify any additional mandatory fields against the actual Swagger schema before executing the full suite. Also, the numeric maximums and exact validation constraints are not confirmed by the saved document.



Location  id  1 : 3a24d629-0d56-a428-baa1-98493a77e614
location id  2  : 3a24d646-b3cf-b1d4-61bb-1adf094b52fc
location  id  3 : 3a24d667-0dcc-e3d1-74a3-cbee98168772

ex : https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/locationId/3a24d629-0d56-a428-baa1-98493a77e614/worktemplates/fixed


tenane name dont consider in payload


Yes. I'll generate the complete Fixed Work Template POST and PATCH payload set, including all fields in every request.

I'll use the following structure consistently:

- `tenantName`
- `templateName`
- `shortCode`
- `templateType`
- `totalWorkDurationInMinutes`
- `totalWorkingDays`
- `totalDaysOff`
- `timeZoneId`
- `fixedTimeSlots[]` with all five slot properties.

Important: These are based on the fields and stored document you previously shared. The MongoDB file confirms the persisted `FixedWorkTemplate` structure, but it does not contain the Swagger request DTO. Therefore, confirm the exact request property names against Swagger before execution.&#x20;

Sahab.ERP.Attendance.WorkTemplates.json



## 1. Common baseline values

| Field                        | Baseline                 |
| ---------------------------- | ------------------------ |
| `templateType`               | `1` (Fixed)              |
| `totalWorkingDays`           | `5`                      |
| `totalDaysOff`               | `2`                      |
| `totalWorkDurationInMinutes` | `2700`                   |
| `timeZoneId`                 | `Asia/Riyadh`            |
| Working day                  | 540 minutes, 08:00–17:00 |
| Off day                      | 0 minutes, 00:00–00:00   |

Day enum: Sunday `1`, Monday `2`, Tuesday `3`, Wednesday `4`, Thursday `5`, Friday `6`, Saturday `7`.

Recurrence: First `1`, Second `2`, Third `3`, Fourth `4`, Fifth `5`.

## 2. POST – Positive payloads

Endpoint: `POST /api/companies/{companyId}/worktemplates/fixed`

### P01 – Standard five-day template

```
{
  "tenantName": {
    "en": "Attendance",
    "ar": "Attendance"
  },
  "templateName": {
    "en": "Standard Fixed Template",
    "ar": "قالب العمل الثابت القياسي"
  },
  "shortCode": "FIX001",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### P02 – Six working days

```
{
  "tenantName": {"en":"Attendance","ar":"Attendance"},
  "templateName": {"en":"Six Day Fixed Template","ar":"قالب عمل لستة أيام"},
  "shortCode": "FIX002",
  "templateType": 1,
  "totalWorkDurationInMinutes": 3240,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":6,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### P03 – Four working days

```
{
  "tenantName": {"en":"Attendance","ar":"Attendance"},
  "templateName": {"en":"Four Day Fixed Template","ar":"قالب عمل لأربعة أيام"},
  "shortCode": "FIX003",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2160,
  "totalWorkingDays": 4,
  "totalDaysOff": 3,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

P03 is a schedule-count test candidate: verify that the first slot's off-day duration is zero; the example above should be corrected to `workDurationInMinutes: 0` for that slot before execution.

### P04 – Different working durations

```
{
  "tenantName": {"en":"Attendance","ar":"Attendance"},
  "templateName": {"en":"Different Duration Template","ar":"قالب بمدد عمل مختلفة"},
  "shortCode": "FIX004",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {"workDurationInMinutes":480,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"16:00:00"},
    {"workDurationInMinutes":510,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"16:30:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":570,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:30:00"},
    {"workDurationInMinutes":600,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

Expected total for P04 is 2700 minutes.

### P05 – Selected monthly recurrences

```
{
  "tenantName": {"en":"Attendance","ar":"Attendance"},
  "templateName": {"en":"Selected Recurrence Template","ar":"قالب بتكرار محدد"},
  "shortCode": "FIX005",
  "templateType": 1,
  "totalWorkDurationInMinutes": 1620,
  "totalWorkingDays": 3,
  "totalDaysOff": 4,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,3,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":4,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":5,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

Expected: Validate recurrence-specific total calculation; `totalWorkingDays` may not simply equal the number of slot objects when recurrence subsets are used.

### P06 – India timezone

```
{
  "tenantName": {"en":"Attendance","ar":"Attendance"},
  "templateName": {"en":"India Fixed Template","ar":"قالب العمل الهندي"},
  "shortCode": "FIX006",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Kolkata",
  "fixedTimeSlots": [
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### P07 – One-minute duration boundary

```
{
  "tenantName": {"en":"Attendance","ar":"Attendance"},
  "templateName": {"en":"One Minute Fixed Template","ar":"قالب دقيقة واحدة"},
  "shortCode": "FIX007",
  "templateType": 1,
  "totalWorkDurationInMinutes": 1,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {"workDurationInMinutes":1,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"08:01:00"},
    {"workDurationInMinutes":0,"dayEnum":2,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":3,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":4,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":5,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### P08 – Twelve-hour duration candidate

```
{
  "tenantName": {"en":"Attendance","ar":"Attendance"},
  "templateName": {"en":"Twelve Hour Fixed Template","ar":"قالب اثنتي عشرة ساعة"},
  "shortCode": "FIX008",
  "templateType": 1,
  "totalWorkDurationInMinutes": 720,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {"workDurationInMinutes":720,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"06:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":0,"dayEnum":2,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":3,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":4,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":5,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### P09 – Inactive/default-independent schedule candidate

The persisted schema does not establish a request `isActive` property for this endpoint, so I have not invented one. This scenario instead tests another schedule configuration: one working day and six off-days.

```
{
  "tenantName": {"en":"Attendance","ar":"Attendance"},
  "templateName": {"en":"Single Working Day Template","ar":"قالب يوم عمل واحد"},
  "shortCode": "FIX009",
  "templateType": 1,
  "totalWorkDurationInMinutes": 540,
  "totalWorkingDays": 1,
  "totalDaysOff": 6,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":2,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":3,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":4,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":5,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

## 3. POST – Negative payloads

Endpoint: `POST /api/companies/{companyId}/worktemplates/fixed`

All negative payloads below include the complete baseline structure. Each changes the intended validation field.

### N01 – Empty template name

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"","ar":"قالب العمل الثابت"},
  "shortCode":"FIXN001",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N02 – Null template name

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":null,
  "shortCode":"FIXN002",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N03 – Empty short code

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Empty Short Code Test","ar":"اختبار رمز فارغ"},
  "shortCode":"",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N04 – Duplicate short code

Use an already existing short code, for example `GDEGSDD` from your saved document.

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Duplicate Short Code Test","ar":"اختبار رمز مكرر"},
  "shortCode":"GDEGSDD",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N05 – Invalid template type

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Invalid Template Type","ar":"نوع قالب غير صالح"},
  "shortCode":"FIXN005",
  "templateType":999,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N06 – Invalid day enum

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Invalid Day Enum","ar":"يوم غير صالح"},
  "shortCode":"FIXN006",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":8,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N07 – Invalid recurrence

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Invalid Recurrence","ar":"تكرار غير صالح"},
  "shortCode":"FIXN007",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,6],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N08 – Negative duration

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Negative Duration","ar":"مدة سالبة"},
  "shortCode":"FIXN008",
  "templateType":1,
  "totalWorkDurationInMinutes":2159,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":-1,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N09 – Decimal duration

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Decimal Duration","ar":"مدة عشرية"},
  "shortCode":"FIXN009",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540.5,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N10 – Invalid start time

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Invalid Start Time","ar":"وقت بداية غير صالح"},
  "shortCode":"FIXN010",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"25:70:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N11 – End time earlier than start time

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"End Before Start","ar":"وقت النهاية قبل البداية"},
  "shortCode":"FIXN011",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"17:00:00","endTime":"08:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N12 – Invalid timezone

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Invalid Timezone","ar":"منطقة زمنية غير صالحة"},
  "shortCode":"FIXN012",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Invalid/Timezone",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N13 – Incorrect total duration

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Incorrect Total Duration","ar":"إجمالي مدة غير صحيح"},
  "shortCode":"FIXN013",
  "templateType":1,
  "totalWorkDurationInMinutes":2701,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N14 – Incorrect working-day count

Use the complete P01 baseline payload but set `"totalWorkingDays": 6`. Expected: verify count validation against the five working slots.

### N15 – Incorrect days-off count

Use the complete P01 baseline payload but set `"totalDaysOff": 3`. Expected: verify count validation against the two off-day slots.

### N16 – Working day with zero duration

Use the complete P01 baseline payload but set the first slot's `workDurationInMinutes` to `0` while retaining `isWorkingDay: true` and its 08:00–17:00 time range.

### N17 – Off-day with non-zero duration

Use the complete P01 baseline payload but set the Saturday slot to `workDurationInMinutes: 540`, `startTime: "08:00:00"`, `endTime: "17:00:00"` while keeping `isWorkingDay: false`.

### N18 – Duplicate overlapping day

Use the complete P01 baseline payload but add a second Monday slot (`dayEnum: 2`) with recurrence `[3,4]` that overlaps the original Monday recurrence.

### N19 – Wrong data type for `isWorkingDay`

Use the complete P01 baseline payload but change Monday's `isWorkingDay` from `true` to `"true"`.

### N20 – Wrong data type for duration

Use the complete P01 baseline payload but change Monday's `workDurationInMinutes` from `540` to `"540"`.

Expected for N14–N20: Verify validation and ensure the API does not silently save inconsistent totals or schedules. These are negative test candidates; some rules may be enforced by server-side recalculation rather than rejection.

## 4. PATCH – Positive payloads

Endpoint: `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}`

Use an existing Fixed template ID from a successful POST. The URL ID identifies the template; the body below follows the assumed request DTO and does not include a separate ID field.

### P01 – Update template name

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Updated Fixed Template","ar":"قالب العمل الثابت المحدث"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### P02 – Update working hours

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Updated Working Hours","ar":"ساعات عمل محدثة"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### P03 – Update to six working days

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Six Days Updated Template","ar":"قالب محدث لستة أيام"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":3240,
  "totalWorkingDays":6,
  "totalDaysOff":1,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":6,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### P04 – Update to four working days

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Four Days Updated Template","ar":"قالب محدث لأربعة أيام"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2160,
  "totalWorkingDays":4,
  "totalDaysOff":3,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":0,"dayEnum":1,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### P05 – Update one working day's duration

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Monday Duration Updated","ar":"مدة يوم الاثنين محدثة"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2640,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":480,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"16:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### P06 – Update timezone

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"India Timezone Updated Template","ar":"قالب محدث بتوقيت الهند"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Kolkata",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"09:00:00","endTime":"18:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### P07 – Update recurrence

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Updated Recurrence Template","ar":"قالب تكرار محدث"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,3,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### P08 – Update all fields

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Fully Updated Fixed Template","ar":"قالب ثابت محدث بالكامل"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2640,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":480,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"16:00:00"},
    {"workDurationInMinutes":510,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"16:30:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":570,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:30:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

## 5. PATCH – Negative payloads

For these cases, use the same existing template ID in the URL. Each JSON body includes the complete request structure.

### N01 – Null template name

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":null,
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N02 – Invalid template type

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Invalid Type Update","ar":"تحديث نوع غير صالح"},
  "shortCode":"FIX001",
  "templateType":999,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N03 – Invalid day enum

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Invalid Day Update","ar":"تحديث يوم غير صالح"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":0,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N04 – Negative duration

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Negative Duration Update","ar":"تحديث مدة سالبة"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2159,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":-1,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N05 – Decimal duration

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Decimal Duration Update","ar":"تحديث مدة عشرية"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540.5,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N06 – Invalid recurrence

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Invalid Recurrence Update","ar":"تحديث تكرار غير صالح"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,6],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N07 – Incorrect total duration

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Incorrect Total Duration Update","ar":"تحديث إجمالي مدة غير صحيح"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2701,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Asia/Riyadh",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N08 – Invalid timezone

```
{
  "tenantName":{"en":"Attendance","ar":"Attendance"},
  "templateName":{"en":"Invalid Timezone Update","ar":"تحديث منطقة زمنية غير صالحة"},
  "shortCode":"FIX001",
  "templateType":1,
  "totalWorkDurationInMinutes":2700,
  "totalWorkingDays":5,
  "totalDaysOff":2,
  "timeZoneId":"Invalid/Timezone",
  "fixedTimeSlots":[
    {"workDurationInMinutes":540,"dayEnum":1,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":2,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":3,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":4,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":540,"dayEnum":5,"isWorkingDay":true,"recurrenceOfMonth":[1,2,3,4,5],"startTime":"08:00:00","endTime":"17:00:00"},
    {"workDurationInMinutes":0,"dayEnum":6,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"},
    {"workDurationInMinutes":0,"dayEnum":7,"isWorkingDay":false,"recurrenceOfMonth":[],"startTime":"00:00:00","endTime":"00:00:00"}
  ]
}
```

### N09 – Non-existing template ID

Use a validly formatted but non-existing GUID in the URL:

```
PATCH /api/companies/{companyId}/worktemplates/fixed/00000000-0000-0000-0000-000000000001
```

Use P01's complete body.

Expected: Not found; no new record should be created.

### N10 – Invalid template ID format

```
PATCH /api/companies/{companyId}/worktemplates/fixed/invalid-id
```

Use P01's complete body.

Expected: Route/ID validation error.

### N11 – Company mismatch

Use a valid Fixed template ID from Company B but pass Company A's ID in the URL.

Use P01's complete body.

Expected: The API must not update another company's template.

### N12 – Flexible template ID passed to Fixed endpoint

Use an existing Flexible template ID in the Fixed PATCH URL.

Use P01's complete body.

Expected: The API must reject the cross-template-type update or otherwise prevent modification of the Flexible template.

## 6. Boundary payload values

Use these values individually in the complete P01 request body. Keep all other fields and all seven slots unchanged.

| Test ID | Field                        | Value         |
| ------- | ---------------------------- | ------------- |
| BVA01   | `workDurationInMinutes`      | -1            |
| BVA02   | `workDurationInMinutes`      | 0             |
| BVA03   | `workDurationInMinutes`      | 1             |
| BVA04   | `workDurationInMinutes`      | 480           |
| BVA05   | `workDurationInMinutes`      | 540           |
| BVA06   | `workDurationInMinutes`      | 1440          |
| BVA07   | `workDurationInMinutes`      | 2147483647    |
| BVA08   | `workDurationInMinutes`      | 2147483648    |
| BVA09   | `dayEnum`                    | 0             |
| BVA10   | `dayEnum`                    | 1             |
| BVA11   | `dayEnum`                    | 7             |
| BVA12   | `dayEnum`                    | 8             |
| BVA13   | `recurrenceOfMonth`          | `[]`          |
| BVA14   | `recurrenceOfMonth`          | `[1]`         |
| BVA15   | `recurrenceOfMonth`          | `[1,2,3,4,5]` |
| BVA16   | `recurrenceOfMonth`          | `[0]`         |
| BVA17   | `recurrenceOfMonth`          | `[6]`         |
| BVA18   | `totalWorkingDays`           | 0             |
| BVA19   | `totalWorkingDays`           | 7             |
| BVA20   | `totalWorkingDays`           | 8             |
| BVA21   | `totalDaysOff`               | 0             |
| BVA22   | `totalDaysOff`               | 7             |
| BVA23   | `totalDaysOff`               | 8             |
| BVA24   | `totalWorkDurationInMinutes` | 0             |
| BVA25   | `totalWorkDurationInMinutes` | 2700          |
| BVA26   | `totalWorkDurationInMinutes` | 10080         |

For every BVA test, change the matching field in the full JSON payload and retain the remaining values. These are test inputs, not confirmed API maximums.

## 7. Important corrections before execution

- P03 correction: For the Sunday off-day slot, use `workDurationInMinutes: 0`, not 540. The off-day must have zero duration.
- P05 recurrence: The recurrence array `[1,3,5]` may affect how often the day is counted. Confirm how your backend calculates `totalWorkingDays` and `totalWorkDurationInMinutes` for recurrence-based schedules.
- PATCH body: If Swagger requires an `id`, add the existing template ID to every PATCH body and ensure it matches the URL ID.
- Tenant field: `tenantName` is present in your saved document. Confirm that it is writable in the API request rather than populated server-side.

## 8. MongoDB verification after POST and PATCH

```
db.getCollection("ERP.Attendance.WorkTemplates").findOne({
    _id: UUID("YOUR_TEMPLATE_ID"),
    CompanyId: UUID("YOUR_COMPANY_ID")
})
```

Verify:

- `_t` contains `FixedWorkTemplate`.
- `TemplateType` is `1`.
- `FixedTimeSlots` matches the request.
- `TotalWorkDurationInMinutes` matches the schedule.
- `TotalWorkingDays` and `TotalDaysOff` are correct.
- `TimeZoneId` is correct.
- `Version`, `_id`, `LocationId`, and `LocationName` behave correctly after PATCH.

The saved collection confirms that updates can create versioned/superseded documents, so check the old and new records rather than assuming the original document is overwritten.&#x20;

Sahab.ERP.Attendance.WorkTemplates.json



Final recommendation: Before running this entire suite, compare the assumed request names (`templateName`, `tenantName`, `templateType`) with the actual Swagger DTO. The database's `WorkTemplateName` and `TemplateType` names are confirmed storage fields, not proof of the exact API JSON property names.




now testing shfit & raotion -> Regular shift (not a default work temapalte) with location assogned


I will prove dthe DB information edit and updted , delenet only do valaidate collection details

DB : 10.1.0.4:27018

DEV


Sahab

ERP.Attendance.WorkTemplates

{
  CompanyId: UUID(
    "3a249871-7a8d-dec5-2d72-47795dd2662d"
  )
}


validte dthe request  post and patch api value ister db verify 

note: donat edit , updte and delte db

know bug : TenantName: Object (2)
en: "Attendance"
ar: "Attendance" detail si know dont consider

</USER_REQUEST>
<ADDITIONAL_METADATA>
The current local time is: 2026-11-10T13:11:02+05:30.
</ADDITIONAL_METADATA>