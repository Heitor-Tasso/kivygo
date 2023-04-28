

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivygo.uix.image import ImageWithSVG

from kivy.properties import (
	ColorProperty, ListProperty, 
	NumericProperty, StringProperty,
	ObjectProperty
)
from kivy.metrics import dp
from kivy.core.window import Window


Builder.load_string("""


<ResizableRectangleBord>:
	size_hint: None, None
	size: '8dp', '8dp'
	radius: [sum(self.size)/2] * 4
	mipmap: True
	allow_strech: True
	keep_ratio: False
	
	canvas:
		Clear
		Color:
			rgba: [0]*4 if self.image_source else root.line_color
		RoundedRectangle:
			pos: [ ( self.x - self.outline_width ), ( self.y - self.outline_width ) ]
			size: [ ( self.width + (self.outline_width*2) ), ( self.height + (self.outline_width*2) ) ]
			radius: root.radius
		Color:
			rgba: [0]*4 if self.image_source else root.background_color
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: root.radius

	canvas.after:
		Color:
			rgba: self.color if self.image_source else [0]*4
		Rectangle:
			texture: self.texture
			pos: self.pos
			size: self.size


<ResizableLineBord>:
	canvas:
		Color:
			rgba: self.color
		Line:
			width: dp(1)
			points: self.points


<ResizeSelectBehavior>:
	ResizableLineBord: # TOP LINE
		id: top_line
		color: root._top_line_color
		points: [top_left_rect.right, root.top, top_right_rect.x, root.top]

	ResizableLineBord: # BOTTOM LINE
		id: bottom_line
		color: root._bottom_line_color
		points: [bottom_left_rect.right, root.y, bottom_right_rect.x, root.y]

	ResizableLineBord: # LEFT LINE
		id: left_line
		color: root._left_line_color
		points: [root.x, top_left_rect.y, root.x, bottom_left_rect.top]
	
	ResizableLineBord: # RIGHT LINE
		id: right_line
		color: root._right_line_color
		points: [root.right, top_right_rect.y, root.right, bottom_right_rect.y]

	
	ResizableRectangleBord: # TOP LEFT RECTANGLE
		id: top_left_rect
		x: self.parent.x - (self.width/2)
		y: self.parent.top - (self.height/2)
		background_color: root._bord_background_color
		line_color: root._bord_line_color
		image_source: root.bord_icon_source
		size: root.bord_size
		
	ResizableRectangleBord: # BOTTOM LEFT RECTANGLE
		id: bottom_left_rect
		x: self.parent.x-(self.width/2)
		y: self.parent.y-(self.height/2)
		background_color: root._bord_background_color
		line_color: root._bord_line_color
		image_source: root.bord_icon_source
		size: root.bord_size
	
	ResizableRectangleBord: # BOTTOM RIGHT RECTANGLE
		id: bottom_right_rect
		x: self.parent.right-(self.width/2)
		y: self.parent.y-(self.height/2)
		background_color: root._bord_background_color
		line_color: root._bord_line_color
		image_source: root.bord_icon_source
		size: root.bord_size
	
	ResizableRectangleBord:  # TOP RIGHT RECTANGLE
		id: top_right_rect
		x: self.parent.right - (self.width/2)
		y: self.parent.top - (self.height/2)
		background_color: root._bord_background_color
		line_color: root._bord_line_color
		image_source: root.bord_icon_source
		size: root.bord_size

	ResizableRectangleBord:  # TOP CENTER RECTANGLE
		id: top_center_rect
		x: self.parent.x + (self.parent.width/2) - (self.width/2)
		y: self.parent.top - (self.height/2)
		background_color: root._bord_background_color
		line_color: root._bord_line_color
		image_source: root.bord_icon_source
		size: root.bord_size
	
	ResizableRectangleBord:  # LEFT CENTER RECTANGLE
		id: left_center_rect
		x: self.parent.x - (self.width/2)
		y: self.parent.y + (self.parent.height/2) - (self.height/2)
		background_color: root._bord_background_color
		line_color: root._bord_line_color
		image_source: root.bord_icon_source
		size: root.bord_size

	ResizableRectangleBord:  # RIGHT CENTER RECTANGLE
		id: right_center_rect
		x: self.parent.right - (self.width/2)
		y: self.parent.y + (self.parent.height/2) - (self.height/2)
		background_color: root._bord_background_color
		line_color: root._bord_line_color
		image_source: root.bord_icon_source
		size: root.bord_size

	ResizableRectangleBord:  # BOTTOM CENTER RECTANGLE
		id: bottom_center_rect
		x: self.parent.x + (self.parent.width/2) - (self.width/2)
		y: self.parent.y - (self.height/2)
		background_color: root._bord_background_color
		line_color: root._bord_line_color
		image_source: root.bord_icon_source
		size: root.bord_size

""")


