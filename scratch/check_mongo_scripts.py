import sys
import glob

sys.stdout.reconfigure(encoding='utf-8')

for f in glob.glob('scratch/*.py'):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
        if 'pymongo' in content or 'mongodb' in content.lower():
            print(f"Found mongo in {f}")

