import sqlite3
import shutil
from pathlib import Path

from kivy.app import App
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.properties import BooleanProperty


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


def get_db_path():
    if platform == 'android':
        user_dir = Path(App.get_running_app().user_data_dir)
        db_path = user_dir / 'words.db'
        if not db_path.exists():
            print(">>> Копирование words.db в память телефона...")
            user_dir.mkdir(exist_ok=True)
            shutil.copy('data/words.db', db_path)
            print(">>> Копирование завершено:", db_path)
        return db_path
    else:
        return Path('data/words.db')


class FlashcardApp(App):
    is_dark_theme = BooleanProperty(True)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_dark_theme = True 

    def build(self):
        db_path = get_db_path()
        if not db_path.exists():
            self._create_reserve_db(db_path)
        self.db = Database(db_path)


        if platform == 'android':
            try:
                from jnius import autoclass
                activity = autoclass('org.kivy.android.PythonActivity').mActivity
                activity.setRequestedOrientation(1)
            except:
                pass

        self.apply_theme()
        return FlashcardScreenManager()

    def apply_theme(self):
        dark_bg = (0.05, 0.06, 0.07, 1)    
        light_bg = (0.90, 0.93, 0.96, 1)   
        Window.clearcolor = dark_bg if self.is_dark_theme else light_bg

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
        sm = self.root
        for screen_name in sm.screen_names:
            screen = sm.get_screen(screen_name)
            if hasattr(screen, 'apply_theme'):
                screen.apply_theme()

    def _create_reserve_db(self, db_path: Path):
        db_path.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        with open('data/schema.sql', 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
        test_words = [
            (None, 'hello', 'привет', 'здравствуйте', 'добрый день', 'hi', 'hey',
             'Привет! Как дела?', 'Hello! How are you?', '/ˈhe.ləʊ/'),
        ]
        cursor.executemany(
            'INSERT OR IGNORE INTO words VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            test_words
        )
        conn.commit()
        conn.close()

    def on_stop(self):
        if hasattr(self, 'db'):
            self.db.close()


if __name__ == '__main__':
    FlashcardApp().run()