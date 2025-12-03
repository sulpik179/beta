from kivy.uix.popup import Popup
from kivy.app import App


class LanguageSelectPopup(Popup):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self._callback = callback

    def apply_theme(self):
        """Обновляет только фон main_box, если есть."""
        app = App.get_running_app()

        if "main_box" in self.ids:
            box = self.ids["main_box"]
            # canvas.before = [Color, Rectangle]
            # Rectangle всегда по индексу 1
            rect = box.canvas.before.children[0]
            rect.rgba = (
                app.color_dark if app.is_dark_theme else app.color_light
            )

    def _on_select(self, code):
        try:
            self._callback(code)
        except Exception:
            pass
        self.dismiss()