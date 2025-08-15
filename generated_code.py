import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

try:
    url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
    response = requests.get(url)
    response.raise_for_status()

    tables = pd.read_html(response.text)
    df = tables[0]  # The first table contains the movie data

    titles = df['Title'].tolist()

    result = {
        "result": titles,
        "image": None,
        "error": None
    }
except Exception as e:
    result = {
        "result": None,
        "image": None,
        "error": str(e)
    }

import json
print(json.dumps(result))