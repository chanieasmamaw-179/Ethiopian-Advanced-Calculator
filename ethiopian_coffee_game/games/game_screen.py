from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        btn = Button(
            text="I AM GAME SCREEN",
            font_size=30
        )

        self.add_widget(btn)