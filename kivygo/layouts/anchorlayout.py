
from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from kivygo.behaviors.ripple_effect import RippleEffectBehavior
from kivygo.colors import ColorBase


Builder.load_string("""


<GoColoredAnchorLayout>:
	background_color: GoColors.background_default
	background_hover: GoColors.background_hover
	background_disabled: GoColors.background_disabled
	border_color: GoColors.background_border
	border_hover: GoColors.background_border_pressed
	border_disabled: GoColors.background_border_disabled


""")


class GoColoredAnchorLayout(ColorBase, AnchorLayout, RippleEffectBehavior):

	def on_touch_down(self, touch):
		if not self.collide_point(*touch.pos):
			return False
		
		self.ripple_show(touch)        
		return super().on_touch_down(touch)

	def on_touch_up(self, touch):
		if not self.collide_point(*touch.pos):
			return False

		self.ripple_fade()
		return super().on_touch_up(touch)

