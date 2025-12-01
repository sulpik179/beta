from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class DictionaryScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.created_labels = []

    def on_enter(self):
        self.apply_theme()
        self.load_dictionary()

    def apply_theme(self):
        app = App.get_running_app()
        is_dark = app.is_dark_theme

        dark_text = (0.90, 0.93, 0.96, 1)
        light_text = (0.11, 0.14, 0.15, 1)
        text_color = dark_text if is_dark else light_text

        for label in self.created_labels:
            label.color = text_color

    def load_dictionary(self):
        app = App.get_running_app()
        is_dark = app.is_dark_theme
        dark_text = (0.90, 0.93, 0.96, 1)
        light_text = (0.11, 0.14, 0.15, 1)
        text_color = dark_text if is_dark else light_text

        dict_ids = app.db.get_all_dict_ids()
        if not dict_ids:
            label = Label(
                text='Словарь пуст.\nИзучайте слова в Learn и повторяйте их в Practice.',
                font_size=18,
                font_name='JetBrainsMono',
                halign='center',
                color=text_color
            )
            self.created_labels = [label]  # <-- сохраняем Label
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

            word_box = BoxLayout(orientation='vertical', size_hint_y=None, height=120)

            main_label = Label(
                    text=f'{word_en.strip()} — {word_ru.strip()}',
                    size_hint_y=None,
                    height=30,
                    font_size=16,
                    font_name='JetBrainsMono',
                    halign='left',
                    color=text_color
                )
            word_box.add_widget(main_label)
            
            transcr_label = Label(
                    text=transcription.strip(),
                    size_hint_y=None,
                    height=30,
                    font_size=14,
                    font_name='DejaVuSans',  
                    halign='left',
                    color=text_color
                )
            word_box.add_widget(transcr_label)

            self.ids.dict_layout.add_widget(word_box)
            self.created_labels.append(main_label)
            self.created_labels.append(transcr_label)