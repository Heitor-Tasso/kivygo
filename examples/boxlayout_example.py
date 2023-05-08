import __init__
from kivygo.app import kivygoApp
from kivy.lang import Builder
from kivygo.uix.boxlayout import ColoredBoxLayout
from kivygo.uix.button import ButtonEffect

Builder.load_string("""

<Manager>:
    orientation: 'vertical'
	background_color: [1, 1, 1, 0.8]
	padding: "40dp"
	ButtonEffect:
		size_hint_y: None
		height: "300dp"
		text: "ButtonEffect"
	ColoredBoxLayout:
		background_color: [0, 1, 0, 1]
		padding: "40dp"
		ButtonEffect:
			text: 'Effect 1'
		ButtonEffect:
			text: 'Effect 2'
""")


class Manager(ColoredBoxLayout):
	pass

class ExampleUixApp(kivygoApp):
	def build(self):
		return Manager()
	

if __name__ == "__main__":
	ExampleUixApp().run()

