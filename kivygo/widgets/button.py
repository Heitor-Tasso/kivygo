
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivygo.behaviors.effect import GoRippleEffectBehavior
from kivygo.behaviors.effect import GoFadeEffectBehavior
from kivygo.behaviors.button import GoButtonBehavior, GoToggleButtonBehavior
from kivygo.colors import GoColorBase


Builder.load_string("""

<GoButton>:
	color: GoColors.at_terciary_default
	background_color: GoColors.terciary_default
	background_hover: GoColors.terciary_hover
	effect_color: GoColors.terciary_effect
	background_pressed: self.background_hover

	border_color: GoColors.no_color
	border_hover: GoColors.no_color
	border_disabled: GoColors.no_color


<GoButtonRipple>:
			
<GoToggleButtonRipple>:
	

<GoButtonFade>:
		
<GoToggleButtonFade>:

""")

class GoButton(GoColorBase, GoButtonBehavior, Label):

	background_pressed = ListProperty([0]*4)

	def on_touch_down(self, touch):
		if not self.collide_point(*touch.pos):
			return False

		result = super().on_touch_down(touch)

		if self.state == "down":
			self._background_color = self.background_pressed

		return result

	def on_touch_up(self, touch):
		result = super().on_touch_up(touch)

		if self.state == "normal":
			if not self.hover_visible:
				self._background_color = self.background_color
			else:
				self._background_color = self.background_hover
		
		if not self.collide_point(*touch.pos):
			return False

		return result


class GoButtonRipple(GoRippleEffectBehavior, GoButton):
	pass

class GoToggleButtonRipple(GoToggleButtonBehavior, GoButtonRipple):
	pass


class GoButtonFade(GoFadeEffectBehavior, GoButton):
	pass

class GoToggleButtonFade(GoToggleButtonBehavior, GoButtonFade):
	pass

