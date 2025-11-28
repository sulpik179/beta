import sqlite3
import shutil
from pathlib import Path

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.utils import platform

# регистрация шрифтов
try:
    LabelBase.register(name='JetBrainsMono', fn_regular='assets/fonts/JetBrainsMono.ttf')
    LabelBase.register(name='DejaVuSans', fn_regular='assets/fonts/DejaVuSans.ttf')
except Exception as e:
    print("Ошибка регистрации шрифтов:", e)

from db_manager import Database
from gui.widgets.answer_button import AnswerButton

Builder.load_file('main.kv')

from gui.screens.main_screen import MainScreen
from gui.screens.learn_screen import LearnScreen
from gui.screens.practice_screen import PracticeScreen
from gui.screens.dictionary_screen import DictionaryScreen


class FlashcardScreenManager(ScreenManager):
    pass


# ---------- NEW: правильный путь к БД на Android ----------
def get_db_path():
    """
    Возвращает корректный путь к базе.
    На Android — копирует data/words.db в user_data_dir при первом запуске.
    """
    if platform == 'android':
        # путь вида: /data/data/<package>/files/
        user_dir = Path(App.get_running_app().user_data_dir)
        db_path = user_dir / 'words.db'

        if not db_path.exists():
            print(">>> Копирование words.db в память телефона...")
            user_dir.mkdir(exist_ok=True)
            shutil.copy('data/words.db', db_path)
            print(">>> Копирование завершено:", db_path)

        return db_path
    else:
        # ПК
        return Path('data/words.db')


# ---------------------------------------------------------


class FlashcardApp(App):
    def build(self):
        db_path = get_db_path()

        if db_path.exists():
            print(f"Используем БД: {db_path}")
        else:
            print("База не найдена, создаём резерв...")
            self._create_reserve_db(db_path)

        self.db = Database(db_path)
        return FlashcardScreenManager()

    def _create_reserve_db(self, db_path: Path):
        """
        Создаёт резервную БД, если основной файл отсутствует.
        Работает и на ПК, и на Android.
        """
        db_path.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        with open('data/schema.sql', 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())

        test_words = [
            (None, 'hello', 'привет', 'здравствуйте', 'добрый день', 'hi', 'hey',
             'Привет! Как дела?', 'Hello! How are you?', '/ˈhe.ləʊ/'),
            (None, 'book', 'книга', 'журнал', 'газета', 'novel', 'magazine',
             'Я читаю книгу', 'I am reading a book', '/bʊk/'),
            (None, 'water', 'вода', 'чай', 'кофе', 'juice', 'tea',
             'Пейте воду', 'Drink water', '/ˈwɔː.tər/')
        ]

        cursor.executemany(
            'INSERT OR IGNORE INTO words VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            test_words
        )
        conn.commit()
        conn.close()

        print("✅ Резервная БД создана:", db_path)

    def on_stop(self):
        if hasattr(self, 'db'):
            self.db.close()


if __name__ == '__main__':
    FlashcardApp().run()

# import sqlite3
# from kivy.app import App
# from kivy.uix.screenmanager import ScreenManager
# from kivy.lang import Builder
# from kivy.core.text import LabelBase
# from pathlib import Path


# try:
#     LabelBase.register(name='JetBrainsMono', fn_regular='assets/fonts/JetBrainsMono.ttf')
#     LabelBase.register(name='DejaVuSans', fn_regular='assets/fonts/DejaVuSans.ttf')
# except:
#     pass

# from db_manager import Database 
# from gui.widgets.answer_button import AnswerButton

# Builder.load_file('main.kv')

# from gui.screens.main_screen import MainScreen
# from gui.screens.learn_screen import LearnScreen
# from gui.screens.practice_screen import PracticeScreen
# from gui.screens.dictionary_screen import DictionaryScreen

# class FlashcardScreenManager(ScreenManager):
#     pass

# # class FlashcardApp(App):
# #     def build(self):
# #         self.db = Database()  
# #         return FlashcardScreenManager()  

# #     def on_stop(self):
# #         if hasattr(self, 'db'):  
# #             self.db.close()

# class FlashcardApp(App):
#     def build(self):
#         db_path = Path('data/words.db')
#         if db_path.exists():
#             print(f"БД: {db_path}")
#         else:
#             print("БД не найдена, создаём резерв...")
#             self._create_reserve_db()
        
#         self.db = Database()  
#         return FlashcardScreenManager()  

#     def _create_reserve_db(self):

#         db_path = Path('data/words.db')
#         db_path.parent.mkdir(exist_ok=True)
        
#         conn = sqlite3.connect(db_path)
#         cursor = conn.cursor()
        
#         with open('data/schema.sql', 'r', encoding='utf-8') as f:
#             cursor.executescript(f.read())
        
#         test_words = [
#             (None, 'hello', 'привет', 'здравствуйте', 'добрый день', 'hi', 'hey', 
#              'Привет! Как дела?', 'Hello! How are you?', '/ˈhe.ləʊ/'),
#             (None, 'book', 'книга', 'журнал', 'газета', 'novel', 'magazine', 
#              'Я читаю книгу', 'I am reading a book', '/bʊk/'),
#             (None, 'water', 'вода', 'чай', 'кофе', 'juice', 'tea', 
#              'Пейте воду', 'Drink water', '/ˈwɔː.tər/')
#         ]
#         cursor.executemany('INSERT OR IGNORE INTO words VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', test_words)
#         conn.commit()
#         conn.close()
#         print("✅ Резервная БД создана (3 слова)")

#     def on_stop(self):
#         if hasattr(self, 'db'):  
#             self.db.close()


# if __name__ == '__main__':
#     FlashcardApp().run()