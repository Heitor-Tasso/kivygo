
from __init__ import ExampleAppDefault
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from kivygo.widgets.slider import GoSlider



from kivygo.widgets.screenmanager import GoSwapScreen
from kivygo.layouts.boxlayout import GoBoxLayout


Builder.load_string("""

#:import BoxLayout kivy.uix.boxlayout.BoxLayout


<ManagerScreen>:

	GoSwapScreen:
		name: "screen_5"
		
		GoBoxLayout:
			background_color: GoHexToRgba("#333333")
			orientation: "vertical"
			padding: "40dp"
			spacing: "30dp"

			Label:
				text: 'GoSlider'
				size_hint_y: None
				height: "90dp"
				valign: "center"
				halign: "center"
				text_size: self.size
				font_size: '30sp'
				font_name: 'Arial'

			GoSlider:
				elevation: 2
				border_width: 10
				thumb_color: [0.9, .3, .3, 1]
				shadow_color: [0.8, 0.8, 0.85, 0.01]
				outline_color: [0.8, 0.8, 0.85, 0.01]
				
			GoSlider:
				elevation: -2
				border_width: 10
				thumb_color: [0.8, .4, .1, 1]

			GoSlider:
				elevation: -2
				border_width: 10
				thumb_color: [0.2, 0.9, .2, 1]
				thumb_padding: 20

			GoSlider:
				elevation: -2
				border_width: 5
				thumb_color: [0.4, .4, .9, 1]
				height: dp(20)



""")


class ManagerScreen(ScreenManager):
	pass

class ExampleUixApp(ExampleAppDefault):
	def build(self):
		return ManagerScreen()
	

if __name__ == "__main__":
	ExampleUixApp().run()

