import os
import shutil

artifact_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
workspace_img_dir = r"D:\Code\Attendance Testing\defect_evidence"
os.makedirs(workspace_img_dir, exist_ok=True)

imgs = [
    (r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded\media_1794295602441_e86c3128.png", "evidence_54_user_post_fixed_location_swagger.png"),
    (r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded\media_1794295602447_39c19ceb.png", "evidence_54_user_patch_fixed_location_swagger.png"),
    (r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded\media_1794295602449_4cd907c7.png", "evidence_54_user_ui_regular_shift_locations.png"),
    (r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded\media_1794295650745_eaaed3d1.jpg", "evidence_54_user_mongodb_patch_location_wiped_createdat.jpg")
]

for src, name in imgs:
    if os.path.exists(src):
        dst_ws = os.path.join(workspace_img_dir, name)
        dst_art = os.path.join(artifact_dir, name)
        shutil.copyfile(src, dst_ws)
        shutil.copyfile(src, dst_art)
        print(f"Copied {name} to workspace and artifact directory.")
    else:
        print(f"Source not found: {src}")
