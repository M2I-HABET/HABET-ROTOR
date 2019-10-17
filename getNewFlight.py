import requests
import time
import json



r = requests.post('http://10.29.188.15/REST/V1/new_flight')
json_data = json.loads(r.text)
flightID = json_data["flightID"]
scriptID = json_data["scriptID"]
print("Flight:" + flightID)
print("script:" + scriptID)
