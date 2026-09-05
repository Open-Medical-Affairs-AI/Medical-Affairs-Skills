---
name: data-connection
description: >-
  Connect Medical Affairs work to available data using authorized connectors, exported files or read-only database queries. Use when a task mentions Veeva, Salesforce, SharePoint, CRM, SQL or missing system access. Discover the actual platform and schema, map fields, and offer synthetic workshop inputs when appropriate.
license: Apache-2.0
metadata:
  version: "0.2.0"
  tier: data
  maturity: beta
  requires:
    - medical-affairs-foundations
  produces: Connection assessment, field mapping and sourced data extract
---

# Data Connection

Read [connections.md](../../docs/connections.md) for the platform-specific route.

1. Determine whether this is a workshop or real work. Workshop mode immediately
   uses [connected practice data](../../workshop/data/connected/README.md).
2. Inspect the host tools. Prefer an authorized existing connector. Otherwise use
   an approved export or local read-only query. Do not claim a connector is installed.
3. For Veeva, identify Vault CRM, Salesforce-based CRM, or another Vault application
   before choosing an API. Product names are not interchangeable schemas.
4. Inspect actual objects/tables, column names, data types, scope and row counts.
   Record the mapping, timezone, currencies, missing values and extraction date.
5. Join on stable IDs including therapeutic area for workshop data. Do not guess
   that an enquiry role is a particular HCP, or merge people by name alone.
6. Retrieve only what the task needs. Preserve source IDs and row counts so an
   analyst can reproduce the result. Read [execution.md](../../docs/execution.md).

The local practice database requires Python only:

```bash
python3 scripts/query_database.py --db workshop/data/connected/medical-affairs.sqlite --schema
python3 scripts/query_database.py --db workshop/data/connected/medical-affairs.sqlite --sql 'SELECT * FROM hcps LIMIT 5'
```

A cloud agent cannot see a laptop database automatically. Use an authorized local
agent, approved network connection or export. Never expose a database publicly to
make the demo work. Authentication belongs in supported sign-in/secret storage,
not a prompt, a source file or the public repository.

Report exactly what was connected, what scope was tested and what remains missing.
Real writes need user authorization and supported APIs; workshop values do not
provide that authorization. Read `house-rules/data-connection.md`.
