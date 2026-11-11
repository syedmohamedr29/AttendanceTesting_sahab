import shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

src_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.user_uploaded"
art_dir = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc"
ws_dir = r"D:\Code\Attendance Testing\defect_evidence"

img_map = {
    "media_1793086102921_98b4cefb.png": "ui_flexi_per_day_screen.png",
    "media_1793086109620_2830b26d.png": "ui_flexi_per_day_days_list.png",
    "media_1793086123363_35e4792c.png": "ui_flexi_per_week_screen.png",
    "media_1793086139676_9d4495c5.png": "ui_flexi_per_day_recurrence_open.png"
}

for s, d in img_map.items():
    sp = os.path.join(src_dir, s)
    if os.path.exists(sp):
        shutil.copy2(sp, os.path.join(art_dir, d))
        shutil.copy2(sp, os.path.join(ws_dir, d))
        print(f"Copied {s} -> {d}")

print("Copied flexi UI images!")

