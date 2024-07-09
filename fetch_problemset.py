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

    conn = sqlite3.connect("problemset.db")
    df.to_sql('problems', conn, if_exists='replace', index=False)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_rating ON problems (rating)")
    
    conn.close()