
import __init__
from kivygo.app import GoApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder


from kivygo.widgets.camera import PlantCamera, QRCode



from kivygo.widgets.screenmanager import SwapScreen
from kivygo.layouts.boxlayout import GoColoredBoxLayout


Builder.load_string("""


<CameraExample>:

	SwapScreen:
		name: "screen_2"
		PlantCamera:
		
	SwapScreen:
		name: "screen_5"
		QRCode:

""")


class CameraExample(ScreenManager):
	pass

class CameraExampleApp(GoApp):
	def build(self):
		return CameraExample()
	

if __name__ == "__main__":
	CameraExampleApp().run()

