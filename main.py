import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.resources import resource_find
from shutil import copy


LabelBase.register(name='JetBrainsMono', fn_regular='assets/fonts/JetBrainsMono.ttf')
LabelBase.register(name='DejaVuSans', fn_regular='assets/fonts/DejaVuSans.ttf')


from db_manager import Database 
from gui.widgets.answer_button import AnswerButton


Builder.load_file('main.kv')

from gui.screens.main_screen import MainScreen
from gui.screens.learn_screen import LearnScreen
from gui.screens.practice_screen import PracticeScreen
from gui.screens.dictionary_screen import DictionaryScreen


class FlashcardScreenManager(ScreenManager):
    pass


class FlashcardApp(App):
    def build(self):
        user_data_dir = self.user_data_dir

        local_db_path = os.path.join(user_data_dir, 'words.db')

        if not os.path.exists(local_db_path):
            source_db_path = resource_find('words.db')
            if source_db_path:
                copy(source_db_path, local_db_path)
                print("БД скопирована из assets в user_data_dir")
            else:
                print("Ошибка: words.db не найдена в ресурсах")

        self.db = Database(local_db_path)

        return FlashcardScreenManager()    

    def on_stop(self):
        self.db.close()


if __name__ == '__main__':
    FlashcardApp().run()