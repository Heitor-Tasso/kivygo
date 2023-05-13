import __init__
from kivygo.app import kivygoApp
from kivy.lang import Builder
from kivygo.uix.anchorlayout import ColoredAnchorLayout
from kivygo.uix.button import ButtonEffect

Builder.load_string("""

#:import colors kivygo.colors

<Manager>:
    anchor_y: "center"
	anchor_x: "center"
	background_color: app.primary_color
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

