import githubAPI

g = githubAPI.GitHubAPI("NicholasSynovic", "nicholassynovic.github.io", token="b95550b589af46afd5fd46a5fdaea592e9f1f0a5")

print(type(g.get_CommitsRequestObj()))
