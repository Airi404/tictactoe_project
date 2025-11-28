import requests
response = requests.get("https://api.agify.io?name=meelad")
response_json = response.json()
print(response_json)