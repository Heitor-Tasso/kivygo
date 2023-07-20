
from kivy.utils import get_color_from_hex
from kivy.event import EventDispatcher
from kivy.properties import (
    ColorProperty, ObjectProperty, 
    ListProperty, NumericProperty
)

from kivy.lang import Builder
from kivy.metrics import dp
from kivygo.behaviors.hover import GoHoverBehavior
from kivygo.widgets.widget import GoWidget
from kivy.clock import Clock


Builder.load_string("""

<GoBackgroundColor>:
	background_color: GoColors.primary_default
	
	canvas.before: 
		Color:
			rgba: self._background_color
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: self.radius
			
<GoBorderColor>:
	border_color: GoColors.primary_border
	canvas.after:
		Color:
			rgba: self._border_color
		Line:
			rounded_rectangle: [*self.pos, *self.size, *self.radius]
			width: self.border_width

<GoHoverColor>:
	background_hover: GoColors.primary_hover

<GoColorBase>:
	background_color: GoColors.primary_default
	

""")

class GoBackgroundColor(GoWidget):
	radius = ListProperty([0]*4)

	background_color = ListProperty([0]*4)
	background_disabled = ListProperty([0]*4)
	_background_color = ListProperty([0]*4)

	def __init__(self, **kwargs):

		super().__init__(**kwargs)
		Clock.schedule_once(self.set_color)
		self.bind(background_color=self.set_color)

	def set_color(self, *args):
		self._background_color = self.background_color
		if hasattr(super(), "set_color"):
			return super().set_color(*args)

	def on_disabled(self, *args):
		self._background_color = self.background_disabled
		if hasattr(super(), "on_disabled"):
			return super().on_disabled(*args)
	

class GoBorderColor(GoWidget):
	_border_color = ListProperty([0]*4)
	border_color = ListProperty([0]*4)
	border_hover = ListProperty([0]*4)
	border_disabled = ListProperty([0]*4)
	border_width = NumericProperty(dp(1.01))
	
	radius = ListProperty([0]*4)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.bind(border_color=self.set_color)

	def set_color(self, *args):
		self._border_color = self.border_color
		if hasattr(super(), "set_color"):
			return super().set_color(*args)

	def on_disabled(self, *args):
		self._border_color = self.border_disabled
		if hasattr(super(), "on_disabled"):
			return super().on_disabled(*args)

class GoHoverColor(GoHoverBehavior, GoBackgroundColor):
	background_hover = ListProperty([0]*4)

	def on_cursor_enter(self, *args):
		self._background_color = self.background_hover

		return super().on_cursor_enter(*args)

	def on_cursor_leave(self, *args):
		self._background_color = self.background_color
		return super().on_cursor_leave(*args)


class GoColorBase(GoHoverColor, GoBorderColor, GoBackgroundColor):	
	pass



