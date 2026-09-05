#!/usr/bin/env python3
"""Public evidence gateway. Standard-library only; no company connector required.

Examples (from the repository root):
  python3 scripts/public_evidence.py pubmed --query 'multiple myeloma' --limit 5
  python3 scripts/public_evidence.py europepmc --query 'atopic dermatitis' --limit 5
  python3 scripts/public_evidence.py crossref --query 'obesity randomized trial'
  python3 scripts/public_evidence.py trials --query 'multiple myeloma'
  python3 scripts/public_evidence.py labels --query metformin
  python3 scripts/public_evidence.py faers --query metformin

Results are retrieved records, not appraised claims. A failed request never becomes
a synthetic result or a zero-hit search. Exit 0=search completed, 1=unavailable,
2=invalid request. Existing specialist clients remain the route for full records,
date filters, trial status, MeSH, label sections and citation verification.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ('pubmed', 'trials', 'labels', 'faers', 'europepmc', 'crossref')


def request_json(url, *, fixture=None, timeout=15):
    if fixture is not None:
        record = fixture.get(url)
        if record is None:
            raise ValueError('No test fixture for this request; network was not used')
        if record['status'] != 200:
            raise ValueError(f"Fixture HTTP {record['status']}")
        return record['body']
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'medical-affairs-skills/0.2', 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise ValueError(f'Public service returned HTTP {exc.code}') from None
            retry = exc.headers.get('Retry-After', '')
            time.sleep(min(float(retry), 10) if retry.isdigit() else 2 ** attempt)
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise ValueError('Public service could not be reached within the request budget') from None
            time.sleep(2 ** attempt)


def additional_source(source, query, limit, fixture=None, timeout=15):
    if source == 'europepmc':
        url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?' + urllib.parse.urlencode({
            'query': query, 'format': 'json', 'pageSize': limit, 'resultType': 'core'})
        data = request_json(url, fixture=fixture, timeout=timeout)
        if not isinstance(data, dict) or not isinstance(data.get('resultList'), dict) or 'hitCount' not in data:
            raise ValueError('Europe PMC response schema is not recognized')
        rows = [{key: row.get(key) for key in (
            'id', 'source', 'pmid', 'pmcid', 'doi', 'title', 'authorString',
            'pubYear', 'isOpenAccess', 'abstractText', 'fullTextUrlList')}
            for row in data['resultList'].get('result', [])]
        return {'total': data['hitCount'], 'records': rows, 'request_url': url}
    params = {'query.bibliographic': query, 'rows': limit}
    contact = os.environ.get('API_CONTACT_EMAIL')
    if contact:
        params['mailto'] = contact
    url = 'https://api.crossref.org/works?' + urllib.parse.urlencode(params)
    data = request_json(url, fixture=fixture, timeout=timeout)
    msg = data.get('message', {}) if isinstance(data, dict) else {}
    if not isinstance(msg, dict) or 'items' not in msg or 'total-results' not in msg:
        raise ValueError('Crossref response schema is not recognized')
    rows = [{key: row.get(key) for key in (
        'DOI', 'title', 'author', 'published', 'container-title', 'type',
        'license', 'link', 'update-to', 'URL')} for row in msg['items']]
    # Contact information is not needed in the public provenance URL.
    params.pop('mailto', None)
    return {'total': msg['total-results'], 'records': rows,
            'request_url': 'https://api.crossref.org/works?' + urllib.parse.urlencode(params)}


def search(source, query, limit=5, fixture=None, timeout=15):
    result = {'source': source, 'query': query, 'requested_limit': limit,
              'retrieved_at': dt.datetime.now(dt.timezone.utc).isoformat(),
              'source_kind': 'test_fixture' if fixture is not None else 'real_public',
              'status': 'unavailable', 'claim_support_checked': False}
    # Do not try to validate fictional products against real registries.
    if re.search(r'\b(NORVANTIB|norvantimab|DERMALYX|lyxekimab|ADIPOSYN|trelagludide|NVB-\d+|SYN[-:][\w-]+)\b', query, re.I):
        result['reason'] = 'Fictional identifier: use the workshop source file; search real disease/class terms separately.'
        return result
    try:
        if source in ('europepmc', 'crossref'):
            result['data'] = additional_source(source, query, limit, fixture, timeout)
        else:
            if fixture is not None:
                raise ValueError('Use specialist --fixtures clients for recorded PubMed, trials and FDA tests')
            scripts = {
                'pubmed': ['skills/pubmed-search/scripts/pubmed.py', 'search', '--query', query, '--limit', str(limit), '--format', 'json'],
                'trials': ['skills/clinical-trials-search/scripts/ctgov.py', 'search', '--term', query, '--limit', str(limit), '--format', 'json'],
                'labels': ['skills/regulatory-label-intelligence/scripts/openfda.py', '--format', 'json', 'label', '--generic', query],
                'faers': ['skills/regulatory-label-intelligence/scripts/openfda.py', '--format', 'json', 'faers', '--generic', query, '--limit', str(limit)],
            }
            completed = subprocess.run([sys.executable, str(ROOT / scripts[source][0]), *scripts[source][1:]],
                                       capture_output=True, text=True, timeout=timeout * 3, cwd=ROOT)
            if completed.returncode:
                raise ValueError(f'{source} client returned {completed.returncode}; run its command directly for diagnostics')
            result['data'] = json.loads(completed.stdout)
        result['status'] = 'retrieved'
    except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
        result['reason'] = str(exc)
        result['next_step'] = 'Continue with named workshop sources. Do not report this as zero results or live verification.'
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source', choices=SOURCES)
    ap.add_argument('--query', required=True)
    ap.add_argument('--limit', type=int, default=5)
    ap.add_argument('--timeout', type=int, default=15)
    ap.add_argument('--out', type=Path)
    args = ap.parse_args()
    if not 1 <= args.limit <= 100 or not 1 <= args.timeout <= 30:
        ap.error('limit must be 1..100; timeout must be 1..30 seconds')
    result = search(args.source, args.query, args.limit, timeout=args.timeout)
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        # A new search must not silently overwrite a prior evidence snapshot.
        with args.out.open('x', encoding='utf-8') as stream:
            stream.write(encoded + '\n')
    print(encoded)
    return 0 if result['status'] == 'retrieved' else 1


if __name__ == '__main__':
    raise SystemExit(main())
