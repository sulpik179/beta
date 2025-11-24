import sqlite3

# Подключаемся к БД (если её нет — она создастся)
conn = sqlite3.connect('data/words.db')
cursor = conn.cursor()

# Создаём таблицы
cursor.executescript('''
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_en TEXT NOT NULL,
    word_ru TEXT NOT NULL,
    distractor_ru1 TEXT NOT NULL,
    distractor_ru2 TEXT NOT NULL,
    distractor_en1 TEXT NOT NULL,
    distractor_en2 TEXT NOT NULL,
    sentence_ru TEXT NOT NULL,
    sentence_en TEXT NOT NULL,
    transcription TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS practice (
    word_id INTEGER PRIMARY KEY,
    k INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(word_id) REFERENCES words(id)
);

CREATE TABLE IF NOT EXISTS dictionary (
    word_id INTEGER PRIMARY KEY,
    FOREIGN KEY(word_id) REFERENCES words(id)
);
''')

conn.commit()
conn.close()

print("БД и таблицы созданы.")