import sqlite3

def init_db():
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_url(short_code, original_url):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO urls (short_code, original_url) VALUES (?, ?)',
                   (short_code, original_url))
    conn.commit()
    conn.close()

def get_original_url(short_code):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_all_urls():
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT short_code, original_url, created_at FROM urls ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows