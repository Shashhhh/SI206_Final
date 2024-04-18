from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
from bs4 import BeautifulSoup as BS
import sqlite3

def read_api_key(file_path="api_key.txt"):
    with open(file_path, "r") as file:
        api_key = file.read().strip()
        return api_key
    
api_key = read_api_key()

def create_database(table):
    conn = sqlite3.connect('CFB_teams.db')
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY,
                School TEXT,
                Talent FLOAT
                )''')
    conn.commit()
    conn.close()

def insert_data(data, table):
    conn = sqlite3.connect('CFB_teams.db')
    c = conn.cursor()
    c.executemany(f"INSERT INTO {table} (School, Talent) VALUES (?, ?)", data)
    conn.commit()
    conn.close()

def get_last_id(table):
    conn = sqlite3.connect('CFB_teams.db')
    c = conn.cursor()
    c.execute(f"SELECT MAX(id) FROM {table}")
    last_id = c.fetchone()[0]
    conn.close()
    return last_id if last_id else 0 


configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = api_key
configuration.api_key_prefix['Authorization'] = 'Bearer'

api_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))
year = 2023

try:
    api_response = api_instance.get_talent(year=year)
except ApiException as e:
    print("Exception when calling TeamsApi->get_talent: %s\n" % e)
data = []

for team in api_response:
    data.append((team.school, team.talent))

create_database('team_talent')
last_id = get_last_id('team_talent')
new_data = data[last_id:last_id+25]
insert_data(new_data, 'team_talent')