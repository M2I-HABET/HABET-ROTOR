import requests
import time
import json



r = requests.post('http://cytracking.com/REST/V1/new_flight')
print(r)
json_data = json.loads(r.text)
flightID = json_data["flightID"]
scriptID = json_data["scriptID"]
print("Flight:" + flightID)
print("script:" + scriptID)
