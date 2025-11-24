from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.lang import Builder


from db_manage import Database

Builder.load_file('main.kv')


class LanguageSelectPopup(Popup):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback

    def set_language(self, lang_code):
        self.callback(lang_code)
        self.dismiss()

class MainScreen(Screen):
    pass

class LearnScreen(Screen):
    def on_enter(self):
        popup = LanguageSelectPopup(callback=self.start_learning)
        popup.open()

    def start_learning(self, lang_code):
        print(f'Learn: выбран режим {lang_code}')

class PracticeScreen(Screen):
    def on_enter(self):
        popup = LanguageSelectPopup(callback=self.start_learning)
        popup.open()

    def start_learning(self, lang_code):
        print(f'Learn: выбран режим {lang_code}')

class Dictionary(Screen):
    pass

class FlashcardScreenManager(ScreenManager):
    pass

class FlashcardApp(App):
    def build(self):
        self.db = Database
        return FlashcardScreenManager    

    def on_stop(self):
        self.db.close()


if __name__ == '__main__':
    FlashcardApp().run()