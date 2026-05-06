from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.app import App
from kivy.metrics import sp, dp


class MenuScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()

        # ✅ Dark brown background — binds to layout size
        with self.layout.canvas.before:
            Color(0.13, 0.08, 0.04, 1)  # deep espresso brown
            self.bg = Rectangle(pos=self.layout.pos, size=self.layout.size)

        self.layout.bind(size=self._update_bg, pos=self._update_bg)

        # ☕ Coffee emoji large icon
        icon = Label(
            text="☕",
            font_size=sp(64),
            pos_hint={"center_x": 0.5, "center_y": 0.78},
        )

        # 🏷️ Title
        title = Label(
            text="Ethiopian Coffee",
            font_size=sp(26),
            bold=True,
            color=(0.96, 0.78, 0.42, 1),   # golden amber
            pos_hint={"center_x": 0.5, "center_y": 0.66},
            halign="center",
            valign="middle",
        )
        title.bind(size=title.setter("text_size"))

        # 🏷️ Subtitle
        subtitle = Label(
            text="Match the Flavors",
            font_size=sp(15),
            color=(0.75, 0.60, 0.40, 1),   # muted gold
            pos_hint={"center_x": 0.5, "center_y": 0.59},
            halign="center",
            valign="middle",
        )
        subtitle.bind(size=subtitle.setter("text_size"))

        # 🎮 Start button
        btn = Button(
            text="START GAME",
            font_size=sp(18),
            bold=True,
            size_hint=(0.65, 0.09),
            pos_hint={"center_x": 0.5, "center_y": 0.38},
            background_normal="",
            background_color=(0.72, 0.40, 0.10, 1),   # rich coffee orange
            color=(1, 1, 1, 1),
        )
        btn.bind(on_press=self.start_game)

        # 🏅 How to play hint
        hint = Label(
            text="Match coffee cards before time runs out!",
            font_size=sp(12),
            color=(0.55, 0.45, 0.30, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.28},
            halign="center",
            valign="middle",
        )
        hint.bind(size=hint.setter("text_size"))

        self.layout.add_widget(icon)
        self.layout.add_widget(title)
        self.layout.add_widget(subtitle)
        self.layout.add_widget(btn)
        self.layout.add_widget(hint)
        self.add_widget(self.layout)

    def _update_bg(self, *args):
        self.bg.pos = self.layout.pos
        self.bg.size = self.layout.size

    def start_game(self, instance):
        print("BUTTON CLICKED")
        app = App.get_running_app()
        print("Current before:", app.root.current)
        app.root.current = "game"
        print("Switched to:", app.root.current)