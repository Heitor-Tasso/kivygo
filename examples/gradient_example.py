from __init__ import ExampleAppDefault
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivygo.widgets.gradient import GoGradientWidget


Builder.load_string("""

<GradientExample>:
	FloatLayout:

		GoGradientWidget:
			pos_hint: {"center_x":.5, "center_y":.5}

		BoxLayout:
			size_hint: .5, .5
			orientation: "vertical"
			pos_hint: {"center_x":.5, "center_y":.5}

			BoxLayout:
				GoLabel:
					text: "Hello World"
					font_style: "H3"
					halign: "center"

			BoxLayout:
				orientation: "vertical"

				AnchorLayout:
					GoButton:
						text: "Button1"
						on_release:
							print("Button1")
				AnchorLayout:
					GoButton:
						text: "Button2"
						on_release:
							print("Button2")

""")


class GradientExample(Screen):
	pass


class GradientExampleApp(ExampleAppDefault):
	def build(self):
		return GradientExample()


if __name__ == "__main__":
	GradientExampleApp().run()

