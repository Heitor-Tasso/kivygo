
from kivy.uix.floatlayout import FloatLayout
from kivygo.behaviors.hover import HoverBehavior
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, NumericProperty


Builder.load_string("""

<ColoredFloatLayout>:
	canvas.before: 
		Color:
			rgba: self.background_color
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: self.radius
	canvas.after:
		Color:
			rgba: self.stroke_color
		Line:
			rounded_rectangle: [*self.pos, *self.size, *self.radius]
			width: self.stroke_width

""")


class ColoredFloatLayout(FloatLayout, HoverBehavior):
	background_color = ListProperty([0, 0, 0, 0])
	radius = ListProperty([0, 0, 0, 0])
	stroke_color = ListProperty([0, 0 ,0 ,0])
	stroke_width = NumericProperty(2)

