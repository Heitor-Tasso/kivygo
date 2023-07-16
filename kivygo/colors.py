
from kivygo.widgets.widget import GoWidget
from kivy.properties import ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivygo.behaviors.hover import HoverBehavior
from kivy.event import EventDispatcher
from kivy.properties import ColorProperty, ObjectProperty

PALETTE_KEY_COLORS = [
	"no_color", "dif_color",

	"background_default", "background_disabled", "background_hover",
	"background_border", "background_border_hover", "background_border_pressed",
	"background_border_disabled", "background_pressed", "background_effect",

	"background_variant_default",
	"on_background_variant",
	"on_background_variant_hover",
	
	"primary_default", "primary_disabled", "primary_hover", "primary_border",
	"primary_border_hover", "primary_border_pressed", "primary_border_disabled",
	"primary_pressed", "primary_effect",

	"on_primary",
	
	"secondary_default", "secondary_disabled", "secondary_hover", "secondary_border",
	"secondary_border_hover", "secondary_border_pressed", "secondary_border_disabled",
	"secondary_pressed", "secondary_effect",
	
	"terciary_default", "terciary_disabled", "terciary_hover", "terciary_border",
	"terciary_border_hover", "terciary_border_pressed", "terciary_border_disabled",
	"terciary_pressed", "terciary_effect", "on_terciary",
	
	"title_default", "title_disabled", "title_hover", "title_border",
	"title_border_hover", "title_border_pressed", "title_border_disabled",
	"title_pressed", "title_effect",
	
	"text_default", "text_disabled", "text_hover", "text_border",
	"text_border_hover", "text_border_pressed", "text_border_disabled",
	"text_pressed", "text_effect",
	
	"success_default", "success_disabled", "success_hover", "success_border",
	"success_border_hover", "success_border_pressed", "success_border_disabled",
	"success_pressed", "success_effect",
	
	"error_default", "error_disabled", "error_hover", "error_border",
	"error_border_hover", "error_border_pressed", "error_border_disabled",
	"error_pressed", "error_effect",
	
	"warning_default", "warning_disabled", "warning_hover", "warning_border",
	"warning_border_hover", "warning_border_pressed", "warning_border_disabled",
	"warning_pressed", "warning_effect",
	
	"support_default", "support_disabled", "support_hover", "support_border",
	"support_border_hover", "support_border_pressed", "support_border_disabled",
	"support_pressed", "support_effect",
	
	"info_default", "info_disabled", "info_hover", "info_border",
	"info_border_hover", "info_border_pressed", "info_border_disabled",
	"info_pressed", "info_effect",
	
	"danger_default", "danger_disabled", "danger_hover", "danger_border",
	"danger_border_hover", "danger_border_pressed", "danger_border_disabled",
	"danger_pressed", "danger_effect",
	
	"link_default", "link_disabled", "link_hover", "link_border",
	"link_border_hover", "link_border_pressed", "link_border_disabled",
	"link_pressed", "link_effect"
]

