
from kivy.lang import Builder
from kivygo.widgets.widget import GoWidget
from kivy.properties import ListProperty, NumericProperty
from kivy.metrics import dp
import numpy as np


Builder.load_string('''

#:import chain itertools.chain


<GoBezierLine>:
	_points: list(chain(*self.points))

	canvas:
		Color:
			rgba: [1, 1, 1, 0.2]
		SmoothLine:
			points: self._points

		Color:
			rgba: [1, 1, 1, 1]
		Line:
			bezier: self._points
			width: 2

		Color:
			rgba: [1, 1, 1, 0.5]
		Point:
			points: self._points
			pointsize: 5

''')


def TwoPoints(t, P1, P2):
	"""
	Returns a point between P1 and P2, parametised by t.
	INPUTS:
		t     float/int; a parameterisation.
		P1    numpy array; a point.
		P2    numpy array; a point.
	OUTPUTS:
			numpy array; a point.
	"""

	if not isinstance(P1, np.ndarray) or not isinstance(P2, np.ndarray):
		raise TypeError("Points must be an instance of the numpy.ndarray!")
	
	if not isinstance(t, (int, float)):
		raise TypeError("Parameter t must be an int or float!")

	return ( (1 - t) * P1 + t * P2 )

def Points(t, points):
	"""
	Returns a list of points interpolated by the Bezier process
	INPUTS:
		t            float/int; a parameterisation.
		points       list of numpy arrays; points.
	OUTPUTS:
		newpoints    list of numpy arrays; points.
	"""

	newpoints = []
	for i1 in range(len(points) - 1):
		newpoints += [TwoPoints(t, points[i1], points[i1 + 1])]

	return newpoints

def Point(t, points):
	"""
	Returns a point interpolated by the Bezier process
	INPUTS:
		t            float/int; a parameterisation.
		points       list of numpy arrays; points.
	OUTPUTS:
		newpoint     numpy array; a point.
	"""

	newpoints = points
	while len(newpoints) > 1:
		newpoints = Points(t, newpoints)

	return newpoints[0]

def Curve(t_values, points):
	"""
	Returns a point interpolated by the Bezier process
	INPUTS:
		t_values     list of floats/ints; a parameterisation.
		points       list of numpy arrays; points.
	OUTPUTS:
		curve        list of numpy arrays; points.
	"""

	if not hasattr(t_values, "__iter__") \
		or not isinstance(t_values[0], (int, float)) \
		or len(t_values) < 1:
		
		raise TypeError("`t_values` Must be an iterable of integers or floats, of length greater than 0 .")
	
	
	curve = np.array([[0.0] * len(points[0])])
	for t in t_values:
		curve = np.append(curve, [Point(t, points)], axis=0)

	curve = np.delete(curve, 0, 0)
	return curve



def dist(a, b):
	return ( ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5 )


class GoBezierLine(GoWidget):

	_points = ListProperty([])
	points = ListProperty([])
	select_dist = NumericProperty(10)
	delete_dist = NumericProperty(5)

	def on_touch_down(self, touch):
		if super().on_touch_down(touch):
			return True

		max_dist = dp(self.select_dist)

		for i, p in enumerate(self.points):
			if dist(touch.pos, p) < max_dist:
				touch.ud['selected'] = i
				touch.grab(self)
				return True

		for i, p in enumerate(self.points[:-1]):
			index = (i + 1)
			new_dist = dist(touch.pos, p) + dist(touch.pos, self.points[index])
			new_dist -= dist(p, self.points[index])
			
			if (new_dist < max_dist):
				self.points = self.points[:index] + [list(touch.pos)] + self.points[index:]
				touch.ud['selected'] = index
				touch.grab(self)
				return True

	def on_touch_move(self, touch):
		if touch.grab_current is not self:
			return super().on_touch_move(touch)
		
		point = touch.ud['selected']
		self.points[point] = touch.pos

	def on_touch_up(self, touch):
		if touch.grab_current is not self:
			return super().on_touch_up(touch)
		
		touch.ungrab(self)
		i = touch.ud['selected']
		
		if touch.is_double_tap:
			if len(self.points) < 3:
				self.parent.remove_widget(self)
			elif i <= 0:
				self.points = self.points[i + 1::]
			else:
				self.points = self.points[::i] + self.points[i + 1::]


