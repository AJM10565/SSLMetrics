import sqlite3
import os

def open_connection(repo_name):
    '''
This is some SQL code that creates the tables and columns in a database named after the repository its data is holding.
    '''    
    try:
        connection = sqlite3.connect('/metrics/' + str(repo_name) + '_historical.db')
    except sqlite3.OperationalError:
        connection = sqlite3.connect('/metrics/' + str(repo_name) + '_historical.db')

    cursor = connection.cursor()

    # Create table - COMMITS
    cursor.execute('''CREATE TABLE IF NOT EXISTS COMMITS
            (author VARCHAR(3000) ,
            comments_url VARCHAR(3000),
            author_date VARCHAR(3000),
            commits_url VARCHAR(3000),
            committer VARCHAR(3000),
            committer_date VARCHAR(3000),
            message VARCHAR(30000),
            comment_count VARCHAR(3000));''')
    
    # Create table - ISSUES
    cursor.execute('''CREATE TABLE IF NOT EXISTS ISSUES
            (user VARCHAR(3000) ,
                    user_id VARCHAR(3000) ,
                    issue_id VARCHAR(3000) ,
                    comments_url VARCHAR(3000) ,
                    node_id VARCHAR(3000) ,
                    number VARCHAR(3000) ,
                    title VARCHAR(3000) ,
                    labels VARCHAR(3000) ,
                    state VARCHAR(3000) ,
                    locked VARCHAR(3000) ,
                    assignee VARCHAR(3000) ,
                    assignees VARCHAR(3000) ,
                    comments VARCHAR(3000) ,
                    created_at VARCHAR(3000) ,
                    updated_at VARCHAR(3000) ,
                    closed_at VARCHAR(3000) ,
                    body VARCHAR(30000) ,
                    comment_user VARCHAR(3000) ,
                    comment_user_id VARCHAR(3000) ,
                    comment_id VARCHAR(3000) ,
                    issue_url VARCHAR(3000) ,
                    comment_node_id VARCHAR(3000) ,
                    comment_created_at VARCHAR(3000) ,
                    comment_updated_at VARCHAR(3000) ,
                    comment_body VARCHAR(3000)) ;''')

            # Create table - PULL_REQUESTS
    cursor.execute('''CREATE TABLE IF NOT EXISTS PULLREQUESTS
            (user VARCHAR(3000) ,
                    user_id VARCHAR(3000) ,
                    pull_req_id VARCHAR(3000) ,
                    comments_url VARCHAR(3000) ,
                    node_id VARCHAR(3000) ,
                    number VARCHAR(3000) ,
                    title VARCHAR(30000) ,
                    labels VARCHAR(3000) ,
                    state VARCHAR(3000) ,
                    locked VARCHAR(3000) ,
                    assignee VARCHAR(3000) ,
                    assignees VARCHAR(3000) ,
                    created_at VARCHAR(3000) ,
                    updated_at VARCHAR(3000) ,
                    closed_at VARCHAR(3000) ,
                    body VARCHAR(30000) ,
                    comment_user VARCHAR(3000) ,
                    comment_user_id VARCHAR(3000) ,
                    comment_id VARCHAR(3000) ,
                    comment_node_id VARCHAR(3000) ,
                    comment_created_at VARCHAR(3000) ,
                    comment_updated_at VARCHAR(3000) ,
                    comment_body VARCHAR(3000)) ;''')

            # Create table - MASTER
    cursor.execute('''CREATE TABLE IF NOT EXISTS MASTER
            (date VARCHAR(300) ,
            commits INT(3000),
            issues INT(3000),
            pull_requests INT(3000));''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS LINES_OF_CODE_NUM_OF_CHARS
            (date VARCHAR(300) ,
            oid VARCHAR(3000),
            total_lines VARCHAR(3000),
            total_chars VARCHAR(3000));''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS DEFECT_DENSITY
            (date VARCHAR(300) ,
            DD VARCHAR(3000));''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ISSUE_SPOILAGE
            (date VARCHAR(300) ,
            Min VARCHAR(3000),
            Max VARCHAR(300),
            Avg VARCHAR(300));''')
            
    connection.commit()
    
    return cursor, connection
