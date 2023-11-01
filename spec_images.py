import pandas as pd
import numpy as np
import requests, json
import sys

client_id = secrets.BNET_CLIENT_ID
client_secret = secrets.BNET_CLIENT_SECRET

def create_access_token(client_id, client_secret, region = 'us'):
    data = { 'grant_type': 'client_credentials' }
    response = requests.post('https://%s.battle.net/oauth/token' % region, data=data, auth=(client_id, client_secret))
    return response.json()

token = create_access_token(client_id, client_secret)['access_token']
print(token)
