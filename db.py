
import sqlite3
import json

def init_db():
    conn = sqlite3.connect("ocr_results.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ocr_text TEXT,
        translation TEXT,
        entities TEXT
    )''')
    conn.commit()
    conn.close()

def insert_record(ocr_text, translation, entities):
    conn = sqlite3.connect("ocr_results.db")
    c = conn.cursor()
    c.execute("INSERT INTO results (ocr_text, translation, entities) VALUES (?, ?, ?)",
              (ocr_text, translation, json.dumps(entities)))
    conn.commit()
    conn.close()
