# Flask Codeforces Problem Fetcher
- [Flask Codeforces Problem Fetcher](#flask-codeforces-problem-fetcher)
  - [Description](#description)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Contributing](#contributing)

## Description

This Flask application fetches random problems from Codeforces based on the user's specified minimum and maximum rating range and the number of problems desired. It fetches the desired number of problems within the specified range randomly to help practicing. It utilizes a SQLite database to store problem data and provides a simple web interface for users to interact with.

## Features

- Fetch random Codeforces problems within a specified rating range.
- Simple web interface for user input.
- Error handling for invalid input.
- Utilizes SQLite database for storing problem data.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MohamedAbdelfattah022/Contests-Generator-Flask.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   <br>
   Use `run_app.bat` script to open the app directly or using the following command
   ```bash
   python app.py
   ```

## Usage

1. Open the application in your web browser.
2. Enter the minimum and maximum rating range for Codeforces problems.
3. Specify the number of problems you want to fetch.
4. Click on the "Fetch Problems" button.
5. View the list of randomly fetched problem codes.

## Configuration

- You can modify the SQLite database (problemset.db) to include additional problem data or update existing data using `fetch_problemset.py` scraping script.
- Adjust the secret_key in app.py for session security.

## Contributing

- Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.
