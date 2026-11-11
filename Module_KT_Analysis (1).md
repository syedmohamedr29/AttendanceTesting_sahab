# Developer KT Analysis --- Shifts & Rotation

> **Source:** Microsoft Teams recording, "Call with Shivam and 1 other",
> recorded 20 October 2026\
> **Recording length:** approximately 54 minutes 40 seconds\
> **Analysis status:** Visual review of sampled video frames. The
> recording's audio has not been transcribed in this document, so spoken
> explanations, exact business rules, API names, and backend details are
> not treated as confirmed facts. Items marked **Confirm in KT** need
> validation against the developer's explanation.

## 1. Module identification

The visible application is SahabPayroll. The main area shown repeatedly
is **Shifts & Rotation**, including pages or flows labelled:

-   Regular & Rotation Plans
-   Regular & Rotation Templates
-   Create New Rotation Work Plan
-   Teams & Rotation
-   Add Employees
-   Scheduler
-   Work Schedule
-   Attendance Policies / Attendance Log

The recording also briefly shows work-schedule configuration and
holiday-plan screens. Confirm with the developer whether these are part
of the same KT scope or supporting dependencies.

## 2. Purpose and scope to confirm

Based on the visible screens, this module appears to configure work
shifts and work schedules, define reusable work templates, create
rotation plans, and associate employees or teams with plans.

**Confirm in KT:** - The official module name and business objective. -
Which user roles can configure templates, create plans, assign
employees, publish schedules, and edit existing schedules. - Whether the
module supports fixed, flexible-hours, and split-interval schedules in
production. - Whether rotation plans are used for attendance
calculation, payroll, or both. - The boundary between Work Schedule,
Shifts & Rotation, Attendance Policies, and Holiday Plans.

## 3. Visible screens and apparent workflow

The following is a screen-based workflow hypothesis, not a verified
business sequence. Confirm the exact order with the developer.

1.  **Configure a work schedule / shift**
    -   A form visibly contains a shift type or work-schedule type.
    -   Options shown include **Fixed**, **Flexible**, and **Split
        Shift**.
    -   Examples of labels include "Work Schedule - Fixed", "Work
        Schedule - Flexible hours", and "Work Schedule - split
        intervals".
    -   One screen includes an option resembling "Copy first day to all
        working days"; verify its exact meaning and behavior.
2.  **Create or maintain reusable templates**
    -   A page labelled **Regular & Rotation Templates** is visible.
    -   Fields include **Work Template Name**, **Template Code**, and
        **Shift Type**.
    -   A success notification appears to indicate that a company work
        template was updated.
    -   Confirm whether templates are company-wide, whether codes must
        be unique, and whether a template can be edited after
        assignment.
3.  **Create a rotation work plan**
    -   A page labelled **Create New Rotation Work Plan** is visible.
    -   The UI contains a **Rotation Pattern** section and a **Rotation
        Pattern Summary**.
    -   Visible pattern descriptions include employees rotating shifts
        alternatively and employees rotating shifts in uneven cycles.
    -   Shift-sequence configuration is also visible.
    -   Confirm the exact rotation algorithms, sequence rules, cycle
        length, and how rest days are represented.
4.  **Configure teams and shifts**
    -   A **Teams & Rotation** step or section is visible.
    -   Shift labels such as **Morning Shift** and **Evening Shift**
        appear in the UI.
    -   A summary shows a duration-like value for a shift (for example,
        "45h/week" appears in sampled frames); verify the actual
        calculation and whether this is illustrative or saved data.
    -   Confirm whether teams are mandatory and whether employees can
        belong to more than one team or rotation plan.
5.  **Add employees**
    -   A screen labelled **Add Employees** contains the instruction
        "Select the employees to add".
    -   Confirm eligibility rules, bulk-selection behavior, duplicate
        assignment behavior, and what happens when an employee joins or
        leaves a team.
