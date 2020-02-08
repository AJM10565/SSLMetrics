# Import statements
import sys

import requests


def main(user_id, headers, c, conn2):
    user_details = requests.get("https://api.github.com/users?since=" + str(user_id) + ">; rel='next'", headers=headers)
    counter = user_id
    while user_details:
        if not user_details.json():
            print("There are no users!")

        else:
            for users in user_details.json():
                login = "None"
                id = "None"
                node_id = "None"
                avatar_url = "None"
                gravatar_id = "None"
                url = "None"
                html_url = "None"
                followers_url = "None"
                following_url = "None"
                gists_url = "None"
                starred_url = "None"
                subscriptions_url = "None"
                organizations_url = "None"
                repos_url = "None"
                events_url = "None"
                received_events_url = "None"
                type = "None"
                site_admin = "None"

                login = users["login"]
                id = users["id"]
                node_id = users["node_id"]
                avatar_url = users["avatar_url"]
                gravatar_id = users["gravatar_id"]
                url = users["url"]
                html_url = users["html_url"]
                followers_url = users["followers_url"]
                following_url = users["following_url"]
                gists_url = users["gists_url"]
                starred_url = users["starred_url"]
                subscriptions_url = users["subscriptions_url"]
                organizations_url = users["organizations_url"]
                repos_url = users["repos_url"]
                events_url = users["events_url"]
                received_events_url = users["received_events_url"]
                type = users["type"]
                site_admin = users["site_admin"]

                sql = "INSERT INTO Users (login, id, node_id, avatar_url, gravatar_id, url, html_url, followers_url, following_url, gists_url, starred_url, subscriptions_url,organizations_url, repos_url, events_url, received_events_url, type,  site_admin) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
                c.execute(sql, (
                    str(login), str(id), str(node_id), str(avatar_url), str(gravatar_id), str(url),
                    str(html_url), str(followers_url), str(following_url), str(gists_url), str(starred_url),
                    str(subscriptions_url),
                    str(organizations_url), str(repos_url), str(events_url), str(received_events_url),
                    str(type), str(site_admin)))

                conn2.commit()
            try:
                link = user_details.headers['link']
                # print(link)
                if "next" not in link:
                    user_details = False
                # Should be a comma separated string of links
                links = link.split(',')

                for link in links:
                    # If there is a 'next' link return the URL between the angle brackets, or None
                    if 'rel="next"' in link:
                        user_details = requests.get((link[link.find("<") + 1:link.find(">")]), headers=headers)
                        print((link[link.find("<") + 1:link.find(">")]))

            except Exception as e:
                print(e)
                user_details = False
