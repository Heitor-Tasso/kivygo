from kivy.uix.boxlayout import BoxLayout
from kivygo.behaviors.button import ButtonBehavior
from kivygo.behaviors.drag_and_drop import DraggableLayoutBehavior
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivygo.colors import ColorBase


Builder.load_string("""

<GoColoredBoxLayout>:
	background_color: GoColors.background_default
	background_hover: GoColors.background_hover
	background_disabled: GoColors.background_disabled
	border_color: GoColors.background_border
	border_hover: GoColors.background_border_pressed
	border_disabled: GoColors.background_border_disabled

""")


class GoColoredBoxLayout(ColorBase, BoxLayout):
	pass

class GoColoredButtonBoxLayout(ButtonBehavior, GoColoredBoxLayout):
	
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


class GoDraggableBoxLayout(GoColoredBoxLayout, DraggableLayoutBehavior):
	def compare_pos_to_widget(self, widget, pos):
		if self.orientation == 'vertical':
			return 'before' if pos[1] >= widget.center_y else 'after'
		return 'before' if pos[0] < widget.center_x else 'after'

