import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def fetch_data():
    """
    Fetch talent and wins data from the 'CFB_teams' table in the SQLite database.

    Returns:
    - list of tuples: List of tuples containing talent and wins data.
    """
    conn = sqlite3.connect('Main_db.db')
    c = conn.cursor()
    c.execute("SELECT Talent, Wins FROM CFB_teams")
    data = c.fetchall()
    conn.close()
    return data

def plot_talent_vs_wins(data):
    """
    Plot talent vs wins, and fit a linear regression line.

    Parameters:
    - data (list of tuples): List of tuples containing talent and wins data.
    
    Returns:
    - None
    """
    talents = [row[0] for row in data]
    wins = [row[1] for row in data]

    plt.scatter(talents, wins, label='Data')
    plt.title('Talent vs Wins (R = {:.2f})'.format(stats.pearsonr(talents, wins)[0])) 
    plt.xlabel('Talent')
    plt.ylabel('Wins')
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(talents, wins)
    line = slope * np.array(talents) + intercept
    plt.plot(talents, line, color='red', label='Linear Regression')

    plt.legend()
    plt.grid(True)
    plt.show()
    
    with open('talent_vs_wins_results.txt', 'w') as file:
        file.write("Talent\tWins\n")
        for talent, win in zip(talents, wins):
            file.write(f"{talent}\t{win}\n")

data = fetch_data()
plot_talent_vs_wins(data)
