import csv



import re





# 🔧 Настройка — укажи имя CSV-файла (лучше уже очищенный и без дублей)


CSV_FILE = "csv/words.csv"  # ← измени, если нужно





# Предзагрузка данных для быстрого поиска


words_data = []





try:


    with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:


        reader = csv.reader(f, delimiter=';')


        words_data = list(reader)


    print(f"✅ Загружено {len(words_data)} строк из '{CSV_FILE}'\n")


except FileNotFoundError:


    print(f"❌ Файл '{CSV_FILE}' не найден. Проверь имя и папку.")


    exit(1)


except Exception as e:


    print(f"❌ Ошибка при загрузке: {e}")


    exit(1)





def normalize_ru(text: str) -> str:


    """Убирает ё/е неоднозначность и приводит к нижнему регистру."""


    return text.lower().replace('ё', 'е')





print("🔍 Введи слово (англ. или рус.) — я найду его в базе.")


print("   Напиши 'exit' или 'quit', чтобы выйти.\n")





while True:


    query = input("🔎 Поиск: ").strip()


    if not query:


        continue


    if query.lower() in ('exit', 'quit'):


        print("👋 До встречи!")


        break





    found = []


    query_lower = query.lower()


    query_ru_norm = normalize_ru(query)





    for idx, row in enumerate(words_data, start=1):


        if not row or len(row) < 2:


            continue





        eng = row[0].strip()


        ru = row[1].strip()





        # Точное совпадение (регистронезависимо для англ., с ё/е — для рус.)


        if eng.lower() == query_lower or normalize_ru(ru) == query_ru_norm:


            found.append((idx, row))





    if found:


        print(f"\n✅ Найдено {len(found)} совпадений:\n")


        for idx, row in found:


            eng = row[0].strip()


            ru = row[1].strip()


            transcr = row[-1].strip() if len(row) > 2 else ""


            example_ru = row[6].strip() if len(row) > 6 else ""


            example_en = row[7].strip() if len(row) > 7 else ""





            print(f"📌 Строка {idx}:")


            print(f"   🇬🇧 {eng}")


            print(f"   🇷🇺 {ru}")


            if transcr:


                print(f"   🔊 /{transcr}/")


            if example_ru:


                print(f"   📖 RU: {example_ru}")


            if example_en:


                print(f"   📖 EN: {example_en}")


            print("-" * 50)


    else:


        print(f"\n❌ Слово '{query}' не найдено в базе.\n")


        # Подсказка: частичный поиск (первые 3 совпадения по началу слова)


        suggestions = []


        for idx, row in enumerate(words_data, start=1):


            if len(row) < 2: continue


            eng = row[0].strip()


            ru = row[1].strip()


            if eng.lower().startswith(query_lower) or normalize_ru(ru).startswith(query_ru_norm):


                suggestions.append((eng, ru))


                if len(suggestions) >= 3:


                    break


        if suggestions:


            print("💡 Возможно, вы имели в виду:")


            for eng, ru in suggestions:


                print(f"   • {eng} — {ru}")


        print()