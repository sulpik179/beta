import sqlite3 
from pathlib import Path


DB_PATH = Path('data/words.db')
SCHEMA_PATH = Path('data/schema.sql')

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = sqlite3.conn.cursor()
        self._apply_schema()

    def _apply_schema(self):    
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.conn.commit()

    def get_word_for_learn(self):
        return self.cursor.execute(
            'SELECT * FROM words WHERE id NOT IN (SELECT word_id FROM dictionary) ORDER BY RANDOM() LIMIT 1'
        ).fetchone()

    def add_to_practice(self, word_id):
        self.cursor.execute(
            'INSERT OR IGNORE INTO practice(word_id, k) VALUES(?, 0)',
            (word_id,)
        )   
        self.conn.commit()  

    def get_word_for_practice(self):
        return self.cursor.execute(
            'SELECT word_id, k FROM practice ORDER BY RANDOM() LIMIT 1'
        ).fetchone()

    def get_word_by_id(self, word_id):
        return self.cursor.execute(
            'SELECT * FROM words WHERE id = ?',
            (word_id,)
        ).fetchone()

    def increase_k(self, word_id):
        self.cursor.execute(
            'UPDATE practice SET k = MIN(k + 1, 5) WHERE word_id = ?',
            (word_id,)
        )
        self.conn.commit()

    def add_to_dictionary(self, word_id):
        self.cursor.execute(
            'INSERT OR IGNORE INTO dictionary VALUES(?)', 
            (word_id,)
        )
        self.conn.commit()

    def get_k(self, word_id):
        return self.cursor.execute(
            'SELECT k FROM practice WHERE word_id = ?',
            (word_id,)
        ).fetchone()[0]

    def get_all_dict(self):
        return self.cursor.execute(
            'SELECT word_id FROM dictionary'
        ).fetchall()

    def get_all_learn(self):
        return self.cursor.execute(
            'SELECT * FROM words'
        ).fetchall()