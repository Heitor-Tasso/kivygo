from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivygo.behaviors.hover import HoverBehavior
from kivy.properties import ListProperty, NumericProperty
from kivygo.behaviors.drag_and_drop import DraggableLayoutBehavior
from kivy.lang.builder import Builder


Builder.load_string("""

<ColoredGridLayout>:
	canvas.before: 
		Color:
			rgba: self.background_color
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: self.radius
		Color:
			rgba: [1, 1, 1, 1]
	canvas.after:
		Color:
			rgba: self.stroke_color
		Line:
			rounded_rectangle: [*self.pos, *self.size, *self.radius]
			width: self.stroke_width
		Color:
			rgba: [1, 1, 1, 1]

""")


class ColoredGridLayout(GridLayout, HoverBehavior):
	background_color = ListProperty([0, 0, 0, 0])
	radius = ListProperty([0, 0, 0, 0])
	stroke_color = ListProperty([0, 0 ,0 ,0])
	stroke_width = NumericProperty(dp(2))


class AdjustSizeGridLayout(ColoredGridLayout):

	max_size = ListProperty([dp(235), dp(250)])

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.config)
	
	def config(self, *args):
		Window.bind(on_flip=self.set_grid_cols)
		self.set_grid_cols()


	def on_size(self, *args):
		Clock.schedule_once(self.set_grid_cols)

	def set_grid_cols(self, *args):
		w1, w2 = self.max_size
		tc = max(2, len(self.children)+1)

		for i in range(1, tc):
			w = round(self.width/i)

			if (w > w1 and w < w2) or w < w1:

				self.cols =  i - (1 if w < w1 and i > 1 else 0)
				break

			elif i == (tc - 1):
				
				self.cols = i
				break
		
		self.padding = 0
		self.spacing = 0
		Clock.schedule_once(self.check_max_width)
	
	def check_max_width(self, *args):
		if not self.children:
			return None

		w1, w2 = self.max_size

		if self.cols >= len(self.children):

			if self.children[0].width > (w2+dp(20)):

				t = int( (self.children[0].width - w2) / 2 )
				self.padding = [t, 0, t, 0]
				self.spacing = t
				return None
		
		self.padding = dp(10)
		self.spacing = dp(10)


class DraggableGridLayout(ColoredGridLayout, DraggableLayoutBehavior):

	def compare_pos_to_widget(self, widget, pos):
		x, y = pos

		if y > widget.top:
			return 'before'

		elif y < widget.y:
			return 'after'

		elif x > widget.right:
			return 'after'

		elif x < widget.x:
			return 'before'

		else:
			spacer = self.spacer_widget
			if widget.parent is spacer.parent:

				children = widget.parent.children
				if children.index(spacer) > children.index(widget):
					return 'after'

		return 'before'
