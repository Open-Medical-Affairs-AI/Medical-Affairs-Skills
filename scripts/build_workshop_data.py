#!/usr/bin/env python3
"""Build deterministic linked workshop records from the three existing TA packs.

Preserves source packs, including deliberate inconsistencies. Joins use therapeutic
area plus original ID because IDs repeat between packs. No real people or data.
"""
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'workshop/data'
OUT = DATA / 'connected'
TAS = ('oncology-mm', 'immunology-ad', 'cardiometabolic-obesity')
BANNER = 'SYNTHETIC DATA - fictional training records, not clinical evidence.'


def read_csv(path):
    return list(csv.DictReader(line for line in path.read_text().splitlines() if not line.startswith('#')))


def write_csv(name, rows):
    path = OUT / f'{name}.csv'
    with path.open('w', newline='', encoding='utf-8') as f:
        f.write('# ' + BANNER + '\n')
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def generate():
    OUT.mkdir(parents=True, exist_ok=True)
    tables = {key: [] for key in ('accounts', 'hcps', 'interactions', 'enquiries', 'content_assets',
                                 'engagement', 'patient_partnerships', 'projects', 'access_log', 'msl_tasks', 'source_links')}
    for ta in TAS:
        fields = read_csv(DATA / ta / 'field-observations.csv')
        contacts = sorted({r['contact_id'] for r in fields})
        for number in range(1, 9):
            tables['accounts'].append({'account_id': f'{ta}:ACC-{number:02}', 'therapeutic_area': ta,
                'name': f'Fictional {ta} care network {number}', 'capacity_hours_month': 8 + number,
                'scientific_need': ['long-term evidence', 'care access', 'safety education'][number % 3]})
        for i, contact in enumerate(contacts):
            first = next(r for r in fields if r['contact_id'] == contact)
            tables['hcps'].append({'hcp_id': f'{ta}:{contact}', 'original_id': contact, 'therapeutic_area': ta,
                'account_id': f'{ta}:ACC-{i % 8 + 1:02}', 'name': f'Fictional clinician {contact}',
                'country': first['country'], 'setting': first['setting'],
                'email_permission': 'no' if i % 5 == 0 else 'yes',
                'preferred_channel': ['Virtual', 'Phone', 'Face-to-face'][i % 3],
                'profile_note': 'Workshop identity; do not search for this person online'})
        for row in fields:
            tables['interactions'].append({'interaction_id': f"{ta}:{row['record_id']}",
                'hcp_id': f"{ta}:{row['contact_id']}", 'therapeutic_area': ta,
                'date': row['date'], 'msl': row['msl'], 'channel': row['channel'],
                'verbatim': row['observation'],
                'source_file': f'workshop/data/{ta}/field-observations.csv', 'source_record': row['record_id']})
        for i, row in enumerate(read_csv(DATA / ta / 'medical-information-enquiries.csv')):
            tables['enquiries'].append({'enquiry_id': f"{ta}:{row['id']}", 'therapeutic_area': ta,
                'requester': row['requester'], 'country': row['country'], 'date': row['date'],
                'verbatim': row['verbatim'], 'response_status': row['response_status'],
                'source_file': f'workshop/data/{ta}/medical-information-enquiries.csv', 'source_record': row['id']})
        for i in range(1, 13):
            tables['content_assets'].append({'asset_id': f'{ta}:ASSET-{i:02}', 'therapeutic_area': ta,
                'topic': ['care access', 'long-term evidence', 'safety education'][i % 3],
                'audience': 'HCP' if i % 3 else 'patient organization',
                'format': ['brief', 'video script', 'FAQ', 'slide deck'][i % 4],
                'version': '1.0', 'review_status': 'expired' if i % 4 == 0 else 'draft',
                'review_due': '2026-09-01' if i % 4 == 0 else '2026-11-01',
                'jurisdiction': 'US', 'language': 'en',
                'source_file': f'workshop/data/{ta}/product-profile.md'})
        for i, hcp in enumerate([h for h in tables['hcps'] if h['therapeutic_area'] == ta]):
            tables['access_log'].append({'access_id': f'{ta}:ACCESS-{i+1:03}', 'hcp_id': hcp['hcp_id'],
                'therapeutic_area': ta, 'route': ['institution medical office', 'existing scientific relationship', 'public professional enquiry route'][i % 3],
                'status': 'declined' if i % 11 == 0 else ('unverified' if i % 5 == 0 else 'review institution procedure'),
                'institution_rule': 'Appointment required; do not assume unrestricted access',
                'contact_detail': '', 'last_checked': '2026-09-25',
                'note': 'Fictional access scenario; no real address, relationship or introduction is asserted'})
            for j in range(2):
                tables['msl_tasks'].append({'task_id': f'{ta}:TASK-{i+1:03}-{j+1}', 'hcp_id': hcp['hcp_id'],
                    'therapeutic_area': ta, 'source_commitment_id': f'{ta}:SCENARIO-{i+1:03}-{j+1}',
                    'task_text': ['Review evidence for the next scientific discussion', 'Check approved material availability'][j],
                    'owner_role': 'MSL', 'due_date': '2026-10-05' if j else '2026-09-30',
                    'status': 'completed' if i % 7 == 0 and j == 1 else 'open',
                    'note': 'Added fictional task register; not a commitment extracted from historical field notes'})
            tables['engagement'].append({'event_id': f'{ta}:ENG-{i+1:03}', 'hcp_id': hcp['hcp_id'],
                'asset_id': f'{ta}:ASSET-{i % 12 + 1:02}', 'therapeutic_area': ta,
                'invited': 1, 'attended': int(i % 3 != 0), 'completed': int(i % 4 != 0 and i % 3 != 0),
                'pre_score': '' if i % 7 == 0 else 40 + i % 20,
                'post_score': '' if i % 4 == 0 or i % 3 == 0 else 50 + i % 25,
                'note': 'Paired scores only where both observed; no causal impact claim'})
        for i in range(1, 5):
            tables['patient_partnerships'].append({'partner_id': f'{ta}:PATORG-{i}', 'therapeutic_area': ta,
                'organization': f'Fictional patient partnership {i}',
                'need': ['travel burden', 'plain language evidence', 'caregiver support', 'accessible meeting format'][i-1],
                'input': ['Offer remote participation and short sessions', 'Include absolute benefits and harms',
                          'Ask about time away from work', 'Provide captions and translated summaries'][i-1],
                'permission_to_quote': 'no' if i == 2 else 'yes', 'commercial_link': 'none'})
        for i in range(1, 7):
            tables['projects'].append({'project_id': f'{ta}:PROJECT-{i}', 'therapeutic_area': ta,
                'objective': ['evidence gap', 'education', 'publication'][i % 3], 'cost_gbp': i * 75000,
                'hours': i * 20, 'status': 'proposed', 'dependency': f'{ta}:PROJECT-{i-1}' if i > 1 else '',
                'decision_needed': 'prioritize within budget; no spending authorization'})
    for ta in TAS:
        for p in sorted((DATA / ta).glob('*')):
            if p.is_file():
                tables['source_links'].append({'source_id': f'SYN:{ta}:{p.stem}',
                    'path': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                    'source_kind': 'synthetic', 'license': 'Apache-2.0',
                    'note': 'Fictional workshop source. Conflicts may be intentional; not a truth label.'})
    for name, rows in tables.items():
        write_csv(name, rows)
    db = OUT / 'medical-affairs.sqlite'
    # This is a generated artifact under the fixed output path, never a user DB.
    if db.exists():
        db.unlink()
    conn = sqlite3.connect(db)
    conn.execute('PRAGMA foreign_keys=ON')
    relations = {'hcps': {'account_id': 'accounts(account_id)'},
                 'interactions': {'hcp_id': 'hcps(hcp_id)'},
                 'engagement': {'hcp_id': 'hcps(hcp_id)', 'asset_id': 'content_assets(asset_id)'},
                 'access_log': {'hcp_id': 'hcps(hcp_id)'}, 'msl_tasks': {'hcp_id': 'hcps(hcp_id)'}}
    numeric = {'capacity_hours_month', 'cost_gbp', 'hours', 'invited', 'attended', 'completed', 'pre_score', 'post_score'}
    for name, rows in tables.items():
        cols = list(rows[0])
        definitions = [f'"{col}" {"INTEGER" if col in numeric else "TEXT"}' + (' PRIMARY KEY' if i == 0 else '')
                       for i, col in enumerate(cols)]
        for col, parent in relations.get(name, {}).items():
            definitions.append(f'FOREIGN KEY("{col}") REFERENCES {parent}')
        conn.execute(f'CREATE TABLE {name} ({", ".join(definitions)})')
        values = [[None if r[c] == '' and c in numeric else r[c] for c in cols] for r in rows]
        conn.executemany(f'INSERT INTO {name} VALUES ({", ".join("?" for _ in cols)})', values)
    conn.execute('CREATE TABLE dataset_metadata (label TEXT, snapshot TEXT)')
    conn.execute('INSERT INTO dataset_metadata VALUES (?,?)', (BANNER, '2026-10-01 fictional scenario'))
    assert not conn.execute('PRAGMA foreign_key_check').fetchall()
    conn.commit()
    conn.close()
    schema = {'label': BANNER, 'version': '0.2.0', 'scenario_date': '2026-10-01',
              'tables': {n: {'rows': len(r), 'columns': list(r[0])} for n, r in tables.items()},
              'joins': relations,
              'notes': ['HCP and account assignments are synthetic, not real entity matches.',
                        'Original IDs are namespaced by therapeutic area. Never join on bare HCP-101.',
                        'Existing pack contradictions are preserved for appraisal.',
                        'Medical enquiry requesters are not guessed to be named HCPs.',
                        'No outreach is authorized by a yes value in a fictional permission column.']}
    (OUT / 'data-dictionary.json').write_text(json.dumps(schema, indent=2) + '\n')
    (OUT / 'README.md').write_text('# Connected practice organization\n\n' + BANNER + '\n\n'
        'Use the CSV files directly, or query `medical-affairs.sqlite` with the read-only helper. '
        'The SQLite file needs no installation, account, connector or credentials.\n\n'
        'The scenario date is **1 October 2026**, not a claim about the real date. '
        'HCPs and interactions link to the existing packs. Enquiries retain original requester roles without invented HCP links.\n\n'
        'See `data-dictionary.json` for joins, fields and counts; `source_links.csv` for original source hashes. '
        'All output remains a synthetic draft. Use local policy to handle real data separately.\n\n'
        '```bash\npython3 scripts/query_database.py --db workshop/data/connected/medical-affairs.sqlite --schema\n'
        'python3 scripts/query_database.py --db workshop/data/connected/medical-affairs.sqlite '
        '--sql "SELECT h.country, COUNT(*) AS interactions FROM interactions i JOIN hcps h ON h.hcp_id=i.hcp_id GROUP BY h.country"\n```\n')
    print(json.dumps({n: len(r) for n, r in tables.items()}, indent=2))


if __name__ == '__main__':
    generate()
