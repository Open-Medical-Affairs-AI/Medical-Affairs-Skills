#!/usr/bin/env python3
"""Prepare a workshop run without installing packages or using any connector.

python3 scripts/workshop.py list
python3 scripts/workshop.py start --mission field-insights --ta oncology-mm
python3 scripts/workshop.py check --live
python3 scripts/workshop.py resume --run outputs/<run-directory>

This is an input launcher and checkpoint helper, not an LLM runtime. The agent
reads RUN.md and does the analysis. It never labels unexecuted work complete.
"""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
TAS = ('oncology-mm', 'immunology-ad', 'cardiometabolic-obesity')
MANIFEST = ROOT / 'workshop/catalog.json'


def catalog():
    return json.loads(MANIFEST.read_text())


def start(mission, ta, out):
    spec = next(m for m in catalog()['missions'] if m['id'] == mission)
    run = Path(out) / (dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + mission + '-' + uuid.uuid4().hex[:6])
    run.mkdir(parents=True, exist_ok=False)
    inputs = []
    for rel in spec['inputs']:
        rel = rel.replace('{ta}', ta)
        path = ROOT / rel
        inputs.append({'path': rel, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'source_kind': 'synthetic'})
    manifest = {'version': 1, 'mode': 'workshop', 'mission': mission, 'therapeutic_area': ta,
                'objective': spec['objective'], 'status': 'prepared', 'inputs': inputs,
                'outputs': [], 'decisions': [], 'open_questions': [], 'completed_steps': [],
                'next_step': 'Read inputs, scan relevant records, execute the objective using the named skills',
                'note': 'Prepared inputs only. An agent has not yet executed this task.'}
    (run / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (run / 'RUN.md').write_text(f"# {spec['title']}\n\nSYNTHETIC WORKSHOP DRAFT\n\n{spec['objective']}\n\n"
        + f"Therapeutic area: {ta}. Scenario date: 1 October 2026.\n\n"
        + '## Inputs\n\n' + '\n'.join('- ' + i['path'] for i in inputs)
        + '\n\n## Start with these skills\n\n' + ', '.join(spec['skills'])
        + '\n\n## Expected deliverables\n\n' + '\n'.join('- ' + d for d in spec['deliverables'])
        + '\n\nRead AGENTS.md and docs/execution.md. Save files alongside this run. Update run.json '
        'at meaningful checkpoints with actual completed steps, source IDs, output paths and the next step. '
        'Do not mark a draft reviewed or sent. Public evidence is optional, separate context for the real disease; '
        'fictional products are supported only by fictional source files.\n')
    return run


def inspect_run(run):
    state = json.loads((Path(run) / 'run.json').read_text())
    changed = [r['path'] for r in state['inputs'] if not (ROOT / r['path']).exists()
               or hashlib.sha256((ROOT / r['path']).read_bytes()).hexdigest() != r['sha256']]
    return {'run': str(run), 'state': state, 'changed_inputs': changed,
            'instruction': 'Review changed sources and dependent outputs before continuing.' if changed else
                           'Read actual saved outputs; continue from next_step without repeating completed work.'}


def preflight(live=False):
    missing = []
    for m in catalog()['missions']:
        for ta in TAS:
            missing += [p.replace('{ta}', ta) for p in m['inputs'] if not (ROOT / p.replace('{ta}', ta)).is_file()]
    result = {'python': sys.version.split()[0], 'mission_count': len(catalog()['missions']),
              'missing_inputs': sorted(set(missing)), 'company_connectors_required': False,
              'workshop_ready': not missing, 'live_apis': 'not tested',
              'audio': 'local whisper available' if shutil.which('whisper') and shutil.which('ffmpeg') else 'use supplied transcripts',
              'agent_execution': 'requires an agent that can read repository files; this check is not a GrokBot test'}
    if live:
        from public_evidence import SOURCES, search
        result['live_apis'] = {}
        for source in SOURCES:
            query = 'metformin' if source in ('labels', 'faers') else 'multiple myeloma'
            response = search(source, query, 1, timeout=10)
            result['live_apis'][source] = {k: response[k] for k in ('status', 'retrieved_at', 'reason') if k in response}
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='command', required=True)
    sub.add_parser('list')
    s = sub.add_parser('start')
    s.add_argument('--mission', choices=[m['id'] for m in catalog()['missions']], default='field-insights')
    s.add_argument('--ta', choices=TAS, default='oncology-mm')
    s.add_argument('--out', type=Path, default=ROOT / 'outputs')
    c = sub.add_parser('check'); c.add_argument('--live', action='store_true')
    r = sub.add_parser('resume'); r.add_argument('--run', type=Path, required=True)
    args = ap.parse_args()
    if args.command == 'list':
        for m in catalog()['missions']:
            print(f"{m['id']:22} {m['title']}")
    elif args.command == 'start':
        print(start(args.mission, args.ta, args.out).resolve())
    elif args.command == 'resume':
        print(json.dumps(inspect_run(args.run), indent=2))
    else:
        result = preflight(args.live)
        print(json.dumps(result, indent=2))
        return 0 if result['workshop_ready'] else 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
