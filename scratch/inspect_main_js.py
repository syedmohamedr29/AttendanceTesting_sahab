import requests
import re
import json

r = requests.get('https://sp.dev.zoolwork.com/main.2c0e557f753c3386.js')
text = r.text

print("Length of main.js:", len(text))
matches = re.findall(r'.{0,100}auth8\.dev\.zoolwork\.com.{0,200}', text)
for m in matches[:10]:
    print("Match auth8:", m)

matches_client = re.findall(r'.{0,50}clientId.{0,100}', text)
for m in matches_client[:10]:
    print("Match clientId:", m)
