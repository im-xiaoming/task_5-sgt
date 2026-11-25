import requests
import os


def export(
    headers,
    base_url='http://localhost:8069/json/2/crm.lead',
    endpoint='search_read',
):
    res = requests.post(
        url=f'{base_url}/{endpoint}',
        headers=headers,
        json={
            'domain': [],
            'fields': [
                'id', 'name', 'email_from',
                'phone', 'expected_revenue',
            ],
        },
    )
    try:
        res.raise_for_status()
    except Exception as e:
        return None
    
    import pandas as pd
    df = pd.DataFrame(res.json())
    df.to_excel('leads.xlsx', index=False)

    return res


def check_duplicate_by_email(
    headers,
    email,
    base_url='http://localhost:8069/json/2/crm.lead',
    endpoint='search_read',
    limit=1
):
    res = requests.post(
        url=f'{base_url}/{endpoint}',
        headers=headers,
        json={
            'domain': [
                ['email_from', '=ilike', email]
            ],
            'fields': ['id', 'name'],
            'limit': limit,
        },
    )
    try:
        res.raise_for_status()
    except Exception as e:
        return None
    return res


def update(
    headers,
    ids: list[int],
    payload: dict,
    base_url='http://localhost:8069/json/2/crm.lead',
    endpoint='write',
):
    res = requests.post(
        url=f'{base_url}/{endpoint}',
        headers=headers,
        json={
            'ids': ids,
            'vals': payload
        },
    )
    try:
        res.raise_for_status()
    except Exception as e:
        return None
    return res



def create(
    headers,
    payloads: list[dict],
    base_url='http://localhost:8069/json/2/crm.lead',
    endpoint='create',
):
    res = requests.post(
        url=f'{base_url}/{endpoint}',
        headers=headers,
        json={
            'vals_list': payloads
        }
    )

    try:
        res.raise_for_status()
    except Exception as e:
        return None
    
    return res
    