class ResizableRectangleBord(ImageWithSVG):
	outline_width = NumericProperty(dp(2))
	radius = ListProperty([0, 0, 0, 0])
	background_color = ColorProperty("#FFFFFF")
	line_color = ColorProperty("#25d2a2")


class ResizableLineBord(Widget):
	color = ColorProperty("red")
	points = ListProperty([0, 0])


class ResizeSelectBehavior(Widget):

	top_line_color = ColorProperty("#25d2a2")
	bottom_line_color = ColorProperty("#25d2a2")
	left_line_color = ColorProperty("#25d2a2")
	right_line_color = ColorProperty("#25d2a2")

	_top_line_color = ColorProperty("#25d2a2")
	_bottom_line_color = ColorProperty("#25d2a2")
	_left_line_color = ColorProperty("#25d2a2")
	_right_line_color = ColorProperty("#25d2a2")
	
	_bord_background_color = ColorProperty("#FFFFFF")
	_bord_line_color = ColorProperty("#25d2a2")

	bord_background_color = ColorProperty("#FFFFFF")
	bord_line_color = ColorProperty("#25d2a2")
	bord_icon_source = StringProperty("")
	bord_size = ListProperty([dp(8), dp(8)])
	line_color = ColorProperty([0, 0, 0, 0])
	line_highlight_color = ColorProperty("#12715e")

	last_touch_pos = (0, 0)

	__resizes = []
	_last_parent = ObjectProperty(None)
	change_pos_varible = StringProperty("pos")
	moved = 0
	touched = 0
	_in_resize = False


	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.selected_side = None

		if not ResizeSelectBehavior.__resizes:
			Window.bind(mouse_pos=self.on_mouse_pos)
		ResizeSelectBehavior.__resizes.append(self)

		self.bind(
			on_top_line_color=self._set_default_colors,
			on_bottom_line_color=self._set_default_colors,
			on_left_line_color=self._set_default_colors,
			on_right_line_color=self._set_default_colors,

			on_bord_background_color=self._set_default_colors,
			on_bord_line_color=self._set_default_colors
		)
		self._set_default_colors()
	
	def on_parent(self, *args):
		if self.parent != None:
			self._last_parent = self.parent
		
		if self.parent == None and ResizeSelectBehavior.__resizes:
			if ResizeSelectBehavior.__resizes[0] is self:
				Window.unbind(mouse_pos=self.on_mouse_pos)
				del ResizeSelectBehavior.__resizes[0]
				
				if ResizeSelectBehavior.__resizes:
					Window.bind(mouse_pos=ResizeSelectBehavior.__resizes[0].on_mouse_pos)
			else:
				ResizeSelectBehavior.__resizes.remove(self)


	def _set_default_colors(self, *args):
		if self._in_resize:
			self._top_line_color = self.top_line_color
			self._bottom_line_color = self.bottom_line_color
			self._left_line_color = self.left_line_color
			self._right_line_color = self.right_line_color

			self._bord_background_color = self.bord_background_color
			self._bord_line_color = self.bord_line_color
		else:
			self._top_line_color = [0, 0, 0, 0]
			self._bottom_line_color = [0, 0, 0, 0]
			self._left_line_color = [0, 0, 0, 0]
			self._right_line_color = [0, 0, 0, 0]
			self._bord_background_color = [0, 0, 0, 0]
			self._bord_line_color = [0, 0, 0, 0]


	def on_line_color(self, *args):
		self.top_line_color = self.line_color
		self.bottom_line_color = self.line_color
		self.left_line_color = self.line_color
		self.right_line_color = self.line_color

	def on_mouse_pos(self, window, touch):
		"""
		When the mouse moves, we check the position of the mouse
		and update the cursor accordingly.
		"""
		for wid in ResizeSelectBehavior.__resizes:
			if wid.collide_point(*wid.to_widget(*touch)):
				collision = wid.collides_with_control_points(wid.to_widget(*touch))
				if collision in ["top left", "bottom right"]:
					Window.set_system_cursor("size_nwse")
				elif collision in ["top right", "bottom left"]:
					Window.set_system_cursor("size_nesw")
				elif collision in ["top", "bottom"]:
					Window.set_system_cursor("size_ns")
				elif collision in ["left", "right"]:
					Window.set_system_cursor("size_we")
				else:
					Window.set_system_cursor("size_all")
				return True
		
		Window.set_system_cursor("arrow")

	def collides_with_control_points(self, touch_pos):
		"""
		Returns True if the mouse is over a control point.
		"""
		x, y = touch_pos

		# Checking mouse is on left edge
		if self.x <= x <= self.x + dp(7):

			if self.y <= y <= self.y + dp(7):

				return "bottom left"
			
			elif self.y + dp(7) <= y <= self.y + self.height - dp(7):

				return "left"
			
			else:
				return "top left"

		# Checking mouse is on top edge
		elif self.x + dp(7) <= x <= self.x + self.width - dp(7):

			if self.y <= y <= self.y + dp(7):

				return "bottom"
			
			elif self.y + self.height - dp(7) <= y <= self.y + self.height:

				return "top"
			
			else:
				return False

		# Checking mouse is on right edge
		elif self.x + self.width - dp(7) <= x <= self.x + self.width:

			if self.y <= y <= self.y + dp(7):

				return "bottom right"
			
			elif self.y + dp(7) <= y <= self.y + self.height - dp(7):

				return "right"
			
			else:
				return "top right"

	def on_touch_down(self, touch):
		if not self.collide_point(*touch.pos):
			return False

		print("TOUCH_DOUBLE -=> ", touch.is_double_tap, self.touched)
		
		self.touched += 1
		# if touch.is_double_tap:
		# 	self.touched = 0
		print("TOQUE -=> ", self.touched)

		if self.touched == 2 and self.moved == -1:
			self._in_resize = False
			self._set_default_colors()
			# self.moved = 2
			return True
		
		if self.touched == 5 and self.moved == -1:
			self._in_resize = True
			self._set_default_colors()
			self.moved = 1
			return True

		if self.touched == 1 or touch.is_double_tap:
			self._in_resize = True
			self._set_default_colors()

			if touch.is_double_tap:
				self.moved = 1
			
			return True

		if self.touched > 2:
			if self.touched in [3, 4, 5]:
				self._in_resize = False
				self._set_default_colors()
				return super().on_touch_down(touch)
			
			return True

		self.moved = 0	
		touch.grab(self)
		self.last_touch_pos = touch.pos
		collision = self.collides_with_control_points(touch.pos)
		selected_side = collision

		if collision == "top":
			self._top_line_color = self.line_highlight_color

		elif collision == "bottom":
			self._bottom_line_color = self.line_highlight_color

		elif collision == "left":
			self._left_line_color = self.line_highlight_color

		elif collision == "right":
			self._right_line_color = self.line_highlight_color

		else:
			if collision not in ["bottom right", "bottom left"]:
				self._top_line_color = self.line_highlight_color
				
			if collision not in ["top right", "top left"]:
				self._bottom_line_color = self.line_highlight_color

			if collision not in ["bottom right", "top right"]:
				self._left_line_color = self.line_highlight_color
			
			if collision not in ["bottom left", "top left"]:
				self._right_line_color = self.line_highlight_color

			if collision not in ["top left", "bottom right", "top right", "bottom left"]:
				selected_side = None
		
		self.selected_side = selected_side
		return True
		
	def on_touch_move(self, touch):
		if self.parent == None:
			return None

		if self.touched in [3, 4, 5]:
			self.moved = 2
			return super().on_touch_move(touch)
		
		self.moved = 1
		lx, ly = self.last_touch_pos
		dx = (touch.x - lx)
		dy = (touch.y - ly)

		lpx, lpy = getattr(self, self.change_pos_varible)
		set_pos = lambda x, y: setattr(self, self.change_pos_varible, [x, y])

		if touch.grab_current is self:
			self.last_touch_pos = touch.pos

			if self.selected_side == "top":
				self.height += dy

			elif self.selected_side == "bottom":
				self.height -= dy
				set_pos(lpx, lpy+dy)

			elif self.selected_side == "left":
				self.width -= dx
				set_pos(lpx+dx, lpy)

			elif self.selected_side == "right":
				self.width += dx

			elif self.selected_side == "top left":
				self.width -= dx
				set_pos(lpx+dx, lpy)
				self.height += dy

			elif self.selected_side == "top right":
				self.width += dx
				self.height += dy

			elif self.selected_side == "bottom left":
				self.width -= dx  # OK
				self.height -= dy
				set_pos(lpx+dx, lpy+dy)

			elif self.selected_side == "bottom right":
				self.width += dx
				self.height -= dy
				set_pos(lpx, lpy+dy)

			elif not self.selected_side:
				# Moving
				set_pos(lpx+dx, lpy+dy)
		
		return True

	def on_touch_up(self, touch):
		if self.moved == 1:
			self.touched = 1

		elif self.moved == 2:
			self.touched = 2

		else:
			self.moved = -1
		# 	self.touched = 1

		
		if self.touched in [3, 4, 5]:
			return super().on_touch_up(touch)

		if touch.grab_current is self:
			touch.ungrab(self)
			self._top_line_color = self.top_line_color
			self._bottom_line_color = self.bottom_line_color
			self._left_line_color = self.left_line_color
			self._right_line_color = self.right_line_color
		
		return True

