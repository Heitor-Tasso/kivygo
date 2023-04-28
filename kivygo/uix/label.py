
from kivygo.behaviors.button import ButtonBehavior

from kivy.core.text.markup import MarkupLabel as CoreLabel
from kivy.lang import Builder
from kivy.graphics.texture import Texture

from kivy.uix.label import Label
from kivy.properties import (
	NumericProperty, DictProperty,
	StringProperty, ObjectProperty,
	ListProperty, AliasProperty,
)

from kivy.clock import Clock
from kivy.graphics.vertex_instructions import Quad
from kivy.animation import AnimationTransition
from kivy.compat import string_types
from math import pi, cos, sin, radians
from kivy.vector import Vector
from kivygo.transformations import Transformations


Builder.load_string("""

<LabelGradient>:
	canvas.before:
		# draw the gradient below the normal Label Texture
		Color:
			rgba: [1, 1, 1, 1]
		Rectangle:
			texture: self.gradient
			size: self.texture_size
			pos: [ \
			int(self.center_x - self.texture_size[0] / 2.0), \
			int(self.center_y - self.texture_size[1] / 2.0)]
			
<LabelButton>:
	color: [1, 1, 1, 1]

<LabelToScroll>:
	text: 'Section Option'
	padding_x: '15dp'
	size_hint_y: None
	on_size: self.update_content()
	text_size: self.size
	valign: 'center'
	halign: 'center'
	multiline: True

""")


class LabelGradient(Label):

	gradient = ObjectProperty(None)
	bg_color = ListProperty([0, 0, 0, 255])

	def __init__(self, **kwargs):
		super(LabelGradient, self).__init__(**kwargs)

		# bind to texture to trigger use of gradient
		self.bind(texture=self.fix_texture)

	def fix_texture(self, instance, texture):
		if self.gradient is None:
			return

		# unbind, so we don't loop
		self.unbind(texture=self.fix_texture)

		# The normal Label texture is transparent except for the text itself
		# This code changes the texture to make the text transparent, and everything else
		# gets set to self.bg_color (a property of LabelGradient)
		pixels = list(self.texture.pixels)
		
		for index in range(3, len(pixels)-4, 4):

			if pixels[index] == 0:
				# change transparent pixels to the bg_color
				pixels[index-3:index+1] = self.bg_color
			else:
				# make the text itself transparent
				pixels[index] = 0

		# create a new texture, blit the new pixels, and apply the new texture
		new_texture = Texture.create(size=self.texture.size, colorfmt='rgba')
		new_texture.blit_buffer(bytes(pixels), colorfmt='rgba', bufferfmt='ubyte')
		new_texture.flip_vertical()
		self.texture = new_texture

	
class LabelButton(ButtonBehavior, Label):
	pass


class LabelToScroll(Label):

	n_lines = NumericProperty(0)
	d_height = NumericProperty(0)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.update_content, 3)

	def update_content(self, *args):
		kw = self._label.options.copy()
		kw['text'] = self.text
		kw['text_size'] = [self.text_size[0], None]
		lb = CoreLabel(**kw)
		lb.refresh()
		self.height = lb.texture.size[1]


