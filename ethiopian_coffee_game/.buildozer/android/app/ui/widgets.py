from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle, Ellipse


class CupWidget(FloatLayout):
    def __init__(self, cup_index, has_bean=False, **kwargs):
        super().__init__(**kwargs)

        self.cup_index = cup_index
        self.has_bean = has_bean
        self.correct = False
        self.wrong = False
        self.lifted = False

        with self.canvas:
            self.color = Color(0.55, 0.28, 0.08, 1)
            self.rect = RoundedRectangle()

        self.bind(pos=self.update, size=self.update)
        self.update()

    def update(self, *args):
        x, y = self.pos
        w, h = self.size

        self.rect.pos = (x, y)
        self.rect.size = (w, h)

        self.canvas.after.clear()
        with self.canvas.after:
            if self.lifted and self.has_bean:
                Color(0.2, 0.1, 0.05, 1)
                Ellipse(pos=(x + w * 0.35, y + 10), size=(w * 0.3, w * 0.2))

            if self.correct:
                Color(0, 1, 0, 0.3)
                Ellipse(pos=(x-5, y-5), size=(w+10, h+10))

            if self.wrong:
                Color(1, 0, 0, 0.3)
                Ellipse(pos=(x-5, y-5), size=(w+10, h+10))