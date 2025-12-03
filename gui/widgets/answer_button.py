# gui/widgets/answer_button.py
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from kivy.graphics import InstructionGroup
from kivy.properties import ListProperty


class AnswerButton(Button):
    border_color = ListProperty([0, 0, 0, 0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Подписываемся на изменение цвета/позиции/размера
        self.bind(border_color=self._on_prop_change, pos=self._on_prop_change, size=self._on_prop_change)
        self._border_instruction = None

    def _on_prop_change(self, *args):
        self.update_border()

    def update_border(self):
        # Удаляем только нашу инструкцию (если есть)
        if self._border_instruction is not None:
            try:
                self.canvas.after.remove(self._border_instruction)
            except Exception:
                # на всякий случай — игнорируем, если уже удалили
                pass
            self._border_instruction = None

        # Если цвет полностью прозрачный — ничего не рисуем
        if not self.border_color or self.border_color == [0, 0, 0, 0]:
            return

        # Создаем группу инструкций и добавляем в canvas.after (без глобальной очистки)
        ig = InstructionGroup()
        ig.add(Color(*self.border_color))
        ig.add(Line(rectangle=(self.x, self.y, self.width, self.height), width=2))
        self.canvas.after.add(ig)
        self._border_instruction = ig
