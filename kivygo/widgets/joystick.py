import math
from kivy.lang.builder import Builder
from kivygo.widgets.widget import GoWidget
from kivy.properties import (
	BooleanProperty, NumericProperty,
	ListProperty, ReferenceListProperty,
)

OUTLINE_ZERO = 0.00000000001
# replaces user's 0 value for outlines, avoids invalid width exception


Builder.load_string("""

<GoTouchData>:

<GoJoystickPad>:
	id: pad
	canvas:
		Color:
			rgba: self._background_color
		Ellipse:
			pos: (self.center_x - self._radius), (self.center_y - self._radius)
			size: (self._diameter, self._diameter)

		Color:
			rgba: self._line_color
		Line:
			circle: (self.center_x, self.center_y, (self._diameter - (self._line_width * 2)) / 2)
			width: self._line_width

			
<GoJoyStick>:
	canvas:
		Color:
			rgba: self.outer_background_color
		Ellipse:
			pos: (self.center_x - self._outer_radius), (self.center_y - self._outer_radius)
			size: (self._outer_diameter, self._outer_diameter)

		Color:
			rgba: self.outer_line_color
		Line:
			circle: (self.center_x, self.center_y, (self._outer_radius - (self._outer_line_width / 2)))
			width: self._outer_line_width

		Color:
			rgba: self.inner_background_color
		Ellipse:
			pos: (self.center_x - self._inner_radius), (self.center_y - self._inner_radius)
			size: (self._inner_diameter, self._inner_diameter)

		Color:
			rgba: self.inner_line_color
		Line:
			circle: (self.center_x, self.center_y, self._inner_radius)
			width: self._inner_line_width

	GoJoystickPad:
		id: pad


""")


class GoTouchData(GoWidget):
	x_distance = None
	y_distance = None
	x_offset = None
	y_offset = None
	relative_distance = None
	is_external = None
	in_range = None

	def __init__(self, joystick, touch):
		self.joystick = joystick
		self.touch = touch
		self._calculate()

	def _calculate(self):
		js = self.joystick
		touch = self.touch
		x_distance = js.center_x - touch.x
		y_distance = js.center_y - touch.y
		x_offset = touch.x - js.center_x
		y_offset = touch.y - js.center_y
		relative_distance = ((x_distance ** 2) + (y_distance ** 2)) ** 0.5
		is_external = relative_distance > js._total_radius
		in_range = relative_distance <= js._radius_difference
		self._update(x_distance, y_distance, x_offset, y_offset,
					 relative_distance, is_external, in_range)

	def _update(self, x_distance, y_distance, x_offset, y_offset,
				relative_distance, is_external, in_range):
		self.x_distance = x_distance
		self.y_distance = y_distance
		self.x_offset = x_offset
		self.y_offset = y_offset
		self.relative_distance = relative_distance
		self.is_external = is_external
		self.in_range = in_range


class GoJoystickPad(GoWidget):
	_diameter = NumericProperty(1)
	_radius = NumericProperty(1)
	_background_color = ListProperty([0, 0, 0, 1])
	_line_color = ListProperty([1, 1, 1, 1])
	_line_width = NumericProperty(1)


