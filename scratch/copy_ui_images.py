import shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

src_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded"
artifact_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
ws_dir = r"D:\Code\Attendance Testing\defect_evidence"

img_map = {
    "media_1793085083523_9859209a.png": "ui_fixed_schedule_grid.png",
    "media_1793085083507_2431958c.png": "ui_recurrence_dropdown_menu.png",
    "media_1793085083521_840885ce.png": "ui_recurrence_dropdown_menu_detail.png"
}

for s, d in img_map.items():
    sp = os.path.join(src_dir, s)
    if os.path.exists(sp):
        shutil.copy2(sp, os.path.join(artifact_dir, d))
        shutil.copy2(sp, os.path.join(ws_dir, d))
        print(f"Copied {s} -> {d}")

print("Copied UI images!")

