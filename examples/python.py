# Python 3.7.9

import requests

# By default, returns the 10 recent news headlines in the database.
url = "https://newscast-api.herokuapp.com/api"

response = requests.get(url)
results = response.json()['results']
results_length = response.json()['len']

print(f"Number of news articles returned: {results_length}")
print(*results, sep='\n')