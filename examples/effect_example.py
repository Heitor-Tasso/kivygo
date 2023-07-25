from __init__ import ExampleAppDefault
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

Builder.load_string("""

#:import EffectWidget kivy.uix.effectwidget.EffectWidget
#:import GoMaskEffect kivygo.widgets.effect.GoMaskEffect


<EffectExample>:
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
        effects: [GoMaskEffect(mask=mask, mode='substract')]
        Widget:
            canvas:
                PushMatrix
                Rotate:
                    origin: label.center
                    angle: root.time * 10
                Color:
                    rgba: [0.3, 0.8, 0.8, 0.9]
                Rectangle:
                    pos: label.pos
                    size: label.size
                PopMatrix
""")

class EffectExample(FloatLayout):
    time = NumericProperty(0)
    
    def update_time(self, dt):
        self.time += dt


class EffectExampleApp(ExampleAppDefault):
    
    def build(self):
        root = EffectExample()
        Clock.schedule_interval(root.update_time, 0)
        return root


if __name__ == "__main__":
    EffectExampleApp().run()