class AnimatedLabel(Label):
	'''duration of the animation of each letter'''
	letter_duration = NumericProperty()

	'''time to wait before starting to animate each letter'''
	letter_offset = NumericProperty()

	'''target text to set to animate'''
	target_text = StringProperty(u'')

	transition_function = ObjectProperty(AnimationTransition.linear)

	'''this function will get the destination coordinates of the letter,
	and the progress for this letter, must return the current
	coordinates, for a Quad to use
	(x3, y3)¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨(x2, y2)
	       |      /------\      |
	       |     / __--__ \     |
	(x0, y0)____________________(x1, y1)
	'''
	transform = ObjectProperty(Transformations.bouncey)

	_cache = DictProperty({})
	_time = NumericProperty()

	def _get_progress(self):
		duration = (self.letter_offset * len(self.target_text))
		duration += self.letter_duration 
		if not duration:
			return 0

		return (self._time / duration)

	progress = AliasProperty(
		_get_progress,
		bind=['_time', 'target_text', 'letter_duration', 'letter_offset']
	)

	def on_transition_function(self, instance, value):
		if isinstance(value, string_types):
			self.transition_function = getattr(AnimationTransition, value)

	def on_transform(self, instance, value):
		if isinstance(value, string_types):
			self.transform = getattr(Transformations, value)

	def on_target_text(self, instance, value):
		self.markup = True
		self.text = ''.join(
			u'[ref={}]{}[/ref]'.format(i, l)
			for i, l in enumerate(value)
		)

	def cache_text(self, *args):
		self._cache = {}
		for l in self.target_text:
			if l not in self._cache:
				self._cache[l] = l = Label(
					text=l,
					color=self.color,
					font_size=self.font_size,
					font_name=self.font_name)

	def cleanup(self):
		self.quads = []

	def on_texture(self, instance, value):
		self.canvas.clear()
		self.cache_text()
		self.cleanup()
		with self.canvas:
			for l in self.target_text:
				self.create_letter(l)

	def create_letter(self, letter):
		new_quad = Quad(
					points=[0, 0, 0, 0, 0, 0, 0, 0],
					texture=self._cache[letter].texture
		)
		self.quads.append(new_quad)

	def tick(self, dt):
		self._time += dt
		return (
			self._time < self.letter_duration +
			len(self.target_text) * self.letter_offset
		)

	def on__time(self, instance, value):
		if not self.texture:
			print("texture not ready")
			return None
		
		if len(self.refs) != len(self.target_text):
			print("still no refs?")
			return None

		for i, l in enumerate(self.target_text):
			n_value = value - i * self.letter_offset
			if not 0 < n_value < self.letter_duration:
				continue

			self.update_letter(value, i, l)

	def update_letter(self, time, index, letter):
		new_offset = (time - index * self.letter_offset)
		a = self.transition_function(new_offset / self.letter_duration)
		
		# ref can contain multiple rects, but we will always have
		# just one, assuming no letter is cut in half
		coords = list(self.refs[str(index)][0])
		coords[0] += (self.center_x - self.texture_size[0] / 2)
		coords[1] += (self.center_y - self.texture_size[1] / 2)
		coords[2] += (self.center_x - self.texture_size[0] / 2)
		coords[3] += (self.center_y - self.texture_size[1] / 2)

		points = self.transform(coords, a)
		self.quads[index].points = points
		self.quads[index].texture = self._cache[letter].texture

	def animate(self):
		if not self.target_text:
			return None
		
		self._time = 0
		Clock.unschedule(self.tick)
		Clock.schedule_interval(self.tick, 0)


class AnimatedBezierLabel(AnimatedLabel):

	def compute_bezier(self, points, n):
		'''compute nth segment point among segments of the bezier line
		defined by points

		Beware, complexity is quadratic to the number of points
		'''
		# http://en.wikipedia.org/wiki/De_Casteljau%27s_algorithm
		# as the list is in the form of (x1, y1, x2, y2...) iteration is
		# done on each item and the current item (xn or yn) in the list is
		# replaced with a calculation of "xn + x(n+1) - xn" x(n+1) is
		# placed at n+2. each iteration makes the list one item shorter
		_points = points[:]
		n_points = len(_points)
		for i in range(1, n_points):
			for j in range(n_points - 2 * i):
				_points[j] = _points[j] + (_points[j + 2] - _points[j]) * n

		# we got the coordinates of the point in T[0] and T[1]
		return [_points[0], _points[1]]


	def compute_bezier_length(self, *args):
		if not self.points:
			return 0

		a = 0
		l = 0
		v = Vector(self.compute_bezier(self.points, 0))

		while a < 1:
			a += 0.01
			p = self.compute_bezier(self.points, a)
			l += v.distance(p)
			v = Vector(p)
		return l
	
	points = ListProperty([])

	bezier_length = AliasProperty(
		compute_bezier_length,
		cache=True, bind=['points', ]
	)

	def bezier(self, points, progress):
		# XXX for now we don't care about the original position, so
		# kerning is out, along any sane spacing, this is an experiment
		if not self.points:
			return [0, 0, 0, 0, 0, 0, 0, 0]

		d_ratio = 1 / (self.bezier_length or 1)
		x0, y0, x1, y1 = points

		# initial letter offset of the letter
		dx = (x1 + x0) / 2 - (self.center_x - self.texture_size[0] / 2)
		
		# convert it to a progress offset on the bezier curve
		da = (dx * d_ratio)
		progress = (progress - da)
		w = (x1 - x0)
		h = (y1 - y0)
		e = 0.01
		
		b1 = self.compute_bezier(
			self.points,
			max(0, progress - e)
		)

		b2 = self.compute_bezier(
			self.points,
			min(progress + e, 1)
		)

		cx = (b2[0] + b1[0]) / 2
		cy = (b2[1] + b1[1]) / 2
		a = - pi / 2 + radians((Vector(b2) - Vector(b1)).angle((0, 1)))

		if not 0 <= progress < (1 + e):
			a += pi

		return [
			(cx + cos(a - 3 * pi / 4) * w / 2), (cy + sin(a - 3 * pi / 4) * h / 2),
			(cx + cos(a - 1 * pi / 4) * w / 2), (cy + sin(a - 1 * pi / 4) * h / 2),
			(cx + cos(a + 1 * pi / 4) * w / 2), (cy + sin(a + 1 * pi / 4) * h / 2),
			(cx + cos(a + 3 * pi / 4) * w / 2), (cy + sin(a + 3 * pi / 4) * h / 2),
		]


