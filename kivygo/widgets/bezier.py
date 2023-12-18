
from kivy.lang import Builder
from kivygo.widgets.widget import GoWidget
from kivy.properties import ListProperty, NumericProperty
from kivy.metrics import dp
import numpy as np

from kivy.graphics import Canvas, RenderContext, Color, Rectangle, Color, Line


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


GLOW_LINE_SHADER = '''
$HEADER$

/*uniform float brightness;
uniform vec4 points;
*/
uniform vec2 resolution;
uniform vec2 startPos;
uniform vec2 endPos;
uniform float brightnessFactor;
uniform float th;
uniform vec4 color;

void main(){
	/*variables for the main shader stuff*/
	vec2 center = (startPos+endPos)/2.0;
	float alpha = -atan((startPos - center).y/(startPos - center).x);
	float l = distance(startPos, endPos);
	float factor = brightnessFactor;
	/**/
	float x = gl_FragCoord.x;
	float y = gl_FragCoord.y;
	
	float dx = x - center.x; float dy = y - center.y;
	l+=factor;
	for(float i =th+factor; i>= th; i -= 1.){
		float c = i;
		float b = 0.;//height/2.0 - c;
		float a = (l-1.)/2.0 - c/1.7;
		float leftOp = pow(max(abs(dx*cos(alpha) - dy*sin(alpha)) - a/1.1, 0.), 2.);
		float rightOp = pow(max(abs(dx*sin(alpha)+dy*cos(alpha)) - b, 0.), 2.4);
		if (leftOp + rightOp <= c*c){
			vec3 fr = (color*texture2D(texture0, tex_coord0)).rgb;
			gl_FragColor = vec4(
				fr,
				1.0 -(i-th)/factor);
		}
	}
}
'''

class GlowingLine(Canvas):
	def __init__(self, glowBrightness=30, width=2, **kws):
		#:keyword argument width is the main width(thickness) of the line.
		#:keyword argument is the brightness factor of the glow. Adjust to suit your needs
		super().__init__(**kws)
		
		self.glowBrightness = glowBrightness
		self.mode = kws.get("mode", "rgba")
		##:keyword argument 'mode' here is supplied to the Color instruction which is applied to the glowing line.
		#for instance, Color(..., mode="rgba")
		with self:
			self.rc = RenderContext(use_parent_projection=True, use_parent_modelview = True)
			self.rc.shader.fs = GLOW_LINE_SHADER
		with self.rc:
			self.color = kws.get('color',  [1,1,0,1])
			self.color_inst = Color(*self.color, mode=self.mode)
			self._points = kws.get('points', [0,0, 100,100])
			self._points = list(map(float,self._points[:4]))
			self.rect = Rectangle(size=[1000,1000])
		Color(*self.color, mode=self.mode)
		line = Line(points = self._points, width=width)
		self.line = line
		self.update_glsl()
		
	@property
	def points(self):
		return self.line.points
	@points.setter
	def points(self, val):
		self.line.points = list(map(float,self.points[:4]))
		self.update_glsl()
		
	def update_glsl(self):
		self.rc['resolution'] = self.rect.size
		self.rc['startPos'] = self.points[:2]
		self.rc['endPos'] = self.points[2:]
		self.rc['brightnessFactor'] = float(self.glowBrightness)
		self.rc['th'] = float(self.line.width)
		self.rc['color'] = list(map(float,self.color))

