# Odoo CRM Lead Importer

A Python script that imports leads from a CSV file into Odoo CRM using the JSON-2 API. It checks each email address before creating a lead and updates the first matching lead when one already exists.

## Requirements

- Python with support for the versions pinned in `requirements.txt`.
- An Odoo instance exposing the JSON-2 API with the CRM app installed.
- An Odoo API key belonging to a user with permission to read, create, and update CRM leads.

The default endpoint is `http://localhost:8069/json/2/crm.lead`.

## Setup

Run these commands from the project directory in PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```dotenv
ODOO_MCP_KEY=your_odoo_api_key
```

The `.env` file is excluded by `.gitignore`. Keep the actual key out of source control.

For a different Odoo server, change the default `base_url` in the functions in `api.py`, or pass it explicitly when calling those functions. Changing `url` in `main.py` alone does not change the helper functions' endpoints.

## CSV input

The included `odoo_dummy_leads.csv` contains 30 sample leads, with these columns:

```text
name,contact_name,partner_name,email_from,phone,stage_id,expected_revenue,probability,recurring_revenue,city,country_id,description,date_open
```

| Field | Meaning |
| --- | --- |
| `name` | Lead title |
| `contact_name` | Contact person's name |
| `partner_name` | Company name |
| `email_from` | Email used for duplicate matching |
| `phone` | Phone number; preserve as text |
| `stage_id` | Existing CRM stage record ID |
| `expected_revenue` | Expected revenue amount |
| `probability` | Probability from 0 to 100 |
| `recurring_revenue` | Recurring revenue amount |
| `city` | City name |
| `country_id` | Existing country record ID |
| `description` | Lead notes |
| `date_open` | Opening date, supplied as `YYYY-MM-DD` |

The sample uses `stage_id=1`, `country_id=241`, and `recurring_revenue=0`. Verify that the stage and country IDs refer to the intended records in your database. `date_open` is the opening date, not the record creation timestamp. Odoo assigns each new lead's `id` automatically.

## Run the importer

```powershell
.\venv\Scripts\python.exe main.py
```

Run from the project directory so the script can find the CSV. This writes to your Odoo database:

1. Load each CSV row as a payload.
2. Search for a lead with an email matching case-insensitively.
3. Create the lead if no match is found.
4. Otherwise, update the first matching lead with the CSV values.

The script prints `Create!` or `Update!` for each processed row. These messages indicate the branch taken; the current script does not verify the helper's response before printing them.

## API helpers

The functions in `api.py` use POST requests and return a `requests.Response` on success, or `None` when the HTTP status check fails.

| Function | Purpose |
| --- | --- |
| `check_duplicate_by_email(headers, email, ..., limit=1)` | Find matching lead IDs and names |
| `create(headers, payloads, ...)` | Create leads from a list of dictionaries |
| `update(headers, ids, payload, ...)` | Update specified lead IDs |
| `export(headers, ...)` | Fetch selected lead fields and write `leads.xlsx` |

For example, fetch matching leads without running the importer:

```python
import os
from dotenv import load_dotenv
from api import check_duplicate_by_email

load_dotenv()
headers = {
    "Authorization": f"bearer {os.environ['ODOO_MCP_KEY']}",
    "Content-Type": "application/json",
}

response = check_duplicate_by_email(headers, "contact@example.com")
if response is not None:
    print(response.json())
```

## Export to Excel

The export helper needs an Excel writer. Install `openpyxl`, which is not currently listed in `requirements.txt`:

```powershell
.\venv\Scripts\python.exe -m pip install openpyxl
```

Using the `headers` from the example above:

```python
from api import export

response = export(headers)
if response is not None:
    print("Saved leads.xlsx")
```

This exports `id`, `name`, `email_from`, `phone`, and `expected_revenue` to the current directory, replacing an existing `leads.xlsx`. It exports record data rather than an Odoo Spreadsheet's formulas, charts, or layout. `main.py` does not call this helper automatically.

## Current limitations and troubleshooting

- **Phone leading zeros:** `main.py` currently uses pandas' default CSV type inference, which can remove leading zeros. To preserve phone numbers, change its read call to `pd.read_csv('odoo_dummy_leads.csv', dtype={'phone': str})` before importing.
- **Duplicate handling:** Only the first matching email is updated. This does not merge existing duplicates or prevent simultaneous import processes from creating duplicates.
- **HTTP failures:** Helpers return `None` for failed HTTP status checks. The importer calls `.json()` directly on the duplicate lookup result, so a failed lookup can stop it with a `NoneType` error. Inspect the HTTP response in `api.py` to diagnose the original failure.
- **Connection failures:** Check that Odoo is running and reachable on the configured host and port. Network exceptions are not caught by the helpers.
- **404 errors:** Verify the endpoint and JSON-2 availability. These helpers already use POST.
- **Authentication or permission errors:** Check `ODOO_MCP_KEY` and the API user's CRM access rights. Deployments requiring explicit database selection may also need an `X-Odoo-Database` header.
- **Invalid related record IDs:** Check the CSV's `stage_id` and `country_id` values against your Odoo database.

## Project files

```text
main.py                CSV import and create/update loop
api.py                 Odoo API helper functions
odoo_dummy_leads.csv    Sample lead data
requirements.txt       Pinned Python dependencies
.gitignore             Excludes .env and venv
```
