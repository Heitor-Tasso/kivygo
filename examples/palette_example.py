from __init__ import ExampleAppDefault
from kivy.lang import Builder
from kivygo.layouts.boxlayout import GoBoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from kivygo import colors
from kivy.properties import ListProperty


Builder.load_string("""

#:import Dark kivygo.palette.Dark
#:import Light kivygo.palette.Light

<ItemColor>:
	padding: ('10dp', '0dp', '10dp', '0dp')
	Label:
		text: root.values[0]
		size_hint_x: 0.65
		text_size: self.size[0], None
		halign: "left"
	AnchorLayout:
		anchor_x: 'center'
		anchor_y: 'center'
		size_hint_x: 0.15
		GoBackground:
			size_hint: None, None
			size: dp(25), dp(25)
		    radius: [dp(4)]
		    background_color: root.values[1] if GoColors.palette else root.values[1]
		
	Label:
		text: str(list(map(lambda x: round(x, 2), root.values[1])))
		size_hint_x: 0.5
		text_size: self.size[0], None
		halign: "right"

<SectionColor>:
	background_color: GoColors.dif_color
	orientation: 'vertical'
	size_hint_y: None
	height: dp(400)
	ItemColor:
		values: root.values[0]
	ItemColor:
		values: root.values[1]
	ItemColor:
		values: root.values[2]
	ItemColor:
		values: root.values[3]
	ItemColor:
		values: root.values[4]
	ItemColor:
		values: root.values[5]
	ItemColor:
		values: root.values[6]
	ItemColor:
		values: root.values[7]
	ItemColor:
		values: root.values[8]
		    
<PaletteExample>:
	GoSwapScreen:
        name: "light_screen"
		id: light_screen
		background_color: GoColors.background_default
		on_leave: GoColors.palette = Dark
		ScrollView:
			GoAutoGridLayout:
				id: grid_light_screen
				size_hint_y: None
		    	height: self.minimum_height
		    	padding: dp(20)
				max_size: [dp(380), dp(400)]
		
	GoSwapScreen:
        name: "dark_screen"
		id: dark_screen
		background_color: GoColors.background_default
		on_leave: GoColors.palette = Light
		ScrollView:
			GoAutoGridLayout:
				id: grid_dark_screen
				size_hint_y: None
				height: self.minimum_height
		    	padding: dp(20)
				max_size: [dp(380), dp(400)]

""")

class ItemColor(GoBoxLayout):
	values = ListProperty(["", [0, 0, 0, 1]])

class SectionColor(GoBoxLayout):
	values = ListProperty([[["", [0, 0, 0, 1]]]*9])

class PaletteExample(ScreenManager):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		Clock.schedule_once(self.init)
	
	def init(self, *args):
		keys = colors.PALETTE_KEY_COLORS.copy()
		del keys[0:2]

		light_grid = self.ids.grid_light_screen
		dark_grid = self.ids.grid_dark_screen

		# default, disabled, hover, border, border_hover, border_pressed, border_disabled, pressed, effect
		index = 0
		while index < len(keys):
			names = keys[index:index+9]
			index += 9

			light_grid.add_widget(SectionColor(values = [[name, getattr(colors.Light, name)] for name in names]))
			dark_grid.add_widget(SectionColor(values = [[name, getattr(colors.Dark, name)] for name in names]))


class PaletteExampleApp(ExampleAppDefault):
	def build(self):
		return PaletteExample()
	

if __name__ == "__main__":
	PaletteExampleApp().run()

