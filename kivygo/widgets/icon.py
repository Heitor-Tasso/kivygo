
from kivygo.behaviors.button import ButtonBehavior, ToggleButtonBehavior
from kivygo.behaviors.ripple_effect import RippleEffectBehavior
from kivygo.behaviors.hover import HoverBehavior

from kivygo.widgets.image import ImageWithSVG
from kivygo.layouts.anchorlayout import GoColoredAnchorLayout
from kivy.properties import (
    ListProperty, BooleanProperty,
    StringProperty, OptionProperty
)
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.clock import Clock


Builder.load_string("""

#:import ImageWithSVG kivygo.widgets.image.ImageWithSVG

<Icon>:
	anchor_y: 'center'
	anchor_x: 'center'
	fit_mode: "fill"
	BoxLayout:
		padding: ['5dp', '5dp', '5dp', '5dp']
		size_hint: [None, None]
		size: root.icon_size

		ImageWithSVG:
			image_source: root.icon_source
			fit_mode: root.fit_mode
			mipmap: root.mipmap
			color: root.color


<ButtonIcon>:
	size_hint: [None, None]
	mipmap: True
	allow_strech: True
	fit_mode: "fill"
	canvas:
		Clear
	canvas.before:
		Color:
			rgba: self._background_color
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: self.radius
	canvas.after:
		Color:
			rgba: self.color
		Rectangle:
			texture: self.texture
			pos: self.pos
			size: self.size


<ToggleButtonIcon>:
	size: ['30dp', '30dp']


""")


class Icon(GoColoredAnchorLayout):

	fit_mode = OptionProperty(
        "fill", options=["scale-down", "scale-down", "contain", "cover"]
    )

	color = ListProperty([1, 1, 1, 1])
	mipmap = BooleanProperty(True)
	icon_source = StringProperty("")
	icon_size = ListProperty([dp(40), dp(40)])


class ButtonIcon(ButtonBehavior, ImageWithSVG, RippleEffectBehavior, HoverBehavior):

	# Properties
	icon_state_color = ListProperty([-1, -1, -1, -1])
	icon_color = ListProperty([1, 1, 1, 1])
	icon_state_source = ListProperty(['', ''])
	background_color = ListProperty([-1, -1, -1, -1])
	_background_color = ListProperty([0, 0, 0, 0])
	radius = ListProperty([0, 0, 0, 0])
	
	def __init__(self, **kwargs):
		self.color = [1, 1, 1, 1]
		super().__init__(**kwargs)
		Clock.schedule_once(self.set_color)
	
	def set_color(self, *args):

		if self.image_source != '' and len(self.image_source) != 2:
			self.set_source(self.image_source)

		elif len(self.image_source) == 2 and '' not in self.image_source:
			self.set_source(self.image_source[0])

		elif len(self.icon_state_source) == 2 and '' not in self.icon_state_source:
			self.set_source(self.icon_state_source[0])
		
		if isinstance(self.icon_color[0], (int, float)):
			self.color = self.icon_color
		else:
			self.color = self.icon_color[0]
		
		if isinstance(self.icon_state_color[0], (int, float)):

			if self.icon_state_color != [-1, -1, -1, -1]:
				self.color = self.icon_state_color
		else:
			self.color = self.icon_state_color[0]
		
		if isinstance(self.background_color[0], (int, float)):

			if self.background_color != [-1, -1, -1, -1]:
				self._background_color = self.background_color
		else:
			self._background_color = self.background_color[0]

		Clock.schedule_once(lambda *a: self.on_state(self, self.state))
	

	def on_state(self, widget, state):
		
		if len(self.icon_state_source) == 2 and '' not in self.icon_state_source:

			if state == 'normal':
				self.set_source(self.icon_state_source[0])

			elif state == 'down':
				self.set_source(self.icon_state_source[1])

		if state == "down":

			if not isinstance(self.icon_state_color[0], (int, float)):
				self.color = self.icon_state_color[1]

			if not isinstance(self.background_color[0], (int, float)):
				self._background_color = self.background_color[1]
			
			return None
		
		if not isinstance(self.icon_state_color[0], (int, float)):
			self.color = self.icon_state_color[0]

		if not isinstance(self.background_color[0], (int, float)):

			self._background_color = self.background_color[0]


	def on_cursor_enter(self, *args):

		if len(self.image_source) == 2 and '' not in self.image_source:
			self.set_source(self.image_source[1])

		if not isinstance(self.icon_color[0], (int, float)):
			self.color = self.icon_color[1]

		return super().on_cursor_enter(*args)

	def on_cursor_leave(self, *args):
		
		if len(self.image_source) == 2 and '' not in self.image_source:
			self.set_source(self.image_source[0])
		
		if not isinstance(self.icon_color[0], (int, float)):
			self.color = self.icon_color[0]
			
		return super().on_cursor_leave(*args)

	def on_touch_down(self, touch):
		v = super().on_touch_down(touch)
		if not self.collide_point(*touch.pos):
			return False
		
		self.ripple_show(touch)
		return v
		
	def on_touch_up(self, touch):
		v = super().on_touch_up(touch)
		if not self.collide_point(*touch.pos):
			return False
		
		self.ripple_fade()
		return v


class ToggleButtonIcon(ToggleButtonBehavior, ButtonIcon):
	pass

