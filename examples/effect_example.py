import __init__
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

Builder.load_string("""

#:import EffectWidget kivy.uix.effectwidget.EffectWidget
#:import MaskEffect kivygo.uix.effect.MaskEffect


<MainWidget>:
    EffectWidget:
        id: mask
        opacity: 0
        Label:
            id: label
            size_hint: None, None
            size: self.texture_size
            text: 'test'
            center: self.size and root.center
            font_size: '200dp'

    AsyncImage:
        source: 'data/logo/kivy-icon-512.png'
    
    EffectWidget:
        effects: [MaskEffect(mask=mask, mode='substract')]
        Widget:
            canvas:
                PushMatrix
                Rotate:
                    origin: label.center
                    angle: app.time * 10
                Color:
                    rgba: [0.3, 0.8, 0.8, 0.9]
                Rectangle:
                    pos: label.pos
                    size: label.size
                PopMatrix
""")

class MainWidget(FloatLayout):
    pass

class MaskApp(App):
    time = NumericProperty(0)

    def build(self):
        Clock.schedule_interval(self.update_time, 0)
        return MainWidget()

    def update_time(self, dt):
        self.time += dt


if __name__ == "__main__":
    MaskApp().run()
