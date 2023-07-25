
from __init__ import ExampleAppDefault
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from kivygo.widgets.camera import PlantCamera, QRCode


from kivygo.widgets.screenmanager import GoSwapScreen
from kivygo.layouts.boxlayout import GoBoxLayout


Builder.load_string("""


<CameraExample>:

	GoSwapScreen:
		name: "screen_2"
		PlantCamera:
		
	GoSwapScreen:
		name: "screen_5"
		QRCode:

""")


class CameraExample(ScreenManager):
	pass

class CameraExampleApp(ExampleAppDefault):
	def build(self):
		return CameraExample()
	

if __name__ == "__main__":
	CameraExampleApp().run()

