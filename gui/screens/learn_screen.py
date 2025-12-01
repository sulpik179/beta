from kivy.app import App
from kivy.uix.screenmanager import Screen
from random import shuffle
from kivy.graphics import Color, Rectangle


from gui.utils.lang_popup import LanguageSelectPopup


class LearnScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.apply_theme()

    def on_enter(self):
        self.apply_theme()
        app = App.get_running_app()
        word_row = app.db.get_word_for_learn()

        if not word_row:
            self.ids.word_label.text = 'Больше нет слов для изучения :('
            self.ids.transcription_label.text = ''
            self.ids.sentence_label.text = 'Попробуйте режим Practice'
        
            self.ids.option1.opacity = 0
            self.ids.option1.disabled = True
            self.ids.option2.opacity = 0
            self.ids.option2.disabled = True
            self.ids.option3.opacity = 0
            self.ids.option3.disabled = True

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
        is_dark = app.is_dark_theme

        # Цвета фона
        dark_bg = (0.05, 0.06, 0.07, 1)    # #0c1013
        light_bg = (0.90, 0.93, 0.96, 1)   # #e6edf4

        # Цвета текста
        dark_text = (0.90, 0.93, 0.96, 1)  # светлый для тёмной темы
        light_text = (0.11, 0.14, 0.15, 1) # тёмный для светлой темы
        text_color = dark_text if is_dark else light_text

        # Создаём или обновляем фон
        with self.canvas.before:
            Color(*dark_bg if is_dark else light_bg)
            Rectangle(pos=self.pos, size=self.size)

        # Обновляем цвета текста у main_word, transcription, sentence
        for label_id in ['word_label', 'transcription_label', 'sentence_label']:
            if hasattr(self.ids, label_id):
                self.ids[label_id].color = text_color
        
        

    def start_learning(self, lang_code, word_row):
        self.lang_code = lang_code

        if not word_row:
            print('word_row is empty')

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
        for btn_id in ['option1', 'option2', 'option3']:
            self.ids[btn_id].disabled = not enabled

    def reset_colors(self):
        for btn_id in ['option1', 'option2', 'option3']:
            btn = self.ids[btn_id]
            # Оставляем фиксированный фон кнопки
            btn.background_color = [0.62, 0.71, 0.75, 1]
            btn.border_color = [0, 0, 0, 0]

    def hide_buttons(self):
        self.ids.next_button.disabled = True
        self.ids.next_button.opacity = 0
        


    def check_answer(self, answer):
        self.enable_answer_buttons(False)

        # Сбросим цвета обводки
        for btn_id in ['option1', 'option2', 'option3']:
            btn = self.ids[btn_id]
            btn.border_color = [0, 0, 0, 0]

        if answer != self.correct_answer:
            for btn_id in ['option1', 'option2', 'option3']:
                btn = self.ids[btn_id]
                if btn.text == answer:
                    btn.border_color = [0.9, 0.3, 0.3, 1] # красная обводка

        for btn_id in ['option1', 'option2', 'option3']:
            btn = self.ids[btn_id]
            if btn.text == self.correct_answer:
                btn.border_color = [0.3, 0.8, 0.4, 1] # зелёная обводка

        if answer == self.correct_answer:
            app = App.get_running_app()
            app.db.add_to_practice(self.word_id)
        
        fixed_alpha = 0.6  # <-- ваша фиксированная прозрачность
        fixed_color = (0.62, 0.71, 0.75, fixed_alpha)

        for btn_id in ['option1', 'option2', 'option3', 'next_button']:
            if hasattr(self.ids, btn_id):
                btn = self.ids[btn_id]
                btn.background_color = fixed_color

        self.ids.next_button.disabled = False
        self.ids.next_button.opacity = 1
        # Устанавливаем цвет кнопки "Next" при показе
        


    def next_word(self):
        if self.ids.next_button.text == 'Main':
            self.go_to_main(None)
            return
        
        self.reset_colors()
        self.enable_answer_buttons(True)

        app = App.get_running_app()
        word_row = app.db.get_word_for_learn()
        if word_row:
            self.start_learning(self.lang_code, word_row)  
        else:
            self.ids.word_label.text = 'Больше нет слов для изучения :('
            self.enable_answer_buttons(False)
            self.ids.next_button.text = 'Main'

    def go_to_main(self, instance):
        from kivy.app import App
        app = App.get_running_app()
        app.root.current = 'main'
        