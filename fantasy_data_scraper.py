
import requests
from bs4 import BeautifulSoup as BS
import sqlite3
import json
import os

def create_database():
    conn = sqlite3.connect('main_db.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS fantasy_stats (
                id INTEGER PRIMARY KEY,
                Player TEXT,
                Tm TEXT,
                Pos TEXT,
                Age FLOAT,
                G FLOAT,
                GS FLOAT,
                PassingAtt FLOAT,
                PassingYds FLOAT,
                PassingTD FLOAT,
                RushingAtt FLOAT,
                RushingYds FLOAT,
                RushingTD FLOAT,
                Tgt FLOAT,
                Rec FLOAT,
                ReceivingYds FLOAT,
                ReceivingTD FLOAT,
                FantasyPoints FLOAT
                )''')
    conn.commit()
    conn.close()

def insert_data(data):
    conn = sqlite3.connect('main_db.db')
    c = conn.cursor()
    c.executemany("INSERT INTO fantasy_stats (Player, Tm, Pos, Age, G, GS, PassingAtt, PassingYds, PassingTD, RushingAtt, RushingYds, RushingTD, Tgt, Rec, ReceivingYds, ReceivingTD, FantasyPoints) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

def get_last_id():
    conn = sqlite3.connect('main_db.db')
    c = conn.cursor()
    c.execute("SELECT MAX(id) FROM fantasy_stats")
    last_id = c.fetchone()[0]
    conn.close()
    return last_id if last_id else 0 

URL = 'https://www.pro-football-reference.com/years/2023/fantasy.htm'

res = requests.get(URL)
soup = BS(res.content, 'html.parser')
table = soup.find('table', {'id': 'fantasy'})
data = []

for row in table.find_all('tr'):
    cols = row.find_all('td')
    if cols:
        cols = [ele.text.strip() for ele in cols]
        selected_cols = [cols[i] for i in [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 14, 15, 16, 17, 19, 26]]
        data.append(selected_cols)

data = [row for row in data if row[0] != 'Player']
data = [[ele.split('*')[0].strip() if '*' in ele else ele for ele in row] for row in data]

for row in data:
    for i in range(3, len(row)):
        try:
            row[i] = float(row[i])
        except ValueError:
            pass  

create_database()
last_id = get_last_id()
new_data = data[last_id:last_id+25]
insert_data(new_data)

