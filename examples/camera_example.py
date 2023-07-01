
import __init__
from kivygo.app import kivygoApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder


from kivygo.uix.camera import PlantCamera, QRCode



from kivygo.uix.screenmanager import SwapScreen
from kivygo.uix.boxlayout import ColoredBoxLayout


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

class CameraExampleApp(kivygoApp):
	def build(self):
		return CameraExample()
	

if __name__ == "__main__":
	CameraExampleApp().run()

