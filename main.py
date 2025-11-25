from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.lang import Builder
from random import shuffle
from kivy.core.text import LabelBase


LabelBase.register(name='JetBrainsMono', fn_regular='assets/fonts/JetBrainsMono.ttf')
LabelBase.register(name='DejaVuSans', fn_regular='assets/fonts/DejaVuSans.ttf')

from gui.widgets.answer_button import AnswerButton
from db_manager import Database


Builder.load_file('main.kv')


class LanguageSelectPopup(Popup):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback

    def set_language(self, lang_code):
        print(f"Выбран режим: {lang_code}") 
        self.callback(lang_code)
        self.dismiss()


class MainScreen(Screen):
    pass


class LearnScreen(Screen):
    def on_enter(self):
        popup = LanguageSelectPopup(callback=self.start_learning)
        popup.open()

    def start_learning(self, lang_code):
        app = App.get_running_app()
        self.lang_code = lang_code

        word_row = app.db.get_word_for_learn()
        if not word_row:
            self.ids.word_label.text = 'Больше нет слов для изучения :(\n' \
            'Попробуйте режим Practice'   
            return

        word_id, word_en, word_ru, distractor_ru1, distractor_ru2, distractor_en1, distractor_en2, sentence_ru, sentence_en, transcription = word_row

        if lang_code == 'en_ru':
            main_word = word_en
            correct_answer = word_ru
            distractors = [distractor_ru1, distractor_ru2]
            sentence = sentence_en
            transcription = transcription
        else:
            main_word = word_ru
            correct_answer = word_en
            distractors = [distractor_en1, distractor_en2]
            sentence = sentence_ru
            transcription = ''

        self.ids.word_label.text = main_word
        self.ids.transcription_label.text = transcription
        self.ids.sentence_label.text = sentence

        options = [correct_answer] + distractors
        shuffle(options)

        self.ids.option1.text = options[0].strip()
        self.ids.option2.text = options[1].strip()
        self.ids.option3.text = options[2].strip()

        self.correct_answer = correct_answer.strip()
        self.word_id = word_id


        for btn_id in ['option1', 'option2', 'option3']:
            btn = self.ids[btn_id]
            btn.border_color = [0, 0, 0, 0]

        self.reset_colors()
        self.hide_buttons()

    def reset_colors(self):
        for btn_id in ['option1', 'option2', 'option3']:
            btn = self.ids[btn_id]
            btn.background_color = [1, 1, 1, 1]

    def hide_buttons(self):
        self.ids.next_button.disabled = True
        self.ids.next_button.opacity = 0

    def check_answer(self, answer):
        for btn_id in ['option1', 'option2', 'option3']:
            btn = self.ids[btn_id]
            btn.border_color = [0, 0, 0, 0]

        for btn_id in ['option1', 'option2', 'option3']:
            btn = self.ids[btn_id]
            if btn.text == self.correct_answer:
                btn.border_color = [0.3, 0.8, 0.4, 1]

        if answer != self.correct_answer:
            for btn_id in ['option1', 'option2', 'option3']:
                btn = self.ids[btn_id]
                if btn.text == answer:
                    btn.border_color = [0.9, 0.3, 0.3, 1]

        if answer == self.correct_answer:
            app = App.get_running_app()
            app.db.add_to_practice(self.word_id)

        self.ids.next_button.disabled = False
        self.ids.next_button.opacity = 1

    def next_word(self):
        self.start_learning(self.lang_code)



class PracticeScreen(Screen):
    def on_enter(self):
        popup = LanguageSelectPopup(callback=self.start_practice)
        popup.open()

    def start_practice(self, lang_code):
        app = App.get_running_app()
        self.lang_code = lang_code 

        word_id = None

        practice_row = app.db.get_word_for_practice()
        if not practice_row:
            self.ids.word_label.text = 'Пока нет слов для изучения :(\n' \
            'Попробуйте режим Learn'

        word_id, k = practice_row

        full_word_row = app.db.get_word_by_id(word_id)
        if not full_word_row:
            print('Ошибка, слово не найдено по id')
            return

        
        word_id, word_en, word_ru, distractor_ru1, distractor_ru2, distractor_en1, distractor_en2, sentence_ru, sentence_en, transcription = full_word_row

        if lang_code == 'en_ru':
            main_word = word_en
            correct_answer = word_ru
            distractors = [distractor_ru1, distractor_ru2]
            sentence = sentence_en
            transcription = transcription
        else:
            main_word = word_ru
            correct_answer = word_en
            distractors = [distractor_en1, distractor_en2]
            sentence = sentence_ru
            transcription = ''

        self.ids.word_label.text = main_word
        self.ids.transcription_label.text = transcription
        self.ids.sentence_label.text = sentence

        options = [correct_answer] + distractors
        shuffle(options)

        self.ids.option1.text = options[0].strip()
        self.ids.option2.text = options[1].strip()
        self.ids.option3.text = options[2].strip()

        self.correct_answer = correct_answer.strip()
        self.word_id = word_id

        for btn_id in ['option1', 'option2', 'option3']:
            btn = self.ids[btn_id]
            btn.border_color = [0, 0, 0, 0]

        self.reset_colors()
        self.hide_buttons()

    def reset_colors(self):
        for btn_id in ['option1', 'option2', 'option3']:
            btn = self.ids[btn_id]
            btn.background_color = [1, 1, 1, 1]

    def hide_buttons(self):
        self.ids.next_button.disabled = True
        self.ids.next_button.opacity = 0

    def check_answer(self, answer):
        for btn_id in ['option1', 'option2', 'option3']:
            btn = self.ids[btn_id]
            btn.border_color = [0, 0, 0, 0]

        for btn_id in ['option1', 'option2', 'option3']:
            btn = self.ids[btn_id]
            if btn.text == self.correct_answer:
                btn.border_color = [0.3, 0.8, 0.4, 1]

        if answer != self.correct_answer:
            for btn_id in ['option1', 'option2', 'option3']:
                btn = self.ids[btn_id]
                if btn.text == answer:
                    btn.border_color = [0.9, 0.3, 0.3, 1]

        if answer == self.correct_answer:
            app = App.get_running_app()
            app.db.increase_k(self.word_id)
            if app.db.get_k(self.word_id) == 5:
                app.db.add_to_dictionary(self.word_id)


        self.ids.next_button.disabled = False
        self.ids.next_button.opacity = 1

    def next_word(self):
        self.start_practice(self.lang_code)


class DictionaryScreen(Screen):
    pass


class FlashcardScreenManager(ScreenManager):
    pass


class FlashcardApp(App):
    def build(self):
        self.font_name = 'JetBrainsMono'
        self.db = Database()
        return FlashcardScreenManager()    
        
    def on_stop(self):
        self.db.close()


if __name__ == '__main__':
    FlashcardApp().run()