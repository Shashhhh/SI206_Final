import sqlite3
import matplotlib.pyplot as plt

team_colors = {
    'Arizona Cardinals': '#97233F',    # Cardinal Red
    'Atlanta Falcons': '#A71930',       # Falcon Red
    'Baltimore Ravens': '#241773',      # Raven Purple
    'Buffalo Bills': '#00338D',         # Bills Blue
    'Carolina Panthers': '#0085CA',     # Panther Blue
    'Chicago Bears': '#0B162A',         # Bear Navy Blue
    'Cincinnati Bengals': '#FB4F14',    # Bengal Orange
    'Cleveland Browns': '#311D00',      # Brown Orange
    'Dallas Cowboys': '#041E42',        # Cowboys Navy Blue
    'Denver Broncos': '#002244',        # Bronco Navy Blue
    'Detroit Lions': '#0076B6',         # Lion Blue
    'Green Bay Packers': '#203731',     # Packer Green
    'Houston Texans': '#03202F',        # Texan Navy Blue
    'Indianapolis Colts': '#002C5F',    # Colt Blue
    'Jacksonville Jaguars': '#006778',  # Jaguar Teal
    'Kansas City Chiefs': '#E31837',    # Chief Red
    'Las Vegas Raiders': '#000000',      # Raider Black
    'Los Angeles Chargers': '#002A5E',  # Charger Navy Blue
    'Los Angeles Rams': '#002244',      # Ram Navy Blue
    'Miami Dolphins': '#008E97',        # Dolphin Aqua
    'Minnesota Vikings': '#4F2683',     # Viking Purple
    'New England Patriots': '#002244',  # Patriot Blue
    'New Orleans Saints': '#D3BC8D',    # Saint Gold
    'New York Giants': '#0B2265',       # Giant Blue
    'New York Jets': '#125740',         # Jet Green
    'Philadelphia Eagles': '#004C54',   # Eagle Green
    'Pittsburgh Steelers': '#FFB612',   # Steeler Gold
    'San Francisco 49ers': '#AA0000',   # 49er Scarlet Red
    'Seattle Seahawks': '#69BE28',      # Seahawk Green
    'Tampa Bay Buccaneers': '#D50A0A',  # Buccaneer Red
    'Tennessee Titans': '#0C2340',      # Titan Navy Blue
    'Washington Commanders': '#773141'  # Washington Burgundy
}

def plot_players_by_team():
    """
    Plot the number of players with Fantasy Points > 200 for each NFL team.

    This function retrieves data from the SQLite database 'Main_db.db', counts the number of players 
    with Fantasy Points > 200 for each NFL team, and plots the results using matplotlib.

    Returns:
    - None
    """
    conn = sqlite3.connect('Main_db.db')
    c = conn.cursor()

    c.execute('''
        SELECT NFL_teams.Tm AS Team_name, COUNT(*) AS num_players_over_200
        FROM NFL_teams
        INNER JOIN fantasy_stats ON NFL_teams.Team_id = fantasy_stats.Team_id
        WHERE fantasy_stats.FantasyPoints > 200
        GROUP BY NFL_teams.Tm
    ''')

    results = c.fetchall()
    with open('players_by_team_results.txt', 'w') as file:
        file.write("Team\tNumber of Players\n")
        for row in results:
            team = row[0]
            num = row[1]
            file.write(f"{team}\t{num}\n")
    c.close()
    conn.close()

    teams = [row[0] for row in results]
    num_players = [row[1] for row in results]

    plt.figure(figsize=(14, 8))
    bars = plt.bar(teams, num_players)

    for bar, team in zip(bars, teams):
        bar.set_color(team_colors.get(team, 'gray'))  

    plt.xlabel('Team')
    plt.ylabel('Number of Players with Fantasy Points > 200')
    plt.title('Number of Players on Each Team with Fantasy Points > 200')

    for bar, num in zip(bars, num_players):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05, num, ha='center', va='bottom')

    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

plot_players_by_team()
