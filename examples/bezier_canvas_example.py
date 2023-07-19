import __init__
from kivygo.app import GoApp
from kivygo.widgets.widget import GoWidget
from kivygo.layouts.boxlayout import GoBoxLayoutColor
from kivy.lang import Builder
from kivygo.widgets.bezier import GoBezierLine


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<BezierCanvasExample>:
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
					rgba: GoColors.secondary_default
				Rectangle:
					pos: self.pos
					size: self.size

		BezierCanvas:
""")


class BezierCanvas(GoWidget):

	def on_touch_down(self, touch):
		resp = super().on_touch_down(touch)
		if not self.collide_point(*touch.pos):
			return resp

		bezierline = GoBezierLine()
		bezierline.points = [touch.pos, touch.pos]
		touch.ud['selected'] = 1
		touch.grab(bezierline)
		self.add_widget(bezierline)
		return True

class BezierCanvasExample(GoBoxLayoutColor):
	pass

class BezierCanvasExampleApp(GoApp):
	def build(self):
		return BezierCanvasExample()
	

if __name__ == "__main__":
	BezierCanvasExampleApp().run()

