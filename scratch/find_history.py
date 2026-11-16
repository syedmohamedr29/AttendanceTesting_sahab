import os, glob

matches = glob.glob('scratch/*work*assignment*.py') + glob.glob('scratch/*excel*.py')
for m in matches:
    print(m)
