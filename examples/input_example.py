from __init__ import ExampleAppDefault
from kivy.lang import Builder
from kivygo.layouts.boxlayout import GoBoxLayout


Builder.load_string("""

#:import Dark kivygo.palette.Dark
#:import Light kivygo.palette.Light

<InputExample>:
	padding: "20dp"
	spacing: "20dp"
	GoInputBox:
	
	GoInputBox:
		label_text: "Login"
		size_hint_y: None
		height: dp(70)
		label_font_size: sp(16)
		outline_width: dp(2)
		GoIconButtonFade:
			type_widget: "Icon"
			size_hint_x: None
			width: dp(35)
		AnchorLayout:
			GoInputForBox:
				type_widget: "Input"
				size_hint_y: None
				height: self.minimum_height
		GoAnchorLayout:
			size_hint_x: None
			width: dp(50)
			GoIconButtonFade:
				type_widget: "Icon"
				size_hint: None, None
				size: dp(40), dp(40)
""")


class InputExample(GoBoxLayout):
	pass

class InputExampleApp(ExampleAppDefault):
	def build(self):
		return InputExample()
	

if __name__ == "__main__":
	InputExampleApp().run()

