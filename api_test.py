import requests
import json

url = "https://sandbox.tradier.com/v1/"

access_token = "ZLHHCC0Z5mzm4V2zK5Odp5ijTZEl"

headers = {"Accept": "application/json",
           "Authorization": "Bearer ZLHHCC0Z5mzm4V2zK5Odp5ijTZEl"}

params = {"symbol": "GOOG"}

requestResponse = requests.get(url + "markets/history", params=params, headers=headers)

print(requestResponse.json())
