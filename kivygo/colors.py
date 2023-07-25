
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

	background_default = get_color_from_hex("F2F2F2")
	background_hover = get_color_from_hex("F7F7F7")
	background_border = get_color_from_hex("F0F0F0")
	background_pressed = get_color_from_hex("DEDEDE")
	background_effect = get_color_from_hex("FCFEFF")
	at_background_default = get_color_from_hex("151920")
	at_background_hover = get_color_from_hex("657899")
	at_background_border = get_color_from_hex("121E33")
	at_background_pressed = get_color_from_hex("14294D")
	at_background_effect = get_color_from_hex("AFBCCC")

	primary_default = get_color_from_hex("1D9BF0")
	primary_hover = get_color_from_hex("187FC4")
	primary_border = get_color_from_hex("115E91")
	primary_pressed = get_color_from_hex("243845")
	primary_effect = get_color_from_hex("73BAF0")
	at_primary_default = get_color_from_hex("F8F8F8")
	at_primary_hover = get_color_from_hex("F2F7F9")
	at_primary_border = get_color_from_hex("EFEFEF")
	at_primary_pressed = get_color_from_hex("D6DDE3")
	at_primary_effect = get_color_from_hex("E4F1F7")

	secondary_default = get_color_from_hex("1db954")
	secondary_hover = get_color_from_hex("44C268")
	secondary_border = get_color_from_hex("2ACC58")
	secondary_pressed = get_color_from_hex("2E8547")
	secondary_effect = get_color_from_hex("72F9A1")
	at_secondary_default = get_color_from_hex("F8F8F8")
	at_secondary_hover = get_color_from_hex("F2F7F9")
	at_secondary_border = get_color_from_hex("EFEFEF")
	at_secondary_pressed = get_color_from_hex("D6DDE3")
	at_secondary_effect = get_color_from_hex("E4F1F7")

	terciary_default = get_color_from_hex("820ad1")
	terciary_hover = get_color_from_hex("602C84")
	terciary_border = get_color_from_hex("672F8F")
	terciary_pressed = get_color_from_hex("5D1E8A")
	terciary_effect = get_color_from_hex("dcc1f1")
	at_terciary_default = get_color_from_hex("F8F8F8")
	at_terciary_hover = get_color_from_hex("F2F7F9")
	at_terciary_border = get_color_from_hex("EFEFEF")
	at_terciary_pressed = get_color_from_hex("D6DDE3")
	at_terciary_effect = get_color_from_hex("E4F1F7")

	title_default = get_color_from_hex("F0F4F7")
	title_hover = get_color_from_hex("E6EAED")
	title_border = get_color_from_hex("BCBFC2")
	title_pressed = get_color_from_hex("C8CBCF")
	title_effect = get_color_from_hex("F2F6FA")

	text_default = get_color_from_hex("cdd6e1")
	text_hover = get_color_from_hex("B8CAE0")
	text_border = get_color_from_hex("B0B8C2")
	text_pressed = get_color_from_hex("6B7F98")
	text_effect = get_color_from_hex("A2C2E8")

	success_default = get_color_from_hex("00CE61")
	success_hover = get_color_from_hex("00C15B")
	success_border = get_color_from_hex("00813D")
	success_pressed = get_color_from_hex("26965C")
	success_effect = get_color_from_hex("74D2A1")
	at_success_default = get_color_from_hex("00C853")
	at_success_hover = get_color_from_hex("00A64F")
	at_success_border = get_color_from_hex("00A64F")
	at_success_pressed = get_color_from_hex("26965C")
	at_success_effect = get_color_from_hex("74D2A1")

	error_default = get_color_from_hex("E32B2B")
	error_hover = get_color_from_hex("D92929")
	error_border = get_color_from_hex("B52A2A")
	error_pressed = get_color_from_hex("731A1A")
	error_effect = get_color_from_hex("E87171")
	at_error_default = get_color_from_hex("F8F8F8")
	at_error_hover = get_color_from_hex("F2F7F9")
	at_error_border = get_color_from_hex("EFEFEF")
	at_error_pressed = get_color_from_hex("D6DDE3")
	at_error_effect = get_color_from_hex("E4F1F7")

	warning_default = get_color_from_hex("FFBB0F")
	warning_hover = get_color_from_hex("FFD735")
	warning_border = get_color_from_hex("D98E04")
	warning_pressed = get_color_from_hex("FFA70F")
	warning_effect = get_color_from_hex("FFDB80")
	at_warning_default = get_color_from_hex("F8F8F8")
	at_warning_hover = get_color_from_hex("F2F7F9")
	at_warning_border = get_color_from_hex("EFEFEF")
	at_warning_pressed = get_color_from_hex("D6DDE3")
	at_warning_effect = get_color_from_hex("E4F1F7")

	support_default = get_color_from_hex("4BC3F2")
	support_hover = get_color_from_hex("50A7F2")
	support_border = get_color_from_hex("3B8CF5")
	support_pressed = get_color_from_hex("536EF5")
	support_effect = get_color_from_hex("C4E4FF")
	at_support_default = get_color_from_hex("F8F8F8")
	at_support_hover = get_color_from_hex("F2F7F9")
	at_support_border = get_color_from_hex("EFEFEF")
	at_support_pressed = get_color_from_hex("D6DDE3")
	at_support_effect = get_color_from_hex("E4F1F7")

	info_default = get_color_from_hex("007AFF")
	info_hover = get_color_from_hex("005CE6")
	info_border = get_color_from_hex("005CE6")
	info_pressed = get_color_from_hex("003999")
	info_effect = get_color_from_hex("007AFF")
	at_info_default = get_color_from_hex("007AFF")
	at_info_hover = get_color_from_hex("005CE6")
	at_info_border = get_color_from_hex("005CE6")
	at_info_pressed = get_color_from_hex("003999")
	at_info_effect = get_color_from_hex("007AFF")

	link_default = get_color_from_hex("26FBD4")
	link_hover = get_color_from_hex("04DEB6")
	link_border = get_color_from_hex("1F6158")
	link_pressed = get_color_from_hex("03AB8C")
	link_effect = get_color_from_hex("8DE3D8")
	

