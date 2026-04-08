from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

import math
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt


class CalculatorApp(App):

    def comma(self, instance):
        # Avoid duplicate commas next to each other
        if not self.display.text.endswith(','):
            if self.display.text == '0':
                self.display.text = ','
            else:
                self.display.text += ','
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title = Label(
            text='Ethiopian Advanced Calculator Created by Dr. Asmamaw Yehun - 2026',
            size_hint=(1, 0.1),
            font_size='20sp'
        )
        main_layout.add_widget(title)

        self.display = TextInput(
            text='0',
            readonly=False,
            size_hint=(1, 0.2),
            font_size='22sp'
        )
        main_layout.add_widget(self.display)

        button_grid = GridLayout(cols=4, spacing=5, size_hint=(1, 0.7))

        buttons = [

            ('C', self.clear), ('(', self.bracket), (')', self.bracket), ('÷', self.operation),
            ('7', self.number), ('8', self.number), ('9', self.number), ('×', self.operation),
            ('4', self.number), ('5', self.number), ('6', self.number), ('-', self.operation),
            ('1', self.number), ('2', self.number), ('3', self.number), ('+', self.operation),
            ('0', self.number), ('.', self.decimal), ('=', self.calculate), ('←', self.backspace),

            ('sin', self.scientific), ('cos', self.scientific), ('tan', self.scientific), ('√', self.scientific),
            ('log', self.scientific), ('ln', self.scientific),

            ('π', self.constant), ('e', self.constant),

            ('d/dx', self.derivative), ('∫', self.integral), ('lim', self.limit),
            ('det', self.determinant), ('inv', self.inverse),

            ('F=ma', self.force), ('KE', self.kinetic_energy), ('PE', self.potential_energy),

            ('Matrix', self.matrix_mode),

            ('Plot', self.plot_graph)
        ]

        for text, callback in buttons:
            btn = Button(
                text=text,
                font_size='16sp',
                background_color=(0.3, 0.6, 0.8, 1)
                if text in ['+', '-', '×', '÷', '='] else (0.9, 0.9, 0.9, 1)
            )
            btn.bind(on_press=callback)
            button_grid.add_widget(btn)

        main_layout.add_widget(button_grid)

        return main_layout

    # ---------------- BASIC ----------------

    def clear(self, instance):
        self.display.text = '0'

    def backspace(self, instance):
        self.display.text = self.display.text[:-1] if len(self.display.text) > 1 else '0'

    def number(self, instance):
        self.display.text = instance.text if self.display.text == '0' else self.display.text + instance.text

    def decimal(self, instance):
        if '.' not in self.display.text:
            self.display.text += '.'

    def operation(self, instance):
        self.display.text += instance.text

    def bracket(self, instance):
        if self.display.text == '0':
            self.display.text = instance.text
        else:
            self.display.text += instance.text

    def calculate(self, instance):
        try:
            expr = self.display.text.replace('×', '*').replace('÷', '/')

            # Convert commas to proper separators (safe fix)
            expr = expr.replace(',', ',')

            self.display.text = str(sp.sympify(expr))
        except:
            self.display.text = 'Error'

    # ---------------- SCIENTIFIC ----------------

    def scientific(self, instance):
        try:
            value = float(self.display.text)

            if instance.text == 'sin':
                result = math.sin(value)
            elif instance.text == 'cos':
                result = math.cos(value)
            elif instance.text == 'tan':
                result = math.tan(value)
            elif instance.text == '√':
                result = math.sqrt(value)
            elif instance.text == 'log':
                result = math.log10(value)
            elif instance.text == 'ln':
                result = math.log(value)

            self.display.text = str(result)

        except:
            self.display.text = 'Error'

    def constant(self, instance):
        if instance.text == 'π':
            self.display.text = str(math.pi)
        elif instance.text == 'e':
            self.display.text = str(math.e)

    # ---------------- ADVANCED MATH ----------------

    def derivative(self, instance):
        try:
            x = sp.symbols('x')
            expr = sp.sympify(self.display.text)
            self.display.text = str(sp.diff(expr, x))
        except:
            self.display.text = 'Error'

    def integral(self, instance):
        try:
            x = sp.symbols('x')
            expr = sp.sympify(self.display.text)
            self.display.text = str(sp.integrate(expr, x))
        except:
            self.display.text = 'Error'

    def limit(self, instance):
        try:
            x = sp.symbols('x')
            expr = sp.sympify(self.display.text)
            self.display.text = str(sp.limit(expr, x, 0))
        except:
            self.display.text = 'Error'

    def determinant(self, instance):
        try:
            matrix = sp.Matrix(eval(self.display.text))
            self.display.text = str(matrix.det())
        except:
            self.display.text = 'Error'

    def inverse(self, instance):
        try:
            matrix = sp.Matrix(eval(self.display.text))
            self.display.text = str(matrix.inv())
        except:
            self.display.text = 'Error'

    # ---------------- PHYSICS ----------------

    def force(self, instance):
        try:
            m, a = map(float, self.display.text.split(','))
            self.display.text = str(m * a)
        except:
            self.display.text = 'Enter: mass,acceleration'

    def kinetic_energy(self, instance):
        try:
            m, v = map(float, self.display.text.split(','))
            self.display.text = str(0.5 * m * v**2)
        except:
            self.display.text = 'Enter: mass,velocity'

    def potential_energy(self, instance):
        try:
            m, g, h = map(float, self.display.text.split(','))
            self.display.text = str(m * g * h)
        except:
            self.display.text = 'Enter: m,g,h'

    # ---------------- MATRIX ----------------

    def matrix_mode(self, instance):
        self.display.text = "[[1,2],[3,4]]"

    # ---------------- GRAPH ----------------

    def plot_graph(self, instance):
        try:
            x = np.linspace(-10, 10, 100)
            y = np.sin(x)

            plt.plot(x, y)
            plt.title("Graph")
            plt.show()
        except:
            self.display.text = 'Error'


# Run app
if __name__ == '__main__':
    CalculatorApp().run()