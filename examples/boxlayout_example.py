import __init__
from kivygo.app import GoApp
from kivy.lang import Builder
from kivygo.layouts.boxlayout import GoBoxLayoutColor
from kivygo.widgets.button import GoButtonRipple

Builder.load_string("""

#:import Dark kivygo.colors.Dark
#:import Light kivygo.colors.Light

<BoxLayoutExample>:
    orientation: 'vertical'
	background_color: [1, 1, 1, 0.8]
	padding: "40dp"
	GoButtonRipple:
		size_hint_y: None
		height: "300dp"
		text: "GoButtonRipple"
		on_release:
			GoColors.palette = (Light if GoColors.palette == Dark else Dark)
	GoBoxLayoutColor:
		background_color: [0, 1, 0, 1]
		padding: "40dp"
		background_color: [0, 0, 0, 1]
		background_hover: [0, 0, 0, 1]
		background_disabled: [0, 0, 0, 1]
		border_color: [0, 0, 0, 1]
		border_hover: [0, 0, 0, 1]
		border_disabled: [0, 0, 0, 1]
		GoButtonRipple:
			text: 'Effect 1'
		GoButtonRipple:
			text: 'Effect 2'
""")


class BoxLayoutExample(GoBoxLayoutColor):
	pass

class BoxLayoutExampleApp(GoApp):
	def build(self):
		return BoxLayoutExample()
	

if __name__ == "__main__":
	BoxLayoutExampleApp().run()

