import random
import os

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.app import App
from kivy.metrics import sp, dp
from kivy.clock import Clock
from kivy.core.audio import SoundLoader


# ─────────────────────────────
# LEVEL CONFIG
# ─────────────────────────────
LEVELS = [
    (2, 2, 1.2),
    (3, 3, 1.1),
    (4, 4, 1.0),
    (5, 4, 0.95),
    (6, 4, 0.90),
    (7, 4, 0.80),
    (8, 4, 0.75),
    (9, 4, 0.65),
    (10, 4, 0.55),
    (10, 5, 0.45),
]

ALL_COFFEE_ITEMS = [
    "BUNA", "JEBENA", "KAFA", "SIDAMA", "HARAR",
    "YIRGALEM", "LIMU", "GUJI", "TEPPI", "GIMBI"
]


# ─────────────────────────────
# SAFE SOUND LOADER
# ─────────────────────────────
def load_sound(path):
    try:
        if os.path.exists(path):
            snd = SoundLoader.load(path)
            if snd:
                snd.volume = 1.0
                return snd
    except Exception as e:
        print("[SOUND ERROR]", e)

    print(f"[SOUND MISSING]: {path}")
    return None


# ─────────────────────────────
# CARD BUTTON (FIXED)
# ─────────────────────────────
class CardButton(Button):
    def __init__(self, symbol, **kwargs):
        super().__init__(**kwargs)

        self.symbol = symbol
        self.revealed = False
        self.matched = False

        self.background_normal = ""
        self.background_color = (0.32, 0.18, 0.06, 1)
        self.text = "?"
        self.bold = True

    def flip_open(self):
        self.text = self.symbol
        self.background_color = (0.72, 0.40, 0.10, 1)
        self.revealed = True

    def flip_close(self):
        self.text = "?"
        self.background_color = (0.32, 0.18, 0.06, 1)
        self.revealed = False

    def mark_matched(self):
        self.background_color = (0.12, 0.48, 0.16, 1)
        self.matched = True


# ─────────────────────────────
# GAME SCREEN
# ─────────────────────────────
class GameScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()
        self.add_widget(self.layout)

        with self.layout.canvas.before:
            Color(0.08, 0.05, 0.02, 1)
            self.bg = Rectangle()

        self.layout.bind(size=self._update_bg, pos=self._update_bg)

        # state
        self.current_level = 1
        self.selected_cards = []
        self.matches = 0
        self.attempts = 0
        self.score = 0
        self.locked = False
        self.flip_delay = 1.0

        # sounds
        self.snd_correct = load_sound("assets/sounds/correct.wav")
        self.snd_wrong = load_sound("assets/sounds/wrong.wav")
        self.snd_shuffle = load_sound("assets/sounds/shuffle.wav")

        # UI
        self.title = Label(text="ETHIOPIAN COFFEE MATCH",
                           pos_hint={"center_x": 0.5, "center_y": 0.96},
                           font_size=sp(16), bold=True)

        self.level_label = Label(text="LEVEL 1",
                                 pos_hint={"center_x": 0.5, "center_y": 0.92})

        self.score_label = Label(text="Score: 0",
                                 pos_hint={"x": 0.1, "y": 0.85})

        self.attempts_label = Label(text="Tries: 0",
                                    pos_hint={"x": 0.7, "y": 0.85})

        self.grid = GridLayout(cols=4,
                               spacing=dp(6),
                               padding=dp(8),
                               size_hint=(1, 0.7),
                               pos_hint={"center_x": 0.5, "center_y": 0.5})

        self.status = Label(text="Tap to play",
                            pos_hint={"center_x": 0.5, "center_y": 0.12})

        self.layout.add_widget(self.title)
        self.layout.add_widget(self.level_label)
        self.layout.add_widget(self.score_label)
        self.layout.add_widget(self.attempts_label)
        self.layout.add_widget(self.grid)
        self.layout.add_widget(self.status)

    # ─────────────────────────────
    # SAFE BG UPDATE
    # ─────────────────────────────
    def _update_bg(self, *args):
        self.bg.pos = self.layout.pos
        self.bg.size = self.layout.size

    # ─────────────────────────────
    # IMPORTANT: Android-safe start
    # ─────────────────────────────
    def on_enter(self):
        self.start_level()

    # ─────────────────────────────
    def start_level(self):
        self.grid.clear_widgets()
        self.selected_cards = []
        self.matches = 0
        self.attempts = 0
        self.locked = False

        idx = min(self.current_level - 1, len(LEVELS) - 1)
        pairs, cols, self.flip_delay = LEVELS[idx]

        self.grid.cols = cols

        self.level_label.text = f"LEVEL {self.current_level}"
        self.status.text = "Find matching pairs!"

        items = ALL_COFFEE_ITEMS[:pairs]
        cards = items * 2
        random.shuffle(cards)

        for symbol in cards:
            card = CardButton(symbol=symbol)
            card.bind(on_press=self.on_card)
            self.grid.add_widget(card)

        if self.snd_shuffle:
            self.snd_shuffle.play()

    # ─────────────────────────────
    def on_card(self, card):
        if self.locked or card.revealed or card.matched:
            return

        card.flip_open()
        self.selected_cards.append(card)

        if len(self.selected_cards) == 2:
            self.locked = True
            self.attempts += 1
            Clock.schedule_once(self.check_match, self.flip_delay)

    # ─────────────────────────────
    def check_match(self, dt):
        c1, c2 = self.selected_cards

        if c1.symbol == c2.symbol:
            c1.mark_matched()
            c2.mark_matched()

            self.matches += 1
            self.score += 10

            self.status.text = "MATCH!"
            if self.snd_correct:
                self.snd_correct.play()

            if self.matches == LEVELS[self.current_level - 1][0]:
                Clock.schedule_once(self.next_level, 1)

        else:
            c1.flip_close()
            c2.flip_close()

            self.status.text = "Try again"
            if self.snd_wrong:
                self.snd_wrong.play()

        self.selected_cards = []
        self.locked = False

        self.score_label.text = f"Score: {self.score}"
        self.attempts_label.text = f"Tries: {self.attempts}"

    # ─────────────────────────────
    def next_level(self, dt):
        self.current_level += 1

        if self.current_level > 10:
            self.status.text = "YOU FINISHED ALL LEVELS!"
            return

        self.start_level()

    # ─────────────────────────────
    def go_menu(self, *args):
        App.get_running_app().root.current = "menu"