class Light:
	no_color = [0, 0, 0, 0]
	dif_color = get_color_from_hex("d242bf")

	background_default = get_color_from_hex("F4F4F4")
	background_hover = get_color_from_hex("D8D8D8")
	background_border = get_color_from_hex("C2C2C2")
	background_pressed = get_color_from_hex("C2C2C2")
	background_effect = get_color_from_hex("F4F4F4")
	on_background_default = get_color_from_hex("F4F4F4")
	on_background_hover = get_color_from_hex("F4F4F4")
	on_background_border = get_color_from_hex("F4F4F4")
	on_background_pressed = get_color_from_hex("F4F4F4")
	on_background_effect = get_color_from_hex("F4F4F4")

	background_variant_default = get_color_from_hex("1c7947")
	background_variant_hover = get_color_from_hex("1c7947")
	background_variant_border = get_color_from_hex("1c7947")
	background_variant_pressed = get_color_from_hex("1c7947")
	background_variant_effect = get_color_from_hex("1c7947")
	on_background_variant = get_color_from_hex("FFFFFF")
	on_background_variant_hover = get_color_from_hex("ECECEC")
	on_background_variant_border = get_color_from_hex("1c7947")
	on_background_variant_pressed = get_color_from_hex("1c7947")
	on_background_variant_effect = get_color_from_hex("1c7947")

	primary_default = get_color_from_hex("0099CC")
	primary_hover = get_color_from_hex("0077B3")
	primary_border = get_color_from_hex("0077B3")
	primary_pressed = get_color_from_hex("005580")
	primary_effect = get_color_from_hex("0099CC")
	on_primary_default = get_color_from_hex("0099CC")
	on_primary_hover = get_color_from_hex("0077B3")
	on_primary_border = get_color_from_hex("0077B3")
	on_primary_pressed = get_color_from_hex("005580")
	on_primary_effect = get_color_from_hex("0099CC")

	secondary_default = get_color_from_hex("FF8800")
	secondary_hover = get_color_from_hex("E66A00")
	secondary_border = get_color_from_hex("E66A00")
	secondary_pressed = get_color_from_hex("994C00")
	secondary_effect = get_color_from_hex("FF8800")
	on_secondary_default = get_color_from_hex("FF8800")
	on_secondary_hover = get_color_from_hex("E66A00")
	on_secondary_border = get_color_from_hex("E66A00")
	on_secondary_pressed = get_color_from_hex("994C00")
	on_secondary_effect = get_color_from_hex("FF8800")

	terciary_default = get_color_from_hex("8ec63f")
	terciary_hover = get_color_from_hex("4CAF50")
	terciary_border = get_color_from_hex("4CAF50")
	terciary_pressed = get_color_from_hex("388E3C")
	terciary_effect = get_color_from_hex("66BB6A")
	on_terciary_default = get_color_from_hex("F4F4F4")
	on_terciary_hover = get_color_from_hex("D8D8D8")
	on_terciary_border = get_color_from_hex("C2C2C2")
	on_terciary_pressed = get_color_from_hex("F4F4F4")
	on_terciary_effect = get_color_from_hex("F4F4F4")

	title_default = get_color_from_hex("333333")
	title_hover = get_color_from_hex("4A4A4A")
	title_border = get_color_from_hex("4A4A4A")
	title_pressed = get_color_from_hex("333333")
	title_effect = get_color_from_hex("333333")
	on_title_default = get_color_from_hex("333333")
	on_title_hover = get_color_from_hex("4A4A4A")
	on_title_border = get_color_from_hex("4A4A4A")
	on_title_pressed = get_color_from_hex("333333")
	on_title_effect = get_color_from_hex("333333")

	text_default = get_color_from_hex("555555")
	text_hover = get_color_from_hex("777777")
	text_border = get_color_from_hex("777777")
	text_pressed = get_color_from_hex("555555")
	text_effect = get_color_from_hex("555555")
	on_text_default = get_color_from_hex("555555")
	on_text_hover = get_color_from_hex("777777")
	on_text_border = get_color_from_hex("777777")
	on_text_pressed = get_color_from_hex("555555")
	on_text_effect = get_color_from_hex("555555")

	success_default = get_color_from_hex("00C853")
	success_hover = get_color_from_hex("00A64F")
	success_border = get_color_from_hex("00A64F")
	success_pressed = get_color_from_hex("007B33")
	success_effect = get_color_from_hex("00C853")
	on_success_default = get_color_from_hex("00C853")
	on_success_hover = get_color_from_hex("00A64F")
	on_success_border = get_color_from_hex("00A64F")
	on_success_pressed = get_color_from_hex("007B33")
	on_success_effect = get_color_from_hex("00C853")

	error_default = get_color_from_hex("FF3D00")
	error_hover = get_color_from_hex("D84315")
	error_border = get_color_from_hex("D84315")
	error_pressed = get_color_from_hex("A62807")
	error_effect = get_color_from_hex("FF3D00")
	on_error_default = get_color_from_hex("FF3D00")
	on_error_hover = get_color_from_hex("D84315")
	on_error_border = get_color_from_hex("D84315")
	on_error_pressed = get_color_from_hex("A62807")
	on_error_effect = get_color_from_hex("FF3D00")

	warning_default = get_color_from_hex("FFB300")
	warning_hover = get_color_from_hex("FF8F00")
	warning_border = get_color_from_hex("FF8F00")
	warning_pressed = get_color_from_hex("FF6F00")
	warning_effect = get_color_from_hex("FFB300")
	on_warning_default = get_color_from_hex("FFB300")
	on_warning_hover = get_color_from_hex("FF8F00")
	on_warning_border = get_color_from_hex("FF8F00")
	on_warning_pressed = get_color_from_hex("FF6F00")
	on_warning_effect = get_color_from_hex("FFB300")

	support_default = get_color_from_hex("757575")
	support_hover = get_color_from_hex("999999")
	support_border = get_color_from_hex("999999")
	support_pressed = get_color_from_hex("666666")
	support_effect = get_color_from_hex("757575")
	on_support_default = get_color_from_hex("757575")
	on_support_hover = get_color_from_hex("999999")
	on_support_border = get_color_from_hex("999999")
	on_support_pressed = get_color_from_hex("666666")
	on_support_effect = get_color_from_hex("757575")

	info_default = get_color_from_hex("007AFF")
	info_hover = get_color_from_hex("005CE6")
	info_border = get_color_from_hex("005CE6")
	info_pressed = get_color_from_hex("003999")
	info_effect = get_color_from_hex("007AFF")
	on_info_default = get_color_from_hex("007AFF")
	on_info_hover = get_color_from_hex("005CE6")
	on_info_border = get_color_from_hex("005CE6")
	on_info_pressed = get_color_from_hex("003999")
	on_info_effect = get_color_from_hex("007AFF")

	danger_default = get_color_from_hex("D50000")
	danger_hover = get_color_from_hex("B71C1C")
	danger_border = get_color_from_hex("B71C1C")
	danger_pressed = get_color_from_hex("7F0000")
	danger_effect = get_color_from_hex("D50000")
	on_danger_default = get_color_from_hex("D50000")
	on_danger_hover = get_color_from_hex("B71C1C")
	on_danger_border = get_color_from_hex("B71C1C")
	on_danger_pressed = get_color_from_hex("7F0000")
	on_danger_effect = get_color_from_hex("D50000")

	link_default = get_color_from_hex("007AFF")
	link_hover = get_color_from_hex("005CE6")
	link_border = get_color_from_hex("005CE6")
	link_pressed = get_color_from_hex("003999")
	link_effect = get_color_from_hex("007AFF")
	on_link_default = get_color_from_hex("007AFF")
	on_link_hover = get_color_from_hex("005CE6")
	on_link_border = get_color_from_hex("005CE6")
	on_link_pressed = get_color_from_hex("003999")
	on_link_effect = get_color_from_hex("007AFF")

