from __future__ import print_function
import cfbd
from cfbd.rest import ApiException
import sqlite3

def read_api_key(file_path="api_key.txt"):
    with open(file_path, "r") as file:
        api_key = file.read().strip()
        return api_key

def create_database():
    conn = sqlite3.connect('Main_db.db')
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS CFB_teams (
                id INTEGER PRIMARY KEY,
                School TEXT,
                Talent FLOAT,
                Wins INTEGER
                )''')
    conn.commit()
    conn.close()

def insert_data(data, table):
    conn = sqlite3.connect('Main_db.db')
    c = conn.cursor()
    c.executemany(f"INSERT INTO {table} (School, Talent, Wins) VALUES (?, ?, ?)", data)
    conn.commit()
    conn.close()

def get_last_id(table):
    conn = sqlite3.connect('Main_db.db')
    c = conn.cursor()
    c.execute(f"SELECT MAX(id) FROM {table}")
    last_id = c.fetchone()[0]
    conn.close()
    return last_id if last_id else 0 

def inserter(data, table):
    last_id = get_last_id(table)
    if (last_id < 200):
        insert_data(data, table)


api_key = read_api_key()
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = api_key
configuration.api_key_prefix['Authorization'] = 'Bearer'
talent_api = cfbd.TeamsApi(cfbd.ApiClient(configuration))
wins_api = cfbd.GamesApi(cfbd.ApiClient(configuration))
year = 2023

try:
    api_response = talent_api.get_talent(year=year)
except ApiException as e:
    print("Exception when calling TeamsApi->get_talent: %s\n" % e)

create_database()
data = []
last_id = get_last_id('CFB_teams')
api_response = api_response[last_id:last_id+25]
for team in api_response:
    wins_response = wins_api.get_team_records(year=year, team = team.school)
    data.append((team.school, team.talent, wins_response[0].total.wins))


inserter(data, 'CFB_teams')