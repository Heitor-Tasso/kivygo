
import __init__
from kivygo.app import kivygoApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder


from kivygo.uix.button import NeuButton, NeuCircularButton
from kivygo.uix.slider import NeuSlider



from kivygo.uix.screenmanager import SwapScreen
from kivygo.uix.boxlayout import ColoredBoxLayout


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex
#:import BoxLayout kivy.uix.boxlayout.BoxLayout


<ManagerScreen>:

	SwapScreen:
		name: "screen_2"
		
		ColoredBoxLayout:
			orientation: "vertical"
			background_color: hex("#ccccd9")

			Label:
				text_size: self.size
				size_hint_y: None
				height: '80dp'
				halign: "center"
				valign: "center"
				font_size: '40sp'
				text: 'NeuKivy Buttons'
				color: hex("#8a49e3")

			BoxLayout:
				padding: ['40dp']
				spacing: "30dp"

				Widget:

				NeuButton:
					up_elevation: 2
					text: 'NeuButton'
					icon:'plus'
					size: [dp(150), dp(150)]
					icon_pos: 'right'
					text_color: hex("#8a49e3")
					comp_color: hex("#ccccd9")
					
				NeuButton:
					up_elevation: 2
					text: 'NeuButton Rounded'
					size: [150, 150]
					text_color: hex("#8a49e3")
					radius: [dp(20)] * 4
				
				NeuCircularButton:
					up_elevation: 2
					text: 'NeuCircularButton'
					radius: dp(150)
					text_color: hex("#8a49e3")
				
				Widget:
								
			ColoredBoxLayout:
				background_color: hex("#333333")
				
				Widget:

				NeuCircularButton:
					pos_hint: {'center_x':.3,'center_y':.5}
					text: 'NeuKivy'
					radius: dp(200)
					down_elevation: 1
					up_elevation: 3
					font_size: '20sp'
					text_color: hex("#b7597f")
				
				Widget:

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

