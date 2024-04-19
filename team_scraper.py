
import requests
from bs4 import BeautifulSoup as BS
import sqlite3
import json
import os

def create_database():
    conn = sqlite3.connect('main_db.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS NFL_teams (
                Team_id INTEGER PRIMARY KEY,
                Tm TEXT
                )''')
    conn.commit()
    conn.close()

def insert_data(data):
    conn = sqlite3.connect('main_db.db')
    c = conn.cursor()
    c.executemany("INSERT INTO NFL_teams (Tm) VALUES (?)", [(team,) for team in data])
    conn.commit()
    conn.close()

def get_last_id():
    conn = sqlite3.connect('main_db.db')
    c = conn.cursor()
    c.execute("SELECT MAX(id) FROM NFL_teams")
    last_id = c.fetchone()[0]
    conn.close()
    return last_id if last_id else 0 

URL ='https://www.pro-football-reference.com/years/2023/advanced.htm'

res = requests.get(URL)
soup = BS(res.content, 'html.parser')

table = soup.find('table', {'id': 'air_yards'})
data = []

for row in table.find_all('tr'):
    cols = row.find_all('th', {'data-stat': 'team'})
    for col in cols:
        col.find('a')
        data.append(col.text)
data = data[1:]
create_database()
last_id = get_last_id()
if last_id == 25:
    new_data = data[last_id:]
else:
    new_data = data[last_id:last_id+25]
insert_data(new_data)
  
