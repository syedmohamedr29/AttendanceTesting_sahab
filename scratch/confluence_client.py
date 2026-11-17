import requests
import json
import os
import sys

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'confluence_config.json')

class ConfluenceClient:
    def __init__(self, config_path=CONFIG_FILE):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found at: {config_path}. Please create it from template.")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
            
        self.base_url = self.config.get('confluence_url', '').rstrip('/')
        self.auth_type = self.config.get('auth_type', 'cloud').lower()
        self.email = self.config.get('email', '')
        self.api_token = self.config.get('api_token', '')
        
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        if self.auth_type == 'cloud':
            self.session.auth = (self.email, self.api_token)
        else: # bearer token / PAT
            self.session.headers.update({
                'Authorization': f"Bearer {self.api_token}"
            })

    def test_connection(self):
        """Tests connectivity to Confluence REST API."""
        url = f"{self.base_url}/rest/api/user/current"
        print(f"Testing connection to: {url} ...", flush=True)
        try:
            r = self.session.get(url, timeout=15)
            if r.status_code == 200:
                user = r.json()
                print(f"[SUCCESS] Connected as: {user.get('displayName')} ({user.get('email') or user.get('username')})", flush=True)
                return True, user
            else:
                # Try fallback for some Confluence server setups
                url_fallback = f"{self.base_url}/rest/api/space?limit=1"
                r_fb = self.session.get(url_fallback, timeout=15)
                if r_fb.status_code == 200:
                    print(f"[SUCCESS] Connected successfully to Confluence API via space endpoint.", flush=True)
                    return True, r_fb.json()
                print(f"[FAILED] HTTP {r.status_code}: {r.text}", flush=True)
                return False, r.text
        except Exception as e:
            print(f"[ERROR] Connection exception: {e}", flush=True)
            return False, str(e)

    def get_page(self, page_id):
        """Fetches page details including current version and storage HTML body."""
        url = f"{self.base_url}/rest/api/content/{page_id}?expand=body.storage,version,space"
        r = self.session.get(url, timeout=20)
        if r.status_code == 200:
            return r.json()
        else:
            raise RuntimeError(f"Failed to fetch page {page_id}: HTTP {r.status_code} - {r.text}")

    def update_page(self, page_id, title, storage_html_content, version_comment="Automated QA Defect Log Update"):
        """Updates a Confluence page using storage format XHTML."""
        page = self.get_page(page_id)
        current_version = page['version']['number']
        new_version = current_version + 1
        
        payload = {
            "id": str(page_id),
            "type": "page",
            "title": title or page.get('title'),
            "space": {"key": page['space']['key']},
            "body": {
                "storage": {
                    "value": storage_html_content,
                    "representation": "storage"
                }
            },
            "version": {
                "number": new_version,
                "message": version_comment
            }
        }
        
        url = f"{self.base_url}/rest/api/content/{page_id}"
        r = self.session.put(url, json=payload, timeout=30)
        if r.status_code == 200:
            print(f"[SUCCESS] Page {page_id} updated to version {new_version}.", flush=True)
            return r.json()
        else:
            raise RuntimeError(f"Failed to update page {page_id}: HTTP {r.status_code} - {r.text}")

if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        print(f"Please create '{CONFIG_FILE}' with your Confluence credentials first.")
        sys.exit(1)
        
    client = ConfluenceClient()
    ok, info = client.test_connection()
    if ok:
        print("Confluence Client is ready!")
    else:
        print("Confluence connection failed.")
