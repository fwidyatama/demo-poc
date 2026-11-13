# Order Desk

A small Flask app where customers track their orders, search products and download invoices.

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
flask --app orderdesk init-db
flask --app orderdesk users create alice alice@example.com --admin
flask --app orderdesk run --debug
```

## Code scanning

Every pull request is scanned by Code Vuln through SmartX (`.github/workflows/codevuln.yml`): only the lines the pull
request adds or changes are audited. The result appears as an overview comment, one comment per finding and a
`codevuln` commit status, and the findings are tracked in SmartX. The check is warn-only.

The job runs on a self-hosted runner, so it runs only for branches of this repository, never for forks.
