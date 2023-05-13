
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.graphics import PushMatrix, Rotate, PopMatrix
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.atlas import Atlas

from kivy.properties import (
	NumericProperty, ReferenceListProperty,
	AliasProperty, ObjectProperty, BooleanProperty,
	ListProperty, BoundedNumericProperty,
	StringProperty
)

from math import radians, sin, cos
import json

from kivygo.bounds_math import (
	peers, define_bounds, resize,
	update_bounds, aniresize, aniupdate_bounds,
	point_in_bounds, collide_bounds
)


class Rotabox(Widget):

	source_crop = StringProperty("")

	current_image = StringProperty("bounds")

	source_bounds = StringProperty("")

	atlas = ObjectProperty(None)
	

	image = ObjectProperty(None)
	'''This should be the image that any custom bounds are meant for.
	If not defined, widget will try to locate the topmost image in its tree.
	'''

	aspect_ratio = NumericProperty(0.0)
	'''The widget's aspect ratio. If not defined, image's ratio will be used.
	'''

	angle = NumericProperty(0)
	'''Angle of Rotation.
	'''


	def get_origin(self):
		return self.pivot

	def set_origin(self, point):
		angle = -radians(self.last_angle)
		orig = self.origin
		s = sin(angle)
		c = cos(angle)

		# normalize (translate point so origin will be 0,0)
		dx = point[0] - orig[0]
		dy = point[1] - orig[1]

		# un-rotate point
		xnew = dx * c - dy * s
		ynew = dx * s + dy * c

		# translate point back:
		pivot = xnew + orig[0], ynew + orig[1]

		# lock pos-pivot relation
		self.pivot_bond = [(pivot[0] - self.x) / float(self.width),
						   (pivot[1] - self.y) / float(self.height)]

		# Since the image (on canvas) always starts each frame in zero angle,
		# an [origin] change in any non-zero angle breaks the continuity of
		# motion/rotation, introducing an image translation (jump).
		# compensating by changing the widget's position.

		# prevent a bounds' update to [pos] change below.
		self.allow = 0

		# compensating for image translation
		self.pos = (self.x - (pivot[0] - point[0]),
					self.y - (pivot[1] - point[1]))

		# cannot wait for the triggered [update], at the end of this frame,
		# since it might concern other changes that require a bounds' update.
		# self.update()
		self.trigger_update()

	origin = AliasProperty(get_origin, set_origin)
	'''Sets the point of rotation. Default value is the widget's center.
	Works nicely with the [get_point] method below and points already defined in
	[custom_bounds].
	'''


	allow_rotabox = BooleanProperty(True)
	'''Enables widget's advanced collision detection. If False, widget will
	collide as a normal (non-Rotabox) widget.
	'''

	custom_bounds = ObjectProperty([[(0., 0.), (1., 0.), (1., 1.), (0., 1.)]])
	'''Custom bounds' definition interface. (See module's documentation).
	'''

	segment_mode = BooleanProperty(True)
	'''Collision detection method switch (see documentation above).
	'''

	open_bounds = ListProperty([])
	'''(segment_mode) If a polygon's index is in this list, the segment
	between the last and first points of the polygon is not considered in the
	collision checks.
	'''

	pre_check = BooleanProperty(False)
	'''(Cython) A collision optimization switch for larger widgets (45+ points).
	It's always True in Python but in Cython, for small widgets, the slight tax 
	in updating the bounds outweighs the benefit in collision.
	'''


	def get_allow_drag(self):
		return self.allow_drag_x, self.allow_drag_y

	def set_allow_drag(self, value):
		if type(value) in (list, tuple):
			self.allow_drag_x, self.allow_drag_y = value
		else:
			self.allow_drag_x = self.allow_drag_y = bool(value)

	allow_drag = AliasProperty(get_allow_drag, set_allow_drag, bind=('allow_drag_x', 'allow_drag_y'))
	'''Allow touch translation on the X or Y axis.
	'''

	allow_drag_x = BooleanProperty(False)
	'''Allow touch translation on the X axis.
	'''

	allow_drag_y = BooleanProperty(False)
	'''Allow touch translation on the Y axis.
	'''


	single_touch_rotation = BooleanProperty(False)
	'''Allow rotation around [origin].
	'''

	single_touch_scaling = BooleanProperty(False)
	'''Allow scaling around [origin].
	'''

	multi_touch_rotation = BooleanProperty(False)
	'''Allow multitouch rotation. [origin] is defined each time by the touch.
	'''

	multi_touch_scaling = BooleanProperty(False)
	'''Allow multitouch scaling. [origin] is defined each time by the touch.
	'''

	single_drag_touch = BoundedNumericProperty(1, min=1)
	'''How many touches will be treated as one single drag touch.
	'''

	single_trans_touch = BoundedNumericProperty(1, min=1)
	'''How many touches will be treated as one single rotation/scaling touch.
	'''

	touched_to_front = BooleanProperty(False)
	'''If touched, widget will be pushed to the top of parent widget tree.
	'''

	collide_after_children = BooleanProperty(False)
	'''If True, limiting the touch inside the bounds will be done after
	dispaching the touch to the child and grandchildren, so even outside the
	bounds they can still be touched.
	IMPORTANT NOTE: Grandchildren, inside or outside the bounds, can collide
		independently ONLY if widget is NOT ROTATED ([angle] must be 0).
	'''


	def get_scale(self):
		return float(self.width) / self.original_size[0]

	def set_scale(self, amount):
		if amount < self.scale_min:
			amount = self.scale_min
		elif amount > self.scale_max:
			amount = self.scale_max

		pivot = self.pivot[:]
		self.size = (amount * self.original_size[0],
					 amount * self.original_size[1])
		self.pivot = pivot
		if self.initial_scale:
			return
		self.initial_scale = self.scale
	
	scale = AliasProperty(get_scale, set_scale, bind=('width', 'height', 'original_size'))
	'''
	Widget's current scale. Calculated from [original_size] (user's input
	[size] or [image]'s [texture_size]). Used for touch scaling but it can be an
	alternative to [size].
	'''

	scale_min = NumericProperty(0.01)
	'''Minimum scale allowed.
	'''

	scale_max = NumericProperty(1e20)
	'''Maximum scale allowed.
	'''


	def get_pivot_x(self):
		return self.x + self.width * self.pivot_bond[0]

	def set_pivot_x(self, value):
		if self.width > 1:
			self.x = value - self.width * self.pivot_bond[0]
		elif value > 1:
			self.temp_piv_x = value

	def get_pivot_y(self):
		return self.y + self.height * self.pivot_bond[1]

	def set_pivot_y(self, value):
		if self.height > 1:
			self.y = value - self.height * self.pivot_bond[1]
		elif value > 1:
			self.temp_piv_y = value

	pivot_x = AliasProperty(get_pivot_x, set_pivot_x, bind=('x', 'width', 'pivot_bond'))
	pivot_y = AliasProperty(get_pivot_y, set_pivot_y, bind=('y', 'height', 'pivot_bond'))
	pivot = ReferenceListProperty(pivot_x, pivot_y)
	'''
	Point of rotation and scaling.
	While [origin] property sets [pivot]'s relation to widget, [pivot]
	itself can be used to position the widget, much like [pos] or [center].
	'''

	prepared = BooleanProperty(False)
	'''
	Its state change signifies a reset. The reset completion signal, however,
	is the consequent [ready] state change to True.
	'''

	draw_bounds = BooleanProperty(False)
	'''Enables bounds visualization (for testing).
	'''


	__events__ = ('on_transform_with_touch', 'on_touched_to_front')

	def on_transform_with_touch(self, touch):
		'''
		Called when a touch event has transformed the widget.
		By default this does nothing, but can be overriden by derived
		classes that need to react to transformations caused by user
		input.
		'''
		pass

	def on_touched_to_front(self, touch):
		'''
		Called when a touch event causes the widget to be brought to the
		front of the parent (only if :attr:`touched_to_front` is True)
		'''
		pass


	def __init__(self, **kwargs):
		self.size = [1, 1]
		self.temp_piv_x = self.temp_piv_y = 0
		self.initial_scale = 0
		self.touches = []
		self.last_touch_pos = {}
		
		super().__init__(**kwargs)
		
		self.image = Image()
		self.sized_by_img = False
		self.ratio = 1
		self.last_pos = [0, 0]
		self.last_size = self.size[:]
		self.last_angle = 0
		self.anim = False
		self.rid = 0
		self.curr_key = 'bounds'
		self.draw_color = Color(rgba=[0.29, 0.518, 1, 1])
		self.box_color = Color(rgba=[0.35, 0.15, 0, 1])
		self.draw_lines = []
		self.box_lines = []
		self.rotation = Rotate(angle=0, origin=self.center)
		self.canvas.before.add(PushMatrix())
		self.canvas.before.add(self.rotation)
		self.canvas.after.add(PopMatrix())

		self.trigger_update = Clock.create_trigger(self.update, -1)
		self.trigger_draw = Clock.create_trigger(self.draw, -1)

		self.bind(
			children=self.trigger_update,
			parent=self.trigger_update,
			pos=self.trigger_update,
			pos_hint=self.trigger_update,
			angle=self.trigger_update,
			image=self.on_reset,
			aspect_ratio=self.on_reset,
			custom_bounds=self.on_reset,
			allow_rotabox=self.on_reset,
			draw_bounds=self.on_reset
		)
	
	def add_widget(self, widget, **kwargs):
		if self.children:
			raise Exception('Rotabox can only have one child.')
		super().add_widget(widget)

	def on_open_bounds(self, *args):
		if self.open_bounds and not self.segment_mode:
			raise Exception('Open bounds are only applicable in Segment mode.')

	def on_source_bounds(self, *args):
		self.custom_bounds = self.read_bounds(self.source_bounds)

	def on_current_image(self, *args):
		if self.atlas == None:
			return None
		
		self.image.texture = self.atlas.textures[self.current_image]
		self.prepared = False
		self.trigger_update()

	def on_source_crop(self, *args):
		if self.source_crop == "":
			self.atlas = None
			self.image = None
			self.clear_widgets()
			return None
		
		if self.image != None and not self.image in self.children:
			self.add_widget(self.image)
		
		self.atlas = Atlas(self.source_crop)
		self.image.texture = tuple(self.atlas.textures.values())[0]
		
	def on_size(self, *args):
		self.trigger_update()

	def on_reset(self, *args):
		self.trigger_update()

	def reset_draw_bounds(self, *args):
		for line in self.draw_lines:
			self.canvas.after.remove(line)
		self.draw_lines = []

		for line in self.box_lines:
			self.canvas.after.remove(line)
		self.box_lines = []

	def prepare(self, n=None, *args):
		self.prepared = True
		tempscale = self.initial_scale

		if self.source_crop or self.image:
			try:
				self.image.texture.mag_filter = 'nearest'
			except AttributeError:
				pass

			self.image.allow_stretch = True

			# Calculating widget's size from available inputs.
			if (not (self.width - tempscale > 1 or self.height - tempscale > 1) or self.sized_by_img):
				try:
					self.original_size = self.image.texture.size
				except AttributeError:
					# If animation, texture not ready (?)
					self.original_size = self.image.size

				if not tempscale:
					tempscale = 1
				self.size = list(map(lambda n: (n * tempscale), self.original_size))

				if self.sized_by_img:
					dw = self.width - self.last_size[0]
					dh = self.height - self.last_size[1]
					self.pivot = ( (self.pivot_x - dw * 0.5), (self.pivot_y - dh * 0.5) )
			else:
				self.original_size = self.size[:]
				if tempscale:
					self.size = list(map(lambda n: (n * tempscale), self.size))
		else:
			self.original_size = self.size[:]
			if not tempscale:
				tempscale = 1
			self.size = list(map(lambda n: (n * tempscale), self.size))

		# Setting the widget's ratio.
		if not self.aspect_ratio:
			if self.source_crop and self.sized_by_img:
				self.ratio = self.image.image_ratio
			else:
				self.ratio = (self.width / float(self.height))
		else:
			self.ratio = self.aspect_ratio

		# If [size] is not specified explicitly by the user, any input values
		# for [pivot] are withheld in [temp_piv_x] and [temp_piv_y], until
		# [size] gets its values from [image]. Then, [pivot] gets the withheld
		# values, here.
		if self.temp_piv_x or self.temp_piv_y:
			self.pivot = self.temp_piv_x, self.temp_piv_y
			self.temp_piv_x = self.temp_piv_y = 0

		if self.allow_rotabox:
			# Generating a unique key for each instance
			try:
				self.rid = sorted(peers.keys())[-1] + 1
			except IndexError:
				pass

			if isinstance(self.custom_bounds, dict):
				self.curr_key = self.current_image
				self.anim = True
			
			define_bounds(self.custom_bounds, self.open_bounds, self.segment_mode, self.rid, self.pre_check)
			
			if self.draw_bounds:
				self.set_draw()
				self.bind(
					children=self.trigger_draw,
					parent=self.trigger_draw,
					pos=self.trigger_draw,
					pos_hint=self.trigger_draw,
					angle=self.trigger_draw,
				)

		self.trigger_update()

	def get_point(self, pol_index, point_index):
		'''Access a point's current position, based on [custom_bounds] structure.'''
		bounds = peers[self.rid][self.curr_key]
		index = (sum(bounds['pol_lens'][:pol_index]) + point_index) * 2
		return list(bounds['points'][index:index + 2])

	def read_bounds(self, filename, delayed=False, *args):
		'''
		Define [custom_bounds] using a rotaboxer's project file.
		To work, [size] should be already defined.
		'''
		project = None
	
		try:
			with open(filename, 'r', encoding="UTF8") as proj:
				project = json.load(proj)
		except (IOError, KeyError) as er:
			print('On read_bounds: ', er)
			return None
		
		bounds = {}
		opens = []
		for f, frame in project.items():
			if f in ('image', 'version'):
				continue

			pols = []
			i = 0
			while i < len(frame):
				for pol in frame.values():
					if pol['number'] == i:
						pols.append(pol)
						break
				i += 1
			bounds[f] = []
			for p, pol in enumerate(pols):
				try:
					if pol['open']:
						opens.append(p)
				except KeyError:
					pass
				
				bounds[f].append([(round(float(point[0]) / self.width, 3),
									round(float(point[1]) / self.height, 3))
									for point in pol['points']])

		blen = len(bounds)
		if blen:
			if opens:
				self.open_bounds = opens

			if blen == 1:
				bounds = bounds[list(bounds.keys())[0]]

			if delayed:
				self.custom_bounds = bounds
				return None

			return bounds

		return self.custom_bounds


	def update_size(self, *args):
		
		width, height = self.size
		if round(self.ratio, 3) != round(width / float(height), 3):
			# Adjusting size to fit ratio
			last_size = self.last_size
			if abs(width - last_size[0]) > abs(height - last_size[1]):
				self.size = [width, (float(width) / self.ratio)]
			else:
				self.size = [(height * self.ratio), height]
			
			if last_size != [1, 1]:
				dw = self.width - last_size[0]
				dh = self.height - last_size[1]
				# Moving widget to keep pivot's position the same, to originate the resizing from pivot.
				self.pivot = ( (self.pivot_x - dw * 0.5), (self.pivot_y - dh * 0.5) )

		if self.allow_rotabox:
			# Scaling widget's bounds
			if not self.anim:
				resize(self.width, self.height, self.rid)
				update_bounds(self.pos, radians(self.angle), self.origin, self.rid, self.curr_key)
				self.allow = 0
			else:
				aniresize(self.width, self.height, self.rid)

		if self.children:
			self.children[0].size = self.size

		self.last_size = self.size[:]
		self.trigger_update()

	def update(self, *args):
		'''Updates the widget's angle, point of rotation, bounds and child's
		position.
		Also runs the [update_size] method on size change and the [prepare]
		method initially and on reset.
		'''
		if not self.prepared:
			self.prepare()
			self.update_size()
			return None

		self.angle %= 360
		angle = self.angle
		pos = self.pos

		# Updating the rotation instruction, in canvas.before
		self.rotation.origin = self.origin
		self.rotation.angle = angle

		# Updating the child's position
		if self.children:
			self.children[0].pos = pos

		motion = [pos[0] - self.last_pos[0], pos[1] - self.last_pos[1]]
		if abs(motion[0]) < .01 and abs(motion[1]) < 0.01:
			motion = []
		self.last_pos = pos[:]

		angle_diff = angle - self.last_angle
		if abs(angle_diff) < 0.01:
			angle_diff = 0

		self.last_angle = angle
		if not self.allow:
			self.allow = 1
			return None

		if self.allow_rotabox:
			# Updating the custom bounds
			if self.anim:
				# An identically keyed atlas file is assumed.
				self.curr_key = self.current_image
				aniupdate_bounds(True, pos, radians(angle), self.origin, self.rid, self.curr_key)
				return None

			if motion or angle_diff:
				update_bounds(motion, radians(angle_diff), self.origin, self.rid, self.curr_key)
	

	def collide_point(self, x=0, y=0):
		if self.allow_rotabox:
			return point_in_bounds(x, y, self.rid, frame=self.curr_key)
		else:
			return super().collide_point(x, y)

	def collide_widget(self, wid):
		try:
			try:
				return collide_bounds(self.rid, wid.rid, frame=self.curr_key, tframe=wid.curr_key)
			except AttributeError:
				if self.segment_mode:
					return collide_bounds(self.rid, [wid.x, wid.y, wid.right, wid.top], frame=self.curr_key)
				return super().collide_widget(wid)
		except KeyError:
			return False

	def on_touch_down(self, touch):
		x, y = touch.x, touch.y

		# if the touch isnt on the widget we do nothing
		if not self.collide_after_children:
			if not self.collide_point(x, y):
				return False

		# let the child widgets handle the event if they want
		if super().on_touch_down(touch):
			# ensure children don't have to do it themselves
			if 'multitouch_sim' in touch.profile:
				touch.multitouch_sim = True
			
			self.bring_to_front(touch)
			return True

		# if we don't have any active
		# interaction control, then don't accept the touch.
		if not (self.allow_drag_x
				or self.allow_drag_y
				or self.multi_touch_rotation
				or self.multi_touch_scaling
				or self.single_touch_rotation
				or self.single_touch_scaling):
			return False

		if self.collide_after_children:
			if not self.collide_point(x, y):
				return False

		if 'multitouch_sim' in touch.profile:
			touch.multitouch_sim = True

		# grab the touch so we get all it later move events for sure
		self.bring_to_front(touch)
		touch.grab(self)
		self.touches.append(touch)
		self.last_touch_pos[touch] = x, y
		return True

	def bring_to_front(self, touch):
		if self.touched_to_front and self.parent:
			parent = self.parent
			if parent.children[0] is self:
				return None
			
			parent.remove_widget(self)
			parent.add_widget(self)
			self.dispatch('on_touched_to_front', touch)

	def on_touch_move(self, touch):
		x, y = touch.x, touch.y

		# let the child widgets handle the event if they want
		if self.collide_point(x, y) and not touch.grab_current == self:
			if super().on_touch_move(touch):
				return True

		if touch in self.touches and touch.grab_current == self:
			if self.transform_with_touch(touch):
				self.dispatch('on_transform_with_touch', touch)
			self.last_touch_pos[touch] = x, y

		if self.collide_point(x, y):
			return True

	def transform_with_touch(self, touch):
		changed = False
		touches = len(self.touches)

		if (touches == self.single_drag_touch and (self.allow_drag_x or self.allow_drag_y)):
			dx = (touch.x - self.last_touch_pos[touch][0]) * self.allow_drag_x
			dy = (touch.y - self.last_touch_pos[touch][1]) * self.allow_drag_y
			
			self.x += float(dx) / self.single_drag_touch
			self.y += float(dy) / self.single_drag_touch
			changed = True

		if (touches == self.single_trans_touch and (self.single_touch_rotation or self.single_touch_scaling)):
			anchor = self.pivot
			old_line = Vector(*touch.ppos) - anchor
			new_line = Vector(*touch.pos) - anchor
			if not old_line.length():
				return changed
			
			if self.single_touch_rotation:
				angle = new_line.angle(old_line)
				self.angle += angle

			if self.single_touch_scaling:
				_scale = new_line.length() / old_line.length()
				self.scale *= _scale
			
			changed = True

		if touches == 1:
			return changed

		# we have more than one touch... list of last known pos
		points = [Vector(self.last_touch_pos[t]) for t in self.touches if t is not touch]
		points.append(Vector(touch.pos))

		# we only want to transform if the touch is part of the two touches
		# farthest apart! So first we find anchor, the point to transform
		# around as another touch farthest away from current touch's pos
		anchor = max(points[:-1], key=lambda p: p.distance(touch.pos))

		self.origin = anchor

		# now we find the touch farthest away from anchor, if its not the
		# same as touch. Touch is not one of the two touches used to transform
		farthest = max(points, key=anchor.distance)
		if farthest is not points[-1]:
			return changed

		# ok, so we have touch, and anchor, so we can actually compute the transformation
		old_line = Vector(*touch.ppos) - anchor
		new_line = Vector(*touch.pos) - anchor
		if not old_line.length():
			return changed

		angle = new_line.angle(old_line) * self.multi_touch_rotation
		self.angle += angle

		if self.multi_touch_scaling:
			_scale = new_line.length() / old_line.length()
			self.scale *= _scale
			changed = True
		
		return changed

	def on_touch_up(self, touch):
		# if the touch isnt on the widget we do nothing, just try children
		if not touch.grab_current == self:
			if super().on_touch_up(touch):
				return True

		# remove it from our saved touches
		if touch in self.touches and touch.grab_state:
			touch.ungrab(self)
			del self.last_touch_pos[touch]
			self.touches.remove(touch)

		# stop propagating if its within our bounds
		if self.collide_point(*touch.pos):
			return True

	def set_draw(self, *args):
		'''Setting up canvas for test-drawing the bounds.'''
		self.reset_draw_bounds()
		
		if self.anim:
			pols = max([len(frame) for frame in self.custom_bounds.values()])
			
			length = max([len(pol) for pol in self.custom_bounds.values()])
		else:
			pols = len(self.custom_bounds)
			length = peers[self.rid][self.curr_key]['length']

		for i in range(pols):
			if i not in self.open_bounds or not self.segment_mode:
				self.draw_lines.append(Line(close=True, dash_offset=3, dash_length=5))
			else:
				self.draw_lines.append(Line(close=False, dash_offset=3, dash_length=5))

		self.canvas.after.add(self.draw_color)
		for line in self.draw_lines:
			self.canvas.after.add(line)

		# Securing draw on a stationary widget.
		self.x += 0.001
		self.trigger_draw()

	def draw(self, *args):
		''' If [draw_bounds] is True, visualises the widget's bounds. For testing.
		''' 
		if not self.prepared:
			return None
		
		try:
			bounds = peers[self.rid][self.curr_key]
		except KeyError:
			return None

		start = 0
		for i, leng in enumerate(bounds['pol_lens']):
			self.draw_lines[i].points = [bounds['points'][j] for j in range(start, start + leng * 2)]
			start += leng * 2


	def get_size_hint_x(self):
		# Locking size_hint property to None, None,
		# in order to keep intended aspect ratio (critical for custom bounds).
		return None

	def set_size_hint_x(self, value):
		raise Exception("Rotabox can't use size_hint.")
	
	size_hint_x = AliasProperty(get_size_hint_x, set_size_hint_x)


	def get_size_hint_y(self):
		return None

	def set_size_hint_y(self, value):
		raise Exception("Rotabox can't use size_hint.")

	size_hint_y = AliasProperty(get_size_hint_y, set_size_hint_y)
	size_hint = ReferenceListProperty(size_hint_x, size_hint_y)


	original_size = ListProperty([1, 1])
	"""
	Used for calculating the widget's scale. It's the user's input size
	or the [texture_size] of the widget's [image].
	"""

	pivot_bond = ListProperty([.5, .5])
	"""
	A fractional value that keeps [pivot] relative to the widget's size
	and position. [origin] sets and changes it.
	"""

	allow = BooleanProperty(1)
	""" Switch to suspend bounds' update while repositioning, during an [origin] change or a resize.
	"""
