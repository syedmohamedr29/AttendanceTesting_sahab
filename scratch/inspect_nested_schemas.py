import json

with open('scratch/attendance2_swagger_live.json', 'r', encoding='utf-8') as f:
    sw = json.load(f)

schemas = sw.get('components', {}).get('schemas', {})

target_schemas = [
    'ShiftRotationDto', 'UpdateShiftRotationDto', 'RotationPlanDto', 'RotationStepDto',
    'RotationTeamDto', 'RotationPatternType', 'AddRotationEmployeesDto', 'EditRotationMemberPeriodDto',
    'MoveEmployeeDto', 'MoveRotationMemberTeamDto', 'RotationWorkTemplateDto', 'UpdateRotationWorkTemplateDto',
    'RotationTimeSlotDto', 'WorkTemplateType'
]

for sname in target_schemas:
    sdef = schemas.get(sname, {})
    print(f"=== Schema: {sname} ===")
    print("  Type:", sdef.get('type'))
    if 'enum' in sdef:
        print("  Enum values:", sdef.get('enum'))
    reqs = sdef.get('required', [])
    print("  Required:", reqs)
    props = sdef.get('properties', {})
    for p, pdata in props.items():
        pref = pdata.get('$ref') or pdata.get('type')
        items = pdata.get('items', {}).get('$ref') or pdata.get('items', {}).get('type')
        fmt = pdata.get('format', '')
        print(f"    - {p}: type={pref} items={items} format={fmt}")
