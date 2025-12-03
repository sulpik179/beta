from kivy.app import App
from kivy.uix.screenmanager import Screen
from random import shuffle
from kivy.graphics import Color, Rectangle

from gui.utils.lang_popup import LanguageSelectPopup


class LearnScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        # apply_theme вызываем в on_enter, когда ids уже готовы

    def on_enter(self):
        self.apply_theme()
        app = App.get_running_app()
        try:
            word_row = app.db.get_word_for_learn()
        except Exception:
            word_row = None

        if not word_row:
            # Пустая страница обучения
            self.ids.word_label.text = 'Больше нет слов для изучения :('
            self.ids.transcription_label.text = ''
            self.ids.sentence_label.text = 'Попробуйте режим Practice'

            for opt in ('option1', 'option2', 'option3'):
                if hasattr(self.ids, opt):
                    self.ids[opt].opacity = 0
                    self.ids[opt].disabled = True

            self.ids.next_button.opacity = 0
            self.ids.next_button.disabled = True

            self.ids.next_button.text = 'Main'
            self.ids.next_button.disabled = False
            self.ids.next_button.opacity = 1
            self.ids.next_button.bind(on_press=self.go_to_main)
            return

        popup = LanguageSelectPopup(callback=lambda lang_code: self.start_learning(lang_code, word_row))
        popup.open()

    def apply_theme(self):
        app = App.get_running_app()
        is_dark = app.is_dark_theme if app else True

        dark_bg = (0.05, 0.06, 0.07, 1)
        light_bg = (0.90, 0.93, 0.96, 1)
        dark_text = (0.90, 0.93, 0.96, 1)
        light_text = (0.11, 0.14, 0.15, 1)
        text_color = dark_text if is_dark else light_text

        # Обновляем при изменении размера/позиции
        def _upd_bg(*args):
            if hasattr(self, '_bg_rect'):
                self._bg_rect.pos = self.pos
                self._bg_rect.size = self.size
        self.bind(pos=_upd_bg, size=_upd_bg)

        # Обновление цвета текста, если элементы существуют
        for label_id in ('word_label', 'transcription_label', 'sentence_label'):
            if hasattr(self.ids, label_id):
                self.ids[label_id].color = text_color

    def start_learning(self, lang_code, word_row):
        self.lang_code = lang_code
        if not word_row:
            print('word_row is empty')
            return

        word_id, word_en, word_ru, distractor_ru1, distractor_ru2, distractor_en1, distractor_en2, sentence_ru, sentence_en, transcription = word_row

        if lang_code == 'en_ru':
            main_word = word_en
            correct_answer = word_ru
            distractors = [distractor_ru1, distractor_ru2]
            sentence = sentence_en
            transcription = transcription.strip()
        else:
            main_word = word_ru
            correct_answer = word_en
            distractors = [distractor_en1, distractor_en2]
            sentence = sentence_ru
            transcription = '-'

        self.ids.word_label.text = main_word
        self.ids.transcription_label.text = transcription.strip()
        self.ids.sentence_label.text = sentence

        options = [correct_answer] + distractors
        shuffle(options)

        self.ids.option1.text = options[0].strip()
        self.ids.option2.text = options[1].strip()
        self.ids.option3.text = options[2].strip()

        self.correct_answer = correct_answer.strip()
        self.word_id = word_id

        self.reset_colors()
        self.enable_answer_buttons(True)
        self.hide_buttons()

    def enable_answer_buttons(self, enabled: bool):
        for btn_id in ('option1', 'option2', 'option3'):
            if hasattr(self.ids, btn_id):
                self.ids[btn_id].disabled = not enabled

    def reset_colors(self):
        for btn_id in ('option1', 'option2', 'option3'):
            if hasattr(self.ids, btn_id):
                btn = self.ids[btn_id]
                btn.background_color = [0.62, 0.71, 0.75, 1]
                # убираем рамку
                try:
                    btn.border_color = [0, 0, 0, 0]
                except Exception:
                    pass

    def hide_buttons(self):
        if hasattr(self.ids, 'next_button'):
            self.ids.next_button.disabled = True
            self.ids.next_button.opacity = 0

    def check_answer(self, answer):
        self.enable_answer_buttons(False)
        for btn_id in ('option1', 'option2', 'option3'):
            if hasattr(self.ids, btn_id):
                btn = self.ids[btn_id]
                try:
                    btn.border_color = [0, 0, 0, 0]
                except Exception:
                    pass

        if answer != self.correct_answer:
            for btn_id in ('option1', 'option2', 'option3'):
                if hasattr(self.ids, btn_id):
                    btn = self.ids[btn_id]
                    if btn.text == answer:
                        btn.border_color = [0.9, 0.3, 0.3, 1]

        for btn_id in ('option1', 'option2', 'option3'):
            if hasattr(self.ids, btn_id):
                btn = self.ids[btn_id]
                if btn.text == self.correct_answer:
                    btn.border_color = [0.3, 0.8, 0.4, 1]

        if answer == self.correct_answer:
            app = App.get_running_app()
            try:
                app.db.add_to_practice(self.word_id)
            except Exception:
                pass

        fixed_alpha = 1
        fixed_color = (0.62, 0.71, 0.75, fixed_alpha)
        for btn_id in ('option1', 'option2', 'option3'):
            if hasattr(self.ids, btn_id):
                self.ids[btn_id].background_color = fixed_color

        if hasattr(self.ids, 'next_button'):
            self.ids.next_button.disabled = False
            self.ids.next_button.opacity = 1

    def next_word(self):
        if hasattr(self.ids, 'next_button') and self.ids.next_button.text == 'Main':
            self.go_to_main(None)
            return

        self.reset_colors()
        self.enable_answer_buttons(True)

        app = App.get_running_app()
        try:
            word_row = app.db.get_word_for_learn()
        except Exception:
            word_row = None

        if word_row:
            self.start_learning(self.lang_code, word_row)
        else:
            self.ids.word_label.text = 'Больше нет слов для изучения :('
            self.enable_answer_buttons(False)
            if hasattr(self.ids, 'next_button'):
                self.ids.next_button.text = 'Main'

    def go_to_main(self, instance):
        from kivy.app import App
        app = App.get_running_app()
        app.root.current = 'main'
