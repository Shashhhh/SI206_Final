import sqlite3
import matplotlib.pyplot as plt


"""
    Plot a bar chart to visualize the distribution of books based on their current rank status.

    The function retrieves data from the 'Main_db.db' SQLite database to calculate the number of books
    that are currently still ranked and the number of books that are no longer ranked.
    It then writes this information to a file named 'current_books_ranked_results.txt'.
    The function creates a bar chart using Matplotlib to visualize the distribution of books
    based on their rank status, with labels indicating whether the books are currently still ranked
    or no longer ranked.
"""
def plot_bar_chart():
    conn = sqlite3.connect('Main_db.db')
    c = conn.cursor()

    # Calculate amount of books that still currently ranked
    c.execute("SELECT COUNT(*) FROM nyt_best_sellers WHERE current_rank IS NOT NULL")
    books_with_rank = c.fetchone()[0]

    # Calculate amount of books that are no longer ranked
    c.execute("SELECT COUNT(*) FROM nyt_best_sellers WHERE current_rank IS NULL")
    books_without_rank = c.fetchone()[0]

    conn.close()

    with open('current_books_ranked_results.txt', 'w') as file:
        file.write("{:<15}\t{:<15}\n".format("Still Ranked", "No Longer Ranked"))  # Adjusted spacing
        file.write("{:<15}\t{:<15}\n".format(books_with_rank, books_without_rank))  # Adjusted spacing

    # Create labels and counts for the bar plot
    labels = ['Currently Still Ranked', 'No Longer Ranked']
    counts = [books_with_rank, books_without_rank]

    # Plotting
    plt.bar(labels, counts, color=['blue', 'orange'])
    plt.title('Past NYT Ranked Books')
    plt.xlabel('Rank Status')
    plt.ylabel('Number of Books')
    plt.show()


plot_bar_chart()