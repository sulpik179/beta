import csv
import sqlite3

CSV_FILE = 'csv/o.csv'
DB_FILE = 'data/words.db'

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Проверим, что таблица words существует
cursor.execute('SELECT 1 FROM words LIMIT 1;')
print("Таблица words существует.")

with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    for row_num, row in enumerate(reader, start=1):
        if len(row) != 9:
            print(f'Ошибка в строке {row_num} (ожидалось 9 значений, получено {len(row)}): {row}')
            continue

        word_en, word_ru, distractor_ru1, distractor_ru2, distractor_en1, distractor_en2, sentence_ru, sentence_en, transcription = row

        cursor.execute('''
            INSERT INTO words (
                word_en, word_ru, distractor_ru1, distractor_ru2,
                distractor_en1, distractor_en2, sentence_ru, sentence_en, transcription
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (word_en, word_ru, distractor_ru1, distractor_ru2, distractor_en1, distractor_en2, sentence_ru, sentence_en, transcription))

conn.commit()
conn.close()

print("Загрузка завершена.")