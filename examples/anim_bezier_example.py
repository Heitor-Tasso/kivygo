import __init__
from kivy.app import App
from kivy.lang import Builder
from math import cos, sin, radians
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import ListProperty, BooleanProperty

from kivygo.uix.input import IconInput
from kivygo.uix.slider import NeuSlider
from kivygo.uix.button import ButtonEffect
from kivygo.uix.spinner import EffectSpinner
from kivygo.uix.label import AnimatedBezierLabel
from kivygo.uix.boxlayout import ColoredBoxLayout


Builder.load_string("""

#:import chain itertools.chain
#:import hex kivy.utils.get_color_from_hex

<ValueSlider@BoxLayout>:
    value: slider.value
    on_value: slider.value = self.value
    min: slider.min
    on_min: slider.min = self.min
    max: slider.max
    on_max: slider.max = self.max
    orientation: 'vertical'
    size_hint: None, None
    size: "200dp", self.minimum_height
    label_text: "Example"
        
    Label:
        text: root.label_text
        size_hint_y: None
        height: "30dp"

    BoxLayout:
        size_hint_y: None
        height: "50dp"
        Label:
            text: str(round(root.value, 2))
            size_hint_x: None
            width: "50dp"
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center'
            NeuSlider:
                id: slider
                size_hint_y: None
                height: "30dp"
                thumb_color: [0.2, 0.9, 0.2, 1]
                thumb_padding: 10
                radius: [10, 10, 10, 10]
                background_color: hex("#14b9e3")

<BezierTest>:
    background_color: hex("#333333")
    canvas.after:
        Color:
            rgba: [1, 1, 1, 1]
        Line:
            bezier: self.points
            close: self.loop

        Point:
            points: self.points
            pointsize: 5

        Line:
            points: self.points

            
    BoxLayout:
        orientation: "vertical"
        Label:
            text: str(label.bezier_length)
            size_hint: None, None
            size: self.texture_size[0] + dp(20), self.texture_size[1] + dp(30)

        AnimatedBezierLabel:
            id: label
            points: root.points
            letter_duration: round(duration_slider.value, 2)
            letter_offset: offset_slider.value
            transform: self.bezier
            target_text: ti.input_text
            font_size: dp(font_size_slider.value)
            transition_function: transitions.text or 'linear'

    BoxLayout:
        size_hint_x: None
        width: '250dp'
        orientation: "vertical"
        spacing: "20dp"
        padding: "20dp"
        ValueSlider:
            label_text: "duration"
            id: duration_slider
            value: 5.00
            min: 0.01
            max: 10

        ValueSlider:
            label_text: "time offset"
            id: offset_slider
            value: 0.10
            min: 0.01
            max: 10

        ValueSlider:
            label_text: "font size"
            id: font_size_slider
            value: 50.00
            min: 10
            max: 100

        EffectSpinner:
            label_text: "transition"
            text_autoupdate: True
            id: transitions
            size_hint_y: None
            height: '50dp'
            values: ['linear', 'out_bounce', 'out_elastic', 'out_quad', 'out_sine']

        IconInput:
            id: ti
            multiline: False
            radius: [dp(5)] * 4

        ValueSlider:
            label_text: "progress"
            id: progress
            value: label._time
            on_value: label._time = self.value
            min: 0
            max: label.letter_duration + label.letter_offset + len(label.target_text)

        Widget:

        BoxLayout:
            spacing: '20dp'
            size_hint_y: None
            height: '70dp'

            AnchorLayout:
                anchor_x: "center"
                anchor_y: "center"
                ButtonEffect:
                    text: 'play!'
                    on_press: label.animate()
                    size_hint: None, None
                    size: '70dp', '50dp'
            
            AnchorLayout:
                anchor_x: "center"
                anchor_y: "center"
                ButtonEffect:
                    text: 'export'
                    on_press: app.write_points()
                    size_hint: None, None
                    size: '70dp', '50dp'

""")

class BezierTest(ColoredBoxLayout):
    points = ListProperty([0, 0])
    loop = BooleanProperty(False)
    started = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.d = 10  # pixel tolerance when clicking on a point
        self.ids.label.bind(size=self.start)

    def start(self, *args):
        if self.get_root_window() != None:
            self.ids.label.unbind(size=self.start)
            if not self.started:
                Clock.schedule_once(self.start)
                self.started = True
                return None
        else:
            return None

        x, y = self.ids.label.center_x, self.ids.label.center_y
        l = 150
        points = [x, y]

        for i in range(60, 270, 50):
            i = radians(i)
            points.extend([x + 40 + cos(i) * l, y + sin(i) * l])
            # points.insert(0, x + cos(i) * l)
            # points.insert(1, y + sin(i) * l)
        
        self.points = points

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            points = list(zip(self.points[::2], self.points[1::2]))
            for i, p in enumerate(points):
                if abs(touch.pos[0] - self.pos[0] - p[0]) < self.d \
                    and abs(touch.pos[1] - self.pos[1] - p[1]) < self.d:
                    if touch.is_double_tap:
                        self.points.pop(i * 2)
                        self.points.pop(i * 2)
                        return True
                    touch.ud['current_point'] = i + 1
                    touch.grab(self)
                    return True

            if touch.is_double_tap:
                # find the nearest point
                if not points:
                    self.add_point(0, touch)
                    return

                v = Vector(touch.pos)
                pts = sorted(enumerate(points), key=lambda x: v.distance(x[1]))
                ids = [x[0] for x in pts]
                if ids[0] == 0:
                    # insert before 1st
                    idx = 0
                elif ids[0] == len(ids) - 1:
                    # insert after last
                    idx = len(ids)
                elif ids.index(ids[0] - 1) < ids.index(ids[0] + 1):
                    idx = ids[0]
                else:
                    idx = ids[0] + 1

                self.add_point(idx, touch)
            # insert a point between them, at position of the touch
        return super().on_touch_down(touch)

    def add_point(self, idx, touch):
        self.points.insert(idx * 2, touch.x)
        self.points.insert(idx * 2 + 1, touch.y)
        touch.grab(self)
        touch.ud['current_point'] = idx + 1

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
        else:
            return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            c = touch.ud['current_point']
            self.points[(c - 1) * 2] = touch.pos[0] - self.pos[0]
            self.points[(c - 1) * 2 + 1] = touch.pos[1] - self.pos[1]
            return True
        return super().on_touch_move(touch)




class Main(App):
    def build(self):
        return BezierTest()

    def write_points(self):
        with open('points.csv', 'w') as f:
            f.write(';'.join(str(x) for x in self.root.points))


if __name__ == "__main__":
    Main().run()
