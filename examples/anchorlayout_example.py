import __init__
from kivygo.app import kivygoApp
from kivy.lang import Builder
from kivygo.uix.anchorlayout import ColoredAnchorLayout
from kivygo.uix.button import RippleButton


Builder.load_string("""

#:import Dark kivygo.colors.Dark
#:import Light kivygo.colors.Light

<AnchorLayoutExample>:
    anchor_y: "center"
	anchor_x: "center"
	background_color: app.colors.primary_default
	RippleButton:
		size_hint: None, None
		size: "250dp", "100dp"
		text: "RippleButton"
		on_release:
			app.change_pallet(Light) if app.colors.current_pallet == Dark else app.change_pallet(Dark)
""")


class AnchorLayoutExample(ColoredAnchorLayout):
	pass

class AnchorLayoutExampleApp(kivygoApp):
	def build(self):
		return AnchorLayoutExample()
	

if __name__ == "__main__":
	AnchorLayoutExampleApp().run()

