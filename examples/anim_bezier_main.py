import __init__
from kivy.app import App
from kivy.lang import Builder
from math import cos, sin, radians
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    ListProperty, BooleanProperty,
)
from kivygo.uix.label import AnimatedBezierLabel
from kivy.vector import Vector


Builder.load_string("""

#:import chain itertools.chain
#:import dp kivy.metrics.dp

<BezierTest>:
    canvas:
        Line:
            bezier: self.points
            close: self.loop

        Point:
            points: self.points
            pointsize: 5

        Line:
            points: self.points

    AnimatedBezierLabel:
        id: label
        points: root.points
        letter_duration: duration_slider.value
        letter_offset: offset_slider.value
        transform: self.bezier
        target_text: ti.text
        font_size: dp(font_size_slider.value)
        transition_function: transitions.text or 'linear'

    Label:
        text: str(label.bezier_length)
        size_hint: None, None
        size: self.texture_size

    BoxLayout:
        size_hint_x: None
        width: '250dp'
        pos_hint: {'right': 1}
        orientation: 'vertical'
        Label:
            text: 'duration'

        ValueSlider:
            id: duration_slider
            value: 5
            min: 0.01
            max: 10

        Label:
            text: 'time offset'
        ValueSlider:
            id: offset_slider
            value: .1
            min: 0.01
            max: 10

        Label:
            text: 'font size'
        ValueSlider:
            id: font_size_slider
            value: 50
            min: 10
            max: 100

        Label:
            text: 'transition'
        Spinner:
            id: transitions
            size_hint_y: None
            height: '50dp'
            values: 'linear', 'out_bounce', 'out_elastic', 'out_quad', 'out_sine'

        TextInput:
            id: ti
            multiline: False
            size_hint_y: None
            height: '50dp'

        Label:
            text: 'progress'
        ValueSlider:
            id: progress
            value: label._time
            on_value: label._time = self.value
            min: 0
            max: label.letter_duration + label.letter_offset + len(label.target_text)

        Button:
            text: 'play!'
            on_press: label.animate()
            size_hint_y: None
            height: '50dp'
        Button:
            text: 'export'
            on_press: app.write_points()


<ValueSlider@BoxLayout>:
    value: slider.value
    on_value: slider.value = self.value
    min: slider.min
    on_min: slider.min = self.min
    max: slider.max
    on_max: slider.max = self.max

    Label:
        text: str(root.value)
    Slider:
        id: slider

""")

class BezierTest(FloatLayout):
    points = ListProperty()
    loop = BooleanProperty()

    def __init__(self, points=[], loop=False, *args, **kwargs):
        super(BezierTest, self).__init__(*args, **kwargs)
        self.d = 10  # pixel tolerance when clicking on a point
        self.points = points
        self.loop = loop

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            points = list(zip(self.points[::2], self.points[1::2]))
            for i, p in enumerate(points):
                if (
                    abs(touch.pos[0] - self.pos[0] - p[0]) < self.d and
                    abs(touch.pos[1] - self.pos[1] - p[1]) < self.d
                ):
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
        return super(BezierTest, self).on_touch_down(touch)

    def add_point(self, idx, touch):
        self.points.insert(idx * 2, touch.x)
        self.points.insert(idx * 2 + 1, touch.y)
        touch.grab(self)
        touch.ud['current_point'] = idx + 1

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
        else:
            return super(BezierTest, self).on_touch_up(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            c = touch.ud['current_point']
            self.points[(c - 1) * 2] = touch.pos[0] - self.pos[0]
            self.points[(c - 1) * 2 + 1] = touch.pos[1] - self.pos[1]
            return True
        return super(BezierTest, self).on_touch_move(touch)




class Main(App):
    def build(self):
        x = y = 150
        l = 100
        # Pacman !
        points = [x, y]
        for i in range(45, 360, 45):
            i = radians(i)
            points.extend([x + cos(i) * l, y + sin(i) * l])
        
        return BezierTest(points=points)

    def write_points(self):
        with open('points.csv', 'w') as f:
            f.write(';'.join(str(x) for x in self.root.points))

Main().run()
