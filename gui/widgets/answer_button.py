from kivy.uix.button import Button
from kivy.graphics import Color, Line
from kivy.properties import ListProperty


class AnswerButton(Button):
    border_color = ListProperty([0, 0, 0, 0])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(border_color=self.update_border)
    
    def update_border(self, *args):
        self.canvas.after.clear()
        with self.canvas.after:
            Color(*self.border_color)
            Line(
                rectangle=(self.x, self.y, self.width, self.height),
                width=3
            )