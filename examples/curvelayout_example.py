import __init__
from kivygo.app import GoApp
from kivy.lang.builder import Builder
from kivygo.layouts.curvelayout import CurveLayout
from kivy.properties import StringProperty
from kivygo.widgets.button import GoRippleButton


Builder.load_string("""

<CurveLayoutExample>:
    color: [1, 0, 0, 1]
    GoRippleButton:
        text: root.anim_state
        size_hint: None, None
        size: root.width / 2, root.height / 2
        pos_hint: {"center_x": 0.5, "center_y": 0.5}

""")


class CurveLayoutExample(CurveLayout):

    anim_state = StringProperty("Normal")

    def __init__(self, **kw):
        super().__init__(**kw)
    
    def on_left_start(self, *args):
        self.color = [0, 1, 0, 1]
        self.anim_state = "on_left_start"

    def on_left_second_start(self, *args):
        self.color = [0, 0, 1, 1]
        self.anim_state = "on_left_second_start"

    def on_right_start(self, *args):
        self.color = [1, 1, 1, 1]
        self.anim_state = "on_right_start"

    def on_right_second_start(self, *args):
        self.color = [0, 1, 1, 1]
        self.anim_state = "on_right_second_start"

    def on_right_finish(self, *args):
        self.color = [1, 1, 0, 1]
        self.anim_state = "on_right_finish"

    def on_reset_left(self, *args):
        self.color = [1, 0, 1, 1]
        self.anim_state = "on_reset_left"


class CurveLayoutExampleApp(GoApp):
    def build(self):
        return CurveLayoutExample()


if __name__ == "__main__":
    CurveLayoutExampleApp().run()