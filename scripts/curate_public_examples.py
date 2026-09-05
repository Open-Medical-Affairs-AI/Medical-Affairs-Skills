#!/usr/bin/env python3
"""Refresh curated real bibliographic examples through Crossref DOI resolution.

These are deliberately selected teaching examples, not an exhaustive or current
standard-of-care review. Metadata only; no publisher abstracts or full text.
"""
import argparse
import datetime as dt
import json
from pathlib import Path
import urllib.parse
from public_evidence import request_json

ROOT = Path(__file__).resolve().parents[1]
SEEDS = {
    'oncology-mm': [
        ('10.1056/NEJMoa2203478', 'teclistamab', 'Appraise a study design before translating response rates into claims'),
        ('10.1056/NEJMoa2024850', 'idecabtagene', 'Compare eligibility and follow-up without an unsupported cross-trial ranking'),
        ('10.1056/NEJMoa2303379', 'cilta-cel', 'Distinguish the question a comparative trial can address')],
    'immunology-ad': [
        ('10.1056/NEJMoa1610020', 'dupilumab', 'Identify trial populations, endpoints and analysis sets'),
        ('10.1001/jamadermatol.2021.3023', 'upadacitinib', 'Inspect direct comparison, safety and endpoint hierarchy'),
        ('10.1056/NEJMoa2019380', 'abrocitinib', 'Check the actual comparison before writing a summary')],
    'cardiometabolic-obesity': [
        ('10.1056/NEJMoa2032183', 'semaglutide', 'Preserve estimands, discontinuation and adverse-event context'),
        ('10.1056/NEJMoa2206038', 'tirzepatide', 'Check population and follow-up before comparing trials'),
        ('10.1056/NEJMoa2307563', 'semaglutide', 'Distinguish weight endpoints from cardiovascular outcomes')],
}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ta',choices=list(SEEDS))
    args=parser.parse_args()
    out = ROOT / 'workshop/public-evidence'
    out.mkdir(exist_ok=True)
    failures = []
    for ta, seeds in SEEDS.items():
        if args.ta and ta!=args.ta: continue
        records=[]
        for doi, keyword, exercise in seeds:
            url='https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='')
            try:
                row=request_json(url)['message']
                if row.get('DOI','').lower()!=doi.lower() or keyword not in ' '.join(row.get('title',[])).lower():
                    raise ValueError('DOI/title does not match the curated teaching example')
            except (ValueError,KeyError) as exc:
                failures.append((doi,str(exc)));continue
            record={key:row.get(key) for key in ('DOI','title','author','published','container-title','type','license','link','update-to','URL')}
            record['request_url']=url;record['teaching_exercise']=exercise
            records.append(record)
        if len(records)!=len(seeds):
            continue
        snapshot={'source':'Crossref','source_kind':'real_public','status':'retrieved',
                  'retrieved_at':dt.datetime.now(dt.timezone.utc).isoformat(),
                  'claim_support_checked':False,
                  'selection':'Three deliberately selected scientific teaching examples per therapeutic area; DOI and title checked against Crossref. Not a systematic, comprehensive or current treatment review.',
                  'reuse':'Bibliographic metadata only; inspect article license before obtaining or redistributing text.',
                  'records':records}
        (out/f'{ta}.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
        print(f'{ta}: {len(records)} curated DOI/title matches saved')
    for failure in failures:print(failure)
    return 1 if failures else 0


if __name__=='__main__':
    raise SystemExit(main())
