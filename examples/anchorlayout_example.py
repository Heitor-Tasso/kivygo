from __init__ import ExampleAppDefault
from kivy.lang import Builder
from kivygo.layouts.boxlayout import GoBoxLayout


Builder.load_string("""

#:import Dark kivygo.palette.Dark
#:import Light kivygo.palette.Light

<AnchorLayoutExample>:
	padding: "20dp"
	spacing: "20dp"
	GoAnchorLayout:
		anchor_y: "center"
		anchor_x: "center"
		background_color: GoColors.primary_default
		GoButtonRipple:
			size_hint: None, None
			size: "250dp", "100dp"
			text: "GoAnchorLayout"
			on_release:
				GoColors.palette = (Light if GoColors.palette == Dark else Dark)

	GoAnchorLayoutColor:
		anchor_y: "center"
		anchor_x: "center"
		background_color: GoColors.primary_default
		GoButtonRipple:
			size_hint: None, None
			size: "250dp", "100dp"
			text: "GoAnchorLayoutColor"
			on_release:
				GoColors.palette = (Light if GoColors.palette == Dark else Dark)
""")


class AnchorLayoutExample(GoBoxLayout):
	pass

class AnchorLayoutExampleApp(ExampleAppDefault):
	def build(self):
		return AnchorLayoutExample()
	

if __name__ == "__main__":
	AnchorLayoutExampleApp().run()

