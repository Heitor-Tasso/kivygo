
from kivygo.behaviors.button import ButtonBehavior, ToggleButtonBehavior
from kivygo.behaviors.ripple_effect import RippleEffectBehavior
from kivygo.behaviors.fade_effect import FadeEffectBehavior
from kivygo.behaviors.hover import HoverBehavior

from kivygo.widgets.image import GoImage
from kivy.properties import ColorProperty
from kivy.lang import Builder


Builder.load_string("""

<GoIcon>:
	size_hint: [None, None]
	size: "35dp", "35dp"

<GoIconButton>:
	size: "45dp", "45dp"
	color_hover: list(map(lambda x: max(0, x - 0.2), self.color[0:-1])) + [1]
	color_pressed: list(map(lambda x: max(0, x - 0.1), self.color))

<GoIconButtonRipple>:

<GoIconButtonFade>:
		    
<GoIconToggleButton>:
	size: "45dp", "45dp"

<GoIconToggleButtonRipple>:

<GoIconToggleButtonFade>:
		    
""")


class GoIcon(GoImage):
	pass


class GoIconButton(HoverBehavior, ButtonBehavior, GoIcon):
	
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

class GoIconButtonRipple(RippleEffectBehavior, GoIconButton):
	pass

class GoIconButtonFade(FadeEffectBehavior, GoIconButton):
	pass

class GoIconToggleButton(ToggleButtonBehavior, GoIconButton):
	pass

class GoIconToggleButtonRipple(RippleEffectBehavior, GoIconToggleButton):
	pass

class GoIconToggleButtonFade(FadeEffectBehavior, GoIconToggleButton):
	pass

