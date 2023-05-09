
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Line, Rectangle, Color, Ellipse
from kivy.properties import (
	OptionProperty, BoundedNumericProperty,
	ColorProperty, NumericProperty,
	ObjectProperty, AliasProperty,
	ListProperty, StringProperty,
	BooleanProperty
)

from kivy.metrics import dp
from kivy.lang.builder import Builder
from math import ceil


Builder.load_string("""

<CircularProgressBar>:
	anchor_x: "center"
	anchor_y: "center"
	Widget:
		id: circular_widget
		size_hint: None, None
		size: [root.widget_size] * 2

""")


class CircularProgressBar(AnchorLayout):

	started  = BooleanProperty(False)

	# This constant enforces the cap argument to be one of the caps accepted by the kivy.graphics.Line class
	cap_style = OptionProperty("round", options=["round", "none", "square"])
	""" cap / edge of the bar, check the cap keyword argument in kivy.graphics.Line
	"""

	border_width = BoundedNumericProperty(dp(10), min=dp(1))
	""" border_width of the progress bar line (positive integer)
	"""

	cap_precision = BoundedNumericProperty(10, min=1)
	""" bar car sharpness, check the cap_precision keyword argument in kivy.graphics.Line
	"""

	widget_size = BoundedNumericProperty(dp(200), min=dp(1))
	""" size of the widget, use this to avoid issues with size, width, height etc.
	"""

	progress_color = ColorProperty([1, 0, 0, 1])
	""" Colour progress of the progress bar, check values accepted by kivy.graphics.Color
	"""

	progress_background = ColorProperty([0.26, 0.26, 0.26, 1])
	""" Colour progress of the background bar, check values accepted by kivy.graphics.Color
	"""

	background_color = ColorProperty("#d4c9d0")
	"""
	"""

	_progress = NumericProperty(0)

	def _get_progress(self):
		return self._progress

	def _set_progress(self, progress):
		if progress < 0:
			self._progress = self.min_progress

		elif progress > self.max_progress:
			self._progress = self.max_progress
			# raise ValueError(f"Progress must be between minimum ({self.min_progress}) and maximum ({self.max_progress}), not {self._progress}!")
		else:
			self._progress = progress

	progress = AliasProperty(_get_progress, _set_progress, bind=["_progress"])
	""" progress progress, can you use it initialise the bar to some other progress different from the minimum
	"""

	# Declare the defaults for the normalisation function, these are used in the textual representation (multiplied by 100)
	normalised_max = NumericProperty(1)
	normalised_min = NumericProperty(0)

	max_progress = NumericProperty(100)
	""" maximum progress (progress corresponding to 100%)
	"""

	min_progress = NumericProperty(0)
	""" minimum progress (progress corresponding to 0%) - note that this sets the starting progress to this progress
	"""

	label = ObjectProperty(None)
	"""
		kivy.graphics.Label textually representing the progress - pass a label with an empty text field to remove it,
		use "{}" as the progress progress placeholder (it will be replaced via the format function)
	"""

	label_size = ListProperty([0, 0])
	label_args = ListProperty([])

	label_text = StringProperty("")
	label_color = ColorProperty([0.1, 0.4, 0, 1])

	def get_normalised_progress(self):
		"""
		Function used to normalise the progress using the MIN/MAX normalisation

		:return: Current progress normalised to match the percentage constants
		"""
		dif1 = (self.normalised_max - self.normalised_min)
		dif2 = (self.max_progress - self.min_progress)
		return self.normalised_min + ((self._progress - self.min_progress) * (dif1 / dif2))

	def set_normalised_progress(self, norm_progress):
		"""
		Function used to set the progress progress from a normalised progress, using MIN/MAX normalisation

		:param norm_progress: Normalised progress to update the progress with
		"""
		if not isinstance(norm_progress, (float, int)):
			raise TypeError("Normalised progress must be a float or an integer, not {}!".format(
				type(norm_progress)))

		# if norm_progress < self.normalised_min or norm_progress > self.normalised_max:
		# 	return None

		dif1 = (self.max_progress - self.min_progress)
		dif2 = (self.normalised_max - self.normalised_min)
		self._progress = ceil(
			self.min_progress + (norm_progress - self.normalised_min) * dif1 / dif2)

	value_normalized = AliasProperty(
		get_normalised_progress, set_normalised_progress, bind=["_progress"])

	def on_label(self, *args):
		if not self.label_text:
			self.label_text = self.label.text

	def __init__(self, **kwargs):

		self.label = Label(text="Circular Bar", font_size=19, bold=True)
		self._progress = self.min_progress
		super().__init__(**kwargs)

		self.bind(label=self._draw)
		self.bind(progress_background=self._draw)
		self.bind(background_color=self._draw)
		self.bind(border_width=self._draw)
		self.bind(cap_style=self._draw)
		self.bind(label_text=self._draw)
		self.bind(label_size=self._draw)
		self.bind(_progress=self._draw)
		self.bind(label_color=self._draw)

		Clock.schedule_once(self.start)

	def on_kv_post(self, *args):
		self.ids.circular_widget.bind(size=self.start)
	
	def start(self, *args):
		if self.get_root_window() != None:
			self.ids.circular_widget.unbind(size=self.start)
			if not self.started:
				Clock.schedule_once(self.start)
				self.started = True
				return None
		else:
			return None
	
		self._draw()


	def on_max_progress(self, *args):
		if self.max_progress <= self.min_progress:
			raise ValueError(
				f"Maximum progress - {self.max_progress} - must be greater than minimum progress ({self.min_progress})!")

		if self._progress > self.max_progress:
			self._progress = self.max_progress

	def on_min_progress(self, *args):
		if self.min_progress > self.max_progress:
			raise ValueError(
				f"Minimum progress - {self.min_progress} - must be smaller than maximum progress ({self.max_progress})!")

		if self._progress < self.min_progress:
			self._progress = self.min_progress

	def _refresh_text(self, *args):
		"""
		Function used to refresh the text of the progress label.

		Additionally updates the variable tracking the label's texture size
		"""
		self.label.color = self.label_color

		if self.label_args:
			self.label.text = self.label_text.format(*self.label_args)
		else:
			self.label.text = self.label_text

		self.label_size = self.label.texture_size

	def _draw(self, *args):
		"""
		Function used to draw the progress bar onto the screen.

		The drawing process is as follows:

				1. Clear the canvas
				2. Draw the background_color progress line (360 degrees)
				3. Draw the actual progress line (N degrees where n is between 0 and 360)
				4. Draw the textual representation of progress in the middle of the circle
		"""
		wid = self.ids.circular_widget

		with wid.canvas:
			wid.canvas.clear()
			self._refresh_text()

			# Draw the progress line
			Color(*self.background_color)
			Ellipse(pos=list(map(lambda v: (v + self.border_width), wid.pos)),
					size=list(map(lambda v: (v - (self.border_width * 2)), wid.size)))

			# Draw the background progress line
			Color(*self.progress_background)
			Line(ellipse=(*wid.pos, *wid.size), width=self.border_width)

			# Draw the progress line
			Color(*self.progress_color)
			Line(ellipse=(*wid.pos, *wid.size, 0, self.value_normalized * 360),
				 width=self.border_width, cap=self.cap_style, cap_precision=self.cap_precision)

			# Center and draw the progress text
			Color(1, 1, 1, 1)
			Rectangle(texture=self.label.texture, size=self.label_size,
					  pos=(wid.center_x - (self.label_size[0] / 2),
						   wid.center_y - (self.label_size[1] / 2)))
