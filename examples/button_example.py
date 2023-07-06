import __init__
from kivygo.app import GoApp
from kivy.lang import Builder
from kivygo.layouts.gridlayout import GoColoredGridLayout


Builder.load_string("""

#:import Dark kivygo.colors.Dark
#:import Light kivygo.colors.Light

<ButtonExample>:
	# background_color: GoColors.warning_default
	padding: "70dp"
    spacing: '30dp'
    rows: 3

    GoRippleButton:
        text: "Normal Rectangle Button"
		on_release:
			GoColors.pallet = (Dark if GoColors.pallet == Light else Light)

        background_color: GoColors.primary_default
		background_hover: GoColors.primary_hover
		effect_color: GoColors.primary_effect
		color: GoColors.title_default
    
	GoRippleToggleButton:
        text: "Toggle Rectangle Button"
        group: "toggle"
	
    GoFadeButton:
        text: "Normal Rounded Button"
        radius: [dp(50)] * 4
        radius_effect: self.radius
	    background_color: GoColors.secondary_default
		background_hover: GoColors.secondary_hover
		effect_color: GoColors.secondary_effect
    
    GoFadeToggleButton:
        text: "Toggle Rounded Button"
	    group: "toggle"
	    background_color: GoColors.warning_default
		background_hover: GoColors.warning_hover
		effect_color: GoColors.warning_effect

""")


class ButtonExample(GoColoredGridLayout):
	pass

class ButtonExampleApp(GoApp):
	def build(self):
		return ButtonExample()
	

if __name__ == "__main__":
	ButtonExampleApp().run()

