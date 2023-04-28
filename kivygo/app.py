import os, json
from kivy.properties import (
	StringProperty, ColorProperty,
	ObjectProperty
)
from kivy.utils import get_color_from_hex
from kivy.app import App
from .utils import do_correction_path


class kivygoApp(App):

	primary_color = ColorProperty(get_color_from_hex("007AFF"))
	secondary_color = ColorProperty(get_color_from_hex("5AC8FA"))
	accent_color = ColorProperty(get_color_from_hex("FF2D55"))
	background_color = ColorProperty(get_color_from_hex("FFFFFF"))
	foreground_color = ColorProperty(get_color_from_hex("F2F2F7"))
	border_color = ColorProperty(get_color_from_hex("C2C2C2"))
	text_color = ColorProperty(get_color_from_hex("000000"))
	heading_color = ColorProperty(get_color_from_hex("333333"))
	subheading_color = ColorProperty(get_color_from_hex("4A4A4A"))
	error_color = ColorProperty(get_color_from_hex("FF3B30"))
	success_color = ColorProperty(get_color_from_hex("4CD964"))
	warning_color = ColorProperty(get_color_from_hex("FF9500"))
	info_color = ColorProperty(get_color_from_hex("007AFF"))
	disabled_color = ColorProperty(get_color_from_hex("C7C7CC"))
	active_color = ColorProperty(get_color_from_hex("007AFF"))
	inactive_color = ColorProperty(get_color_from_hex("8E8E93"))
	hover_color = ColorProperty(get_color_from_hex("F2F2F7"))
	focus_color = ColorProperty(get_color_from_hex("007AFF"))
	selected_color = ColorProperty(get_color_from_hex("007AFF"))
	unselected_color = ColorProperty(get_color_from_hex("8E8E93"))

	path_json = StringProperty("pallet")
	theme_json = ObjectProperty(None)

	root_path = StringProperty("")

	icon_path = StringProperty("assets/icons")

	image_path = StringProperty("assets/images")

	font_path = StringProperty("fonts")


	_app_file = StringProperty(os.path.split(__file__)[0])


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
				setattr(self, key, get_color_from_hex(value))
			else:
				setattr(self, key, value)

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

	

