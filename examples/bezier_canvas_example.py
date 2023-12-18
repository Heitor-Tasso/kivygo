from __init__ import ExampleAppDefault
from kivygo.widgets.widget import GoWidget
from kivygo.layouts.boxlayout import GoBoxLayout
from kivy.lang import Builder
from kivygo.widgets.bezier import GoBezierLine, GlowingLine
from kivy.clock import Clock


Builder.load_string("""

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

	GoWidget:
		id: glow

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

class BezierCanvasExample(GoBoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(lambda *a: self.ids.glow.canvas.add(GlowingLine(glowBrightness=75,points=[600,360, 200, 400],rgb=[1., 1, 0],width=10)))

class BezierCanvasExampleApp(ExampleAppDefault):
	def build(self):
		return BezierCanvasExample()
	

if __name__ == "__main__":
	BezierCanvasExampleApp().run()

