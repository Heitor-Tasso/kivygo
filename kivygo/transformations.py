
from kivy.animation import AnimationTransition
from math import pi, cos, sin

class Transformations():

	@staticmethod
	def bouncey(points, alpha):
		x = AnimationTransition.out_elastic(alpha)
		x0, y0, x1, y1 = points
		h = (y1 - y0) * x  # tend to correct height, from 0
		w = (x1 - x0) * (2 - x)

		return [
			x0 + w * (1 - alpha * alpha), y0,
			(x0 + w * (1 - alpha * alpha) + w), y0,
			(x0 + w * (1 - alpha * alpha) + w), (y0 + h),
			x0 + w * (1 - alpha * alpha), (y0 + h)
		]

	@staticmethod
	def sky_down(points, alpha):
		x = AnimationTransition.out_quad(alpha)
		x0, y0, x1, y1 = points
		h = (y1 - y0) * (4 - 3 * x)  # tend to correct height, from 0
		w = (x1 - x0) * (x)
		cx = (x0 + x1) / 2

		return [
			(cx - w * 0.5), y0,
			(cx + w * 0.5), y0,
			(cx + w * 0.5), (y0 + h),
			(cx - w * 0.5), (y0 + h),
		]

	@staticmethod
	def pop_in(points, alpha):
		x = AnimationTransition.out_elastic(alpha)
		x0, y0, x1, y1 = points
		h = (y1 - y0) * x  # tend to correct height, from 0
		w = (x1 - x0) * x
		cx = (x0 + x1) / 2

		return [
			(cx - w * 0.5), y0,
			(cx + w * 0.5), y0,
			(cx + w * 0.5), (y0 + h),
			(cx - w * 0.5), (y0 + h),
		]

	@staticmethod
	def comes_and_go(points, alpha):
		x = AnimationTransition.in_out_quad(alpha)
		x0, y0, x1, y1 = points

		h = (y1 - y0) * (1 - 2 * abs(x - .5))
		center_y = (y0 + y1) / 2

		w = (x1 - x0) * (1 - 2 * abs(x - .5))
		center_x = (x0 + x1) / 2

		return [
			(center_x - w / 2), (center_y - h / 2),
			(center_x + w / 2), (center_y - h / 2),
			(center_x + w / 2), (center_y + h / 2),
			(center_x - w / 2), (center_y + h / 2)
		]

	@staticmethod
	def roll_in(points, alpha):
		x0, y0, x1, y1 = points
		x = AnimationTransition.out_quad(alpha)
		size = [ (x1 - x0), (y1 - y0) ]
		size_1 = [ (size[0] * x / 2), (size[1] * x / 2) ]

		cx = (x0 + x1) / 2 + size[1] * (1 - x)
		cy = (y0 + y1) / 2 - size[1] * 0.4 * (1 - x)
		a = (pi * x)
		pi4 = (pi / 4)

		return [
			(cx + cos(a + 1 * pi4) * size_1[0]), (cy + sin(a + 1 * pi4) * size_1[1]),
			(cx + cos(a + 3 * pi4) * size_1[0]), (cy + sin(a + 3 * pi4) * size_1[1]),
			(cx + cos(a + 5 * pi4) * size_1[0]), (cy + sin(a + 5 * pi4) * size_1[1]),
			(cx + cos(a + 7 * pi4) * size_1[0]), (cy + sin(a + 7 * pi4) * size_1[1]),
		]

