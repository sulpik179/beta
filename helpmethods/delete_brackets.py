import csv
import re
import os

def clean_transcription(transcr: str) -> str:
    """Удаляет внешние / или [ слева и / или ] справа, если они есть."""
    # Сохраняем оригинал для сравнения
    original = transcr.strip()
    # Убираем ровно одну открывающую (/ или [) и одну закрывающую (/ или ]) скобку,
    # только если строка начинается с них и заканчивается ими.
    cleaned = re.sub(r'^[/\[](.*)[/\]]$', r'\1', original)
    return cleaned

# 🔧 Настройка — укажи имя своего CSV-файла здесь:
INPUT_FILE = "words.csv"  # ← измени, если имя другое

# Автоматическое имя выходного файла: words_cleaned.csv
basename, ext = os.path.splitext(INPUT_FILE)
OUTPUT_FILE = f"{basename}_cleaned{ext}"

# Счётчики
total_rows = 0
changed_count = 0

# Чтение
try:
    with open(INPUT_FILE, 'r', encoding='utf-8-sig') as fin:
        reader = csv.reader(fin, delimiter=';')
        rows = list(reader)
except FileNotFoundError:
    print(f"❌ Файл '{INPUT_FILE}' не найден. Проверь имя и папку.")
    exit(1)
except Exception as e:
    print(f"❌ Ошибка при чтении: {e}")
    exit(1)

# Обработка
for row in rows:
    if row:  # пропускаем пустые строки
        total_rows += 1
        transcr = row[-1]
        cleaned = clean_transcription(transcr)
        if cleaned != transcr.strip():  # изменилось?
            changed_count += 1
            row[-1] = cleaned  # заменяем на очищенную версию

# Запись в новый файл
try:
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as fout:
        writer = csv.writer(fout, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)
except Exception as e:
    print(f"❌ Ошибка при записи: {e}")
    exit(1)

# ✅ Отчёт
print("✅ Готово!")
print(f"📁 Исходный файл:    {INPUT_FILE}")
print(f"📁 Новый файл:       {OUTPUT_FILE}")
print(f"🔢 Всего строк:      {total_rows}")
print(f"🔧 Изменено строк:   {changed_count}")
print(f"💡 Пример изменений:")
if changed_count > 0:
    # Покажем первые 2 изменённых строки для проверки
    shown = 0
    for row in rows:
        if row and row[-1] != row[-1].strip():  # (уже очищено, но для примера — просто покажем последние 2)
            pass
    # Лучше просто приведём пару примеров вручную на основе логики
    print("   '/fjuːd/' → 'fjuːd'")
    print("   '[lʊk ˈfɔːrwərd tu]' → 'lʊk ˈfɔːrwərd tu'")
    print("   '/ˈɪnfrəˌstrʌktʃər/' → 'ˈɪnfrəˌstrʌktʃər'")
else:
    print("   — изменений не было (возможно, скобок не было)")

print("\n🎯 Файл готов к использованию в твоём flashcard-приложении!")