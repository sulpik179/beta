from kivy.uix.popup import Popup
from kivy.uix.label import Label


class DictionaryAddedPopup(Popup):
    def __init__(self, word, **kwargs):
        super().__init__(**kwargs)
        self.title = ''
        self.separator_height = 0
        self.size_hint = (0.8, 0.2)
        self.background = ''
        self.background_color = (0, 0, 0, 0)

        self.content = Label(
            text=f"'{word.strip()}'  добавлено в словарь",
            font_name='JetBrainsMono',
            font_size='18sp',
            text_size=(self.width * 0.9, None),
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=60
        )
        self.bind(size=self._update_text_size)
        # Закрываем по тапу вне окна
        self.bind(on_touch_down=lambda *_: self.dismiss())

    def _update_text_size(self, *args):
        if self.content:
            self.content.text_size = (self.width * 0.9, None)