class Dark:
	no_color = [0, 0, 0, 0]
	dif_color = get_color_from_hex("d242bf")

	background_default = get_color_from_hex("151920")
	background_hover = get_color_from_hex("657899")
	background_border = get_color_from_hex("121E33")
	background_pressed = get_color_from_hex("14294D")
	background_effect = get_color_from_hex("AFBCCC")
	at_background_default = get_color_from_hex("F2F2F2")
	at_background_hover = get_color_from_hex("F7F7F7")
	at_background_border = get_color_from_hex("F0F0F0")
	at_background_pressed = get_color_from_hex("DEDEDE")
	at_background_effect = get_color_from_hex("FCFEFF")

	primary_default = get_color_from_hex("168fdc")
	primary_hover = get_color_from_hex("187fb0")
	primary_border = get_color_from_hex("11537d")
	primary_pressed = get_color_from_hex("1b2631")
	primary_effect = get_color_from_hex("6eb0dc")
	at_primary_default = get_color_from_hex("F8F8F8")
	at_primary_hover = get_color_from_hex("F2F7F9")
	at_primary_border = get_color_from_hex("EFEFEF")
	at_primary_pressed = get_color_from_hex("D6DDE3")
	at_primary_effect = get_color_from_hex("E4F1F7")

	secondary_default = get_color_from_hex("16a54d")
	secondary_hover = get_color_from_hex("3eae63")
	secondary_border = get_color_from_hex("26b84f")
	secondary_pressed = get_color_from_hex("23713d")
	secondary_effect = get_color_from_hex("67e596")
	at_secondary_default = get_color_from_hex("F8F8F8")
	at_secondary_hover = get_color_from_hex("F2F7F9")
	at_secondary_border = get_color_from_hex("EFEFEF")
	at_secondary_pressed = get_color_from_hex("D6DDE3")
	at_secondary_effect = get_color_from_hex("E4F1F7")

	terciary_default = get_color_from_hex("7609bd")
	terciary_hover = get_color_from_hex("542570")
	terciary_border = get_color_from_hex("55267b")
	terciary_pressed = get_color_from_hex("4f1a76")
	terciary_effect = get_color_from_hex("c8b3dd")
	at_terciary_default = get_color_from_hex("F8F8F8")
	at_terciary_hover = get_color_from_hex("F2F7F9")
	at_terciary_border = get_color_from_hex("EFEFEF")
	at_terciary_pressed = get_color_from_hex("D6DDE3")
	at_terciary_effect = get_color_from_hex("E4F1F7")

	title_default = get_color_from_hex("F0F4F7")
	title_hover = get_color_from_hex("E6EAED")
	title_border = get_color_from_hex("BCBFC2")
	title_pressed = get_color_from_hex("C8CBCF")
	title_effect = get_color_from_hex("F2F6FA")

	text_default = get_color_from_hex("e1ebf5")
	text_hover = get_color_from_hex("cbe0f4")
	text_border = get_color_from_hex("d6d6d6")
	text_pressed = get_color_from_hex("738fac")
	text_effect = get_color_from_hex("acceff")

	success_default = get_color_from_hex("00CE61")
	success_hover = get_color_from_hex("00C15B")
	success_border = get_color_from_hex("00813D")
	success_pressed = get_color_from_hex("26965C")
	success_effect = get_color_from_hex("74D2A1")
	at_success_default = get_color_from_hex("00C853")
	at_success_hover = get_color_from_hex("00A64F")
	at_success_border = get_color_from_hex("00A64F")
	at_success_pressed = get_color_from_hex("26965C")
	at_success_effect = get_color_from_hex("74D2A1")

	error_default = get_color_from_hex("E32B2B")
	error_hover = get_color_from_hex("D92929")
	error_border = get_color_from_hex("B52A2A")
	error_pressed = get_color_from_hex("731A1A")
	error_effect = get_color_from_hex("E87171")
	at_error_default = get_color_from_hex("F8F8F8")
	at_error_hover = get_color_from_hex("F2F7F9")
	at_error_border = get_color_from_hex("EFEFEF")
	at_error_pressed = get_color_from_hex("D6DDE3")
	at_error_effect = get_color_from_hex("E4F1F7")

	warning_default = get_color_from_hex("FFBB0F")
	warning_hover = get_color_from_hex("FFD735")
	warning_border = get_color_from_hex("D98E04")
	warning_pressed = get_color_from_hex("FFA70F")
	warning_effect = get_color_from_hex("FFDB80")
	at_warning_default = get_color_from_hex("F8F8F8")
	at_warning_hover = get_color_from_hex("F2F7F9")
	at_warning_border = get_color_from_hex("EFEFEF")
	at_warning_pressed = get_color_from_hex("D6DDE3")
	at_warning_effect = get_color_from_hex("E4F1F7")

	support_default = get_color_from_hex("4BC3F2")
	support_hover = get_color_from_hex("50A7F2")
	support_border = get_color_from_hex("3B8CF5")
	support_pressed = get_color_from_hex("536EF5")
	support_effect = get_color_from_hex("C4E4FF")
	at_support_default = get_color_from_hex("F8F8F8")
	at_support_hover = get_color_from_hex("F2F7F9")
	at_support_border = get_color_from_hex("EFEFEF")
	at_support_pressed = get_color_from_hex("D6DDE3")
	at_support_effect = get_color_from_hex("E4F1F7")

	info_default = get_color_from_hex("007AFF")
	info_hover = get_color_from_hex("005CE6")
	info_border = get_color_from_hex("005CE6")
	info_pressed = get_color_from_hex("003999")
	info_effect = get_color_from_hex("007AFF")
	at_info_default = get_color_from_hex("007AFF")
	at_info_hover = get_color_from_hex("005CE6")
	at_info_border = get_color_from_hex("005CE6")
	at_info_pressed = get_color_from_hex("003999")
	at_info_effect = get_color_from_hex("007AFF")

	link_default = get_color_from_hex("26FBD4")
	link_hover = get_color_from_hex("04DEB6")
	link_border = get_color_from_hex("1F6158")
	link_pressed = get_color_from_hex("03AB8C")
	link_effect = get_color_from_hex("8DE3D8")


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

			if hasattr(self, attribute):
				setattr(self, attribute, value)

