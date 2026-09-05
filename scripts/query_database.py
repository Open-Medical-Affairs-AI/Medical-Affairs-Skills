#!/usr/bin/env python3
"""Query an existing local SQLite file read-only. No remote access or drivers.

python3 scripts/query_database.py --db workshop/data/connected/medical-affairs.sqlite --schema
python3 scripts/query_database.py --db workshop/data/connected/medical-affairs.sqlite --sql 'SELECT * FROM hcps LIMIT 5'
"""
import argparse
import json
from pathlib import Path
import sqlite3
import time


def connect_readonly(path):
    path = Path(path).resolve(strict=True)
    connection = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
    connection.execute('PRAGMA query_only=ON')
    denied = {sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH, sqlite3.SQLITE_INSERT,
              sqlite3.SQLITE_UPDATE, sqlite3.SQLITE_DELETE, sqlite3.SQLITE_PRAGMA}
    def authorize(action, arg1, arg2, database, trigger):
        if action in denied or (action == sqlite3.SQLITE_FUNCTION and (arg2 or '').lower() == 'load_extension'):
            return sqlite3.SQLITE_DENY
        return sqlite3.SQLITE_OK
    connection.set_authorizer(authorize)
    deadline = time.monotonic() + 5
    connection.set_progress_handler(lambda: int(time.monotonic() > deadline), 1000)
    return connection


def query(path, sql, limit=200):
    connection = connect_readonly(path)
    try:
        cursor = connection.execute(sql)
        columns = [c[0] for c in cursor.description or []]
        rows = cursor.fetchmany(limit + 1)
        return {'columns': columns, 'rows': rows[:limit], 'truncated': len(rows) > limit,
                'row_limit': limit, 'query': sql}
    finally:
        connection.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--db', type=Path, required=True)
    choice = ap.add_mutually_exclusive_group(required=True)
    choice.add_argument('--sql')
    choice.add_argument('--schema', action='store_true')
    ap.add_argument('--limit', type=int, default=200)
    args = ap.parse_args()
    if not 1 <= args.limit <= 1000:
        ap.error('limit must be 1..1000')
    sql = "SELECT name, sql FROM sqlite_master WHERE type IN ('table','view') ORDER BY name" if args.schema else args.sql
    try:
        print(json.dumps(query(args.db, sql, args.limit), indent=2))
    except (OSError, sqlite3.Error) as exc:
        print(json.dumps({'status': 'error', 'reason': str(exc)}))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
