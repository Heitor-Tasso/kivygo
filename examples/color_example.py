from __init__ import ExampleAppDefault
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty


Builder.load_string("""

#:import Clipboard kivy.core.clipboard.Clipboard
#:import json json

<ColorWidget>:
	size_hint_y: None
	height: "40dp"
	canvas.before:
		Color:
			rgba: json.loads(self.hex_color)
		Rectangle:
			pos: self.pos
		    size: self.size
	on_press:
		print("self.hex_color -=> ", self.hex_color)
		Clipboard.copy(self.hex_color)
	background_color: [0, 0, 0, 0]
			
<ColorsExample>:
	GoAutoGridLayout:
		max_size: [dp(150), dp(250)]
		size_hint_y: None
		height: self.minimum_height
		padding: "20dp"
		spacing: "10dp"
		id: grid
	
""")


class ColorWidget(Button):
	hex_color = StringProperty()

class ColorsExample(ScrollView):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
	
	def on_kv_post(self, base_widget):
		Clock.schedule_once(self.start, 2)
		return super().on_kv_post(base_widget)
	
	def start(self, *args):
		app = ExampleAppDefault.get_running_app()
		if app == None:
			return Clock.schedule_once(self.start)

		names_colors = [x for x in dir(app.colors.palette) if not callable(getattr(app.colors.palette, x)) and not x.startswith("__")]

		nm = ["default", "hover", "border", "pressed", "effect"]
		index_nm = 0
		last_name = ""
		index = 0
		while index < len(names_colors):
			for i, name_color in enumerate(names_colors[index::]):
				if last_name == "" and name_color.endswith(nm[index_nm]):
					last_name = name_color[0: len(name_color)-len(nm[index_nm])-1]

				if name_color.endswith(nm[index_nm]) and last_name in name_color:
					index_nm += 1
					if index_nm == len(nm):
						index_nm = 0
						last_name = ""
					break
			
			names_colors.insert(0, names_colors[i+index])
			del names_colors[i+index+1]
			index += 1

		for color_name in reversed(names_colors):
			color_value = getattr(app.colors.palette, color_name)

			self.ids.grid.add_widget(ColorWidget(
				text=f"{color_name}", hex_color=str(color_value),
				color=app.colors.get_color_text(color_value))
			)


class ColorsExampleApp(ExampleAppDefault):
	def build(self):
		return ColorsExample()


if __name__ == "__main__":
	ColorsExampleApp().run()

