import __init__
from kivygo.app import kivygoApp
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivygo.uix.bezier import BezierLine


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<Manager>:
    Label:
        size_hint_y: None
        text_size: self.width, None
        height: self.texture_size[1]
        pos_hint: {'top': 1}
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
                rgba: [1, 1, 1, 0.8]
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

class Manager(FloatLayout):
	pass

class ExampleUixApp(kivygoApp):
	def build(self):
		return Manager()
	

if __name__ == "__main__":
	ExampleUixApp().run()

