
from kivy.graphics import (
	CanvasBase, Color,
	Ellipse, ScissorPush,
	ScissorPop, RoundedRectangle,
)
from kivy.graphics.stencil_instructions import (
	StencilPop, StencilPush,
	StencilUnUse, StencilUse,
)
from kivy.properties import (
	ListProperty, NumericProperty,
	StringProperty, BooleanProperty
)

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang.builder import Builder

Builder.load_string("""

<RippleEffectBehavior>:
	effect_color: GoColors.primary_effect

""")


class RippleEffectBehavior(Widget):

	#Size Ellipse
	radius_ellipse_default = NumericProperty(dp(10))
	radius_ellipse = NumericProperty(dp(10))

	#Type transition
	transition_in = StringProperty('in_cubic')
	transition_out = StringProperty('out_quad')

	#Duration of transition
	duration_in = NumericProperty(0.3)
	duration_out = NumericProperty(0.2)

	#To know the touch.pos of the widget
	touch_pos = ListProperty([0, 0])

	#Color background_effect
	effect_color = ListProperty([0]*4)
	opacity_effect = NumericProperty(1)
	_color_rgba = ListProperty([0]*4)

	#radius if Rounded
	radius_effect = ListProperty([dp(10)]*4)

	# If the widget don't has radius, set it to 0
	radius = ListProperty([0]*4)

	auto_effect = BooleanProperty(True)

	def __init__(self, **kwargs):
		self.register_event_type('on_touch_anim_end')
		super().__init__(**kwargs)
		self.radius_ellipse_default = self.radius_ellipse

		self.bind(touch_pos=self.set_ellipse,
				  radius_ellipse=self.set_ellipse,
				  _color_rgba=self.set_ellipse)
		
		self.bind(pos=self.draw_effect, size=self.draw_effect)

		self.ripple_ellipse = None
		self.ripple_rectangle = None
		self.ripple_col_instruction = None
		self.ripple_pane = None
		self.anim = None

		Clock.schedule_once(self.set_config)

	def set_config(self,  *args):
		self.ripple_pane = CanvasBase()
		self.canvas.before.add(self.ripple_pane)

	def ripple_show(self, touch):
		Animation.cancel_all(self, 'radius_ellipse', '_color_rgba')
		if isinstance(self, RelativeLayout):
			pos_x, pos_y = self.to_window(*self.pos)
			self.touch_pos = (touch.x-pos_x, touch.y-pos_y)
		else:
			self.touch_pos = (touch.x, touch.y)
		
		self.draw_effect()
		self._color_rgba = self.effect_color[0:-1] + [0]
		self.anim = Animation(
			radius_ellipse=(max(self.size)*2),
			t=self.transition_in,
			_color_rgba=self.effect_color[0:-1] + [self.opacity_effect],
			duration=self.duration_in,
		)
		self.anim.start(self)

	def draw_effect(self, *args):
		if self.ripple_pane == None:
			return None

		self.reset_canvas()

		with self.ripple_pane:
			StencilPush()
			self.ripple_rectangle = RoundedRectangle(
				size=self.size, pos=self.pos,
				radius=self.radius_effect[::-1],
			)
			StencilUse()
			self.ripple_col_instruction = Color(rgba=self._color_rgba)
			self.ripple_ellipse = Ellipse(
				size=(self.radius_ellipse for _ in range(2)),
				pos=(x-self.radius_ellipse/2 for x in self.touch_pos),
			)
			StencilUnUse()
			self.ripple_rectangle = RoundedRectangle(
				size=self.size, pos=self.pos, 
				radius=self.radius_effect[::-1],
			)
			StencilPop()


	def ripple_fade(self, *args):
		if self.anim == None:
			return None
		
		if self._color_rgba[-1] < self.opacity_effect:
			self.anim.bind(on_complete=self.ripple_fade)
			return None
		
		anim = Animation(
			radius_ellipse=max(self.size)*2,
			_color_rgba=self.effect_color[0:-1] + [0],
			t=self.transition_out,
			duration=self.duration_out
		)
		anim.bind(on_complete=self.reset_canvas)
		anim.start(self)

	def set_ellipse(self, instance, value):
		if not self.ripple_ellipse:
			return None

		self.ripple_ellipse.size = (self.radius_ellipse for _ in range(2))
		self.ripple_ellipse.pos = (x-self.radius_ellipse/2 for x in self.touch_pos)
		self.ripple_col_instruction.rgba = self._color_rgba

	def reset_canvas(self, *args):
		self.ripple_rectangle = None
		self.ripple_ellipse = None
		self.radius_ellipse = self.radius_ellipse_default
		self.ripple_pane.clear()
		self.dispatch('on_touch_anim_end')
	
	def on_touch_anim_end(self, *args):
		pass

	def on_touch_down(self, touch):
		result = super().on_touch_down(touch)
		if not self.auto_effect:
			return result
		
		if not self.collide_point(*touch.pos):
			return False
		
		self.ripple_show(touch)
		return result

	def on_touch_up(self, touch):
		result = super().on_touch_up(touch)
		if not self.auto_effect:
			return result
		
		if not self.collide_point(*touch.pos):
			return False

		self.ripple_fade()
		return result
