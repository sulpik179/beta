from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.factory import Factory

class DictionaryScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.created_labels = []

    def on_enter(self):
        self.apply_theme()
        self.load_dictionary()

    def apply_theme(self):
        app = App.get_running_app()
        is_dark = app.is_dark_theme if app else True

        dark_text = (0.90, 0.93, 0.96, 1)
        light_text = (0.11, 0.14, 0.15, 1)
        text_color = dark_text if is_dark else light_text

        for label in self.created_labels:
            label.color = text_color

    def load_dictionary(self):
        app = App.get_running_app()
        is_dark = app.is_dark_theme if app else True
        dark_text = (0.90, 0.93, 0.96, 1)
        light_text = (0.11, 0.14, 0.15, 1)
        text_color = dark_text if is_dark else light_text

        dict_ids = []
        try:
            dict_ids = app.db.get_all_dict_ids()
        except Exception:
            dict_ids = []

        if not dict_ids:
            label = Label(
                text='Словарь пуст.\nИзучайте слова в Learn и повторяйте их в Practice.',
                font_size=18,
                font_name='JetBrainsMono',
                halign='center',
                color=text_color,
            )
            self.ids.dict_layout.clear_widgets()
            self.ids.dict_layout.add_widget(label)
            return

        self.ids.dict_layout.clear_widgets()
        self.created_labels = []

        for word_id in dict_ids:
            word_row = app.db.get_word_by_id(word_id)
            if not word_row:
                continue

            _, word_en, word_ru, _, _, _, _, sentence_ru, sentence_en, transcription = word_row

            # Создаем KV-компонент DictionaryItem
            item = Factory.DictionaryItem()

            # Заполняем текст
            item.ids.main_label.text = f"{word_en.strip()} — {word_ru.strip()}"
            item.ids.transcr_label.text = transcription.strip()

            # Добавляем в список
            self.ids.dict_layout.add_widget(item)

            # Чтобы apply_theme работал
            self.created_labels.append(item.ids.main_label)
            self.created_labels.append(item.ids.transcr_label)
