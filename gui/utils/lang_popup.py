from kivy.uix.popup import Popup

class LanguageSelectPopup(Popup):
    def __init__(self, callback, **kwargs):
        kwargs.setdefault('title', '')
        kwargs.setdefault('separator_height', 0)
        kwargs.setdefault('size_hint', (0.5, 0.3))
        kwargs.setdefault('background', '')
        kwargs.setdefault('background_color', (0, 0, 0, 0))
        
        super().__init__(**kwargs)
        self.callback = callback

    def set_language(self, lang_code):
        self.callback(lang_code)
        self.dismiss()