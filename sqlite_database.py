import sqlite3


def open_connection_users(since):
    conn2 = sqlite3.connect('database/' + 'users_since' + str(since) + '_historical.db')
    c = conn2.cursor()
    # Create Table Users
    c.execute('''CREATE TABLE IF NOT EXISTS USERS
                  (
                      login VARCHAR(3000) ,
                      id VARCHAR(3000) ,
                      node_id VARCHAR(3000) ,
                      avatar_url VARCHAR(3000) ,
                      gravatar_id VARCHAR(3000) ,
                      url VARCHAR(30000) ,
                      html_url VARCHAR(3000) ,
                      followers_url VARCHAR(3000) ,
                      following_url VARCHAR(3000) ,
                      gists_url VARCHAR(3000) ,
                      starred_url VARCHAR(3000) ,
                      subscriptions_url VARCHAR(3000) ,
                      organizations_url VARCHAR(3000) ,
                      repos_url VARCHAR(3000) ,
                      events_url VARCHAR(30000) ,
                      received_events_url VARCHAR(3000) ,
                      type VARCHAR(3000) ,
                      site_admin VARCHAR(3000)) ;''')
    # Create table - MASTER
    c.execute('''CREATE TABLE IF NOT EXISTS USER_MASTER
                (users INT(3000));''')
    conn2.commit()
    return c, conn2


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
                comment_body VARCHAR(3000))
                ;''')

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
                comment_body VARCHAR(3000));''')
    # Create table - MASTER
    c.execute('''CREATE TABLE IF NOT EXISTS MASTER
            (date VARCHAR(300) ,
            commits INT(3000),
            issues INT(3000),
            pull_requests INT(3000));''')

    conn.commit()

    return c, conn