Builder.load_string("""

<GoBackgroundColor>:
	background_color: GoColors.primary_default
	background_disabled: GoColors.primary_disabled
	
	canvas.before: 
		Color:
			rgba: self._background_color
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: self.radius
		    
<GoBorderColor>:
	border_color: GoColors.primary_border
	border_hover: GoColors.primary_border_pressed
	border_disabled: GoColors.primary_border_disabled
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
	background_disabled: GoColors.primary_disabled
	

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

class GoHoverColor(HoverBehavior, GoBackgroundColor):
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
	background_disabled = get_color_from_hex("E0E0E0")
	background_hover = get_color_from_hex("D8D8D8")
	background_border = get_color_from_hex("C2C2C2")
	background_border_hover = get_color_from_hex("A9A9A9")
	background_border_pressed = get_color_from_hex("909090")
	background_border_disabled = get_color_from_hex("E0E0E0")
	background_pressed = get_color_from_hex("C2C2C2")
	background_effect = get_color_from_hex("F4F4F4")

	background_variant_default = get_color_from_hex("1c7947")
	on_background_variant = get_color_from_hex("FFFFFF")
	on_background_variant_hover = get_color_from_hex("ECECEC")

	primary_default = get_color_from_hex("0099CC")
	primary_disabled = get_color_from_hex("99CCFF")
	primary_hover = get_color_from_hex("0077B3")
	primary_border = get_color_from_hex("0077B3")
	primary_border_hover = get_color_from_hex("005580")
	primary_border_pressed = get_color_from_hex("00394D")
	primary_border_disabled = get_color_from_hex("99CCFF")
	primary_pressed = get_color_from_hex("005580")
	primary_effect = get_color_from_hex("0099CC")

	on_primary = get_color_from_hex("ECECEC")
	
	secondary_default = get_color_from_hex("FF8800")
	secondary_disabled = get_color_from_hex("FFCC80")
	secondary_hover = get_color_from_hex("E66A00")
	secondary_border = get_color_from_hex("E66A00")
	secondary_border_hover = get_color_from_hex("994C00")
	secondary_border_pressed = get_color_from_hex("663300")
	secondary_border_disabled = get_color_from_hex("FFCC80")
	secondary_pressed = get_color_from_hex("994C00")
	secondary_effect = get_color_from_hex("FF8800")

	terciary_default = get_color_from_hex("8ec63f")
	terciary_disabled = get_color_from_hex("B2DFDB")
	terciary_hover = get_color_from_hex("4CAF50")
	terciary_border = get_color_from_hex("4CAF50")
	terciary_border_hover = get_color_from_hex("388E3C")
	terciary_border_pressed = get_color_from_hex("1B5E20")
	terciary_border_disabled = get_color_from_hex("B2DFDB")
	terciary_pressed = get_color_from_hex("388E3C")
	terciary_effect = get_color_from_hex("66BB6A")
	on_terciary = get_color_from_hex("FFFFFF")

	title_default = get_color_from_hex("333333")
	title_disabled = get_color_from_hex("808080")
	title_hover = get_color_from_hex("4A4A4A")
	title_border = get_color_from_hex("4A4A4A")
	title_border_hover = get_color_from_hex("333333")
	title_border_pressed = get_color_from_hex("1A1A1A")
	title_border_disabled = get_color_from_hex("808080")
	title_pressed = get_color_from_hex("333333")
	title_effect = get_color_from_hex("333333")

	text_default = get_color_from_hex("555555")
	text_disabled = get_color_from_hex("AAAAAA")
	text_hover = get_color_from_hex("777777")
	text_border = get_color_from_hex("777777")
	text_border_hover = get_color_from_hex("555555")
	text_border_pressed = get_color_from_hex("222222")
	text_border_disabled = get_color_from_hex("AAAAAA")
	text_pressed = get_color_from_hex("555555")
	text_effect = get_color_from_hex("555555")

	success_default = get_color_from_hex("00C853")
	success_disabled = get_color_from_hex("B2FF59")
	success_hover = get_color_from_hex("00A64F")
	success_border = get_color_from_hex("00A64F")
	success_border_hover = get_color_from_hex("007B33")
	success_border_pressed = get_color_from_hex("004D1A")
	success_border_disabled = get_color_from_hex("B2FF59")
	success_pressed = get_color_from_hex("007B33")
	success_effect = get_color_from_hex("00C853")

	error_default = get_color_from_hex("FF3D00")
	error_disabled = get_color_from_hex("FFAB91")
	error_hover = get_color_from_hex("D84315")
	error_border = get_color_from_hex("D84315")
	error_border_hover = get_color_from_hex("A62807")
	error_border_pressed = get_color_from_hex("5A150A")
	error_border_disabled = get_color_from_hex("FFAB91")
	error_pressed = get_color_from_hex("A62807")
	error_effect = get_color_from_hex("FF3D00")

	warning_default = get_color_from_hex("FFB300")
	warning_disabled = get_color_from_hex("FFE082")
	warning_hover = get_color_from_hex("FF8F00")
	warning_border = get_color_from_hex("FF8F00")
	warning_border_hover = get_color_from_hex("FF6F00")
	warning_border_pressed = get_color_from_hex("FF4500")
	warning_border_disabled = get_color_from_hex("FFE082")
	warning_pressed = get_color_from_hex("FF6F00")
	warning_effect = get_color_from_hex("FFB300")

	support_default = get_color_from_hex("757575")
	support_disabled = get_color_from_hex("C7C7C7")
	support_hover = get_color_from_hex("999999")
	support_border = get_color_from_hex("999999")
	support_border_hover = get_color_from_hex("666666")
	support_border_pressed = get_color_from_hex("333333")
	support_border_disabled = get_color_from_hex("C7C7C7")
	support_pressed = get_color_from_hex("666666")
	support_effect = get_color_from_hex("757575")

	info_default = get_color_from_hex("007AFF")
	info_disabled = get_color_from_hex("99CCFF")
	info_hover = get_color_from_hex("005CE6")
	info_border = get_color_from_hex("005CE6")
	info_border_hover = get_color_from_hex("003999")
	info_border_pressed = get_color_from_hex("001F66")
	info_border_disabled = get_color_from_hex("99CCFF")
	info_pressed = get_color_from_hex("003999")
	info_effect = get_color_from_hex("007AFF")

	danger_default = get_color_from_hex("D50000")
	danger_disabled = get_color_from_hex("FF8A80")
	danger_hover = get_color_from_hex("B71C1C")
	danger_border = get_color_from_hex("B71C1C")
	danger_border_hover = get_color_from_hex("7F0000")
	danger_border_pressed = get_color_from_hex("4B0B0B")
	danger_border_disabled = get_color_from_hex("FF8A80")
	danger_pressed = get_color_from_hex("7F0000")
	danger_effect = get_color_from_hex("D50000")

	link_default = get_color_from_hex("007AFF")
	link_disabled = get_color_from_hex("99CCFF")
	link_hover = get_color_from_hex("005CE6")
	link_border = get_color_from_hex("005CE6")
	link_border_hover = get_color_from_hex("003999")
	link_border_pressed = get_color_from_hex("001F66")
	link_border_disabled = get_color_from_hex("99CCFF")
	link_pressed = get_color_from_hex("003999")
	link_effect = get_color_from_hex("007AFF")


class Dark:
	no_color = [0, 0, 0, 0]
	dif_color = get_color_from_hex("d242bf")

	background_default = get_color_from_hex("1F1F1F")
	background_disabled = get_color_from_hex("333333")
	background_hover = get_color_from_hex("2F2F2F")
	background_border = get_color_from_hex("4C4C4C")
	background_border_hover = get_color_from_hex("636363")
	background_border_pressed = get_color_from_hex("7C7C7C")
	background_border_disabled = get_color_from_hex("333333")
	background_pressed = get_color_from_hex("4C4C4C")
	background_effect = get_color_from_hex("1F1F1F")

	background_variant_default = get_color_from_hex("1c7947")
	on_background_variant = get_color_from_hex("FFFFFF")
	on_background_variant_hover = get_color_from_hex("ECECEC")

	primary_default = get_color_from_hex("00A6EB")
	primary_disabled = get_color_from_hex("63B8FF")
	primary_hover = get_color_from_hex("0093D6")
	primary_border = get_color_from_hex("0093D6")
	primary_border_hover = get_color_from_hex("0070A3")
	primary_border_pressed = get_color_from_hex("004C70")
	primary_border_disabled = get_color_from_hex("63B8FF")
	primary_pressed = get_color_from_hex("0070A3")
	primary_effect = get_color_from_hex("00A6EB")

	on_primary = get_color_from_hex("ECECEC")

	secondary_default = get_color_from_hex("FF8A00")
	secondary_disabled = get_color_from_hex("FFBD6A")
	secondary_hover = get_color_from_hex("E67300")
	secondary_border = get_color_from_hex("E67300")
	secondary_border_hover = get_color_from_hex("995200")
	secondary_border_pressed = get_color_from_hex("663300")
	secondary_border_disabled = get_color_from_hex("FFBD6A")
	secondary_pressed = get_color_from_hex("995200")
	secondary_effect = get_color_from_hex("FF8A00")

	terciary_default = get_color_from_hex("4CAF50")
	terciary_disabled = get_color_from_hex("80E27E")
	terciary_hover = get_color_from_hex("43A047")
	terciary_border = get_color_from_hex("43A047")
	terciary_border_hover = get_color_from_hex("2E7D32")
	terciary_border_pressed = get_color_from_hex("1B5E20")
	terciary_border_disabled = get_color_from_hex("80E27E")
	terciary_pressed = get_color_from_hex("2E7D32")
	terciary_effect = get_color_from_hex("4CAF50")
	on_terciary = get_color_from_hex("FFFFFF")

	title_default = get_color_from_hex("FFFFFF")
	title_disabled = get_color_from_hex("B2B2B2")
	title_hover = get_color_from_hex("CCCCCC")
	title_border = get_color_from_hex("CCCCCC")
	title_border_hover = get_color_from_hex("FFFFFF")
	title_border_pressed = get_color_from_hex("E6E6E6")
	title_border_disabled = get_color_from_hex("B2B2B2")
	title_pressed = get_color_from_hex("CCCCCC")
	title_effect = get_color_from_hex("FFFFFF")

	text_default = get_color_from_hex("DDDDDD")
	text_disabled = get_color_from_hex("AAAAAA")
	text_hover = get_color_from_hex("C2C2C2")
	text_border = get_color_from_hex("C2C2C2")
	text_border_hover = get_color_from_hex("DDDDDD")
	text_border_pressed = get_color_from_hex("F5F5F5")
	text_border_disabled = get_color_from_hex("AAAAAA")
	text_pressed = get_color_from_hex("C2C2C2")
	text_effect = get_color_from_hex("DDDDDD")

	success_default = get_color_from_hex("00E676")
	success_disabled = get_color_from_hex("80FFAB")
	success_hover = get_color_from_hex("00C853")
	success_border = get_color_from_hex("00C853")
	success_border_hover = get_color_from_hex("009624")
	success_border_pressed = get_color_from_hex("004D1A")
	success_border_disabled = get_color_from_hex("80FFAB")
	success_pressed = get_color_from_hex("009624")
	success_effect = get_color_from_hex("00E676")

	error_default = get_color_from_hex("FF5252")
	error_disabled = get_color_from_hex("FF8F8F")
	error_hover = get_color_from_hex("D50000")
	error_border = get_color_from_hex("D50000")
	error_border_hover = get_color_from_hex("A00000")
	error_border_pressed = get_color_from_hex("5B0000")
	error_border_disabled = get_color_from_hex("FF8F8F")
	error_pressed = get_color_from_hex("A00000")
	error_effect = get_color_from_hex("FF5252")

	warning_default = get_color_from_hex("FFB300")
	warning_disabled = get_color_from_hex("FFE082")
	warning_hover = get_color_from_hex("E65100")
	warning_border = get_color_from_hex("E65100")
	warning_border_hover = get_color_from_hex("994D00")
	warning_border_pressed = get_color_from_hex("663300")
	warning_border_disabled = get_color_from_hex("FFE082")
	warning_pressed = get_color_from_hex("994D00")
	warning_effect = get_color_from_hex("FFB300")

	support_default = get_color_from_hex("9E9E9E")
	support_disabled = get_color_from_hex("C7C7C7")
	support_hover = get_color_from_hex("BDBDBD")
	support_border = get_color_from_hex("BDBDBD")
	support_border_hover = get_color_from_hex("9E9E9E")
	support_border_pressed = get_color_from_hex("7E7E7E")
	support_border_disabled = get_color_from_hex("C7C7C7")
	support_pressed = get_color_from_hex("9E9E9E")
	support_effect = get_color_from_hex("9E9E9E")

	info_default = get_color_from_hex("64B5F6")
	info_disabled = get_color_from_hex("A6D4FA")
	info_hover = get_color_from_hex("42A5F5")
	info_border = get_color_from_hex("42A5F5")
	info_border_hover = get_color_from_hex("1E88E5")
	info_border_pressed = get_color_from_hex("1565C0")
	info_border_disabled = get_color_from_hex("A6D4FA")
	info_pressed = get_color_from_hex("1E88E5")
	info_effect = get_color_from_hex("64B5F6")

	danger_default = get_color_from_hex("FF1744")
	danger_disabled = get_color_from_hex("FF8A80")
	danger_hover = get_color_from_hex("D50000")
	danger_border = get_color_from_hex("D50000")
	danger_border_hover = get_color_from_hex("9B0000")
	danger_border_pressed = get_color_from_hex("610000")
	danger_border_disabled = get_color_from_hex("FF8A80")
	danger_pressed = get_color_from_hex("9B0000")
	danger_effect = get_color_from_hex("FF1744")

	link_default = get_color_from_hex("64B5F6")
	link_disabled = get_color_from_hex("A6D4FA")
	link_hover = get_color_from_hex("42A5F5")
	link_border = get_color_from_hex("42A5F5")
	link_border_hover = get_color_from_hex("1E88E5")
	link_border_pressed = get_color_from_hex("1565C0")
	link_border_disabled = get_color_from_hex("A6D4FA")
	link_pressed = get_color_from_hex("1E88E5")
	link_effect = get_color_from_hex("64B5F6")


class Colors(EventDispatcher):

	palette = ObjectProperty(Light)

	last_binds = []

	def __init__(self, *args, **kwargs):
		# Set all colors properties to the App accordian to the `colors.PALETTE_KEY_COLORS`

		for key in PALETTE_KEY_COLORS:
			color = getattr(self.palette, key)
			self.apply_property(
				**{ key : ColorProperty(color) }
			)

		super().__init__(*args, **kwargs)

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
		if isinstance(_obj, dict):
			return None

		self.palette = _obj
		
		for key in PALETTE_KEY_COLORS:
			if hasattr(self.palette, key):
				setattr(self, key, getattr(self.palette, key))

