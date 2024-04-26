import sqlite3
import json
import requests


"""
   Read API key from hidden text file.
   
   Parameters:
   - file_path (str): Path to the text file containing the API key. Default is "api_key_alex.txt".
   
   Returns:
   - str: API key read from the file.
"""
def read_api_key(file_path="api_key_alex.txt"):
    with open(file_path, "r") as file:
        api_key = file.read().strip()
        return api_key


"""
    Create a SQLite database and a table for storing New York Times best sellers data if it does not exist.
    
    The function establishes a connection to the SQLite database file named 'Main_db.db'.
    If the database file does not exist, it creates one.
    It then creates a table named 'nyt_best_sellers' if it does not already exist.
    The table has three columns:
    - book_id: INTEGER PRIMARY KEY, serves as a unique identifier for each book
    - name: TEXT, stores the name of the book
    - current_rank: INTEGER, stores the current rank of the book

    There are no paramaters or returns
"""
def create_database():
    conn = sqlite3.connect('Main_db.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS nyt_best_sellers (
            book_id INTEGER PRIMARY KEY,
            name TEXT,
            current_rank INTEGER
            )''')
    conn.commit()
    conn.close()


"""
    Insert data into a specified table in a SQLite database.
    
    Parameters:
    - data (list of tuples): The data to be inserted into the table. Each tuple represents a row of data.
    - table (str): The name of the table where the data will be inserted.
"""
def insert_data(data, table):
    conn = sqlite3.connect('Main_db.db')
    c = conn.cursor()
    c.executemany(f"INSERT INTO {table} (name, current_rank) VALUES (?, ?)", data)
    conn.commit()
    conn.close()


"""
   Get the last ID from the table in the SQLite database.

   Returns:
   - int: Last ID from the 'nyt_best_seller' table.
   - table (str): The name of the table where the data will be inserted.
"""
def get_last_id(table):
    conn = sqlite3.connect('Main_db.db')
    c = conn.cursor()
    c.execute(f"SELECT MAX(book_id) FROM {table}")
    last_id = c.fetchone()[0]
    conn.close()
    return last_id if last_id else 0 


"""
   Insert data into the table in the SQLite database.

   Parameters:
   - data (list of tuples): Data to be inserted into the table.
   - table (str): The name of the table where the data will be inserted.
"""
def insert(data, table):
    last_id = get_last_id(table)
    if (last_id < 100):
        insert_data(data, table)


"""
    Retrieve book data from the New York Times API.
    
    Parameters:
    - base_url (str): The base URL of the New York Times API.
    - api_key (str): The API key required for accessing the New York Times API.
    
    Returns:
    - list of tuples: A list containing tuples of book data. Each tuple contains the book title and its rank.
"""
def get_data(base_url, api_key):
    book_data = []
    for i in range(0, 161, 40):
        book_info = requests.get(f"{base_url}/lists/best-sellers/history.json?api-key={api_key}&offset={i}").json()
        
        for book in book_info['results']:
            title = book['title']
            rank = None

            if 'ranks_history' in book and len(book['ranks_history']) > 0:
                rank = book['ranks_history'][0]['rank']

            book_data.append((title, rank))

    return book_data


api_key = read_api_key()
base_url = "https://api.nytimes.com/svc/books/v3"
book_data = create_database(base_url, api_key)
last_id = get_last_id('nyt_best_sellers')
book_data = book_data[last_id:last_id+25]
insert(book_data, 'nyt_best_sellers')
