
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivygo.behaviors.ripple_effect import RippleEffectBehavior
from kivygo.behaviors.fade_effect import FadeEffectBehavior
from kivygo.behaviors.button import ButtonBehavior, ToggleButtonBehavior
from kivygo.colors import GoColorBase


Builder.load_string("""

<GoButton>:
	color: GoColors.on_terciary
	background_color: GoColors.terciary_default
	background_hover: GoColors.terciary_hover
	background_disabled: GoColors.terciary_disabled
	background_pressed: self.background_hover

	border_color: GoColors.no_color
	border_hover: GoColors.no_color
	border_disabled: GoColors.no_color


<GoBaseEffectButton>:
	radius_effect: self.radius

	effect_color: GoColors.terciary_effect

	
<GoButtonRipple>:
			
<GoToggleButtonRipple>:
	

<GoButtonFade>:
		
<GoToggleButtonFade>:

""")

class GoButton(GoColorBase, ButtonBehavior, Label):

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


class GoButtonRipple(RippleEffectBehavior, GoButton):
	pass

class GoToggleButtonRipple(ToggleButtonBehavior, GoButtonRipple):
	pass


class GoButtonFade(FadeEffectBehavior, GoButton):
	pass

class GoToggleButtonFade(ToggleButtonBehavior, GoButtonFade):
	pass

