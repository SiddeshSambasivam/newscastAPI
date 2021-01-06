import requests

url = "https://newscast-api.herokuapp.com/api"
response = requests.get(url)
result = response.json()["results"]