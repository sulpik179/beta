from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class DictionaryScreen(Screen):
    def on_enter(self):
        self.load_dictionary()

    def load_dictionary(self):
        app = App.get_running_app()

        dict_ids = app.db.get_all_dict_ids()
        if not dict_ids:
            label = Label(
                text='Словарь пуст.\nИзучайте слова в Learn и повторяйте их в Practice.',
                font_size=18,
                font_name='JetBrainsMono',
                halign='center'
            )
            self.ids.dict_layout.add_widget(label)
            return

        self.ids.dict_layout.clear_widgets()

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
                    halign='left'
                )
            word_box.add_widget(main_label)
            
            transcr_label = Label(
                    text=transcription.strip(),
                    size_hint_y=None,
                    height=30,
                    font_size=14,
                    font_name='DejaVuSans',  
                    halign='left'
                )
            word_box.add_widget(transcr_label)

            # sentence_en_label = Label(
            #     text=f'"{sentence_en.strip()}"',
            #     size_hint=(1, None),  
            #     height=45,
            #     font_size=12,
            #     font_name='JetBrainsMono',
            #     halign='left',
            #     text_size=(word_box.width * 0.9, None)
            # )
            # sentence_en_label.bind(
            #     texture_size=lambda instance, value: setattr(instance, 'height', value[1])
            # )
            # word_box.add_widget(sentence_en_label)

            self.ids.dict_layout.add_widget(word_box)