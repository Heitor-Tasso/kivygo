import __init__
from kivy.lang import Builder
from kivygo.app import kivygoApp
from kivy.uix.screenmanager import ScreenManager
from kivygo.transitions import Angular, Squeeze, LinearBlur, Swap, Swirl, Cube

Builder.load_string('''

<MyScreen@Screen>:
	label_text: 'Hello'
	md_bg_color: [1, 1, 1, 1]
	source: ''
	canvas:
		Color:
			rgba: root.md_bg_color if not root.source else [1, 1, 1, 1]
		Rectangle:
			source: root.source
			pos: self.pos
			size: self.size

	BoxLayout:
		Button:
			size_hint: None, None
			size: '40dp', '40dp'
			pos_hint:{'center_x': 0.5,'center_y': 0.5}
			text: "L"
			on_release: app.switch_prev()

		Label:
			text: root.label_text
			font_size: sp(54)
			text_color: [1, 1, 1, 0.8]
			bold: True
			pos_hint:{'center_x': 0.9,'center_y': 0.9}

		Button:
			size_hint: None, None
			size: '40dp', '40dp'
			pos_hint:{'center_x': 0.5,'center_y': 0.5}
			text: "R"
			on_release: app.switch_next()

<MainWidget>:
	id: screens
	
	MyScreen:
		label_text:"Screen 1"
		name: "screen0"
		source: "kivygo/images/busan.jpg"
	
	MyScreen:
		label_text:"Screen 2"
		name: "screen1"
		source:"kivygo/images/lion.jpg"
	
	MyScreen:
		label_text:"Screen 3"
		name: "screen2"
		source: "kivygo/images/iris.jpg"


''')


class MainWidget(ScreenManager):
	pass

class DemoApp(kivygoApp):

	current_screen = 0
	current_shader = 0
	shader_length = 0

	def switch_next(self):
		self.current_shader = (self.current_shader+1)% self.shader_length

		self.root.transition = self.shader_list[self.current_shader](duration=2, direction="rl")
		c = (self.current_screen+1)%3
		self.current_screen = c
		self.root.current = f"screen{c}"
	
	def switch_prev(self):
		self.current_shader = (self.current_shader-1)% self.shader_length

		self.root.transition = self.shader_list[self.current_shader](duration=2, direction="lr")
		c = (self.current_screen - 1) % 3
		self.current_screen = c
		self.root.current = f"screen{c}"

	def on_start(self):
		self.shader_list = [Angular, Squeeze, LinearBlur, Swap, Swirl, Cube]
		self.shader_length = len(self.shader_list)
	
	def _perform_anim(self, *args):
		self.switch_next()

	def build(self):
		return MainWidget()

if __name__ == "__main__":
	DemoApp().run()
