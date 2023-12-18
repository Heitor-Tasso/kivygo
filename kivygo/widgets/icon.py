
from kivygo.behaviors.button import GoButtonBehavior, GoToggleButtonBehavior
from kivygo.behaviors.effect import GoRippleEffectBehavior
from kivygo.behaviors.effect import GoFadeEffectBehavior
from kivygo.behaviors.hover import GoHoverBehavior

from kivygo.widgets.image import GoImage
from kivy.properties import ColorProperty
from kivy.lang import Builder


Builder.load_string("""

<GoIconButton>:
	color_hover: list(map(lambda x: max(0, x - 0.2), self.color[0:-1])) + [1]
	color_pressed: list(map(lambda x: max(0, x - 0.1), self.color))

<GoIconButtonRipple>:

<GoIconButtonFade>:
		    
<GoIconToggleButton>:

<GoIconToggleButtonRipple>:

<GoIconToggleButtonFade>:
		    
""")


class GoIconButton(GoHoverBehavior, GoButtonBehavior, GoImage):
	
	color_hover = ColorProperty([0]*4)
	color_pressed = ColorProperty([0]*4)

	def on_cursor_enter(self, *args):
		self._color = self.color_hover
		return super().on_cursor_enter(*args)

	def on_cursor_leave(self, *args):
		self._color = self.color
		return super().on_cursor_leave(*args)

	def on_state(self, widget, state):
		if state == 'normal':
			self._color = self.color

		elif state == 'down':
			self._color = self.color_pressed

class GoIconButtonRipple(GoRippleEffectBehavior, GoIconButton):
	pass

class GoIconButtonFade(GoFadeEffectBehavior, GoIconButton):
	pass

class GoIconToggleButton(GoToggleButtonBehavior, GoIconButton):
	pass

class GoIconToggleButtonRipple(GoRippleEffectBehavior, GoIconToggleButton):
	pass

class GoIconToggleButtonFade(GoFadeEffectBehavior, GoIconToggleButton):
	pass

