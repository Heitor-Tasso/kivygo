import __init__
from kivygo.app import GoApp
from kivy.lang import Builder
from kivygo.layouts.anchorlayout import GoAnchorLayoutColor


Builder.load_string("""

#:import Dark kivygo.colors.Dark
#:import Light kivygo.colors.Light

<AnchorLayoutExample>:
    anchor_y: "center"
	anchor_x: "center"
	background_color: GoColors.primary_default
	GoButtonRipple:
		size_hint: None, None
		size: "250dp", "100dp"
		text: "GoButtonRipple"
		on_release:
			GoColors.palette = (Light if GoColors.palette == Dark else Dark)
""")


class AnchorLayoutExample(GoAnchorLayoutColor):
	pass

class AnchorLayoutExampleApp(GoApp):
	def build(self):
		return AnchorLayoutExample()
	

if __name__ == "__main__":
	AnchorLayoutExampleApp().run()

