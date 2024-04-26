import sqlite3
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('Main_db.db')
c = conn.cursor()

# Query the database to get the counts of books with and without a rank
c.execute("SELECT COUNT(*) FROM nyt_best_sellers WHERE current_rank IS NOT NULL")
books_with_rank = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM nyt_best_sellers WHERE current_rank IS NULL")
books_without_rank = c.fetchone()[0]

# Close the database connection
conn.close()

# Create labels and counts for the bar plot
labels = ['Currently Still Ranked', 'No Longer Ranked']
counts = [books_with_rank, books_without_rank]

# Plotting
plt.bar(labels, counts, color=['blue', 'orange'])
plt.title('Past NYT Ranked Books')
plt.xlabel('Rank Status')
plt.ylabel('Number of Books')
plt.show()