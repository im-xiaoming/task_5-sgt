import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('ODOO_MCP_KEY')

url = 'http://localhost:8069/json/2/crm.lead'

payload = {
    "name": "Minh Phát Trading - ERP solution",
    "contact_name": "Phương Trần",
    "partner_name": "Minh Phát Trading",
    "email_from": "phương.trần.1@example.com",
    "phone": "0945108603",
    "stage_id": 1,
    "expected_revenue": 10000000,
    "probability": 40,
    "recurring_revenue": 0,
    "city": "Bien Hoa",
    "country_id": 241,
    "description": "AI chatbot. Requested more information about available plans.",
    "date_open": "2026-10-15"
}

headers = {
    'Authorization': f"bearer {api_key}",
    'Content-Type': "application/json"
}


# create
# res = requests.post(
#     url=f'{url}/create',
#     headers=headers,
#     json={
#         'vals_list': [payload]
#     }
# )

# read

# res = requests.post(
#     url=f'{url}/search_read',
#     headers=headers,
#     json={
#         'domain': [
#             ['email_from', '=ilike', payload['email_from']]
#         ],
#         'fields': ['id', 'name'],
#         'limit': 5,
#     },
# )

# res = requests.post(
#     url=f'{url}/write',
#     headers=headers,
#     json={
#         'ids': [48],
#         'vals': {
#             'phone': '0912345678',
#             'expected_revenue': 20000000,
#         },
#     },
# )

res = requests.post(
    url=f'{url}/search_read',
    headers=headers,
    json={
        'domain': [],
        'fields': [
            'id', 'name', 'email_from',
            'phone', 'expected_revenue',
        ],
    },
)

import pandas as pd

df = pd.DataFrame(res.json())
# df.to_excel('leads.xlsx', index=False)
print(df.head())

print(res.status_code)

