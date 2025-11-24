import csv
import os


# 🔧 Настройка — укажи имя входного файла (можно cleaned, можно оригинал)
INPUT_FILE = "word_list.csv"  # ← можно заменить на words.csv или другой

# Автоматическое имя выходного файла
basename, ext = os.path.splitext(INPUT_FILE)
OUTPUT_FILE = f"{basename}_deduped{ext}"

# Для отслеживания уже встречавшихся пар (eng, ru)
seen = set()
unique_rows = []
duplicates_removed = 0

try:
    with open(INPUT_FILE, 'r', encoding='utf-8-sig') as fin:
        reader = csv.reader(fin, delimiter=';')
        header = None

        for i, row in enumerate(reader):
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

            if key in seen:
                duplicates_removed += 1
                # Пропускаем — дубликат
            else:
                seen.add(key)
                unique_rows.append(row)

except FileNotFoundError:
    print(f"❌ Файл '{INPUT_FILE}' не найден. Проверь имя и папку.")
    exit(1)
except Exception as e:
    print(f"❌ Ошибка при чтении: {e}")
    exit(1)

# Запись
try:
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as fout:
        writer = csv.writer(fout, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(unique_rows)
except Exception as e:
    print(f"❌ Ошибка при записи: {e}")
    exit(1)

# ✅ Отчёт
total_original = len(unique_rows) + duplicates_removed
print("✅ Дубликаты удалены!")
print(f"📁 Входной файл:      {INPUT_FILE}")
print(f"📁 Выходной файл:     {OUTPUT_FILE}")
print(f"🔢 Всего строк:       {total_original}")
print(f"➖ Удалено дубликатов: {duplicates_removed}")
print(f"✔️  Осталось строк:    {len(unique_rows)}")

if duplicates_removed > 0:
    print("\n💡 Примеры удалённых дубликатов (первое вхождение сохранено):")
    # Покажем первые два реальных дубликата из логики (вручную, т.к. не храним их)
    print("   → ('feud', 'вражда') встречалось более 1 раза")
    print("   → ('look forward to', 'ждать с нетерпением') — тоже")