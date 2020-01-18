import sqlite3

def open_connection(repo_name):
    
    conn = sqlite3.connect('database/' + str(repo_name) + '_historical.db')
    c = conn.cursor()

    # Create table - CLIENTS
    c.execute('''CREATE TABLE IF NOT EXISTS COMMITS
            (author VARCHAR(300) ,
            comments_url VARCHAR(300),
            author_date VARCHAR(300),
            commits_url VARCHAR(300),
            committer VARCHAR(300),
            committer_date VARCHAR(300),
            message VARCHAR(3000),
            comment_count VARCHAR(300));''')
    
    conn.commit()
    
    return c, conn
