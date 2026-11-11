import pymongo, uuid, sys
from bson.binary import Binary, UuidRepresentation

sys.stdout.reconfigure(encoding='utf-8')
client = pymongo.MongoClient('mongodb://10.1.0.4:27018/?directConnection=true', serverSelectionTimeoutMS=5000)
db = client['Sahab']
col = db['ERP.Attendance.Policies']

att7_bin = Binary.from_uuid(uuid.UUID('3a249870-c8ae-b3dc-1b8d-c44efad14f89'), UuidRepresentation.STANDARD)
docs = list(col.find({'CompanyId': att7_bin}))
print('Total docs in Attendance 7:', len(docs))

# Defect evidence IDs that MUST NOT be deleted
protected_ids = {
    # DEFECT-20261106-04 Overtime evidence
    'aac01ebb-1ca6-426b-8711-dd808aaf3b7b',
    '7f710344-3c75-4dd0-ad31-bb42c84acb43',
    '44641568-e535-47d8-b2f8-cee051360ec4',
    'c5dcdaa3-05d4-4c9a-ae21-13f586f55063',
    '45f7d0ee-fc27-4f93-898a-8d0d12d01348',
    '42d55366-a5e6-42b4-86d1-3c141942d4b4',
    # Overtime baselines
    'ac0d2212-34c2-4ff5-81a1-7d7de0c85627',
    '9796b311-f9a2-4a5c-8719-1abe17d16e8d',
    'f307f0f3-e2e7-478a-939b-caccdf7f6da7',
    'a3104a72-453d-4a26-9771-b8b470971859',
    # DEFECT-20261106-05 & 06 Break evidence & baselines
    '46675ad6-978d-4c02-b676-73193e48c32b',
    'b48d4da6-36ca-4731-b6e2-d52e761841da',
    'd5abd499-041c-4f92-ad77-143516c01660',
    '8891c484-ace3-4791-9c6e-b1b4d646d906',
    # Grace baseline
    'd9c1e312-bba0-4a93-ab9d-e8845aa13180'
}

candidates_for_removal = []
for d in docs:
    u_str = str(uuid.UUID(bytes=d['_id']))
    if u_str not in protected_ids:
        candidates_for_removal.append((d['_id'], u_str, d.get('Type'), d.get('Name')))

print(f"Total candidates available for removal: {len(candidates_for_removal)}")
for raw_id, u_str, ptype, name in candidates_for_removal:
    print(f"  Candidate: {u_str} | Type: {ptype} | Name: {name}")

# Remove up to 10 candidates to leave room for testing
to_delete = [item[0] for item in candidates_for_removal[:10]]
if to_delete:
    res = col.delete_many({'_id': {'$in': to_delete}})
    print(f"Successfully deleted {res.deleted_count} documents.")

current_count = col.count_documents({'CompanyId': att7_bin})
print(f"Updated Attendance 7 Policy Count: {current_count} (Cap: 30, Free Slots: {30 - current_count})")
