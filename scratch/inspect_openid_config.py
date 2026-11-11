import requests
import json

r = requests.get('https://auth8.dev.zoolwork.com/.well-known/openid-configuration')
data = r.json()
print("Grant types supported:", data.get("grant_types_supported"))
print("Scopes supported:", data.get("scopes_supported"))
print("Token endpoint:", data.get("token_endpoint"))
