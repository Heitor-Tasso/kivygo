
import __init__
from kivygo.app import kivygoApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from kivygo.uix.slider import NeuSlider



from kivygo.uix.screenmanager import SwapScreen
from kivygo.uix.boxlayout import ColoredBoxLayout


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex
#:import BoxLayout kivy.uix.boxlayout.BoxLayout


<ManagerScreen>:

	SwapScreen:
		name: "screen_5"
		
		ColoredBoxLayout:
			background_color: hex("#333333")
			orientation: "vertical"
			padding: "40dp"
			spacing: "30dp"

			Label:
				text: 'NeuSlider'
				size_hint_y: None
				height: "90dp"
				valign: "center"
				halign: "center"
				text_size: self.size
				font_size: '30sp'
				font_name: 'Arial'

			NeuSlider:
				elevation: 2
				border_width: 10
				thumb_color: [0.9, .3, .3, 1]
				shadow_color: [0.8, 0.8, 0.85, 0.01]
				outline_color: [0.8, 0.8, 0.85, 0.01]
				
			NeuSlider:
				elevation: -2
				border_width: 10
				thumb_color: [0.8, .4, .1, 1]

			NeuSlider:
				elevation: -2
				border_width: 10
				thumb_color: [0.2, 0.9, .2, 1]
				thumb_padding: 20

			NeuSlider:
				elevation: -2
				border_width: 5
				thumb_color: [0.4, .4, .9, 1]
				height: dp(20)



""")


class ManagerScreen(ScreenManager):
	pass

class ExampleUixApp(kivygoApp):
	def build(self):
		return ManagerScreen()
	

if __name__ == "__main__":
	ExampleUixApp().run()

