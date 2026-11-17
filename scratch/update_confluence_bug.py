import requests
import json
import re

CONFIG_FILE = 'scratch/confluence_config.json'

def append_bugs_to_page(bugs_list):
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    auth = (cfg['email'], cfg['api_token'])
    base_url = cfg['confluence_url']
    page_id = cfg['page_id']

    # 1. Fetch current page
    r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version,space", auth=auth)
    if r.status_code != 200:
        raise RuntimeError(f"Failed to fetch page {page_id}: {r.text}")

    page_data = r.json()
    current_version = page_data['version']['number']
    title = page_data['title']
    space_key = page_data['space']['key']
    storage_value = page_data['body']['storage']['value']

    # 2. Build rows HTML
    rows_html = ""
    for b in bugs_list:
        sno = b.get('sno', '')
        date = b.get('date', '')
        segment = b.get('segment', '')
        severity = b.get('severity', '')
        fe_api = b.get('fe_api', 'API')
        desc = b.get('description', '')
        payload = b.get('payload', '')
        error_msg = b.get('error_message', '')
        screenshot = b.get('screenshot', '')
        dev_status = b.get('dev_status', 'Pending')
        qa_remarks = b.get('qa_remarks', '')

        # Format payload / error into code block
        if payload:
            payload_html = f'<ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{payload}]]></ac:plain-text-body></ac:structured-macro>'
        else:
            payload_html = '<em>N/A</em>'

        if error_msg:
            error_html = f'<ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{error_msg}]]></ac:plain-text-body></ac:structured-macro>'
        else:
            error_html = '<em>N/A</em>'

        # Status badge
        dev_lower = dev_status.lower()
        if 'fixed' in dev_lower:
            badge_class = 'aui-lozenge-success'
        elif 'progress' in dev_lower:
            badge_class = 'aui-lozenge-current'
        elif 'open' in dev_lower or 'reopen' in dev_lower or 'fail' in dev_lower:
            badge_class = 'aui-lozenge-error'
        else:
            badge_class = 'aui-lozenge-subtle'

        dev_badge = f'<span class="status-macro aui-lozenge {badge_class}">{dev_status}</span>'

        rows_html += f"""<tr>
  <td class="confluenceTd">{sno}</td>
  <td class="confluenceTd">{date}</td>
  <td class="confluenceTd"><strong>{segment}</strong></td>
  <td class="confluenceTd">{severity}</td>
  <td class="confluenceTd">{fe_api}</td>
  <td class="confluenceTd">{desc}</td>
  <td class="confluenceTd">{payload_html}</td>
  <td class="confluenceTd">{error_html}</td>
  <td class="confluenceTd">{screenshot}</td>
  <td class="confluenceTd">{dev_badge}</td>
  <td class="confluenceTd">{qa_remarks}</td>
</tr>"""

    # Replace placeholder row or append before </tbody>
    if "<em>Awaiting user bug list...</em>" in storage_value:
        # replace the placeholder row
        placeholder_regex = r'<tr>\s*<td class="confluenceTd"><em>-</em></td>.*?</tr>'
        storage_value = re.sub(placeholder_regex, rows_html, storage_value, flags=re.DOTALL)
    else:
        # append before </tbody>
        storage_value = storage_value.replace("</tbody>", f"{rows_html}\n</tbody>")

    # 3. Update Confluence page
    new_version = current_version + 1
    update_payload = {
        "id": str(page_id),
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": storage_value,
                "representation": "storage"
            }
        },
        "version": {
            "number": new_version,
            "message": f"Added {len(bugs_list)} bug verification record(s)"
        }
    }

    r_put = requests.put(f"{base_url}/rest/api/content/{page_id}", auth=auth, json=update_payload)
    if r_put.status_code == 200:
        print(f"Successfully updated page {page_id} to version {new_version}!")
        return True
    else:
        print(f"Error updating page: {r_put.text}")
        return False

if __name__ == '__main__':
    print("Confluence bug updater ready.")
