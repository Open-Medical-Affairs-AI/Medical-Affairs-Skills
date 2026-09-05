#!/usr/bin/env python3
"""Assemble a fictional MSL administrative/pre-call packet from the practice DB.

Outputs are source context and proposed records, not completed analysis, messages,
appointments or live CRM updates. Standard library only. Input DB is read-only.
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import sqlite3
import uuid

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'workshop/data/connected/medical-affairs.sqlite'
TAS = ('oncology-mm', 'immunology-ad', 'cardiometabolic-obesity')


def unique_tasks(rows):
    unique = {}
    for row in rows:
        key = (row['hcp_id'], row['source_commitment_id'])
        if key not in unique:
            unique[key] = dict(row)
        elif unique[key] != row:
            raise ValueError('Conflicting task versions share an identity; reconcile before exporting')
    return list(unique.values())


def assemble(ta, hcp, out):
    identity = hcp if hcp.startswith(ta + ':') else ta + ':' + hcp
    connection = sqlite3.connect(DB.resolve().as_uri() + '?mode=ro', uri=True)
    connection.row_factory = sqlite3.Row
    def rows(sql, params):
        return [dict(r) for r in connection.execute(sql, params)]
    try:
        people = rows('SELECT * FROM hcps WHERE hcp_id=? AND therapeutic_area=?', (identity, ta))
        if not people:
            raise ValueError('No matching fictional HCP. Inspect hcps.csv; do not guess a person.')
        person = people[0]
        interactions = rows('SELECT * FROM interactions WHERE hcp_id=? ORDER BY date, interaction_id', (identity,))
        tasks = unique_tasks(rows('SELECT * FROM msl_tasks WHERE hcp_id=? ORDER BY due_date, task_id', (identity,)))
        access = rows('SELECT * FROM access_log WHERE hcp_id=?', (identity,))
        account = rows('SELECT * FROM accounts WHERE account_id=?', (person['account_id'],))
    finally:
        connection.close()
    run = Path(out) / ('msl-' + ta + '-' + hcp.split(':')[-1] + '-' + uuid.uuid4().hex[:6])
    run.mkdir(parents=True, exist_ok=False)
    packet = {'label': 'SYNTHETIC WORKSHOP DRAFT', 'status': 'source_context_prepared',
              'source_db': 'workshop/data/connected/medical-affairs.sqlite',
              'source_sha256': hashlib.sha256(DB.read_bytes()).hexdigest(),
              'scenario_date': '2026-10-01', 'hcp': person, 'account': account,
              'historical_interactions': interactions, 'task_register': tasks, 'access_context': access,
              'meeting': {'date': None, 'time_zone': None, 'purpose': None, 'status': 'not scheduled'},
              'remaining_work': 'Use msl-pre-call-planning to analyze these sources. Actual meeting details are not supplied.',
              'live_crm_updated': False, 'outreach_sent': False}
    (run/'context.json').write_text(json.dumps(packet, indent=2) + '\n')
    open_tasks = []
    for task in tasks:
        if task['status'] == 'completed':
            continue
        key = hashlib.sha256((task['hcp_id'] + '|' + task['source_commitment_id']).encode()).hexdigest()[:20]
        open_tasks.append({'proposed_record_key': key, 'hcp_id': identity,
                          'source_task_id': task['task_id'], 'task_text': task['task_text'],
                          'due_date': task['due_date'], 'owner_role': task['owner_role'],
                          'review_status': 'draft for review', 'source_status': task['status'],
                          'overdue_in_scenario': str(task['due_date'] < '2026-10-01').lower()})
    with (run/'proposed-tasks.csv').open('w',newline='') as f:
        f.write('# SYNTHETIC DATA - proposed portable records; not a live CRM import\n')
        columns=['proposed_record_key','hcp_id','source_task_id','task_text','due_date','owner_role','review_status','source_status','overdue_in_scenario']
        writer=csv.DictWriter(f,fieldnames=columns);writer.writeheader();writer.writerows(open_tasks)
    (run/'PRE-CALL.md').write_text('# Prepare the MSL for scientific engagement\n\n'
        'SYNTHETIC WORKSHOP DRAFT. Source context is in context.json.\n\n'
        f"Fictional HCP: {identity}\nHistorical records: {len(interactions)}\nOpen task drafts: {len(open_tasks)}\n\n"
        'Read the source context and the msl-pre-call-planning skill. Create the one-page brief, '
        'neutral scientific questions and evidence gaps. Dates, time zone and meeting purpose '
        'must not be invented. Access restrictions and declined contact must be respected. '
        'The historical records are not notes from a new meeting.\n\n'
        'For an actual post-call draft, use supplied encounter notes and msl-post-call-follow-up. '
        'For a real CRM import, inspect the tenant schema and obtain the relevant action authorization.\n')
    return run


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--ta',choices=TAS,default='oncology-mm')
    ap.add_argument('--hcp',required=True,help='Original fictional ID, e.g. HCP-138, or namespaced ID')
    ap.add_argument('--out',type=Path,default=ROOT/'outputs')
    args=ap.parse_args()
    try:
        print(assemble(args.ta,args.hcp,args.out))
    except (ValueError,OSError,sqlite3.Error) as exc:
        print(str(exc));return 1
    return 0


if __name__=='__main__':
    raise SystemExit(main())
