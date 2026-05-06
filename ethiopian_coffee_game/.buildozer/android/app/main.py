from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from ui.menu import MenuScreen
from ui.game_screen import GameScreen


class EthiopianCoffeeApp(App):

    def build(self):
        print("🔥 BUILD CALLED")

        self.sm = ScreenManager()

        self.sm.add_widget(MenuScreen(name="menu"))
        self.sm.add_widget(GameScreen(name="game"))

        print("Screens:", self.sm.screen_names)

        self.sm.current = "menu"

        return self.sm


if __name__ == "__main__":
    EthiopianCoffeeApp().run()