6.  **Review / schedule**
    -   A **Scheduler** page and a **Regular & Rotation Plans** page are
        visible.
    -   A default work-plan entry is visible.
    -   Confirm whether the scheduler generates dates automatically,
        whether a plan must be published, and how changes affect
        already-generated schedules.

## 4. Visible configuration types

  -----------------------------------------------------------------------
  Configuration           Evidence from visible   Details requiring
                          UI                      confirmation
  ----------------------- ----------------------- -----------------------
  Fixed schedule          "Work Schedule - Fixed" Start/end time, breaks,
                          and "Fixed" are visible working days, overnight
                                                  shifts, grace periods

  Flexible hours          "Work Schedule -        Required hours, allowed
                          Flexible hours" and     arrival/departure
                          "Flexible" are visible  window, overtime
                                                  calculation

  Split shift             "Work Schedule - split  Number of intervals,
                          intervals" and "Split   gap between intervals,
                          Shift" are visible      interval validation

  Rotation pattern        "Create New Rotation    Pattern types, cycle
                          Work Plan" and          length, rotation start
                          "Rotation Pattern" are  date, sequence rules
                          visible                 

  Employee assignment     "Add Employees" is      Eligibility, conflicts,
                          visible                 duplicate assignment,
                                                  effective dates

  Attendance policy       "Attendance Policies"   Relationship to
                          is visible in           schedules and which
                          navigation/screens      rules override others

  Holiday plan            "List of Holiday Plans" How holidays interact
                          and "Holiday Plan       with scheduled shifts
                          Details" are visible in and rotations
                          sampled frames          
  -----------------------------------------------------------------------

## 5. Business rules to document with the developer

Do not assume the following rules are implemented until confirmed.

-   **Schedule validation:** Are start time, end time, workdays, break
    duration, and total hours mandatory?
-   **Time boundaries:** Can a shift end on the next calendar day? How
    are overnight shifts handled?
-   **Fixed schedules:** Does copying the first day replicate times,
    breaks, and other settings to every working day?
-   **Flexible schedules:** Is there a minimum number of hours, a
    core-hours window, or a grace period?
-   **Split shifts:** Must intervals be non-overlapping and
    chronological? Is a minimum break between intervals required?
-   **Rotation patterns:** How are sequence length, cycle repetition,
    uneven cycles, and rest days represented?
-   **Effective dates:** Can a plan start in the past? What happens when
    a plan is changed mid-cycle?
-   **Employee conflicts:** Can an employee have overlapping plans or
    more than one active assignment?
-   **Attendance integration:** Which schedule is used to determine late
    arrival, early departure, absence, and overtime?
-   **Holiday handling:** Does a holiday override a scheduled shift, or
    does the shift remain visible with a holiday status?
-   **Permissions and audit:** Who can create, edit, delete, assign, or
    publish plans? Are changes audited?
-   **Localization:** Are date/time display, language, time zone, and
    regional settings handled consistently?

## 6. API and backend details

The sampled video frames do not provide enough reliable information to
identify API routes, HTTP methods, DTO names, service names, or response
schemas. Do not invent these values.

Capture the following during follow-up with the developer:

  ----------------------------------------------------------------------------
  Operation      HTTP method    Request / DTO  Expected result  Service /
                 and endpoint                                   dependency
  -------------- -------------- -------------- ---------------- --------------
  Create work    Confirm in KT  Confirm in KT  Confirm in KT    Confirm in KT
  template                                                      

  Update work    Confirm in KT  Confirm in KT  UI shows an      Confirm in KT
  template                                     update-success   
                                               notification in  
                                               a sampled frame; 
                                               verify API       
                                               behavior         

  Retrieve       Confirm in KT  Confirm in KT  Confirm in KT    Confirm in KT
  templates                                                     

  Create         Confirm in KT  Confirm in KT  Confirm in KT    Confirm in KT
  rotation plan                                                 

  Update         Confirm in KT  Confirm in KT  Confirm in KT    Confirm in KT
  rotation plan                                                 

  Assign         Confirm in KT  Confirm in KT  Confirm in KT    Confirm in KT
  employees                                                     

  Retrieve       Confirm in KT  Confirm in KT  Confirm in KT    Confirm in KT
  scheduler /                                                   
  plan view                                                     

  Retrieve       Confirm in KT  Confirm in KT  Confirm in KT    Confirm in KT
  attendance                                                    
  policy /                                                      
  holiday plan                                                  
  ----------------------------------------------------------------------------

