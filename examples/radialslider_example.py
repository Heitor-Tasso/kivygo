import __init__
from kivygo.app import kivygoApp
from kivygo.uix.radialslider import RadialSlider
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

Builder.load_string("""

<ManagerRoot>:
    orientation: "vertical"
    AnchorLayout:
        anchor_x: "center"
        anchor_y: "center"
        RadialSlider:
    
    AnchorLayout:
        anchor_x: "center"
        anchor_y: "center"
        RadialSlider:
            size_hint: (None, None)
            size: 200, 200
            track_color: "#DEDEDE"
            track_thickness: 15
            canvas.before:
                Color:
                    rgba: rgba("#FFFFFF")
                Ellipse:
                    size: self.size
                    pos: self.pos
            canvas:
                Color:
                    rgba: rgba("#3086BD")
                Line:
                    width: 15
                    circle: self.center_x, self.center_y, self.width/2 - 15, 0, self.angle
                    cap_precision: 500
            Label:
                pos: self.parent.center_x - self.width/2, self.parent.center_y - self.height/2
                text: "{}%".format(int(self.parent.value))
                color: "#808080"
                font_size: dp(35)

""")


class ManagerRoot(BoxLayout):
    pass

class RadialSliderTestApp(kivygoApp):

    def build(self):
        return ManagerRoot()


if __name__ == '__main__':
    RadialSliderTestApp().run()
