
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.uix.label import Label

from kivygo.behaviors.ripple_effect import RippleEffectBehavior
from kivygo.behaviors.fade_effect import FadeEffectBehavior
from kivygo.behaviors.button import ButtonBehavior, ToggleButtonBehavior
from kivygo.colors import ColorBase


Builder.load_string("""

<GoButton>:
	background_color: GoAppColor.colors.terciary_default
	background_hover: GoAppColor.colors.terciary_hover
	background_disabled: GoAppColor.colors.terciary_disabled
	background_pressed: self.background_hover

	border_color: GoAppColor.colors.terciary_border
	border_hover: GoAppColor.colors.terciary_border_pressed
	border_disabled: GoAppColor.colors.terciary_border_disabled


<BaseEffectButton>:
	radius_effect: self.radius

	effect_color: GoAppColor.colors.terciary_effect

	
<RippleButton>:
			
<RippleToggleButton>:
	

<FadeButton>:
		
<FadeToggleButton>:

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

class BaseEffectButton(GoButton):

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


class RippleButton(BaseEffectButton, RippleEffectBehavior):
	pass

class RippleToggleButton(ToggleButtonBehavior, RippleButton):
	pass


class FadeButton(BaseEffectButton, FadeEffectBehavior):
	pass

class FadeToggleButton(ToggleButtonBehavior, FadeButton):
	pass