For every endpoint, collect: authentication and authorization
requirements, path/query parameters, mandatory fields, enum values,
validation errors, status codes, response schema, tenant/company scope,
and side effects.

## 7. Database and data consistency

No database schema or collection names can be confirmed from the sampled
UI frames. Ask the developer to show the relevant
entity/collection/table and explain how records relate.

Record: - Work-template entity and unique key (including company/tenant
scope). - Shift and interval entities. - Rotation-plan entity,
sequence/pattern representation, and cycle dates. - Employee-to-plan or
team-to-plan assignment records. - Effective start/end dates and
active/inactive status. - Audit fields and soft-delete behavior. - How
schedule changes propagate to generated schedules and attendance
records. - Whether updates are synchronous, event-driven, or handled by
background jobs.

## 8. QA test scenarios

These are recommended tests derived from the visible functionality.
Expected behavior must be aligned with confirmed requirements.

### 8.1 Work schedule and template --- positive tests

-   [ ] Create a valid fixed work schedule.
-   [ ] Create a valid flexible-hours schedule.
-   [ ] Create a valid split-shift schedule with multiple intervals.
-   [ ] Save a template with valid name, code, and shift type.
-   [ ] Edit a template and verify the updated values after reload.
-   [ ] Verify that the UI success notification corresponds to a
    successful persisted update.
-   [ ] Verify company/tenant isolation for templates.

### 8.2 Validation and negative tests

-   [ ] Submit without a required template name or code.
-   [ ] Submit a duplicate template code within the applicable scope.
-   [ ] Enter an invalid or unsupported shift type.
-   [ ] Set an end time earlier than a start time and verify
    overnight-shift rules.
-   [ ] Configure overlapping split intervals.
-   [ ] Configure zero or negative duration where the UI/API permits
    entry.
-   [ ] Attempt to edit or delete a template without permission.
-   [ ] Simulate an API error and verify the UI does not show a false
    success notification.

### 8.3 Rotation plan tests

-   [ ] Create a plan using each supported rotation pattern.
-   [ ] Verify the shift sequence and cycle repeat as specified.
-   [ ] Verify uneven-cycle behavior against a developer-provided
    example.
-   [ ] Verify rest days, holidays, and overnight shifts within a
    rotation.
-   [ ] Verify the plan's effective start date and cycle boundary.
-   [ ] Change a plan after employees have been assigned and verify the
    agreed impact.
-   [ ] Attempt to create a plan with a missing pattern, empty sequence,
    or invalid sequence.
-   [ ] Verify behavior when two plans overlap for the same employee.

### 8.4 Employee assignment tests

-   [ ] Add one eligible employee.
-   [ ] Add multiple employees using bulk selection.
-   [ ] Attempt to add the same employee twice.
-   [ ] Attempt to assign an ineligible, inactive, or terminated
    employee.
-   [ ] Verify employee assignment across different companies/tenants.
-   [ ] Remove or transfer an employee and verify the effective date and
    historical schedule behavior.

### 8.5 Scheduler and integration tests

-   [ ] Verify the scheduler shows the correct shift for each date in a
    rotation cycle.
-   [ ] Verify schedule and attendance behavior for holidays and rest
    days.
-   [ ] Verify attendance calculations for late arrival, early
    departure, and overtime against the configured schedule.
-   [ ] Verify time-zone and daylight-saving behavior if supported.
-   [ ] Verify that API and UI show consistent template, plan, and
    assignment data.
-   [ ] Verify that a failed downstream operation does not leave partial
    or inconsistent assignments.
