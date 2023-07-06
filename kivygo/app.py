import os
from kivy.properties import StringProperty
from kivy.app import App
from kivygo.utils import do_correction_path
from kivy.lang.builder import Builder

Builder.load_string("""

#:import Colors kivygo.colors.Colors
#:import App kivy.app.App

#:set GoColors Colors()


""")

class GoApp(App):

	root_path = StringProperty("")

	icon_path = StringProperty("assets/icons")

	image_path = StringProperty("assets/images")

	font_path = StringProperty("fonts")
	
	_app_file = StringProperty(os.path.split(__file__)[0])


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
