from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
from flask_caching import Cache
import pandas as pd
import requests
from fetch_problemset import fetch
from handles import merge_solved_problems

app = Flask(__name__)
app.secret_key = 'e9aa5b78bce79caa06c445b364058979840b1ab60338fdc6'

app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

@cache.memoize(timeout=300)
def retrieve_data(min_range, max_range):
    df = fetch()
    filtered_df = df[(df['rating'] >= min_range) & (df['rating'] <= max_range)]
    return filtered_df

def get_codes(frame):
    codes = [f"{int(frame['contestId'].iloc[i])}{frame['index'].iloc[i]}" for i in range(len(frame))]
    return ', '.join(codes)

@app.route('/')
def index():
    error_message = get_flashed_messages(category_filter=['error'])
    return render_template('index.html', error_message=error_message)

@cache.memoize(timeout=300)
def get_unsolved_problems(handles, min_range, max_range):
    all_problems = fetch()
    filtered_problems = all_problems[(all_problems['rating'] >= min_range) & (all_problems['rating'] <= max_range)]
    
    solved_problems = merge_solved_problems(handles)
    solved_problems_codes = solved_problems.apply(lambda row: f"{int(row['contestId'])}{row['index']}", axis=1)
    
    unsolved_problems = filtered_problems[~filtered_problems.apply(lambda row: f"{int(row['contestId'])}{row['index']}", axis=1).isin(solved_problems_codes)]
    
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

    if len(handles) == 0 or (len(handles) == 1 and handles[0] == ''):
        print("No Handle")
        df = retrieve_data(min_range, max_range).sample(problems_num)
    else:
        print("Using Handle")
        unsolved_df = get_unsolved_problems(handles, min_range, max_range)
        df = unsolved_df.sample(problems_num)

    codes = get_codes(df)

    return render_template('result.html', codes=codes)

if __name__ == '__main__':
    app.run(debug=True)
