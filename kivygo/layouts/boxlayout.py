from kivy.uix.boxlayout import BoxLayout
from kivygo.behaviors.drag_and_drop import DraggableLayoutBehavior
from kivy.lang.builder import Builder
from kivygo.colors import GoColorBase, GoBackgroundColor


Builder.load_string("""

<GoBoxLayout>:
	background_color: GoColors.no_color
	background_disabled: GoColors.no_color
		    
<GoBoxLayoutColor>:
	background_color: GoColors.background_default
	background_hover: GoColors.background_default
	background_disabled: GoColors.background_disabled
	border_color: GoColors.no_color
	border_hover: GoColors.no_color
	border_disabled: GoColors.no_color

""")


class GoBoxLayout(GoBackgroundColor, BoxLayout):
	pass

class GoBoxLayoutColor(GoColorBase, GoBoxLayout):
	pass

class GoDraggableBoxLayout(GoBoxLayout, DraggableLayoutBehavior):
	def compare_pos_to_widget(self, widget, pos):
		if self.orientation == 'vertical':
			return 'before' if pos[1] >= widget.center_y else 'after'
		return 'before' if pos[0] < widget.center_x else 'after'

