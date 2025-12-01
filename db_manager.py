import sqlite3 
from pathlib import Path


#DB_PATH = Path('data/o.db')
DB_PATH = Path('words.db')
SCHEMA_PATH = Path('data/schema.sql')

class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path('data/words.db')
        else:
            db_path = Path(db_path)

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._apply_schema()

    def _apply_schema(self):
        schema_path = Path('data/schema.sql')  
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.conn.commit()

    def get_word_for_learn(self):
        return self.cursor.execute(
            'SELECT * FROM words WHERE id NOT IN (SELECT word_id FROM dictionary) AND ' \
            'id NOT IN (SELECT word_id FROM practice) ORDER BY RANDOM() LIMIT 1'
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
        cursor = self.cursor.execute(
            'SELECT k FROM practice WHERE word_id = ?',
            (word_id,)
        )
        row = cursor.fetchone()
        return row[0] if row else 0

    def get_all_dict(self):
        return self.cursor.execute(
            'SELECT word_id FROM dictionary'
        ).fetchall()

    def get_all_learn(self):
        return self.cursor.execute(
            'SELECT * FROM words'
        ).fetchall()

    def close(self):
        self.conn.close()

    def add_words_from_csv(self, csv_path: str):
        import csv
        count = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row_num, row in enumerate(reader, start=1):
                if len(row) < 9:
                    print(f'Пропущена строка {row_num} (недостаточно данных): {row}')
                    count += 1
                    continue

                word_en, word_ru, distractor_ru1, distractor_ru2, distractor_en1, distractor_en2, sentence_ru, sentence_en, transcription = row

                existing = self.cursor.execute(
                    'SELECT 1 FROM words WHERE word_en = ? AND word_ru = ?',
                    (word_en, word_ru)
                ).fetchone()

                if existing:
                    print(f'Пропущена строка {row_num} (уже существует): {word_en} - {word_ru}')
                    continue
                try:
                    self.cursor.execute('''
                        INSERT INTO words (
                            word_en, word_ru, distractor_ru1, distractor_ru2, distractor_en1,
                            distractor_en2, sentence_ru, sentence_en, transcription) VALUES
                            (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (word_en, word_ru, distractor_ru1, distractor_ru2,
                            distractor_en1, distractor_en2, sentence_ru, sentence_en, transcription)
                            )
                except Exception as e:
                    print(f"Ошибка при вставке строки {row_num}: {e}")
                    continue
            print(f'Пропущено строк: {count}')

        try:
            self.conn.commit()
            print("Транзакция зафиксирована.")
        except Exception as e:
            print(f"Ошибка при фиксации транзакции: {e}")

    def get_all_dict_ids(self):
        return [row[0] for row in self.cursor.execute('SELECT word_id FROM dictionary').fetchall()]

    def in_dict(self, word_id) -> bool:
        cursor = self.cursor.execute(
            'SELECT 1 FROM dictionary WHERE word_id = ?',
            (word_id,)
        )
        return cursor.fetchone() is not None