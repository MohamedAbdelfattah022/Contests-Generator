import pandas as pd
import requests
import json
import sqlite3

def fetch():
    url = "https://codeforces.com/api/problemset.problems"
    prblmset = requests.get(url)
    problemset = json.loads(prblmset.text)

    problems = problemset['result']['problems']
    df = pd.DataFrame(problems).drop(['points', 'type'], axis=1)
    df['tags'] = df['tags'].apply(lambda x: ', '.join(x))

    return df