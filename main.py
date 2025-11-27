import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.resources import resource_find
from shutil import copy
from pathlib import Path


try:
    LabelBase.register(name='JetBrainsMono', fn_regular='assets/fonts/JetBrainsMono.ttf')
    LabelBase.register(name='DejaVuSans', fn_regular='assets/fonts/DejaVuSans.ttf')
except:
    pass

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
        self.db = Database()  
        return FlashcardScreenManager()  

    def on_stop(self):
        if hasattr(self, 'db'):  
            self.db.close()


if __name__ == '__main__':
    FlashcardApp().run()