
import os
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.app import App
from kivygo.utils import do_correction_path

class GoApp(App):

	root_path = StringProperty("")

	icon_path = StringProperty("assets/icons")

	image_path = StringProperty("assets/images")

	font_path = StringProperty("fonts")
	
	_app_file = StringProperty(os.path.split(__file__)[0])

	show_fps = BooleanProperty(False)

	colors = ObjectProperty()


	def on_root_path(self, *args):
		self.root_path = do_correction_path(self.root_path)

	def get_icon(self, name, ext='png'):
		return self.get_path(f'{self.icon_path}/{name}.{ext}')
	

	def get_image(self, name, ext='png'):
		return self.get_path(f'{self.image_path}/{name}.{ext}')


	def get_font(self, path, name, ext="ttf"):
		return self.get_path(f'{self.font_path}/{path}/{name}.{ext}')


	def get_path(self, local, root_path=None):
		if root_path == None:
			self.root_path
			
		return f'{root_path}/{do_correction_path(local)}'
	
	@classmethod
	def get_root_window(self):
		_app = GoApp.get_running_app()
		if _app == None:
			return None
		return _app.root.get_root_window()

