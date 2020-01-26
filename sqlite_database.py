import sqlite3


def open_connection(repo_name):

    conn = sqlite3.connect('database/' + str(repo_name) + '_historical.db')
    c = conn.cursor()

    # Create table - COMMITS
    c.execute('''CREATE TABLE IF NOT EXISTS COMMITS
            (author VARCHAR(300) ,
            comments_url VARCHAR(300),
            author_date VARCHAR(300),
            commits_url VARCHAR(300),
            committer VARCHAR(300),
            committer_date VARCHAR(300),
            message VARCHAR(3000),
            comment_count VARCHAR(300));''')

    # Create table - ISSUES
    c.execute('''CREATE TABLE IF NOT EXISTS ISSUES
            (user VARCHAR(300) ,
                user_id VARCHAR(300) ,
                issue_id VARCHAR(300) ,
                comments_url VARCHAR(300) ,
                node_id VARCHAR(300) ,
                number VARCHAR(300) ,
                title VARCHAR(300) ,
                labels VARCHAR(300) ,
                state VARCHAR(300) ,
                locked VARCHAR(300) ,
                assignee VARCHAR(300) ,
                assignees VARCHAR(300) ,
                comments VARCHAR(300) ,
                created_at VARCHAR(300) ,
                updated_at VARCHAR(300) ,
                closed_at VARCHAR(300) ,
                body VARCHAR(3000) ,
                comment_user VARCHAR(300) ,
                comment_user_id VARCHAR(300) ,
                comment_id VARCHAR(300) ,
                issue_url VARCHAR(300) ,
                comment_node_id VARCHAR(300) ,
                comment_created_at VARCHAR(300) ,
                comment_updated_at VARCHAR(300) ,
                comment_body VARCHAR(300)) ;''')

    conn.commit()

    return c, conn
