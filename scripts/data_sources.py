#!/usr/bin/env python3
"""Locate the Open-Medical-Affairs/Data-Sources checkout that holds the datasets.

The synthetic workshop packs and the public-source catalog moved out of this
repository into https://github.com/Open-Medical-Affairs/Data-Sources. Paths in
workshop/catalog.json, missions and skills read ``Data-Sources/<path>`` and are
resolved, in order, against:

  1. $MA_DATA_SOURCES                 (an explicit checkout anywhere)
  2. <this repo>/Data-Sources         (recommended; git-ignored here)
  3. <this repo>/../Data-Sources      (a sibling checkout)

    python3 scripts/data_sources.py           # where is it? exit 1 if missing
    python3 scripts/data_sources.py --fetch   # git clone it into ./Data-Sources

Without a checkout, agents can read every file from RAW_BASE (see
Data-Sources/synthetic/index.json for raw links). Standard library only.
"""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'Data-Sources/'
REPO_URL = 'https://github.com/Open-Medical-Affairs/Data-Sources'
RAW_BASE = 'https://raw.githubusercontent.com/Open-Medical-Affairs/Data-Sources/main/'
HINT = (f'Datasets live in {REPO_URL}. From the repository root run:\n'
        f'  git clone {REPO_URL}.git Data-Sources\n'
        '  (or: python3 scripts/data_sources.py --fetch, or set MA_DATA_SOURCES=/path/to/Data-Sources)')


def candidates():
    env = os.environ.get('MA_DATA_SOURCES')
    return ([Path(env).expanduser()] if env else []) + [ROOT / 'Data-Sources', ROOT.parent / 'Data-Sources']


def data_root(required=False):
    """The first checkout that looks like Data-Sources, else the default location."""
    for c in candidates():
        if (c / 'synthetic').is_dir():
            return c.resolve()
    if required:
        raise FileNotFoundError('Data-Sources checkout not found. ' + HINT)
    return ROOT / 'Data-Sources'


def resolve(rel):
    """Map a repository path to the file on disk. 'Data-Sources/x' -> <checkout>/x."""
    rel = str(rel)
    if rel.startswith(PREFIX):
        return data_root() / rel[len(PREFIX):]
    return ROOT / rel


def raw_url(rel):
    rel = str(rel)
    return RAW_BASE + rel[len(PREFIX):] if rel.startswith(PREFIX) else rel


SYNTHETIC = 'Data-Sources/synthetic'
CONNECTED_DB = 'Data-Sources/synthetic/connected/medical-affairs.sqlite'


def main():
    ap = argparse.ArgumentParser(description='Locate or fetch the Data-Sources checkout.')
    ap.add_argument('--fetch', action='store_true', help='git clone Data-Sources into ./Data-Sources if missing')
    a = ap.parse_args()
    try:
        print(data_root(required=True))
        return 0
    except FileNotFoundError:
        if not a.fetch:
            print(HINT, file=sys.stderr)
            return 1
    r = subprocess.run(['git', 'clone', '--depth', '1', REPO_URL + '.git', str(ROOT / 'Data-Sources')])
    if r.returncode == 0:
        print(ROOT / 'Data-Sources')
    return r.returncode


if __name__ == '__main__':
    sys.exit(main())
