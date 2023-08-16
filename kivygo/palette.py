
from kivy.utils import get_color_from_hex
from kivy.event import EventDispatcher
from kivy.properties import (
	ColorProperty, ObjectProperty
)


class Light:
	no_color = [0, 0, 0, 0]
	dif_color = get_color_from_hex("d242bf")

	background_default = get_color_from_hex("F2F2F2")
	
	at_background_default = get_color_from_hex("151920")

	primary_default = get_color_from_hex("1D9BF0")

	at_primary_default = get_color_from_hex("F8F8F8")

	secondary_default = get_color_from_hex("1db954")

	at_secondary_default = get_color_from_hex("F8F8F8")

	terciary_default = get_color_from_hex("820ad1")
	
	at_terciary_default = get_color_from_hex("F8F8F8")

	title_default = get_color_from_hex("F0F4F7")

	text_default = get_color_from_hex("cdd6e1")

	success_default = get_color_from_hex("00CE61")

	at_success_default = get_color_from_hex("00C853")

	error_default = get_color_from_hex("E32B2B")
	
	at_error_default = get_color_from_hex("F8F8F8")

	warning_default = get_color_from_hex("FFBB0F")
	
	at_warning_default = get_color_from_hex("F8F8F8")

	support_default = get_color_from_hex("4BC3F2")

	at_support_default = get_color_from_hex("F8F8F8")

	info_default = get_color_from_hex("007AFF")
	
	at_info_default = get_color_from_hex("007AFF")
	
	link_default = get_color_from_hex("26FBD4")
	
	
class Dark:
	no_color = [0, 0, 0, 0]
	dif_color = get_color_from_hex("d242bf")

	background_default = get_color_from_hex("151920")
	
	at_background_default = get_color_from_hex("F2F2F2")

	primary_default = get_color_from_hex("168fdc")
	
	at_primary_default = get_color_from_hex("F8F8F8")

	secondary_default = get_color_from_hex("16a54d")

	at_secondary_default = get_color_from_hex("F8F8F8")

	terciary_default = get_color_from_hex("7609bd")
	
	at_terciary_default = get_color_from_hex("F8F8F8")
	
	title_default = get_color_from_hex("F0F4F7")
	
	text_default = get_color_from_hex("e1ebf5")
	
	success_default = get_color_from_hex("00CE61")
	
	at_success_default = get_color_from_hex("00C853")
	
	error_default = get_color_from_hex("E32B2B")
	
	at_error_default = get_color_from_hex("F8F8F8")
	
	warning_default = get_color_from_hex("FFBB0F")
	
	at_warning_default = get_color_from_hex("F8F8F8")
	
	support_default = get_color_from_hex("4BC3F2")
	
	at_support_default = get_color_from_hex("F8F8F8")
	
	info_default = get_color_from_hex("007AFF")
	
	at_info_default = get_color_from_hex("007AFF")
	
	link_default = get_color_from_hex("26FBD4")
	


