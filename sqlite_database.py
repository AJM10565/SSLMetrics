import sqlite3

def open_connection(repo_name):
    
    conn = sqlite3.connect('database/' + str(repo_name) + '_historical.db')
    c = conn.cursor()

    # Create table - COMMITS
    c.execute('''CREATE TABLE IF NOT EXISTS COMMITS
            (author VARCHAR(3000) ,
            comments_url VARCHAR(3000),
            author_date VARCHAR(3000),
            commits_url VARCHAR(3000),
            committer VARCHAR(3000),
            committer_date VARCHAR(3000),
            message VARCHAR(30000),
            comment_count VARCHAR(3000));''')
    
    # Create table - ISSUES
    c.execute('''CREATE TABLE IF NOT EXISTS ISSUES
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
    c.execute('''CREATE TABLE IF NOT EXISTS PULLREQUESTS
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
    c.execute('''CREATE TABLE IF NOT EXISTS MASTER
            (date VARCHAR(300) ,
            commits INT(3000),
            issues INT(3000),
            pull_requests INT(3000));''')


    conn.commit()
    
    return c, conn
