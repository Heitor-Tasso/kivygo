import __init__
from kivygo.uix.circularlayout import CircularLayout
from kivygo.app import kivygoApp
from kivy.uix.button import Button


class CircLayoutApp(kivygoApp):
    def build(self):
        cly = CircularLayout(direction="cw", start_angle=-75, inner_radius_hint=.7, padding="20dp")

        for i in range(1, 13):
            cly.add_widget(Button(text=str(i), font_size="30dp"))

        return cly

CircLayoutApp().run()
