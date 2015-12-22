__author__ = 'sneha'
from lxml import html
import requests
import re
import csv
import matplotlib.pyplot as plt
import pylab as pl

def normalize(normalize_list,role):
    min_val = min(normalize_list)
    max_val = max(normalize_list)
    if role == 'batting' or role == 'fielding':
        for i in range(0,len(normalize_list)):
            normalize_list[i] = (normalize_list[i] - min_val) / (max_val - min_val)
    elif role == 'bowling':
        for i in range(0,len(normalize_list)):
            normalize_list[i] = (max_val - normalize_list[i]) / (max_val - min_val)
    return normalize_list

if __name__ == "__main__":
    australia_performance_index = []
    england_performance_index = []
    australia_fielding_index = []
    england_fielding_index = []
    australia_batting_index = []
    england_batting_index = []
    australia_bowling_index = []
    england_bowling_index = []
    australia_players = []
    england_players = []
    with open('fielding_data.csv', 'rb') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        for row in filereader:
            if row[2] == 'Australia':
                australia_players.append(row[0])
                australia_fielding_index.append(float(row[1]))
            else:
                england_players.append(row[0])
                england_fielding_index.append(float(row[1]))

australia_fielding_index = normalize(australia_fielding_index,'fielding')
england_fielding_index = normalize(england_fielding_index,'fielding')

with open('batting_data.csv', 'rb') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    for row in filereader:
        if row[4] == 'Australia':
            australia_batting_index.append((float(row[1])+float(row[2])+float(row[3]))/3)
        else:
            england_batting_index.append((float(row[1])+float(row[2])+float(row[3]))/3)

australia_batting_index = normalize(australia_batting_index,'batting')
england_batting_index = normalize(england_batting_index,'batting')

with open('bowling_data.csv', 'rb') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    for row in filereader:
        if row[4] == 'Australia':
            australia_bowling_index.append((float(row[1])+float(row[2])+float(row[3]))/3)
        else:
            england_bowling_index.append((float(row[1])+float(row[2])+float(row[3]))/3)

australia_bowling_index = normalize(australia_bowling_index,'bowling')
england_bowling_index = normalize(england_bowling_index,'bowling')

for i in range(0,len(australia_players)):
    australia_performance_index.append(0.2 * australia_fielding_index[i]+ 0.4 * australia_batting_index[i] + 0.4 * australia_bowling_index[i])
for i in range(0,len(england_players)):
    england_performance_index.append(0.2 * england_fielding_index[i]+0.4 * england_batting_index[i]+0.4 * england_bowling_index[i])

print australia_performance_index
print england_performance_index

print(sorted(australia_performance_index))
print(sorted(england_performance_index))

pl.figure(1)
x_length = range(len(australia_players))
pl.xticks(x_length, australia_players)
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)
fig = plt.gcf()
fig.subplots_adjust(bottom=0.25)
pl.title('Performance index of Australian Players')
pl.ylim(0,1)
pl.plot(x_length,australia_performance_index,"y")
pl.show()

pl.figure(1)
x_length = range(len(england_players))
pl.xticks(x_length, england_players)
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)
fig = plt.gcf()
fig.subplots_adjust(bottom=0.25)
pl.title('Performance index of English Players')
pl.ylim(0,1)
pl.plot(x_length,england_performance_index,"b")
pl.show()

