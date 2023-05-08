from kivy.uix.boxlayout import BoxLayout
from kivygo.behaviors.hover import HoverBehavior
from kivygo.behaviors.button import ButtonBehavior
from kivygo.behaviors.drag_and_drop import DraggableLayoutBehavior
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty
from kivy.metrics import dp


Builder.load_string("""

<ColoredBoxLayout>:
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


class ColoredBoxLayout(BoxLayout, HoverBehavior):

	background_color = ListProperty([0, 0, 0, 0])
	radius = ListProperty([0, 0, 0, 0])
	stroke_color = ListProperty([0, 0 ,0 ,0])
	stroke_width = NumericProperty(dp(2))


class ColoredButtonBoxLayout(ButtonBehavior, ColoredBoxLayout):
	
	background_state_color = ListProperty([-1, -1, -1, -1])

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.set_colors)

	def set_colors(self, *args):
		back2 = self.get_color(self.background_state_color, 0)
		if back2 != None:
			self._background_color = back2

		Clock.schedule_once(lambda *a: self.on_state(self, self.state))
		return super().set_colors(self, *args)

	def on_state(self, widget, state):
		if state == "down":
			back = self.get_color(self.background_state_color, 1)
			if back != None:
				self._background_color = back
			
		elif state == "normal":
			back = self.get_color(self.background_state_color, 0)
			if back != None:
				self._background_color = back


class DraggableBoxLayout(ColoredBoxLayout, DraggableLayoutBehavior):
	def compare_pos_to_widget(self, widget, pos):
		if self.orientation == 'vertical':
			return 'before' if pos[1] >= widget.center_y else 'after'
		return 'before' if pos[0] < widget.center_x else 'after'

