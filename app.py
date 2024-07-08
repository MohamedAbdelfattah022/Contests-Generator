from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
import pandas as pd
import sqlite3
import requests
from fetch_problemset import fetch

app = Flask(__name__)
app.secret_key = 'e9aa5b78bce79caa06c445b364058979840b1ab60338fdc6'

app.config['data_fetched'] = False

@app.before_request
def initialize_data():
    if not app.config['data_fetched']:
        try:
            fetch()
            app.config['data_fetched'] = True
            print("data fetched")
        except (requests.ConnectionError, requests.HTTPError) as e:
            print("Failed to fetch data:", e)

def retrieve_data(min_range, max_range, problems_num):
    # try:
    #     fetch()
    # except (requests.ConnectionError, requests.HTTPError) as e:
    #     pass

    conn = sqlite3.connect("problemset.db")
    query = f"SELECT * FROM problems WHERE rating >= {min_range} AND rating <= {max_range}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df.sample(problems_num)

def get_codes(frame):
    codes = []
    for i in range(len(frame)):
        code = f"{frame['contestId'].iloc[i]}{frame['index'].iloc[i]}"
        codes.append(code)
    return ', '.join(codes)

@app.route('/')
def index():
    error_message = get_flashed_messages(category_filter=['error'])
    return render_template('index.html', error_message=error_message)

@app.route('/result/', methods=['POST'])
def result():
    min_range = int(request.form['min_range'])
    max_range = int(request.form['max_range'])
    problems_num = int(request.form['problems_num'])

    if max_range < min_range:
        flash("Max range must be greater than or equal to Min range.", "error")
        return redirect(url_for('index'))

    df = retrieve_data(min_range, max_range, problems_num)
    codes = get_codes(df)

    return render_template('result.html', codes=codes)

if __name__ == '__main__':
    app.run(debug=True)
