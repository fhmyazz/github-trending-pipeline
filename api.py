import requests
import pandas as pd

url = "https://api.github.com/search/repositories"
params = {
    "q": "language:python",
    "sort": "stars",
    "order": "desc",
    "per_page": 10
}

response = requests.get(url, params=params)
print("Status Code: ", response.status_code)

data = response.json()
print("Total repos ditemukan: ", data["total_count"])
for i in range(3):
    print("Repos: ", data["items"][i]["full_name"])
    print("Stars: ", data["items"][i]["stargazers_count"])