from __init__ import ExampleAppDefault
from kivygo.layouts.circularlayout import GoCircularLayout
from kivy.uix.button import Button


class CircLayoutExampleApp(ExampleAppDefault):
    def build(self):
        cly = GoCircularLayout(direction="cw", start_angle=-75, inner_radius_hint=.7, padding="20dp")

        for i in range(1, 13):
            cly.add_widget(Button(text=str(i), font_size="30dp"))

        return cly

if __name__ == "__main__":
    CircLayoutExampleApp().run()
