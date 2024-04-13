
import requests
from bs4 import BeautifulSoup as BS
import sqlite3
import json
import os

def create_database():
    conn = sqlite3.connect('fantasy_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS fantasy_stats (
                Player TEXT,
                Tm TEXT,
                Pos TEXT,
                Age TEXT,
                G TEXT,
                GS TEXT,
                Tgt TEXT,
                Rec TEXT,
                PassingYds TEXT,
                PassingTD TEXT,
                PassingAtt TEXT,
                RushingYds TEXT,
                RushingTD TEXT,
                RushingAtt TEXT,
                ReceivingYds TEXT,
                ReceivingTD TEXT,
                FantasyPoints TEXT,
                Int TEXT,
                Fumbles TEXT,
                FumblesLost TEXT
                )''')
    conn.commit()
    conn.close()

def insert_data(data):
    conn = sqlite3.connect('fantasy_data.db')
    c = conn.cursor()
    c.executemany("INSERT INTO fantasy_stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

URL = 'https://www.pro-football-reference.com/years/2023/fantasy.htm'
res = requests.get(URL)
soup = BS(res.content, 'html.parser')
table = soup.find('table', {'id': 'fantasy'})
data = []