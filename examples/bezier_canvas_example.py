import __init__
from kivygo.app import kivygoApp
from kivy.uix.widget import Widget
from kivygo.uix.boxlayout import ColoredBoxLayout
from kivy.lang import Builder
from kivygo.uix.bezier import BezierLine


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<Manager>:
    FloatLayout:
        Label:
            size_hint_y: None
            text_size: self.width, None
            height: self.texture_size[1]
            pos: self.parent.center_x - (self.width / 2), self.parent.top - self.height
            color: [0, 0, 0, 1]
            padding: 10, 10

            text:
                '\\n'.join((
                'click to create line',
                'click near a point to drag it',
                'click near a line to create a new point in it',
                'double click a point to delete it'
                ))

            canvas.before:
                Color:
                    rgba: app.accent_color
                Rectangle:
                    pos: self.pos
                    size: self.size

        BezierCanvas:
""")


class BezierCanvas(Widget):

	def on_touch_down(self, touch):
		if super().on_touch_down(touch):
			return True

		bezierline = BezierLine()
		bezierline.points = [touch.pos, touch.pos]
		touch.ud['selected'] = 1
		touch.grab(bezierline)
		self.add_widget(bezierline)
		return True

class Manager(ColoredBoxLayout):
	pass

class ExampleUixApp(kivygoApp):
	def build(self):
		return Manager()
	

if __name__ == "__main__":
	ExampleUixApp().run()

