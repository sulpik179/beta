from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ListProperty


class RoundedButton(Button):
    radius = ListProperty([10])
    bg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            self._color = Color(*self.bg_color)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)

        self.bind(
            pos=self._update_rect,
            size=self._update_rect,
            bg_color=self._update_color,
        )

    def _update_rect(self, *_):
        self._rect.pos = self.pos
        self._rect.size = self.size

    def _update_color(self, *_):
        self._color.rgba = self.bg_color
