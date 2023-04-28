import __init__
from kivygo.app import kivygoApp
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivygo.uix.gradient import GradientWidget


Builder.load_string("""

<MainScreen>:
	FloatLayout:

		GradientWidget:
			pos_hint: {"center_x":.5, "center_y":.5}

		BoxLayout:
			size_hint: .5, .5
			orientation: "vertical"
			pos_hint: {"center_x":.5, "center_y":.5}

			BoxLayout:
				Label:
					text: "Hello World"
					font_style: "H3"
					halign: "center"
					text_color: [1, 1, 1, 1]

			BoxLayout:
				orientation: "vertical"

				AnchorLayout:
					Button:
						text: "Button1"
						on_release:
							print("Button1")
				AnchorLayout:
					Button:
						text: "Button2"
						on_release:
							print("Button2")

""")


class MainScreen(Screen):
	pass


class ShaderTestApp(kivygoApp):
	def build(self):
		return MainScreen()


if __name__ == "__main__":
	ShaderTestApp().run()
