#!/usr/bin/env python3
"""Behavioral regression checks for launch, sources, data and tool failure paths.

These tests do not simulate a language model or certify clinical quality.
Run the rubric separately on the actual workshop GrokBot environment.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.parse

import public_evidence as gateway
import query_database
import workshop
import msl_admin
from build_starter_bundle import build

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'workshop/data/connected/medical-affairs.sqlite'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


cites = load('citation_check', 'skills/citation-integrity/scripts/verify_citations.py')
fda = load('fda_check', 'skills/regulatory-label-intelligence/scripts/openfda.py')


def cli(*args):
    return subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True, timeout=20)


class WorkshopTests(unittest.TestCase):
    def test_msl_packet_preserves_context_and_stable_task_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            first=msl_admin.assemble('oncology-mm','HCP-138',tmp)
            second=msl_admin.assemble('oncology-mm','HCP-138',tmp)
            self.assertEqual((first/'proposed-tasks.csv').read_text(),(second/'proposed-tasks.csv').read_text())
            packet=json.loads((first/'context.json').read_text())
            self.assertFalse(packet['live_crm_updated'])
            self.assertFalse(packet['outreach_sent'])
            self.assertIsNone(packet['meeting']['date'])
            self.assertTrue(packet['historical_interactions'])
            self.assertTrue(all(r['hcp_id']=='oncology-mm:HCP-138' for r in packet['historical_interactions']))
            with self.assertRaises(ValueError):msl_admin.assemble('oncology-mm','NOT-A-PERSON',tmp)

    def test_msl_tasks_deduplicate_and_reject_conflicting_versions(self):
        record={'hcp_id':'X','source_commitment_id':'A','status':'open'}
        self.assertEqual(len(msl_admin.unique_tasks([record,dict(record)])),1)
        with self.assertRaises(ValueError):msl_admin.unique_tasks([record,{**record,'status':'completed'}])

    def test_all_missions_prepare_all_therapeutic_areas_without_network(self):
        with tempfile.TemporaryDirectory() as tmp, patch('urllib.request.urlopen', side_effect=AssertionError('Network not allowed')):
            for mission in workshop.catalog()['missions']:
                for ta in workshop.TAS:
                    with self.subTest(mission=mission['id'], ta=ta):
                        run = workshop.start(mission['id'], ta, tmp)
                        state = workshop.inspect_run(run)
                        self.assertEqual(state['changed_inputs'], [])
                        self.assertEqual(state['state']['status'], 'prepared')
                        self.assertEqual(state['state']['outputs'], [])
                        self.assertTrue((run/'RUN.md').is_file())

    def test_every_skill_has_existing_practice_inputs(self):
        mapping = workshop.catalog()['skill_inputs']
        self.assertEqual(set(mapping), {p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')})
        for name, inputs in mapping.items():
            self.assertTrue(inputs, name)
            for ta in workshop.TAS:
                for p in inputs:
                    self.assertTrue((ROOT/p.replace('{ta}',ta)).is_file(), (name,p))

    def test_resume_detects_changed_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'source.md').write_text('old')
            state={'inputs':[{'path':'source.md','sha256':hashlib.sha256(b'old').hexdigest()}]}
            (root/'run.json').write_text(json.dumps(state))
            (root/'source.md').write_text('changed')
            with patch.object(workshop,'ROOT',root):
                self.assertEqual(workshop.inspect_run(root)['changed_inputs'],['source.md'])

    def test_database_joins_are_complete(self):
        con=sqlite3.connect(DB)
        try:
            self.assertEqual(con.execute('PRAGMA foreign_key_check').fetchall(),[])
            n=con.execute('SELECT COUNT(*) FROM interactions').fetchone()[0]
            joined=con.execute('SELECT COUNT(*) FROM interactions i JOIN hcps h ON i.hcp_id=h.hcp_id').fetchone()[0]
            self.assertEqual(n,joined)
            self.assertEqual(con.execute('SELECT COUNT(*) FROM engagement WHERE completed > attended OR attended > invited').fetchone()[0],0)
            self.assertEqual(con.execute('SELECT COUNT(*) FROM hcps WHERE hcp_id NOT LIKE therapeutic_area || ":%"').fetchone()[0],0)
        finally:con.close()

    def test_readonly_helper_rejects_writes_and_attachments(self):
        original=hashlib.sha256(DB.read_bytes()).hexdigest()
        for sql in ("DELETE FROM hcps", "ATTACH DATABASE ':memory:' AS other", 'PRAGMA query_only=OFF', 'CREATE TABLE evil (id TEXT)'):
            with self.subTest(sql=sql),self.assertRaises(sqlite3.Error):
                query_database.query(DB,sql)
        self.assertEqual(original,hashlib.sha256(DB.read_bytes()).hexdigest())
        limited=query_database.query(DB,'SELECT hcp_id FROM hcps',3)
        self.assertEqual(len(limited['rows']),3)
        self.assertTrue(limited['truncated'])

    def test_expensive_query_is_interrupted(self):
        # Use a mocked monotonic deadline to exercise the timeout without waiting.
        with patch.object(query_database.time,'monotonic',side_effect=[0,10,10,10]):
            with self.assertRaises(sqlite3.OperationalError):
                query_database.query(DB,'WITH RECURSIVE x(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM x) SELECT sum(n) FROM x')

    def test_transcript_import_needs_no_audio_engine(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'transcript.md'
            source=ROOT/'workshop/data/oncology-mm/advisory-board-transcript.md'
            result=cli('scripts/transcribe.py','--input',str(source),'--out',str(out))
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn(source.read_text(),out.read_text())
            self.assertIn('audio was not transcribed',out.read_text())
            repeat=cli('scripts/transcribe.py','--input',str(source),'--out',str(out))
            self.assertNotEqual(repeat.returncode,0)

    def test_synthetic_product_never_calls_public_api(self):
        with patch('urllib.request.urlopen',side_effect=AssertionError('unexpected network')):
            for product in ('NORVANTIB','DERMALYX','ADIPOSYN','NVB-201'):
                result=gateway.search('crossref',product)
                self.assertEqual(result['status'],'unavailable')
                self.assertIn('Fictional',result['reason'])

    def test_europe_pmc_parse_empty_and_schema_failure(self):
        query='myeloma';url='https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode(
            {'query':query,'format':'json','pageSize':1,'resultType':'core'})
        for body in ({'hitCount':0,'resultList':{'result':[]}}, {'hitCount':1,'resultList':{'result':[{'id':'7','title':'Test fixture'}]}}):
            data=gateway.search('europepmc',query,1,{url:{'status':200,'body':body}})
            self.assertEqual(data['status'],'retrieved')
            self.assertEqual(data['source_kind'],'test_fixture')
        failed=gateway.search('europepmc',query,1,{url:{'status':503,'body':{}}})
        self.assertEqual(failed['status'],'unavailable')
        self.assertNotIn('data',failed)
        malformed=gateway.search('europepmc',query,1,{url:{'status':200,'body':{}}})
        self.assertEqual(malformed['status'],'unavailable')

    def test_crossref_metadata_and_failed_response(self):
        with patch.dict('os.environ',{'API_CONTACT_EMAIL':''}):
            url='https://api.crossref.org/works?'+urllib.parse.urlencode({'query.bibliographic':'test','rows':1})
            fixture={url:{'status':200,'body':{'message':{'total-results':1,'items':[{'DOI':'10.1234/example','title':['Fixture']}]}}}}
            result=gateway.search('crossref','test',1,fixture)
            self.assertEqual(result['status'],'retrieved')
            self.assertFalse(result['claim_support_checked'])

    def test_specialist_json_outputs_parse_and_preserve_counts(self):
        fixtures=str(ROOT/'shared/fixtures')
        commands=[
            ['skills/pubmed-search/scripts/pubmed.py','--fixtures',fixtures,'search','--query','teclistamab AND myeloma','--limit','3','--format','json'],
            ['skills/clinical-trials-search/scripts/ctgov.py','--fixtures',fixtures,'search','--term','teclistamab','--limit','3','--format','json'],
            ['skills/regulatory-label-intelligence/scripts/openfda.py','--fixtures',fixtures,'--format','json','faers','--generic','teclistamab','--limit','5']]
        for command in commands:
            result=cli(*command)
            self.assertEqual(result.returncode,0,result.stderr+result.stdout)
            data=json.loads(result.stdout)
            self.assertTrue(data)
            if 'faers' in command:self.assertIn('No denominator',data['caveat'])

    def test_fda_outage_is_not_empty_results(self):
        for operation in (fda.fetch_label,fda.faers_reactions):
            with patch.object(fda,'http_get',return_value=(503,'')),self.assertRaises(SystemExit):
                operation('metformin','generic' if operation==fda.fetch_label else 5,None)

    def test_identifier_extraction_avoids_dates_and_account_numbers(self):
        found=cites.extract_identifiers('20261001 Account 12345678 NCT04557098 PMID: 12 https://pubmed.ncbi.nlm.nih.gov/36001231/')
        self.assertEqual(found['pmids'],['12','36001231'])
        self.assertEqual(found['ncts'],['NCT04557098'])

    def test_wrong_trial_record_is_not_resolved(self):
        client=cites.Http()
        with patch.object(client,'get',return_value=(200,json.dumps({'protocolSection':{'identificationModule':{'nctId':'NCT00000000','briefTitle':'Wrong record'}}}))):
            self.assertFalse(cites.resolve_nct('NCT04557098',client).resolved)

    def test_offline_starters_are_current_and_include_sources(self):
        for ta in workshop.TAS:
            bundle=ROOT/f'workshop/bundles/first-mission-{ta}.md'
            self.assertEqual(bundle.read_text(),build(ta))
            text=bundle.read_text()
            self.assertIn('record_id,date,msl,contact_id',text)
            self.assertNotIn('workshop/evaluation/rubric.md',text)


if __name__=='__main__':
    unittest.main(verbosity=2)
