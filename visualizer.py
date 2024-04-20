import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('main_db.db')
c = conn.cursor()

c.execute('''
    SELECT NFL_teams.Tm AS Team_name, COUNT(*) AS num_players_over_200
    FROM NFL_teams
    INNER JOIN fantasy_stats ON NFL_teams.Team_id = fantasy_stats.Team_id
    WHERE fantasy_stats.FantasyPoints > 200
    GROUP BY NFL_teams.Tm
''')

results = c.fetchall()

c.close()
conn.close()

teams = [row[0] for row in results]
num_players = [row[1] for row in results]

plt.figure(figsize=(10, 6))
plt.bar(teams, num_players, color='skyblue')
plt.xlabel('Team')
plt.ylabel('Number of Players with Fantasy Points > 200')
plt.title('Number of Players on Each Team with Fantasy Points > 200')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
