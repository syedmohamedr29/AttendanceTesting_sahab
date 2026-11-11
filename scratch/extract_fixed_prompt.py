import json

with open(r'C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('type') == 'USER_INPUT':
                content = data.get('content', '')
                if 'Fixed Work Template API' in content:
                    print(f"Found at step {data.get('step_index')}, len {len(content)}")
                    with open('scratch/fixed_test_scenarios_prompt.md', 'w', encoding='utf-8') as out:
                        out.write(content)
                    print("Written to scratch/fixed_test_scenarios_prompt.md")
        except Exception as e:
            pass
