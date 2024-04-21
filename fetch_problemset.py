import pandas as pd
import requests
import json
import sqlite3

url = "https://codeforces.com/api/problemset.problems"
prblmset = requests.get(url)

problemset = json.loads(prblmset.text)

problems = problemset['result']['problems']

df = pd.DataFrame(problems).drop(['points','type'],axis=1)

def convert(tags):
    return ', '.join(tags)

df['tags'] = df['tags'].apply(lambda x: convert(x))

conn = sqlite3.connect("problemset.db")

df.to_sql('problems', conn, if_exists='replace', index=False)

conn.close()