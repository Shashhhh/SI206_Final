import sqlite3
import json
import requests

def read_api_key(file_path="api_key_alex.txt"):
    with open(file_path, "r") as file:
        api_key = file.read().strip()
        return api_key


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


def insert_data(data, table):
    conn = sqlite3.connect('Main_db.db')
    c = conn.cursor()
    c.executemany(f"INSERT INTO {table} (name, current_rank) VALUES (?, ?)", data)
    conn.commit()
    conn.close()


def get_last_id(table):
    conn = sqlite3.connect('Main_db.db')
    c = conn.cursor()
    c.execute(f"SELECT MAX(book_id) FROM {table}")
    last_id = c.fetchone()[0]
    conn.close()
    return last_id if last_id else 0 


def insert(data, table):
    last_id = get_last_id(table)
    if (last_id < 100):
        insert_data(data, table)


api_key = read_api_key()
base_url = "https://api.nytimes.com/svc/books/v3"
book_data = []
for i in range(0, 161, 40):
    book_info = requests.get(f"{base_url}/lists/best-sellers/history.json?api-key={api_key}&offset={i}").json()
    
    for book in book_info['results']:
        title = book['title']
        rank = None

        if 'ranks_history' in book and len(book['ranks_history']) > 0:
            rank = book['ranks_history'][0]['rank']

        book_data.append((title, rank))
            

create_database()
last_id = get_last_id('nyt_best_sellers')
book_data = book_data[last_id:last_id+25]
insert(book_data, 'nyt_best_sellers')
