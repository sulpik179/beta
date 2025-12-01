import csv
import os
from collections import defaultdict

# 🔧 Настройка — укажи имя входного файла (можно cleaned, можно оригинал)
INPUT_FILE = "csv/words.csv"  # ← можно заменить на words.csv или другой

# Автоматическое имя выходного файла
basename, ext = os.path.splitext(INPUT_FILE)
OUTPUT_FILE = f"{basename}_deduped{ext}"

# Имена файлов для отчётов
DUPLICATE_REPORT_FILE = f"{basename}_duplicate_report.txt"
SIMILAR_REPORT_FILE = f"{basename}_similar_report.txt"

# Для отслеживания уже встречавшихся пар (eng, ru) и строк, на которых они были
seen = {}
unique_rows = []
duplicates_removed = 0
duplicate_log = []  # [(en, ru, line_number)]

# Для отслеживания похожих слов в 1-й колонке (eng), но с разными переводами (ru)
eng_to_ru_lines = defaultdict(list)  # eng -> [(ru, line_no), ...]

try:
    with open(INPUT_FILE, 'r', encoding='utf-8-sig') as fin:
        reader = csv.reader(fin, delimiter=';')
        header = None

        for i, row in enumerate(reader):
            line_number = i + 1  # Нумерация строк с 1

            # Обработка заголовка (если есть и первая строка похожа на него)
            if i == 0 and len(row) >= 2 and not row[0].strip().lower().startswith(('a', 'z', '1', '/')):
                # Пример эвристики: если первый элемент — не слово (например, "word"), оставляем как заголовок
                # Но безопаснее: проверим, выглядит ли как слово + перевод
                # Мы просто сохраним первую строку как есть и не будем её дедуплицировать
                header = row
                unique_rows.append(row)
                continue

            # Пропускаем пустые строки
            if not row or all(cell.strip() == '' for cell in row):
                unique_rows.append(row)  # можно закомментировать, если хочешь их удалять
                continue

            # Должно быть минимум 2 столбца (eng + ru)
            if len(row) < 2:
                unique_rows.append(row)  # сохраняем "битые" строки на всякий
                continue

            eng = row[0].strip().lower()
            ru = row[1].strip().lower()
            key = (eng, ru)

            # Запоминаем, где встречалось каждое en и его ru
            eng_to_ru_lines[eng].append((ru, line_number))

            if key in seen:
                duplicates_removed += 1
                # Логируем дубликат
                duplicate_log.append((row[0].strip(), row[1].strip(), line_number))
                # Пропускаем — дубликат
            else:
                seen[key] = line_number
                unique_rows.append(row)

except FileNotFoundError:
    print(f"❌ Файл '{INPUT_FILE}' не найден. Проверь имя и папку.")
    exit(1)
except Exception as e:
    print(f"❌ Ошибка при чтении: {e}")
    exit(1)

# --- Запись отчёта о дубликатах ---
try:
    with open(DUPLICATE_REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("Отчёт об удалённых дубликатах:\n")
        f.write("Формат: [en_word], [ru_word], [line_number_in_original_file]\n\n")
        for en_word, ru_word, line_num in duplicate_log:
            f.write(f"{en_word}, {ru_word}, {line_num}\n")
    print(f"✅ Отчёт о дубликатах сохранён в: {DUPLICATE_REPORT_FILE}")
except Exception as e:
    print(f"❌ Ошибка при записи отчёта о дубликатах: {e}")

# --- Запись отчёта о похожих словах ---
similar_log = []
for eng_word, ru_line_list in eng_to_ru_lines.items():
    # Если для одного en встречается больше одного *уникального* ru
    unique_ru_set = set([item[0] for item in ru_line_list])
    if len(unique_ru_set) > 1:
        # Значит, есть разные переводы
        for ru_word, line_num in ru_line_list:
            # Добавляем все строки с этим en, если у него разные переводы
            # (можно фильтровать, если нужно только уникальные en, но с разными ru)
            similar_log.append((eng_word, ru_word, line_num))

try:
    with open(SIMILAR_REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("Отчёт о похожих словах в 1-й колонке (разные переводы):\n")
        f.write("Формат: [en_word], [ru_word], [line_number_in_original_file]\n\n")
        for en_word, ru_word, line_num in similar_log:
            f.write(f"{en_word}, {ru_word}, {line_num}\n")
    print(f"✅ Отчёт о похожих словах сохранён в: {SIMILAR_REPORT_FILE}")
except Exception as e:
    print(f"❌ Ошибка при записи отчёта о похожих словах: {e}")

# --- Запись очищенного файла ---
try:
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as fout:
        writer = csv.writer(fout, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(unique_rows)
except Exception as e:
    print(f"❌ Ошибка при записи: {e}")
    exit(1)

# --- Отчёт в консоль ---
total_original = len(unique_rows) + duplicates_removed
print("✅ Дедупликация завершена!")
print(f"📁 Входной файл:      {INPUT_FILE}")
print(f"📁 Выходной файл:     {OUTPUT_FILE}")
print(f"🔢 Всего строк:       {total_original}")
print(f"➖ Удалено дубликатов: {duplicates_removed}")
print(f"✔️  Осталось строк:    {len(unique_rows)}")

print(f"\n📋 Найдено дубликатов: {len(duplicate_log)}")
print(f"📋 Найдено похожих слов (с разными переводами): {len(similar_log)}")

if duplicates_removed > 0:
    print(f"\n📝 Подробности в файле: {DUPLICATE_REPORT_FILE}")
if len(similar_log) > 0:
    print(f"📝 Подробности в файле: {SIMILAR_REPORT_FILE}")
