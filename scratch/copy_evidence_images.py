import shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

src_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded"
artifact_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
workspace_img_dir = r"D:\Code\Attendance Testing\defect_evidence"

os.makedirs(workspace_img_dir, exist_ok=True)

image_mapping = {
    "media_1793083322021_d409fe74.png": "evidence_01_worktemplates_created_with_placeholder.png",
    "media_1793083327020_973443f3.png": "evidence_02_companiesmaster_checklist_false.png",
    "media_1793083332939_7c778928.png": "evidence_03_tenantname_placeholder_detail.png",
    "media_1793083336786_3fcf9fc4.png": "evidence_04_benchmark_createdby_composite_object.png",
    "media_1793083341681_bfe092b8.png": "evidence_05_createdby_plain_email_highlighted.png"
}

for src_name, target_name in image_mapping.items():
    src_path = os.path.join(src_dir, src_name)
    art_path = os.path.join(artifact_dir, target_name)
    ws_path = os.path.join(workspace_img_dir, target_name)
    
    shutil.copy2(src_path, art_path)
    shutil.copy2(src_path, ws_path)
    print(f"Copied {src_name} -> {target_name}")

print("All defect evidence images successfully copied to artifact and workspace directories!")

