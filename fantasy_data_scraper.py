import requests
from bs4 import BeautifulSoup as BS
import sqlite3
nfl_teams = [
    'ARI',  # Arizona Cardinals
    'ATL',  # Atlanta Falcons
    'BAL',  # Baltimore Ravens
    'BUF',  # Buffalo Bills
    'CAR',  # Carolina Panthers
    'CHI',  # Chicago Bears
    'CIN',  # Cincinnati Bengals
    'CLE',  # Cleveland Browns
    'DAL',  # Dallas Cowboys
    'DEN',  # Denver Broncos
    'DET',  # Detroit Lions
    'GNB',   # Green Bay Packers
    'HOU',  # Houston Texans
    'IND',  # Indianapolis Colts
    'JAX',  # Jacksonville Jaguars
    'KAN',   # Kansas City Chiefs
    'LVR',   # Las Vegas Raiders
    'LAC',  # Los Angeles Chargers
    'LAR',  # Los Angeles Rams
    'MIA',  # Miami Dolphins
    'MIN',  # Minnesota Vikings
    'NWE',   # New England Patriots
    'NOR',   # New Orleans Saints
    'NYG',  # New York Giants
    'NYJ',  # New York Jets
    'PHI',  # Philadelphia Eagles
    'PIT',  # Pittsburgh Steelers
    'SFO',   # San Francisco 49ers
    'SEA',  # Seattle Seahawks
    'TAM',   # Tampa Bay Buccaneers
    'TEN',  # Tennessee Titans
    'WAS',  # Washington Football Team
    '2TM',
    '3TM',
]
def create_database():
    conn = sqlite3.connect('main_db.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS fantasy_stats (
                id INTEGER PRIMARY KEY,
                Team_id INTEGER,
                Player TEXT,
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

#inserts data into database
#list of tups
def insert_data(data):
    conn = sqlite3.connect('main_db.db')
    c = conn.cursor()
    c.executemany("INSERT INTO fantasy_stats (Team_id, Player, Pos, Age, G, GS, PassingAtt, PassingYds, PassingTD, RushingAtt, RushingYds, RushingTD, Tgt, Rec, ReceivingYds, ReceivingTD, FantasyPoints) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
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
        selected_cols = [cols[i] for i in [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 14, 15, 16, 17, 19, 26]] #Only grabs relevant stats
        team_col = selected_cols[1] #grabs team str
        data_cols = []
        data_cols.append(str(nfl_teams.index(team_col)+ 1)) #converts team str to int
        #stitch data back together
        selected_cols = [selected_cols[i] for i in range(len(selected_cols)) if i != 1]
        data_cols.extend(selected_cols);
        data.append(data_cols)

#Cleans the data
data = [row for row in data if row[0] != 'Player']
data = [[ele.split('*')[0].strip() if '*' in ele else ele for ele in row] for row in data]

#Converts str data to float values
for row in data:
    for i in range(3, len(row)):
        try:
            row[i] = float(row[i])
        except ValueError:
            pass  

create_database()
last_id = get_last_id()
if (last_id < 200):
    new_data = data[last_id:last_id+25]
    insert_data(new_data)

