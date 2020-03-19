# all the imports
import os
import sqlite3
import pandas as pd
from flask import Flask, g, render_template
from contextlib import closing

# create our little application :)
app = Flask(__name__)

# configuration
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'SSL.db'),
))

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        db.commit()

@app.route('/')
def stacked_bar_chart():
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("SSL.db")
    df = pd.read_sql_query("SELECT * from MASTER", con)

    # verify that result of SQL query is stored in the dataframe
    print(df.to_json())

    con.close()

    date = df['date'].values.tolist() # x axis
    commits = df['commits'].values.tolist()
    issues = df['issues'].values.tolist()
    pull_requests = df['pull_requests'].values.tolist()

    return render_template('linegraph.html', date=date, commits=commits, issues=issues, pull_requests=pull_requests)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)