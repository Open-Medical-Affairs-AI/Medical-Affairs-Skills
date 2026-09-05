# Connect your work data when you are ready

**For the workshop, skip setup.** The agent can use the bundled CSV files and
SQLite practice database immediately. These resemble business records, not exact
Veeva or Salesforce schemas. They are not connected to any real company system.

## Tell the agent

> Find the data needed for this job using my available authorized tools. If this
> is a workshop, use the synthetic pack. For real work, show the missing access
> and the simplest connector or export route. Never substitute fictional facts.

The agent should first inventory its tools, then the actual system and objects.
For every connection, record the tenant/system, permitted scope, extraction date,
source object, selected fields, filters, row count and pagination completeness.
Do not show credentials in that report.

## Choose the route

| System | Preferred starting route | If unavailable |
|---|---|---|
| Veeva Vault CRM | Approved connector or the supported Vault CRM API for your tenant | Approved account/interaction export |
| Veeva CRM on Salesforce | Approved connector or Salesforce APIs for your deployment | CSV export with IDs and object definitions |
| Other Veeva Vault applications | Vault API with the correct application, API version and permissions | Document/object export with version metadata |
| Salesforce | Existing authorized connector; otherwise organization-approved OAuth application | Reports exported as CSV, with stable record IDs |
| SharePoint/OneDrive | Existing authorized Microsoft connector or Microsoft Graph | Downloaded permitted files and a document inventory |
| Local SQLite | Read-only local helper provided here | CSV tables |
| PostgreSQL, SQL Server, Snowflake or another database | Approved connector or a local database client with read-only credentials | Scoped SQL extract or CSV with data dictionary |

## Veeva: identify the product first

Ask the administrator which product and platform the organization uses. Vault CRM,
Salesforce-based Veeva CRM, and Vault document applications require different
objects and access paths. Do not substitute Salesforce field names for Vault fields.

1. Use the tenant URL and supported authentication supplied through the approved
   connector or administrator setup. The agent should not ask for a password in chat.
2. Inspect the accessible metadata. For Vault, confirm available API versions and
   object/document definitions; for Salesforce-based CRM, use object describe.
3. Start with one scoped read: a permitted account, interaction set or document list.
4. Map the real fields to account ID, HCP ID, interaction date, source text, status
   and document version. Treat names as labels, not join keys.
5. Confirm record visibility, pagination and field permissions before summarizing.

Tenant workflows, approval states and custom objects vary. This repository provides
the connection procedure and mapping discipline, not a pre-authorized Veeva session.
Official sources: [Vault API reference](https://developer.veevavault.com/api/) and
[Vault CRM developer portal](https://developer.veevacrm.com/).

## Salesforce

1. Check whether the agent already has an authorized Salesforce connector and the
   relevant records are visible to that user.
2. If not, the administrator configures a supported OAuth application and the
   API access required for the actual task. Use normal sign-in and secret storage.
3. Discover the supported API version using `/services/data/`, then inspect
   `/services/data/vXX.X/sobjects/` and the chosen object `/describe` endpoint.
   `vXX.X` is a placeholder to replace with a version returned by the tenant.
4. Use scoped read queries through the connector or REST query endpoint. Follow
   `nextRecordsUrl` until complete or explicitly report the extraction limit.
5. Review an extract and its mapping with the user before relying on custom fields.

Avoid assuming that Account means a hospital, that Contact includes all HCPs, or
that the user has access to every field. A viewable record is not permission to
modify it. See [Salesforce REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest.htm).

## SharePoint and OneDrive

1. Prefer the host Microsoft connector and sign in with the intended work identity.
2. Select the permitted sites/libraries and retrieve a small known document.
3. When building an approved Graph integration, choose the narrowest appropriate
   delegated or application permissions. Selected permissions require both consent
   and explicit grants to the target resources; consent alone is not access.
4. Preserve site/library, item ID, filename, modified time, version or eTag and
   source URL. Distinguish approved, superseded and draft versions.
5. For repeated synchronization, use supported pagination/delta behavior and record
   deletions or changed versions. A cached document is not necessarily current.

Official source: [Microsoft Graph selected permissions](https://learn.microsoft.com/en-us/graph/permissions-selected-overview).

## Local databases

The workshop database is already built:

```bash
python3 scripts/query_database.py --db workshop/data/connected/medical-affairs.sqlite --schema
python3 scripts/query_database.py --db workshop/data/connected/medical-affairs.sqlite --sql "SELECT h.country, COUNT(*) AS records FROM interactions i JOIN hcps h ON i.hcp_id=h.hcp_id GROUP BY h.country"
```

This helper uses SQLite read-only mode, blocks attachments and writes, limits
returned rows and interrupts expensive queries. It does not connect to remote SQL
servers. For a real database, use its supported driver or connector, discover the
schema, and test a bounded SELECT with the approved read-only role.

A cloud agent cannot reach `localhost` on your laptop. An authorized local agent,
approved private connection or export is needed. Do not expose ports publicly for
the workshop. Keep connection strings outside the repository and use the host
secret manager. Verify the data processing environment before accessing real data.

## Administrator handoff

If setup needs an administrator, produce a concise request containing:

- The business task, system and intended user/service identity.
- Specific objects, fields, sites or tables; read-only scope by default.
- The supported connector/API and authentication method.
- Processing location, retention expectation and a small acceptance query.
- Who can approve access and how it will be revoked.

Do not claim an application is installed, a connection is active, or a write occurred
until the tool result confirms it. Tenant-specific integrations require a tenant
test; the local workshop tests cannot validate them.
