import os, json
from kivy.properties import (
	StringProperty, ColorProperty,
	ObjectProperty
)
from kivy.utils import get_color_from_hex
from kivy.app import App
from kivygo.utils import do_correction_path
from kivygo import colors
from kivy.lang.builder import Builder

Builder.load_string("""

#:import Colors kivygo.colors.Colors
#:import App kivy.app.App

#:set GoAppColor Colors() if App.get_running_app() == None else app.colors

""")

class kivygoApp(App):

	path_json = StringProperty("pallet")
	theme_json = ObjectProperty(None)

	root_path = StringProperty("")

	icon_path = StringProperty("assets/icons")

	image_path = StringProperty("assets/images")

	font_path = StringProperty("fonts")
	
	_app_file = StringProperty(os.path.split(__file__)[0])

	colors = ObjectProperty(None)

	def __init__(self, *args, **kwargs):
		# Set all colors properties to the App accordian to the `colors.PALLET_KEY_COLORS`
		self.colors = colors.Colors()
		
		super().__init__(*args, **kwargs)
	
	def on_current_pallet(self, *args):
		self.change_pallet(self.colors.current_pallet)

	def get_json(self, name, path=None, *args):
		if path == None:
			path = self.path_json

		with open(self.get_path(f"{path}/{name}.json"), 'r', encoding='utf-8') as file:
			return json.load(file)


	def update_json(self, new_json, name, path=None):
		if path == None:
			path = self.path_json
		
		with open(self.get_path(f"{path}/{name}.json"), 'w', encoding='utf-8') as file:
			file.write(json.dumps(new_json, indent=4))

	def on_theme_json(self, *args):
		if isinstance(self.theme_json, str):
			json_dict = self.get_json(self.theme_json)
		
		elif isinstance(self.theme_json, dict):
			json_dict = self.theme_json
		
		path = do_correction_path(self._app_file)
		default_json = self.get_json("default_json_theme", path)
		
		for key, value in json_dict:
			if key not in default_json:
				raise TypeError("Json theme has an inexistent key!")
			
			if isinstance(value, str):
				setattr(self.colors, key, get_color_from_hex(value))
			else:
				setattr(self.colors, key, value)

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

	def change_pallet(self, _obj):
		if isinstance(_obj, dict):
			return None
		
		for key in colors.PALLET_KEY_COLORS:
			if hasattr(_obj, key):
				setattr(self.colors, key, getattr(_obj, key))
			
		self.current_pallet = _obj
