
from kivy.properties import (
	BooleanProperty, ColorProperty,
	ListProperty, NumericProperty,
	StringProperty,
)

from kivygo.behaviors.neumorph import NeuMorphCircular, NeuMorphRectangle
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivygo.behaviors.touch_effecs import EffectBehavior
from kivygo.behaviors.button import ButtonBehavior, ToggleButtonBehavior
from kivygo.behaviors.hover import HoverBehavior
from kivy.uix.label import Label
from kivy.metrics import dp


Builder.load_string("""

<NeuBaseButton>:
	size: [dp(100), dp(100)]
	size_hint: [None, None]
	anchor_x: "center"
	anchor_y: "center"
	
	canvas.before:
		Clear
		Color:
		
		RoundedRectangle:
			size: self.light_shadow_size
			pos: self.light_shadow_pos
			texture: self.light_shadow
		
		Color:
			rgba: [1, 1, 1, 1]
		
		RoundedRectangle:
			size: self.dark_shadow_size
			pos: self.dark_shadow_pos
			texture: self.dark_shadow
	
	Label:
		id: label
		text: root.text
		size: self.texture_size
		size_hint: [None, None]
		font_size: root.font_size
		italic: root.italic
		color: root.text_color
		markup: True
		disabled: root.disabled
		font_name: root.font_name if root.font_name else 'Arial'


<NeuButton>:
	canvas.before:
		Color:
			rgba: self.comp_color
		RoundedRectangle:
			size: self.size
			pos: self.pos
			radius: self.radius
			texture: self.border_texture
		Color:
			rgba: [1, 1, 1, 1]


<NeuCircularButton>:
	canvas.before:
		Color:
			rgba: self.comp_color
		Ellipse:
			size: [self.radius] * 2
			pos: self.pos
			texture: self.border_texture
		Color:
	size: [self.radius] * 2


<ButtonEffect>:
	canvas.before:
		Color:
			rgba: self.background
		RoundedRectangle:
			size: self.size
			pos: self.pos
			radius: self.radius
	canvas.after:
		Color:
			rgba: self.background_line
		Line:
			rounded_rectangle: (self.pos + self.size + self.radius + [100])
			width: self.width_line

			
<ToggleButtonEffect>:
	

""")

class ButtonEffect(ButtonBehavior, Label, EffectBehavior, HoverBehavior):
	#Colors
	background_line = ListProperty([0, 0, 0, 0])
	background = ListProperty([0, 0, 0, 0])
	
	down_color_text = ListProperty([0, 0, 0, 0])
	down_color_line = ListProperty([0, 0, 0, 0])

	radius = ListProperty([0, 0, 0, 0])

	background_color = ListProperty([[0.05, 0.0, 0.4, 1], [0.0625, 0.0, 0.5, 1]])
	color_line = ListProperty([[1, 1, 1, 1], [0.8, 0.925, 1, 1]])
	color_text = ListProperty([[1, 1, 1, 1], [0.8, 0.925, 1, 1]])

	duration_back = NumericProperty(0.2)

	#Sizes
	width_line = NumericProperty(1.01)
	_pressed = False

	def __init__(self, **kwargs):
		self.bind(
			background_color=self.set_color,
			color_line=self.set_color,
			color_text=self.set_color)
		self.type_button = 'rounded'
		super(ButtonEffect, self).__init__(**kwargs)
		Clock.schedule_once(self.set_color)
	
	def set_color(self, *args):
		self.background = self.get_color(self.background_color, 0)
		self.background_line = self.get_color(self.color_line, 0)
		self.color = self.get_color(self.color_text, 0)
	
	def get_color(self, object, index):
		if isinstance(object, (list, tuple)):
			if len(object) == 2 and index > -1 and index < 3:
				return object[index]
		return object


	def set_pressed(self, *args):
		if self.down_color_text[-1] != 0:
			self.color = self.down_color_text
		if self.down_color_line[-1] != 0:
			self.background_line = self.down_color_line

	def on_touch_down(self, touch):
		if not self.collide_point(*touch.pos):
			return False

		Animation.cancel_all(self, 'color', 'background_line')
		self.set_pressed()
		
		touch.grab(self)
		self.ripple_show(touch)
		self._pressed = True
		return super().on_touch_down(touch)

	def on_touch_up(self, touch):
		if touch.grab_current is self:
			touch.ungrab(self)
			self.ripple_fade()
		
		if not self.collide_point(*touch.pos):
			return False
		
		anim = Animation(
			color=self.get_color(self.color_text, 1),
			background_line=self.get_color(self.color_line, 1),
			t=self.transition_out,
			duration=self.duration_out)
		anim.bind(on_complete=self.on_touch_anim_end)
		anim.start(self)
		return super().on_touch_up(touch)

	def on_touch_anim_end(self, *args):
		self._pressed = False
		self.new_dispatch()
		self.hover_visible = True

	def on_cursor_enter(self, *args):
		if not self._pressed:
			self.background_line = self.get_color(self.color_line, 1)
			self.color = self.get_color(self.color_text, 1)
		anim = Animation(
			background=self.get_color(self.background_color, 1),
			d=self.duration_back, t='out_quad')
		anim.start(self)
		return super().on_cursor_enter(*args)

	def on_cursor_leave(self, *args):
		anim = Animation(
			background=self.get_color(self.background_color, 0),
			d=self.duration_back, t='out_quad')
		anim.start(self)
		if not self._pressed:
			self.color = self.get_color(self.color_text, 0)
			self.background_line = self.get_color(self.color_line, 0)
		return super().on_cursor_leave(*args)


class ToggleButtonEffect(ToggleButtonBehavior, ButtonEffect):
	pass


class NeuBaseButton(ButtonBehavior, AnchorLayout):

	text = StringProperty("")
	"""
	Button text
	"""

	font_size = NumericProperty("14sp")
	"""
	Size of font used
	"""

	disabled = BooleanProperty(False)
	"""
	Whether the button is disabled or not. When a button is disabled its text color
	is greyed out and it is not longer clickable
	"""

	font_name = StringProperty(default="Arial")
	"""
	Name of the face to be used
	"""

	text_color = ColorProperty([0, 0, 0, 0])
	"""
	Text color
	"""

	italic = BooleanProperty(False)
	"""
	If set tot true the text will be rendered with its italic font type. WIll only
	work if the given font name has an itallic type.
	"""

	comp_color = ColorProperty("#ccccd9")

	dark_color = ListProperty([0, 0, 0, 0])

	light_color = ListProperty([0, 0, 0, 0])


class NeuButton(NeuBaseButton, NeuMorphRectangle):
	radius = ListProperty([0, 0, 0, 0])


class NeuCircularButton(NeuBaseButton, NeuMorphCircular):

	radius = NumericProperty(dp(20))
	""" Radius of the button
	"""

	def on_size(self, *args):
		self.size = [self.radius] * 2

