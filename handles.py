import pandas as pd
import requests
import json

def convert(tags):
    return ', '.join(tags)

def get_solved_problems(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    
    data = requests.get(url)
    jsonObject = json.loads(data.text)

    if jsonObject["status"] == "FAILED":
        return pd.DataFrame()

    results = jsonObject["result"]
    results_df = pd.DataFrame(results)

    solved = results_df.loc[results_df["verdict"] == "OK"]
    solved = solved["problem"].drop_duplicates().reset_index(drop=True)
    
    for i in range(len(solved)):
        solved[i]['tags'] = convert(solved[i]['tags'])

    df = pd.json_normalize(solved).drop(["type", "points", "problemsetName"], axis=1, errors='ignore')

    return df

def merge_solved_problems(handles):
    all_solved_problems = []
    
    for handle in handles:
        solved = get_solved_problems(handle)
        all_solved_problems.append(solved)
    
    if all_solved_problems:
        df = pd.concat(all_solved_problems, ignore_index=True)
        df = df.drop_duplicates()
        return df.dropna()
    else:
        return pd.DataFrame()
