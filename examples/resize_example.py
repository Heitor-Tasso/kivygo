import __init__
from kivygo.app import GoApp
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivygo.behaviors.resizable import GoSelectResizableBehavior
from kivy.uix.button import Button


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<ButtonResizable@GoSelectResizableBehavior+Button>:

<Manager>:

    GoSelectResizableBehavior:
        canvas.before:
            Color:
                rgba: [1, 1, 0, 1]
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint: [None, None]
        size: [dp(300), dp(300)]
        pos: [20, 40]

    ButtonResizable:
        size_hint: None, None
        size: [dp(200), dp(150)]
        pos: [200, 70]


""")


class Manager(FloatLayout):
	pass

class ExampleUixApp(GoApp):
	def build(self):
		return Manager()
	

if __name__ == "__main__":
	ExampleUixApp().run()

