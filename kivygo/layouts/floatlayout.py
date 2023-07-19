
from kivy.uix.floatlayout import FloatLayout
from kivy.lang.builder import Builder
from kivygo.colors import GoColorBase, GoBackgroundColor


Builder.load_string("""

<GoFloatLayout>:
	background_color: GoColors.no_color
	background_disabled: GoColors.no_color

<GoFloatLayoutColor>:
	background_color: GoColors.background_default
	background_hover: GoColors.background_default
	background_disabled: GoColors.background_disabled
	border_color: GoColors.no_color
	border_hover: GoColors.no_color
	border_disabled: GoColors.no_color

<GoFloatChild>:
	size_hint: None, None
	size: 0, 0
	pos: 0, 0

""")


class GoFloatLayout(GoBackgroundColor, FloatLayout):
	pass

class GoFloatLayoutColor(GoColorBase, GoFloatLayout):
	pass

class GoFloatChild(FloatLayout):
	pass
