
import __init__
from kivygo.app import kivygoApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder


from kivygo.uix.camera import PlantCamera, QRCode



from kivygo.uix.screenmanager import SwapScreen
from kivygo.uix.boxlayout import ColoredBoxLayout


Builder.load_string("""


<ManagerScreen>:

	SwapScreen:
		name: "screen_2"
		PlantCamera:
		
	SwapScreen:
		name: "screen_5"
		QRCode:

""")


class ManagerScreen(ScreenManager):
	pass

class ExampleUixApp(kivygoApp):
	def build(self):
		return ManagerScreen()
	

if __name__ == "__main__":
	ExampleUixApp().run()

