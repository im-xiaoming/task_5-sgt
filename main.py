import requests
import os
from dotenv import load_dotenv
from api import *
import pandas as pd


load_dotenv()

api_key = os.getenv('ODOO_MCP_KEY')

url = 'http://localhost:8069/json/2/crm.lead'
headers = {
    'Authorization': f"bearer {api_key}",
    'Content-Type': "application/json"
}


df = pd.read_csv('odoo_dummy_leads.csv')
payloads = []
for _, row in df.iterrows():
    payloads.append(row.to_dict())

for payload in payloads:
    lead = check_duplicate_by_email(headers,
                                     email=payload['email_from'], limit=1).json()
    if not lead:
        create(headers, [payload])
        print("Create!")
    else:
        try:
            id = lead[0]['id']
            update(headers, ids=[id], payload=payload)
            print("Update!")
        except Exception as e:
            print(e)