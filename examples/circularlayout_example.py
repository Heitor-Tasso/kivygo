import __init__
from kivygo.layouts.circularlayout import GoCircularLayout
from kivygo.app import GoApp
from kivy.uix.button import Button


class CircLayoutExampleApp(GoApp):
    def build(self):
        cly = GoCircularLayout(direction="cw", start_angle=-75, inner_radius_hint=.7, padding="20dp")

        for i in range(1, 13):
            cly.add_widget(Button(text=str(i), font_size="30dp"))

        return cly

if __name__ == "__main__":
    CircLayoutExampleApp().run()
