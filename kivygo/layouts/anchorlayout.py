
from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from kivygo.colors import GoBackgroundColor, GoColorBase


Builder.load_string("""

<GoAnchorLayout>:
	background_color: GoColors.no_color
	background_disabled: GoColors.no_color
	anchor_x: "center"
	anchor_y: "center"

<GoAnchorLayoutColor>:
	background_color: GoColors.background_default
	background_hover: GoColors.background_default
	background_disabled: GoColors.background_disabled
	border_color: GoColors.no_color
	border_hover: GoColors.no_color
	border_disabled: GoColors.no_color


""")

class GoAnchorLayout(GoBackgroundColor, AnchorLayout):
	pass


class GoAnchorLayoutColor(GoColorBase, GoAnchorLayout):
	pass