class GoJoystick(GoWidget):
	'''The joystick base is comprised of an outer circle & an inner circle.
	   The joystick pad is another circle,
		   which the user can move within the base.
	   All 3 of these elements can be styled independently
		   to create different effects.
	   All coordinate properties are based on the
		   position of the joystick pad.'''


	outer_size = NumericProperty(1)
	inner_size = NumericProperty(0.75)
	pad_size = NumericProperty(0.5)
	'''Sizes are defined by percentage,
		   1.0 being 100%, of the total widget size.
		The smallest value of widget.width & widget.height
		   is used as a baseline for these percentages.'''

	outer_background_color = ListProperty([0.75, 0.75, 0.75, 1])
	inner_background_color = ListProperty([0.75, 0.75, 0.75, 1])
	pad_background_color = ListProperty([0.4, 0.4, 0.4, 1])
	'''Background colors for the joystick base & pad'''

	outer_line_color = ListProperty([0.25, 0.25, 0.25, 1])
	inner_line_color = ListProperty([0.7, 0.7, 0.7, 1])
	pad_line_color = ListProperty([0.35, 0.35, 0.35, 1])
	'''Border colors for the joystick base & pad'''

	outer_line_width = NumericProperty(0.01)
	inner_line_width = NumericProperty(0.01)
	pad_line_width = NumericProperty(0.01)
	'''Outline widths for the joystick base & pad.
	   Outline widths are defined by percentage,
		   1.0 being 100%, of the total widget size.'''

	sticky = BooleanProperty(False)
	'''When False, the joystick will snap back to center on_touch_up.
	   When True, the joystick will maintain its final position
		   at the time of on_touch_up.'''


	pad_x = NumericProperty(0.0)
	pad_y = NumericProperty(0.0)
	pad = ReferenceListProperty(pad_x, pad_y)
	'''pad values are touch coordinates in relation to
		   the center of the joystick.
	   pad_x & pad_y return values between -1.0 & 1.0.
	   pad returns a tuple of pad_x & pad_y, and is the best property to
		   bind to in order to receive updates from the joystick.'''

	@property
	def magnitude(self):
		return self._magnitude
	'''distance of the pad, between 0.0 & 1.0,
		   from the center of the joystick.'''

	@property
	def radians(self):
		return self._radians
	'''degrees of the pad, between 0.0 & 360.0, in relation to the x-axis.'''

	@property
	def angle(self):
		return math.degrees(self.radians)
	'''position of the pad in radians, between 0.0 & 6.283,
		   in relation to the x-axis.'''

	'''magnitude, radians, & angle can be used to
		   calculate polar coordinates'''


	_outer_line_width = NumericProperty(OUTLINE_ZERO)
	_inner_line_width = NumericProperty(OUTLINE_ZERO)
	_pad_line_width = NumericProperty(OUTLINE_ZERO)

	_total_diameter = NumericProperty(0)
	_total_radius = NumericProperty(0)

	_inner_diameter = NumericProperty(0)
	_inner_radius = NumericProperty(0)

	_outer_diameter = NumericProperty(0)
	_outer_radius = NumericProperty(0)

	_magnitude = 0

	@property
	def _radians(self):
		if not (self.pad_y and self.pad_x):
			return 0
		arc_tangent = math.atan(self.pad_y / self.pad_x)
		if self.pad_x > 0 and self.pad_y > 0:    # 1st Quadrant
			return arc_tangent
		elif self.pad_x > 0 and self.pad_y < 0:  # 4th Quadrant
			return (math.pi * 2) + arc_tangent
		else:                                    # 2nd & 3rd Quadrants
			return math.pi + arc_tangent

	@property
	def _radius_difference(self):
		return (self._total_radius - self.ids.pad._radius)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.bind(
			pos=self.do_layout,
			size=self.do_layout,
			children=self.do_layout
		)

	def move_pad(self, touch, from_touch_down):
		td = GoTouchData(self, touch)
		if td.is_external and from_touch_down:
			touch.ud['joystick'] = None
			return False
		elif td.in_range:
			self._update_coordinates_from_internal_touch(touch, td)
			return True
		elif not (td.in_range):
			self._update_coordinates_from_external_touch(td)
			return True

	def center_pad(self):
		self.ids.pad.center = self.center
		self._magnitude = 0
		self.pad_x = 0
		self.pad_y = 0

	def _update_coordinates_from_external_touch(self, touchdata):
		td = touchdata
		pad_distance = self._radius_difference * (1.0 / td.relative_distance)
		x_distance_offset = -td.x_distance * pad_distance
		y_distance_offset = -td.y_distance * pad_distance
		x = self.center_x + x_distance_offset
		y = self.center_y + y_distance_offset
		radius_offset = pad_distance / self._radius_difference
		self.pad_x = td.x_offset * radius_offset
		self.pad_y = td.y_offset * radius_offset
		self._magnitude = 1.0
		self.ids.pad.center = (x, y)

	def _update_coordinates_from_internal_touch(self, touch, touchdata):
		td = touchdata
		self.pad_x = td.x_offset / self._radius_difference
		self.pad_y = td.y_offset / self._radius_difference
		self._magnitude = td.relative_distance / \
			(self._total_radius - self.ids.pad._radius)
		self.ids.pad.center = (touch.x, touch.y)
	

	def do_layout(self, *args):
		if 'pad' in self.ids:
			size = min(*self.size)
			self._update_outlines(size)
			self._update_circles(size)
			self._update_pad()

	def _update_outlines(self, size):
		self._outer_line_width = max(self.outer_line_width * size, OUTLINE_ZERO)
		self._inner_line_width = max(self.inner_line_width * size, OUTLINE_ZERO)
		self.ids.pad._line_width = max(self.pad_line_width * size, OUTLINE_ZERO)

	def _update_circles(self, size):
		self._total_diameter = size
		self._total_radius = self._total_diameter / 2
		self._outer_diameter = \
			(self._total_diameter - self._outer_line_width) * self.outer_size
		self._outer_radius = self._outer_diameter / 2
		self.ids.pad._diameter = self._total_diameter * self.pad_size
		self.ids.pad._radius = self.ids.pad._diameter / 2
		self._inner_diameter = \
			(self._total_diameter - self._inner_line_width) * self.inner_size
		self._inner_radius = self._inner_diameter / 2

	def _update_pad(self):
		self.ids.pad.center = self.center
		self.ids.pad._background_color = self.pad_background_color
		self.ids.pad._line_color = self.pad_line_color


	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y):
			touch.ud['joystick'] = self
			return self.move_pad(touch, from_touch_down=True)
		return super().on_touch_down(touch)

	def on_touch_move(self, touch):
		if self._touch_is_active(touch):
			return self.move_pad(touch, from_touch_down=False)
		return super().on_touch_move(touch)

	def on_touch_up(self, touch):
		if self._touch_is_active(touch) and not (self.sticky):
			self.center_pad()
			return True
		return super().on_touch_up(touch)

	def _touch_is_active(self, touch):
		return 'joystick' in touch.ud and touch.ud['joystick'] == self
