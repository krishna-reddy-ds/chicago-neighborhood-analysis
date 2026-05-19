import time
import requests
import pandas as pd
from config import *

def census_api_get(url, params):
    if API_KEY:
        params["key"] = API_KEY
    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, timeout=90)
            if resp.status_code == 200:
                return resp.json()
            time.sleep(1.0)
        except Exception as e:
            if attempt == 2:
                print(f"API error: {e}")
            time.sleep(1.0)
    return None

def fetch_ca_blockgroups(ca_id, tract_list, year="2022"):
    api_url = ACS2022 if year == "2022" else ACS2014
    var_list = list(VARIABLES.keys())
    records = []

    for tract in tract_list:
        params = {
            "get": ",".join(var_list + ["NAME"]),
            "for": "block group:*",
            "in": f"state:{STATE} county:{COUNTY} tract:{tract}"
        }
        data = census_api_get(api_url, params)
        if not data:
            continue

        header, *rows = data
        for row in rows:
            record = dict(zip(header, row))
            record["ca_id"] = ca_id
            record["ca_name"] = CAS[ca_id]
            record["year"] = year
            record["geoid_bg"] = f"{record['state']}{record['county']}{record['tract']}{record['block group']}"
            records.append(record)
        time.sleep(0.3)

    return pd.DataFrame(records)
