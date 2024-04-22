import sqlite3
import matplotlib.pyplot as plt

def plot_fantasy_stats():
    """
    Plot the number of fantasy players with Fantasy Points > 200 by position.

    This function retrieves data from the SQLite database 'main_db.db', counts the number of players 
    by position whose FantasyPoints are greater than 200, normalizes the count by the number of teams
    for each position, and plots the results using matplotlib.

    Returns:
    - None
    """
    conn = sqlite3.connect('main_db.db')
    c = conn.cursor()

    c.execute('''
        SELECT Pos, COUNT(*) AS num_players
        FROM fantasy_stats
        WHERE FantasyPoints > 200
        GROUP BY Pos
    ''')

    results = c.fetchall()
    with open('fantasy_stats_results.txt', 'w') as file:
        file.write("Position\tNormalized Number of Players\n")
        for row in results:
            pos = row[0]
            num = row[1]
            if pos == 'WR':
                normalized_num = num / 96
            else:
                normalized_num = num / 32
            file.write(f"{pos}\t{normalized_num}\n")
    c.close()
    conn.close()

    positions = [row[0] for row in results]
    num_players = [row[1] for row in results]

    normalized_num_players = []
    for pos, num in zip(positions, num_players):
        if pos == 'WR':
            normalized_num_players.append(num / 96)
        else:
            normalized_num_players.append(num / 32)

    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']

    plt.figure(figsize=(10, 6))
    bars = plt.bar(positions, normalized_num_players, color=colors[:len(positions)])

    plt.xlabel('Position')
    plt.ylabel('Normalized Number of Players with Fantasy Points > 200')
    plt.title('Normalized Number of Fantasy Players with Fantasy Points > 200 by Position')

    plt.tight_layout()
    plt.show()

plot_fantasy_stats()
