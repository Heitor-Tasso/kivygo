from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import (
	ColorProperty, ListProperty,
	NumericProperty, ObjectProperty
)
from kivy.uix.slider import Slider
from kivygo.behaviors.neumorph import GoGlowCircular
from kivygo.behaviors.thumb import GoThumb
from kivy.metrics import dp
from kivy.graphics.texture import Texture
from kivygo.utils import dec_2_rgb
from PIL import Image, ImageDraw, ImageFilter


Builder.load_string("""

<GoSlider>
	canvas:
		Clear
		Color:
			rgba: self.background_color
		RoundedRectangle:
			size: self.size
			pos: self.pos
			radius: self.radius

	background_width: 0
	cursor_size: [0, 0]
	padding: (self.height / 2)

	GoSliderThumb:
		canvas.before:
			Color:
			Rectangle:
				size:self.glow_size
				pos:self.glow_pos
				texture:self.glow_texture
		canvas:
			Color:
				rgba:root.thumb_color
			Ellipse:
				size: [ (root.height - root.thumb_padding), (root.height - root.thumb_padding) ]
				pos:self.pos
			Color:

		size_hint: [None, None]
		size: [( root.height - root.thumb_padding ), ( root.height - root.thumb_padding ) ]
		pos: [ ( root.value_pos[0] - self.width / 2), ( root.center_y - self.height / 2) ]
		behind_color: ( root.comp_color[0:3] + [0] ) if root.thumb_bg_color == [0, 0, 0, 0] else root.thumb_bg_color
		glow_color: root.thumb_color if root.glow_color == [0, 0, 0, 0] else root.glow_color

""")


class GoSlider(Slider):

	comp_color = ColorProperty("#333333")

	shadow_behind_color = ColorProperty("#333333")

	background_color = ListProperty([0.6, 0.1, 0.4, 1])

	elevation = NumericProperty(dp(3))
	"""
	Elevation of the widget.Elevation can be any number between -5 and +5(inclusive).
	Negative elevation will cause the widget to go into the screen whereas positive
	elevation will make it pop from the screen
	"""

	radius = ListProperty([dp(20), dp(20), dp(20), dp(20)])
	"""
	Radius of the slider bar. The value defaults to half the height of the slider bar.
	"""

	thumb_color = ColorProperty([0, 0, 0, 0])
	"""
	Color of the thumb of the slider
	"""

	thumb_bg_color = ColorProperty([0, 0, 0, 0])
	"""
	Color of background behind the thumb. This property is needed to
	properly display the glow effect. The property will default to the component
	color. But it can be manually set. If a color is manually set it will create a
	ring of that color around the thumb's glow.

	attr:`thumb_bg_color` is an :class:`~kivy.properties.ColorProperty`
	and defaults to the slider's 'comp_color'.
	"""

	thumb_padding = NumericProperty(0)
	"""
	The top and bottom padding value for the the thumb. This allows you to inset
	the thumb in the slider. It defaults to zero which means the thumb will be
	as big as the height of the slider.
	"""

	glow_color = ColorProperty([0, 0, 0, 0])
	"""
	Color of the glow behind the thumb. Defaults to the thumb's color.
	"""

	glow_radius = NumericProperty(dp(20))
	"""
	Radius of the glow behind the thumb.
	"""

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.elevation_set)
		Clock.schedule_once(self.radius_set)

	def elevation_set(self, *args):
		self.elev = self.elevation

	def radius_set(self, *args):
		self.radius = [(self.height / 2)] * 4


class GoSliderThumb(GoThumb, GoGlowCircular):

	glow_color = ColorProperty([0.8, 0.7, 0.5, 1])

	elevation = NumericProperty(0)

	glow_radius = NumericProperty(dp(20))
	"""
	Radius of the glow
	"""

	color = ColorProperty([0, 0, 0, 0])
	"""
	Color of the glow. It is suggested to set this property to the color of the
	component that the glow is being added to
	"""

	behind_color = ColorProperty([0, 0, 0, 0])
	"""
	Color of the component behind the glow. If left blank it will result in
	a black ring around your glow, so make sure you set this color properly
	"""

	glow_texture = ObjectProperty()
	"""
	The property that holds the actual glow texture object
	"""

	glow_size = ListProperty([0, 0])
	"""
	A list containing the size of the glow texture
	"""

	glow_pos = ListProperty([0, 0])
	"""
	A list containing the position of the glow texture
	"""


	def on_size(self, *args):
		self._create_glow()

	def on_pos(self, *args):
		self._update_glow_pos()

	def on_glow_radius(self, *args):
		self._create_glow()


	def __init__(self, **kwargs):
		self.elev = self.elevation
		self.blank_texture = Texture.create(size=self.size, colorfmt="rgba")
		Clock.schedule_once(self._create_glow)
		super().__init__(**kwargs)


	def _create_glow(self, *args):
		# Create blank image
		blank_x_size = int(self.size[0] + self.glow_radius * 2)
		blank_y_size = int(self.size[1] + self.glow_radius * 2)
		
		shadow = Image.new(
			"RGBA",
			(blank_x_size, blank_y_size),
			color=(tuple(dec_2_rgb(self.behind_color))),
		)

		# Convert to drawable image
		blank_draw = ImageDraw.Draw(shadow)
		
		x0 = (blank_x_size - self.size[0]) / 2.0
		y0 = (blank_y_size - self.size[1]) / 2.0
		
		x1 = (x0 + self.size[0])
		y1 = (y0 + self.size[1])

		blank_draw.ellipse(
			[(x0, y0), (x1, y1)],
			fill=tuple(dec_2_rgb(self.glow_color)),
		)

		texture = Texture.create(size=(blank_x_size, blank_y_size), colorfmt="rgba")
		shadow = shadow.filter(ImageFilter.GaussianBlur(self.glow_radius / 2))
		texture.blit_buffer(shadow.tobytes(), colorfmt="rgba", bufferfmt="ubyte")
		
		self.glow_texture = texture
		self.glow_size = (blank_x_size, blank_y_size)
		self.glow_pos = [(self.pos[0] - x0), (self.pos[1] - y0)]

	def _update_glow_pos(self):
		self.glow_pos = [(self.pos[0] - self.glow_radius), (self.pos[1] - self.glow_radius)]

