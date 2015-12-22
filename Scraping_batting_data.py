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

average_vs_england_index = []
average_aus_in_england_index = []
average_aus_in_2015_index = []
for i in range(0,len(australian_playerid)):
    url = 'http://stats.espncricinfo.com/ci/engine/player/' + australian_playerid[i] + '?class=1;template=results;type=' + "batting"
    player_page = requests.get(url,timeout=50)
    tree = html.fromstring(player_page.text)
    j = 1
    while(j<4):
        country = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[1]/tr['+str(j)+']/td[1]/b/text()')
        if country and country[0] == 'v England':
            header = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/thead/tr/th[2]/a/text()')
            if header[0] == 'Span':
                average_vs_england = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[1]/tr['+str(j)+']/td[8]/text()')
            else:
                average_vs_england = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[1]/tr['+str(j)+']/td[7]/text()')
            average_vs_england_index.append(float(average_vs_england[0]))
            break
        j = j + 1
    if(j == 4):
        average_vs_england_index.append(float(25))

    j = 1
    while(j<5):
        country = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[2]/tr['+str(j)+']/td[1]/b/text()')
        if country and country[0] == 'in England':
            header = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/thead/tr/th[2]/a/text()')
            if header[0] == 'Span':
                average_in_england = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[2]/tr['+str(j)+']/td[8]/text()')
            else:
                average_in_england = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[2]/tr['+str(j)+']/td[7]/text()')
            average_aus_in_england_index.append(float(average_in_england[0]))
            break
        j = j + 1
    if(j == 5):
        average_aus_in_england_index.append(float(20))

    j = 1
    while(j<15):
        year = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[5]/tr['+str(j)+']/td[1]/b/text()')
        if year and year[0] == 'year 2015':
            header = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/thead/tr/th[2]/a/text()')
            if header[0] == 'Span':
                average_in_2015 = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[5]/tr['+str(j)+']/td[8]/text()')
            else:
                average_in_2015 = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[5]/tr['+str(j)+']/td[7]/text()')
            average_aus_in_2015_index.append(float(average_in_2015[0]))
            break
        j = j + 1
    if(j == 15):
        average_aus_in_2015_index.append(float(30))


average_vs_australia_index = []
average_eng_in_england_index = []
average_eng_in_2015_index = []
for i in range(0,len(england_playerid)):
    url = 'http://stats.espncricinfo.com/ci/engine/player/' + england_playerid[i] + '?class=1;template=results;type=' + "batting"
    player_page = requests.get(url,timeout=50)
    tree = html.fromstring(player_page.text)
    j = 1
    while(j<4):
        country = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[1]/tr['+str(j)+']/td[1]/b/text()')
        if country and country[0] == 'v Australia':
            header = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/thead/tr/th[2]/a/text()')
            if header[0] == 'Span':
                average_vs_australia = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[1]/tr['+str(j)+']/td[8]/text()')
            else:
                average_vs_australia = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[1]/tr['+str(j)+']/td[7]/text()')
            average_vs_australia_index.append(float(average_vs_australia[0]))
            break
        j = j + 1
    if(j == 4):
        average_vs_australia_index.append(float(25))

    j = 1
    while(j<5):
        country = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[2]/tr['+str(j)+']/td[1]/b/text()')
        if country and country[0] == 'in England':
            header = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/thead/tr/th[2]/a/text()')
            if header[0] == 'Span':
                average_in_england = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[2]/tr['+str(j)+']/td[8]/text()')
            else:
                average_in_england = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[2]/tr['+str(j)+']/td[7]/text()')
            average_eng_in_england_index.append(float(average_in_england[0]))
            break
        j = j + 1
    if(j == 5):
        average_eng_in_england_index.append(float(40))

    j = 1
    while(j<15):
        year = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[5]/tr['+str(j)+']/td[1]/b/text()')
        if year and year[0] == 'year 2015':
            header = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/thead/tr/th[2]/a/text()')
            if header[0] == 'Span':
                average_in_2015 = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[5]/tr['+str(j)+']/td[8]/text()')
            else:
                average_in_2015 = tree.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[4]/tbody[5]/tr['+str(j)+']/td[7]/text()')
            average_eng_in_2015_index.append(float(average_in_2015[0]))
            break
        j = j + 1
    if(j == 15):
        average_eng_in_2015_index.append(float(30))

with open('batting_data.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    for i in range(0,len(australian_playerid)):
        a.writerows([[australian_players[i],average_vs_england_index[i],average_aus_in_england_index[i],average_aus_in_2015_index[i],'Australia']])
    for j in range(0,len(england_playerid)):
        a.writerows([[england_players[j],average_vs_australia_index[j],average_eng_in_england_index[j],average_eng_in_2015_index[j],'England']])
