from __init__ import ExampleAppDefault
from kivy.lang import Builder
from kivygo.layouts.boxlayout import GoBoxLayout
from kivygo.widgets.button import GoButtonRipple

Builder.load_string("""

#:import Dark kivygo.colors.Dark
#:import Light kivygo.colors.Light

<BoxLayoutExample>:
    orientation: 'vertical'
	background_color: GoColors.background_default
	padding: "40dp"
	GoButtonRipple:
		size_hint_y: None
		height: "300dp"
		text: "GoButtonRipple"
		on_release: GoColors.palette = (Light if GoColors.palette == Dark else Dark)
	GoBoxLayout:
		background_color: [0, 1, 0, 1]
		padding: "20dp"
		spacing: "10dp"
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


class BoxLayoutExample(GoBoxLayout):
	pass

class BoxLayoutExampleApp(ExampleAppDefault):
	def build(self):
		return BoxLayoutExample()
	

if __name__ == "__main__":
	BoxLayoutExampleApp().run()

