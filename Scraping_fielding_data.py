__author__ = 'sneha'
from lxml import html
import requests
import re
import csv

australia_squad_page = requests.get('http://www.espncricinfo.com/the-ashes-2015/content/squad/857481.html')
tree = html.fromstring(australia_squad_page.text)
australian_players = tree.xpath('//a[contains(@href, "/the-ashes-2015/content/player/")]/text()')

for i in range(0,len(australian_players)):
    australian_players[i] = australian_players[i].strip()

australian_playerid = tree.xpath('//div[@class="large-13 medium-13 small-13 columns"]/h3/a/@href')
for i in range(0,len(australian_playerid)):
    australian_playerid[i] = australian_playerid[i].split('/')[-1]


england_squad_page = requests.get('http://www.espncricinfo.com/the-ashes-2015/content/squad/892997.html')
tree = html.fromstring(england_squad_page.text)
england_players = tree.xpath('//a[contains(@href, "/the-ashes-2015/content/player/")]/text()')

for i in range(0,len(england_players)):
    england_players[i] = england_players[i].strip()

england_playerid = tree.xpath('//div[@class="large-13 medium-13 small-13 columns"]/h3/a/@href')
for i in range(0,len(england_playerid)):
    england_playerid[i] = england_playerid[i].split('/')[-1]


australian_fielding_index = []
fielding_list = []
for i in range(0,len(australian_playerid)):
    url = 'http://stats.espncricinfo.com/ci/engine/player/' + australian_playerid[i] + '?class=1;template=results;type=' + "fielding"
    player_page = requests.get(url,timeout=50)
    tree = html.fromstring(player_page.text)
    matches_played = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[3]/tbody/tr/td[3]/text()')
    catches_taken = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[3]/tbody/tr/td[5]/text()')
    if matches_played:
        australian_fielding_index.append(float(catches_taken[0])/float(matches_played[0]))
    else:
        australian_fielding_index.append(0.25)

for i in range(0,len(australian_playerid)):
    fielding_list.append([australian_players[i],australian_fielding_index[i],'Australia'])

england_fielding_index = []
for i in range(0,len(england_playerid)):
    url = 'http://stats.espncricinfo.com/ci/engine/player/' + england_playerid[i] + '?class=1;template=results;type=' + "fielding"
    player_page = requests.get(url,timeout=50)
    tree = html.fromstring(player_page.text)
    matches_played = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[3]/tbody/tr/td[3]/text()')
    catches_taken = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[3]/tbody/tr/td[5]/text()')
    if matches_played:
        england_fielding_index.append(float(catches_taken[0])/float(matches_played[0]))
    else:
        england_fielding_index.append(0.25)

for i in range(0,len(england_playerid)):
    fielding_list.append([england_players[i],england_fielding_index[i],'England'])

with open('fielding_data.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    for i in range(0,len(australian_playerid)):
        a.writerows([fielding_list[i]])
    for j in range(0,len(england_playerid)):
        a.writerows([fielding_list[i+j+1]])