class Dark:
	no_color = [0, 0, 0, 0]
	dif_color = get_color_from_hex("d242bf")

	background_default = get_color_from_hex("333333")
	background_hover = get_color_from_hex("4A4A4A")
	background_border = get_color_from_hex("4A4A4A")
	background_pressed = get_color_from_hex("333333")
	background_effect = get_color_from_hex("333333")
	on_background_default = get_color_from_hex("333333")
	on_background_hover = get_color_from_hex("4A4A4A")
	on_background_border = get_color_from_hex("4A4A4A")
	on_background_pressed = get_color_from_hex("333333")
	on_background_effect = get_color_from_hex("333333")

	background_variant_default = get_color_from_hex("1c7947")
	background_variant_hover = get_color_from_hex("1c7947")
	background_variant_border = get_color_from_hex("1c7947")
	background_variant_pressed = get_color_from_hex("1c7947")
	background_variant_effect = get_color_from_hex("1c7947")
	on_background_variant = get_color_from_hex("FFFFFF")
	on_background_variant_hover = get_color_from_hex("ECECEC")
	on_background_variant_border = get_color_from_hex("1c7947")
	on_background_variant_pressed = get_color_from_hex("1c7947")
	on_background_variant_effect = get_color_from_hex("1c7947")

	primary_default = get_color_from_hex("0099CC")
	primary_hover = get_color_from_hex("0077B3")
	primary_border = get_color_from_hex("0077B3")
	primary_pressed = get_color_from_hex("005580")
	primary_effect = get_color_from_hex("0099CC")
	on_primary_default = get_color_from_hex("0099CC")
	on_primary_hover = get_color_from_hex("0077B3")
	on_primary_border = get_color_from_hex("0077B3")
	on_primary_pressed = get_color_from_hex("005580")
	on_primary_effect = get_color_from_hex("0099CC")

	secondary_default = get_color_from_hex("FF8800")
	secondary_hover = get_color_from_hex("E66A00")
	secondary_border = get_color_from_hex("E66A00")
	secondary_pressed = get_color_from_hex("994C00")
	secondary_effect = get_color_from_hex("FF8800")
	on_secondary_default = get_color_from_hex("FF8800")
	on_secondary_hover = get_color_from_hex("E66A00")
	on_secondary_border = get_color_from_hex("E66A00")
	on_secondary_pressed = get_color_from_hex("994C00")
	on_secondary_effect = get_color_from_hex("FF8800")

	terciary_default = get_color_from_hex("8ec63f")
	terciary_hover = get_color_from_hex("4CAF50")
	terciary_border = get_color_from_hex("4CAF50")
	terciary_pressed = get_color_from_hex("388E3C")
	terciary_effect = get_color_from_hex("66BB6A")
	on_terciary_default = get_color_from_hex("8ec63f")
	on_terciary_hover = get_color_from_hex("4CAF50")
	on_terciary_border = get_color_from_hex("4CAF50")
	on_terciary_pressed = get_color_from_hex("388E3C")
	on_terciary_effect = get_color_from_hex("66BB6A")

	title_default = get_color_from_hex("FFFFFF")
	title_hover = get_color_from_hex("CCCCCC")
	title_border = get_color_from_hex("CCCCCC")
	title_pressed = get_color_from_hex("FFFFFF")
	title_effect = get_color_from_hex("FFFFFF")
	on_title_default = get_color_from_hex("FFFFFF")
	on_title_hover = get_color_from_hex("CCCCCC")
	on_title_border = get_color_from_hex("CCCCCC")
	on_title_pressed = get_color_from_hex("FFFFFF")
	on_title_effect = get_color_from_hex("FFFFFF")

	text_default = get_color_from_hex("DDDDDD")
	text_hover = get_color_from_hex("C2C2C2")
	text_border = get_color_from_hex("C2C2C2")
	text_pressed = get_color_from_hex("DDDDDD")
	text_effect = get_color_from_hex("DDDDDD")
	on_text_default = get_color_from_hex("DDDDDD")
	on_text_hover = get_color_from_hex("C2C2C2")
	on_text_border = get_color_from_hex("C2C2C2")
	on_text_pressed = get_color_from_hex("DDDDDD")
	on_text_effect = get_color_from_hex("DDDDDD")

	success_default = get_color_from_hex("00C853")
	success_hover = get_color_from_hex("00A64F")
	success_border = get_color_from_hex("00A64F")
	success_pressed = get_color_from_hex("007B33")
	success_effect = get_color_from_hex("00C853")
	on_success_default = get_color_from_hex("00C853")
	on_success_hover = get_color_from_hex("00A64F")
	on_success_border = get_color_from_hex("00A64F")
	on_success_pressed = get_color_from_hex("007B33")
	on_success_effect = get_color_from_hex("00C853")

	error_default = get_color_from_hex("FF3D00")
	error_hover = get_color_from_hex("D84315")
	error_border = get_color_from_hex("D84315")
	error_pressed = get_color_from_hex("A62807")
	error_effect = get_color_from_hex("FF3D00")
	on_error_default = get_color_from_hex("FF3D00")
	on_error_hover = get_color_from_hex("D84315")
	on_error_border = get_color_from_hex("D84315")
	on_error_pressed = get_color_from_hex("A62807")
	on_error_effect = get_color_from_hex("FF3D00")

	warning_default = get_color_from_hex("FFB300")
	warning_hover = get_color_from_hex("FF8F00")
	warning_border = get_color_from_hex("FF8F00")
	warning_pressed = get_color_from_hex("FF6F00")
	warning_effect = get_color_from_hex("FFB300")
	on_warning_default = get_color_from_hex("FFB300")
	on_warning_hover = get_color_from_hex("FF8F00")
	on_warning_border = get_color_from_hex("FF8F00")
	on_warning_pressed = get_color_from_hex("FF6F00")
	on_warning_effect = get_color_from_hex("FFB300")

	support_default = get_color_from_hex("757575")
	support_hover = get_color_from_hex("999999")
	support_border = get_color_from_hex("999999")
	support_pressed = get_color_from_hex("666666")
	support_effect = get_color_from_hex("757575")
	on_support_default = get_color_from_hex("757575")
	on_support_hover = get_color_from_hex("999999")
	on_support_border = get_color_from_hex("999999")
	on_support_pressed = get_color_from_hex("666666")
	on_support_effect = get_color_from_hex("757575")

	info_default = get_color_from_hex("007AFF")
	info_hover = get_color_from_hex("005CE6")
	info_border = get_color_from_hex("005CE6")
	info_pressed = get_color_from_hex("003999")
	info_effect = get_color_from_hex("007AFF")
	on_info_default = get_color_from_hex("007AFF")
	on_info_hover = get_color_from_hex("005CE6")
	on_info_border = get_color_from_hex("005CE6")
	on_info_pressed = get_color_from_hex("003999")
	on_info_effect = get_color_from_hex("007AFF")

	danger_default = get_color_from_hex("D50000")
	danger_hover = get_color_from_hex("B71C1C")
	danger_border = get_color_from_hex("B71C1C")
	danger_pressed = get_color_from_hex("7F0000")
	danger_effect = get_color_from_hex("D50000")
	on_danger_default = get_color_from_hex("D50000")
	on_danger_hover = get_color_from_hex("B71C1C")
	on_danger_border = get_color_from_hex("B71C1C")
	on_danger_pressed = get_color_from_hex("7F0000")
	on_danger_effect = get_color_from_hex("D50000")
	
	link_default = get_color_from_hex("007AFF")
	link_hover = get_color_from_hex("005CE6")
	link_border = get_color_from_hex("005CE6")
	link_pressed = get_color_from_hex("003999")
	link_effect = get_color_from_hex("007AFF")
	on_link_default = get_color_from_hex("007AFF")
	on_link_hover = get_color_from_hex("005CE6")
	on_link_border = get_color_from_hex("005CE6")
	on_link_pressed = get_color_from_hex("003999")
	on_link_effect = get_color_from_hex("007AFF")


class Colors(EventDispatcher):

	palette = ObjectProperty(Light)

	last_binds = []

	def __init__(self, *args, **kwargs):
		for color_name in dir(self.palette):
			color_value = getattr(self.palette, color_name)

			if callable(color_value) or color_name.startswith("__"):
				continue

			self.add_new_color(color_name, color_value)

		super().__init__(*args, **kwargs)

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

			if hasattr(_obj, attribute):
				setattr(self, attribute, value)

