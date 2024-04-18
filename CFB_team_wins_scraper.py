from __future__ import print_function
import cfbd
from cfbd.rest import ApiException
import CFB_talent_scraper as scraper
from bs4 import BeautifulSoup as BS
import sqlite3
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = scraper.api_key
configuration.api_key_prefix['Authorization'] = 'Bearer'
api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
year = 2023

def create_database(table):
     conn = sqlite3.connect('CFB_teams.db')
     c = conn.cursor()
     c.execute(f'''CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY,
                Wins INT
                )''')
     conn.commit()
     conn.close()


def get_team_wins(table):
    conn = sqlite3.connect('CFB_teams.db')
    c = conn.cursor()
    last_id = scraper.get_last_id(table)
    for i in range(last_id, last_id + 25):
        c.execute(f"SELECT * FROM {table} WHERE id=?", (i,))
        team = c.fetchone()
        try:
            api_response = api_instance.get_team_records(year=year, team = team)
        except ApiException as e:
            print("Exception when calling GamesApi->get_team_records: %s\n" % e)

data = []

create_database('team_wins')
get_team_wins('team_talent')