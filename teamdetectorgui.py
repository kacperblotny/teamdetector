import re
import requests
import networkx as nx   
from pyvis.network import Network

def main(b,s):
    G = nx.Graph()

    battlemetricsPlayers = getPlayers(b)

    initialFriendList = getFriendList(s)
    friends = { initialFriendList['steamId']: initialFriendList['name']}
    leftToCheck = comparePlayers(battlemetricsPlayers, initialFriendList['friends'])
    for friend in leftToCheck:
        G.add_edges_from([(initialFriendList['name'], friend[1])])

    while True:
        if len(leftToCheck) == 0:
            break

        newLeft = []
        for steamId, name in leftToCheck:
            friendList = getFriendList(f'https://steamcommunity.com/profiles/{steamId}/friends')
            friends[friendList['steamId']] = friendList['name']
            for steamIdC, nameC in comparePlayers(battlemetricsPlayers, friendList['friends']):
                G.add_edges_from([(friendList['name'], nameC)])
                if steamIdC not in friends and not any(steamIdC in x for x in newLeft):
                    newLeft.append([steamIdC, nameC])

        leftToCheck = newLeft

    nt = Network('2000px', '2000px')
    nt.from_nx(G)
    nt.repulsion(damping=1)
    # nt.show('teamNetwork.html')
    nt.save_graph('teamNetwork.html')

    print('\n\nTeam Detector Result:\n')
    print('Name:'.ljust(34) + 'SteamID:'.ljust(19) + 'Link:')

    for steamId, name in friends.items():
        print(f'{name}'.ljust(34) + f'{steamId}'.ljust(19) + f'https://steamcommunity.com/profiles/{steamId}')
    print("\n\n")
    return name,steamId,friends,battlemetricsPlayers

def scrape(url):
    try:
        page = requests.get(url)
        return page.text
    except:
        print(f'Could not scrape: {url}')
        return False

def getPlayers(url):
    content = scrape(url)
    if content == False:
        print('Could not scrape Battlemetrics Server Page')
        exit()

    regex = r'<a class="css-zwebxb" href="/players/\d+?">(.+?)</a>'
    players = re.findall(regex, content)

    print(players)

    with open(r'players.txt', 'w') as fp:
        for item in players:
            fp.write("%s\n" % item)

    if len(players) == 0:
        print('Could not match players on the Battlemetrics Server Page.')
        exit()

    return players

def getFriendList(url):
    if not 'friends' in url:
        url += '/friends'

    content = scrape(url)
    if content == False:
        print('Could not scrape friend list page')
        exit()

    regex = r'<meta property="og:title" content="(.+?)">'
    name = re.findall(regex, content)[0]
    regex = r',"steamid":"(.+?)",'
    steamId = re.findall(regex, content)[0]
    regex = r'data-steamid="(.+?)".*?<div class="friend_block_content">(.+?)<br>'
    friends = re.findall(regex, content, re.MULTILINE|re.S)

    return {"name": name, "steamId": steamId, "friends": friends}

def comparePlayers(battlemetricsPlayers, friendList):
    players = []
    for steamId, name in friendList:
        if name in battlemetricsPlayers:
            players.append([steamId, name])

    return players


if __name__ == '__main__':
    main()