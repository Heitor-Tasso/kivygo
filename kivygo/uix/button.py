
from kivy.properties import ListProperty, NumericProperty
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.label import Label

from kivygo.behaviors.hover import HoverBehavior
from kivygo.behaviors.touch_effecs import EffectBehavior
from kivygo.behaviors.button import ButtonBehavior, ToggleButtonBehavior


Builder.load_string("""

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

	down_background_color = ListProperty([])
	background_color = ListProperty([[0.05, 0.0, 0.4, 1], [0.0625, 0.0, 0.5, 1]])
	color_line = ListProperty([[1, 1, 1, 1], [0.8, 0.925, 1, 1]])
	color_text = ListProperty([[1, 1, 1, 1], [0.8, 0.925, 1, 1]])

	duration_back = NumericProperty(0.2)

	#Sizes
	width_line = NumericProperty(1.01)
	_pressed = False

	def __init__(self, **kwargs):
		self.bind(
			down_background_color=self.set_color,
			background_color=self.set_color,
			color_line=self.set_color,
			color_text=self.set_color)
		self.type_button = 'rounded'
		super().__init__(**kwargs)
		Clock.schedule_once(self.set_color)
	
	def set_color(self, *args):
		if self.down_background_color:
			self.background = self.get_color(self.down_background_color, 0)
		else:
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
		
		if self.down_background_color:
			self.background = self.get_color(self.down_background_color, 1)

	def on_touch_down(self, touch):
		
		if not self.collide_point(*touch.pos):
			return False

		Animation.cancel_all(self, 'color', 'background_line')
		
		touch.grab(self)
		self.ripple_show(touch)
		self._pressed = True
		result = super().on_touch_down(touch)
		if self.state == "down":
			self.set_pressed()
		return result

	def on_touch_up(self, touch):

		if touch.grab_current is self:
			touch.ungrab(self)
			self.ripple_fade()
		
		result = super().on_touch_up(touch)

		if self.down_background_color and self.state == "normal":
			self.background = self.get_color(self.down_background_color, 0)
		
		if not self.collide_point(*touch.pos):
			return False
		
		anim = Animation(
			color=self.get_color(self.color_text, 1),
			background_line=self.get_color(self.color_line, 1),
			t=self.transition_out,
			duration=self.duration_out)
		anim.bind(on_complete=self.on_touch_anim_end)
		anim.start(self)

		return result

	def on_touch_anim_end(self, *args):
		self._pressed = False
		self.new_dispatch()
		self.hover_visible = True

	def on_cursor_enter(self, *args):
		if not self._pressed:
			self.background_line = self.get_color(self.color_line, 1)
			self.color = self.get_color(self.color_text, 1)
		
		if not self.down_background_color:
			anim = Animation(
				background=self.get_color(self.background_color, 1),
				d=self.duration_back, t='out_quad')
			anim.start(self)
		return super().on_cursor_enter(*args)

	def on_cursor_leave(self, *args):
		if not self.down_background_color:
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