-   [ ] Verify concurrent edits and duplicate requests.
-   [ ] Verify audit history for create, update, assignment, and
    deletion actions.

## 9. Automation opportunities

For a Playwright + TypeScript/Python or API automation framework,
consider:

-   **UI:** Template creation/editing, shift-type selection,
    rotation-plan wizard, employee assignment, scheduler rendering,
    validation messages.
-   **API:** CRUD contract tests, DTO validation, authorization,
    duplicate codes, invalid rotation patterns, and tenant isolation.
-   **Database:** Verify persisted template/plan/assignment data and
    ensure updates do not create duplicates.
-   **Integration:** Validate that schedule changes affect the scheduler
    and downstream attendance calculations as specified.
-   **Regression:** Keep stable test data for fixed, flexible, split,
    and rotation schedules.
-   **Test data:** Use unique template codes, controlled effective
    dates, known employee sets, and deterministic rotation patterns.
-   **Reliability:** Avoid relying only on fixed sleeps; wait for
    explicit UI states and verify the final persisted result.

## 10. Questions for the developer

1.  What exact business problem does Shifts & Rotation solve, and what
    is in/out of scope for this KT?
2.  What is the complete end-to-end flow from creating a shift to seeing
    it in the scheduler?
3.  What are the exact meanings of Fixed, Flexible, and Split Shift?
4.  What are the supported rotation patterns? Please give a date-by-date
    example for each.
5.  What rules apply to overnight shifts, breaks, weekly hours, rest
    days, and holidays?
6.  What happens when a template or rotation plan is edited after
    employees are assigned?
7.  Can an employee have more than one active work plan? How are
    conflicts resolved?
8.  Which APIs and DTOs are used for templates, rotation plans, employee
    assignments, and scheduler data?
9.  Which database entities/collections store these records, and how are
    they related?
10. Are any background jobs, events, or downstream services involved?
11. How does this module integrate with Attendance Policies, Attendance
    Log, and payroll?
12. What permissions, audit rules, and tenant-isolation checks apply?
13. Which known bugs, edge cases, or regression tests should QA
    prioritize?

## 11. Glossary

  -----------------------------------------------------------------------
  Term                                Working meaning; confirm with
                                      developer
  ----------------------------------- -----------------------------------
  Work schedule                       Configuration describing expected
                                      working times

  Shift template                      Reusable definition for a type of
                                      shift or work schedule

  Rotation plan                       Plan that assigns shifts according
                                      to a repeating sequence or pattern

  Rotation pattern                    Rule defining how shifts change
                                      over a cycle

  Scheduler                           UI that displays or manages planned
                                      work by date/employee/team

  Effective date                      Date from which a configuration or
                                      assignment applies

  Attendance policy                   Rules used to interpret attendance
                                      against a planned schedule
  -----------------------------------------------------------------------

## 12. Evidence and limitations

-   The recording is approximately 54 minutes and 40 seconds long.
-   Sampled video frames show SahabPayroll pages related to Shifts &
    Rotation, work schedules, templates, rotation-plan setup, teams,
    employee selection, scheduler, attendance policies, and holiday
    plans.
-   The UI appears to include a template-update success notification and
    fixed/flexible/split shift options.
-   **Audio transcription was not available in this analysis pass.**
    Consequently, this document does not claim to capture everything the
    developer said. API routes, exact validation rules, database schema,
    service names, and spoken explanations remain unverified.
-   Treat inferred workflows and proposed test scenarios as a starting
    point, not as confirmed product requirements.

## 13. KT completion checklist

-   [ ] Confirm module scope and terminology.
-   [ ] Document the full workflow from template setup to employee
    schedule.
-   [ ] Capture API routes, DTOs, examples, and error responses.
-   [ ] Capture database entities and relationships.
-   [ ] Confirm rotation calculations with worked examples.
-   [ ] Confirm attendance, holiday, and payroll integration behavior.
-   [ ] Validate the proposed scenarios with the developer.
-   [ ] Link known defects and existing automated tests.
