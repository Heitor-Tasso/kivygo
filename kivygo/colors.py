
from kivy.properties import (
    ListProperty, NumericProperty
)
from kivy.lang import Builder
from kivy.metrics import dp
from kivygo.behaviors.hover import GoHoverBehavior
from kivygo.widgets.widget import GoWidget
from kivy.clock import Clock


Builder.load_string("""

<GoBackgroundColor>:
	background_color: GoColors.primary_default
	
	canvas.before: 
		Color:
			rgba: self._background_color
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: self.radius
			
<GoBorderColor>:
	border_color: GoColors.primary_border
	canvas.after:
		Color:
			rgba: self._border_color
		Line:
			rounded_rectangle: [*self.pos, *self.size, *self.radius]
			width: self.border_width

<GoHoverColor>:
	background_hover: GoColors.primary_hover

<GoColorBase>:
	background_color: GoColors.primary_default
	

""")

class GoBackgroundColor(GoWidget):
	radius = ListProperty([0]*4)

	background_color = ListProperty([0]*4)
	background_disabled = ListProperty([0]*4)
	_background_color = ListProperty([0]*4)

	def __init__(self, **kwargs):

		super().__init__(**kwargs)
		Clock.schedule_once(self.set_color)
		self.bind(background_color=self.set_color)

	def set_color(self, *args):
		self._background_color = self.background_color
		if hasattr(super(), "set_color"):
			return super().set_color(*args)

	def on_disabled(self, *args):
		self._background_color = self.background_disabled
		if hasattr(super(), "on_disabled"):
			return super().on_disabled(*args)
	

class GoBorderColor(GoWidget):
	_border_color = ListProperty([0]*4)
	border_color = ListProperty([0]*4)
	border_hover = ListProperty([0]*4)
	border_disabled = ListProperty([0]*4)
	border_width = NumericProperty(dp(1.01))
	
	radius = ListProperty([0]*4)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.bind(border_color=self.set_color)

	def set_color(self, *args):
		self._border_color = self.border_color
		if hasattr(super(), "set_color"):
			return super().set_color(*args)

	def on_disabled(self, *args):
		self._border_color = self.border_disabled
		if hasattr(super(), "on_disabled"):
			return super().on_disabled(*args)

class GoHoverColor(GoHoverBehavior, GoBackgroundColor):
	background_hover = ListProperty([0]*4)

	def on_cursor_enter(self, *args):
		self._background_color = self.background_hover

		return super().on_cursor_enter(*args)

	def on_cursor_leave(self, *args):
		self._background_color = self.background_color
		return super().on_cursor_leave(*args)


class GoColorBase(GoHoverColor, GoBorderColor, GoBackgroundColor):	
	pass

