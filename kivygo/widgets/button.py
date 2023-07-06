
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivygo.behaviors.ripple_effect import RippleEffectBehavior
from kivygo.behaviors.fade_effect import FadeEffectBehavior
from kivygo.behaviors.button import ButtonBehavior, ToggleButtonBehavior
from kivygo.colors import ColorBase


Builder.load_string("""

<GoButton>:
	color: GoColors.text_default
	background_color: GoColors.terciary_default
	background_hover: GoColors.terciary_hover
	background_disabled: GoColors.terciary_disabled
	background_pressed: self.background_hover

	border_color: GoColors.terciary_border
	border_hover: GoColors.terciary_border_pressed
	border_disabled: GoColors.terciary_border_disabled


<GoBaseEffectButton>:
	radius_effect: self.radius

	effect_color: GoColors.terciary_effect

	
<GoRippleButton>:
			
<GoRippleToggleButton>:
	

<GoFadeButton>:
		
<GoFadeToggleButton>:

""")

class GoButton(ColorBase, ButtonBehavior, Label):

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

class GoBaseEffectButton(GoButton):

	def on_touch_down(self, touch):		
		if not self.collide_point(*touch.pos):
			return False
		
		touch.grab(self)
		self.ripple_show(touch)

		return super().on_touch_down(touch)


	def on_touch_up(self, touch):
		
		if touch.grab_current is self:
			touch.ungrab(self)
			self.ripple_fade()
		
		return super().on_touch_up(touch)


class GoRippleButton(GoBaseEffectButton, RippleEffectBehavior):
	pass

class GoRippleToggleButton(ToggleButtonBehavior, GoRippleButton):
	pass


class GoFadeButton(GoBaseEffectButton, FadeEffectBehavior):
	pass

class GoFadeToggleButton(ToggleButtonBehavior, GoFadeButton):
	pass

