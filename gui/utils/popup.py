from kivy.uix.popup import Popup


class LanguageSelectPopup(Popup):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback

    def set_language(self, lang_code):
        print(f"Выбран режим: {lang_code}") 
        self.callback(lang_code)
        self.dismiss()