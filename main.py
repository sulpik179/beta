# main.py
import sqlite3
import shutil
from pathlib import Path

from kivy.app import App
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.core.window import Window
from gui.utils.lang_popup import LanguageSelectPopup
from kivy.properties import BooleanProperty, ListProperty

# Регистрация шрифтов — безопасно
try:
    LabelBase.register(name='JetBrainsMono', fn_regular='assets/fonts/JetBrainsMono.ttf')
    LabelBase.register(name='DejaVuSans', fn_regular='assets/fonts/DejaVuSans.ttf')
except Exception as e:
    print('Ошибка регистрации шрифтов (можно игнорировать, если шрифты отсутствуют):', e)

# Импорт менеджера БД и кастомных виджетов/экранов ДО загрузки KV
from db_manager import Database
from gui.widgets.answer_button import AnswerButton
from gui.widgets.theme_button import ThemeButton
from gui.screens.main_screen import MainScreen
from gui.screens.learn_screen import LearnScreen
from gui.screens.practice_screen import PracticeScreen
from gui.screens.dictionary_screen import DictionaryScreen

# Загружаем kv после регистрации классов
Builder.load_file('main.kv')


class FlashcardScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = SlideTransition(duration=0.28)


def get_db_path():
    if platform == 'android':
        user_dir = Path(App.get_running_app().user_data_dir)
        db_path = user_dir / 'words.db'
        if not db_path.exists():
            print(">>> Копирование words.db в память телефона...")
            user_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy('data/words.db', db_path)
            print(">>> Копирование завершено:", db_path)
        return db_path
    else:
        return Path('data/words.db')


class FlashcardApp(App):
    # тема
    is_dark_theme = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # дефолты (можно менять)
        self.is_dark_theme = True
        self.color_light = [0.90, 0.93, 0.96, 1]
        self.color_dark = [0.05, 0.06, 0.07, 1]
        self.color_buttons = [0.62, 0.71, 0.75, 1]

    def build(self):
        db_path = get_db_path()
        if not db_path.exists():
            self._create_reserve_db(db_path)
        # инициализируем БД
        self.db = Database(db_path)

        # Под android: попытка зафиксировать ориентацию
        if platform == 'android':
            try:
                from jnius import autoclass
                activity = autoclass('org.kivy.android.PythonActivity').mActivity
                activity.setRequestedOrientation(1)
            except Exception:
                pass

        self.apply_theme()
        return FlashcardScreenManager()

    def apply_theme(self):
        Window.clearcolor = tuple(self.color_dark) if self.is_dark_theme else tuple(self.color_light)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
        # обновляем экраны, если есть
        sm = self.root
        if sm:
            for name in sm.screen_names:
                screen = sm.get_screen(name)
                if hasattr(screen, 'apply_theme'):
                    try:
                        screen.apply_theme()
                    except Exception:
                        pass

    def _create_reserve_db(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            with open('data/schema.sql', 'r', encoding='utf-8') as f:
                cursor.executescript(f.read())
        except Exception as e:
            print('Не удалось прочитать schema.sql:', e)
        test_words = [
            (None, 'hello', 'привет', 'здравствуйте', 'добрый день', 'hi', 'hey',
             'Привет! Как дела?', 'Hello! How are you?', '/ˈhe.ləʊ/'),
        ]
        try:
            cursor.executemany(
                'INSERT OR IGNORE INTO words VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                test_words
            )
            conn.commit()
        finally:
            conn.close()

    def on_stop(self):
        if hasattr(self, 'db'):
            try:
                self.db.close()
            except Exception:
                pass


if __name__ == '__main__':
    FlashcardApp().run()
