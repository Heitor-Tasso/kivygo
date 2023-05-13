
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ListProperty, OptionProperty, NumericProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivygo.behaviors.touch_effecs import EffectBehavior
from kivygo.behaviors.hover import HoverBehavior


Builder.load_string("""


<ColoredAnchorLayout>:
	canvas.before: 
		Color:
			rgba: self._background_color
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: self.radius
	canvas.after:
		Color:
			rgba: self.stroke_color
		Line:
			rounded_rectangle: [*self.pos, *self.size, *self.radius]
			width: self.stroke_width

<AnchorLayoutBaseBack>:
	anchor_x: 'center'
	anchor_y: 'center'
	canvas.before:
		Color:
			rgba: self._background_color
		RoundedRectangle:
			size: self.size
			pos: self.pos
			radius: self.radius

""")


class ColoredAnchorLayout(AnchorLayout, HoverBehavior, EffectBehavior):

	stroke_color = ListProperty([0, 0 ,0 ,0])
	stroke_width = NumericProperty(2)

	background_color = ListProperty([0, 0, 0, 0])
	background_color_pos = ListProperty([0, 0, 0, 0])
	
	_background_color = ListProperty([0, 0, 0, 0])

	radius = ListProperty([0, 0, 0, 0])
	effect_color = ListProperty([0, 0, 0, 0])

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.type_button = 'rounded'
		Clock.schedule_once(self.set_color)
		self.bind(background_color=self.set_color)
	
	def set_color(self, *args):
		if isinstance(self.background_color[0], (int, float)):

			if self.background_color != [0, 0, 0, 0]:
				self._background_color = self.background_color

		elif self.background_color[0] != [0, 0, 0, 0]:
			self._background_color = self.background_color[0]
		
		if isinstance(self.background_color_pos[0], (int, float)):

			if self.background_color_pos != [0, 0, 0, 0]:
				self._background_color = self.background_color_pos
				
		elif self.background_color_pos[0] != [0, 0, 0, 0]:
			self._background_color = self.background_color_pos[0]

	def on_cursor_enter(self, *args):
		if not isinstance(self.background_color_pos[0], (int, float)):
			self._background_color = self.background_color_pos[1]

		return super().on_cursor_enter(*args)

	def on_cursor_leave(self, *args):
		if not isinstance(self.background_color_pos[0], (int, float)):
			self._background_color = self.background_color_pos[0]
			
		return super().on_cursor_leave(*args)

	def on_touch_down(self, touch):
		if not self.collide_point(*touch.pos):
			return False
		
		if len(self.background_color) == 2 and isinstance(self.background_color, (list, tuple)):
			self._background_color = self.background_color[1]
		
		self.ripple_show(touch)        
		return super().on_touch_down(touch)

	def on_touch_up(self, touch):
		if not self.collide_point(*touch.pos):
			return False
		
		if len(self.background_color) == 2 and isinstance(self.background_color, (list, tuple)):
			self._background_color = self.background_color[0]

		self.ripple_fade()
		return super().on_touch_up(touch)



class AnchorLayoutButton(ColoredAnchorLayout):
	
	state = OptionProperty('normal', options=('normal', 'down'))
	
	def set_color(self, *args):
		super().set_color(*args)
		Clock.schedule_once(lambda *a: self.on_state(self, self.state))


	def on_state(self, widget, state):
		toggle = None if not self.children else self.children[0]
		if state == "normal" and hasattr(toggle, "group"):
			if (not toggle.allow_no_selection and toggle.group and toggle.state == 'down'):
				self.state = 'down'
				return None

		if state == "down":
			if not isinstance(self.background_color[0], (int, float)):
				self._background_color = self.background_color[1]
			return None
			
		if not isinstance(self.background_color[0], (int, float)):
			self._background_color = self.background_color[0]


	def on_touch_down(self, touch):
		vl = super().on_touch_down(touch)
		if not vl: return False
		
		toggle = None if not self.children else self.children[0]
		if hasattr(toggle, "group"):
			self.state = 'normal' if self.state == 'down' else 'down'
		else:
			self.state = 'down'

		if hasattr(toggle, "state") and not vl:
			if hasattr(toggle, "group"):
				toggle._do_press()
			toggle.state = self.state
		
		return vl

	def on_touch_up(self, touch):
		vl = super().on_touch_up(touch)
		
		if not vl and hasattr(self.children[0], "group"):
			self.state = self.children[0].state
		elif vl:
			self.state = "normal"
		
		if not vl:
			return False
		
		if not vl and hasattr(self.children[0], "group"):
			self.children[0]._do_release()
			self.state = self.children[0].state
		elif not vl and hasattr(self.children[0], "state"):
			self.children[0].state = self.state

		return vl