class GoColors(EventDispatcher):

	palette = ObjectProperty(Light)
	last_binds = []

	def __init__(self, *args, **kwargs):
		
		self.add_bg_colors_to_palette(Light)
		self.add_bg_colors_to_palette(Dark)

		for color_name in dir(self.palette):
			color_value = getattr(self.palette, color_name)

			if callable(color_value) or color_name.startswith("__"):
				continue

			self.add_new_color(color_name, color_value)

		super().__init__(*args, **kwargs)

	def __getattribute__(self, __name):
		try:
			return super().__getattribute__(__name)
		except Exception:
			self.add_new_color(__name, [0, 0, 0, 0])
			return getattr(self, __name)

	def add_new_color(self, color_name, color_value):
		self.apply_property(
			**{ color_name : ColorProperty(color_value) }
		)

	def on_palette(self, *args):
		self.change_palette(self.palette)

	def fbind(self, *args, **kwargs):
		if len(args) != 3:
			return super().fbind(*args, **kwargs)
		
		prop_name, fn, a = args
		if isinstance(a, list) and len(a) != 5:
			return super().fbind(*args, **kwargs)
		
		element, key, value, rule, idmap = a

		for i, (last_prop_name, last_element, last_key, last_uid) in enumerate(self.last_binds):
			if last_element.__ref__() is element.__ref__() and last_key == key:
				self.unbind_uid(last_prop_name, last_uid)
				self.last_binds.pop(i)
				break

		uid = super().fbind(*args, **kwargs)
		self.last_binds.append([prop_name, element, key, uid])
		return uid

	def change_palette(self, _obj):
		self.palette = _obj

		if isinstance(_obj, dict):
			for key, value in _obj.items():
				if hasattr(_obj, key):
					setattr(self, key, value)

			return None

		for attribute in dir(_obj):
			value = getattr(_obj, attribute)

			if callable(value) or attribute.startswith("__"):
				continue

			if hasattr(self, attribute):
				setattr(self, attribute, value)
			else:
				self.add_new_color(attribute, value)

	@classmethod
	def add_bg_colors_to_palette(self, palette):
		for color_name in dir(palette):
			color_value = getattr(palette, color_name)

			if callable(color_value) or color_name.startswith("__"):
				continue

			new_name = color_name
			if color_name.endswith("_default"):
				new_name = color_name[0 : len(color_name)-8]

			for bg, name in zip((200, 400, 700, 800), ("hover", "border", "pressed", "effect")):
				color = self.adjust_color(color_value, bg)
				setattr(palette, f"{new_name}_{name}", color)

	@classmethod
	def proportional_value(self, input_value):
		# Defina os pontos de entrada e os valores proporcionais correspondentes
		input_points = [100, 450, 1000]
		proportional_values = [-100, 0, 100]
		
		# Tratamento especial para valores fora do intervalo
		if input_value <= input_points[0]:
			return proportional_values[0]
		elif input_value >= input_points[-1]:
			return proportional_values[-1]
		
		# Encontre os índices inferiores e superiores mais próximos
		index_lower = 0
		index_upper = len(input_points) - 1
		for i, value in enumerate(input_points):
			if input_value >= value:
				index_lower = i
			if input_value <= value:
				index_upper = i
				break
		
		# Certifique-se de que os índices não são iguais
		if index_lower == index_upper:
			if index_lower == 0:
				index_upper = 1
			else:
				index_lower = index_upper - 1
		
		# Calcule a proporção usando uma função linear
		proportion = (input_value - input_points[index_lower]) / (input_points[index_upper] - input_points[index_lower])
		
		# Interpole entre os valores proporcionais correspondentes
		return proportional_values[index_lower] + proportion * (proportional_values[index_upper] - proportional_values[index_lower])

	@classmethod
	def get_rgba(self, color):
		if isinstance(color, str):
			return get_color_from_hex(color)
		
		elif len(color) == 3:
			return list(color) + [1]
		
		return color
	
	@classmethod
	def adjust_color(self, color, factor):
		factor = round(self.proportional_value(factor))
		
		# Converte o código hexadecimal para valores de vermelho, verde e azul
		r, g, b = list(map(lambda n: n*255, self.get_rgba(color)[0:-1]))
		
		# Aplica o fator para ajustar as cores
		r = max(0, min(255, r + factor))
		g = max(0, min(255, g + factor))
		b = max(0, min(255, b + factor))

		return list(map(lambda n: n/255, [r, g, b])) + [1]

	@classmethod
	def is_color_light(self, color):
		# Extrair os valores de R, G e B da cor
		r, g, b = list(map(lambda n: n*255, self.get_rgba(color)[0:-1]))
		
		# Calcular a média das cores
		color_avg = (r + g + b) / 3
		
		# Definir um limiar intermediário (128) para determinar se a cor é clara o suficiente
		threshold = 128
		
		# Retornar True se a média das cores for maior ou igual ao limiar, False caso contrário
		return color_avg >= threshold

	@classmethod
	def get_color_text(self, color):
		if self.is_color_light(color):
			return [0, 0, 0, 1]
		return [1, 1, 1, 1]
