import __init__
from kivygo.app import kivygoApp
from kivy.lang import Builder
from kivygo.uix.anchorlayout import ColoredAnchorLayout
from kivygo.uix.button import ButtonEffect

Builder.load_string("""

<Manager>:
    anchor_y: "center"
	anchor_x: "center"
	background_color: [1, 1, 1, 0.8]
	ButtonEffect:
		size_hint: None, None
		size: "250dp", "100dp"
		text: "ButtonEffect"
""")


class Manager(ColoredAnchorLayout):
	pass

class ExampleUixApp(kivygoApp):
	def build(self):
		return Manager()
	

if __name__ == "__main__":
	ExampleUixApp().run()

