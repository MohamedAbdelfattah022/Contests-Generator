from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
from flask_caching import Cache
import pandas as pd
import sqlite3
import requests
from fetch_problemset import fetch
from handles import merge_solved_problems

app = Flask(__name__)
app.secret_key = 'e9aa5b78bce79caa06c445b364058979840b1ab60338fdc6'

app.config['data_fetched'] = False
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

@app.before_request
def initialize_data():  
    if not app.config['data_fetched']:
        try:
            fetch()
            app.config['data_fetched'] = True
            print("Data Fetched")
        except (requests.ConnectionError, requests.HTTPError) as e:
            print("Failed to fetch data:", e)
    else:
        print("Data Already Fetched")

@cache.memoize(timeout=300)
def retrieve_data(min_range, max_range, problems_num):
    conn = sqlite3.connect("problemset.db")
    query = f"SELECT * FROM problems WHERE rating >= {min_range} AND rating <= {max_range}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df.sample(problems_num)

def get_codes(frame):
    codes = []
    for i in range(len(frame)):
        code = f"{int(frame['contestId'].iloc[i])}{frame['index'].iloc[i]}"
        codes.append(code)
    return ', '.join(codes)

@app.route('/')
def index():
    error_message = get_flashed_messages(category_filter=['error'])
    return render_template('index.html', error_message=error_message)

@cache.memoize(timeout=300)
def get_unsolved_problems(handles, min_range, max_range):
    conn = sqlite3.connect("problemset.db")
    query = f"SELECT * FROM problems WHERE rating >= {min_range} AND rating <= {max_range}"
    all_problems = pd.read_sql(query, conn)
    conn.close()

    solved_problems = merge_solved_problems(handles)
    solved_problems_codes = solved_problems.apply(lambda row: f"{int(row['contestId'])}{row['index']}", axis=1)

    unsolved_problems = all_problems[~all_problems.apply(lambda row: f"{int(row['contestId'])}{row['index']}", axis=1).isin(solved_problems_codes)]
    
    return unsolved_problems

@app.route('/result/', methods=['POST'])
def result():
    min_range = int(request.form['min_range'])
    max_range = int(request.form['max_range'])
    problems_num = int(request.form['problems_num'])
    participant_type = request.form.get('participant_type')
    
    if max_range < min_range:
        flash("Max range must be greater than or equal to Min range.", "error")
        return redirect(url_for('index'))

    handles = []
    if participant_type == 'individual':
        handles = [request.form.get('individual_handle')]
    else:
        handles = [request.form.get(f'team_handle_{i}') for i in range(1, 4) if request.form.get(f'team_handle_{i}')]
    
    print(f"\n{'='*10} {len(handles)} {'='*10}\n")
    print(f"\n{'='*10} {handles} {'='*10}\n")

    if (len(handles) == 1 and handles[0] == '' ) or (len(handles) == 0) :
        print("No Handle")
        df = retrieve_data(min_range, max_range, problems_num)
    else:
        print("Using Handle")
        unsolved_df = get_unsolved_problems(handles, min_range, max_range)
        df = unsolved_df.sample(problems_num)
    codes = get_codes(df)

    return render_template('result.html', codes=codes)

if __name__ == '__main__':
    app.run(debug=True)
