
from kivy.properties import (
	ObjectProperty, NumericProperty,
	StringProperty, ListProperty,
	BooleanProperty, ColorProperty
)

from kivy.graphics import (
	Fbo, ClearBuffers, ClearColor,
	Scale, Translate
)

from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock


Builder.load_string("""

<SpacerWidget>:
	size_hint: [None, None]
	size: [0, 0]
	canvas:
		Color:
			rgba: self.outline_color
		Line:
			rectangle: [*self.pos, *self.size]
			width: root.outline_width

<PreviewWidget>:
	size_hint: [None, None]
	size: [0, 0]
	canvas:
		Color:
			rgba: self.outline_color
		Line:
			rectangle: [\
				self.to_window(self.x, 0)[0] - root.outline_width, \
				self.to_window(0, self.y)[1] - root.outline_width, \
				self.width + (root.outline_width * 2), \
				self.height + (root.outline_width * 2)\
				]
			width: root.outline_width
		Color:
			rgba: self.background_color
		Rectangle:
			pos: self.pos
			size: self.size
			texture: self.texture

""")


class SpacerWidget(Widget):
	outline_width = NumericProperty(dp(2))
	outline_color = ColorProperty([1, 0, 0, 1])


class PreviewWidget(Widget):
	texture = ObjectProperty(None)
	outline_width = NumericProperty(dp(1.01))
	outline_color = ColorProperty([1, 0, 0, 1])
	background_color = ColorProperty([1, 1, 1, 1])


class DraggableObjectBehavior(Widget):

	drag_cls = StringProperty('')

	_drag_touch = None

	drag_distance = NumericProperty(dp(10))

	preview_widget = ObjectProperty(None)

	touch_dx = NumericProperty(0)
	touch_dy = NumericProperty(0)

	dragging = BooleanProperty(False)
 
	start_widget_pos = ListProperty([0, 0])


	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.start)
	
	def start(self, *args):
		if self.preview_widget == None:
			self.preview_widget = PreviewWidget()

	def _touch_uid(self):
		return '{}.{}'.format(self.__class__.__name__, self.uid)

	def on_touch_down(self, touch):
		uid = self._touch_uid()
		if uid in touch.ud:
			return touch.ud[uid]

		if super().on_touch_down(touch):
			touch.ud[uid] = False
			return True

		x, y = touch.pos
		if not self.collide_point(x, y):
			touch.ud[uid] = False
			return False

		if self._drag_touch or ('button' in touch.profile and
								touch.button.startswith('scroll')):
			touch.ud[uid] = False
			return False

		self._drag_touch = touch
		touch.grab(self)
		touch.ud[uid] = True

		return self.drag_down(touch)

	def on_touch_move(self, touch):
		uid = self._touch_uid()
		if uid not in touch.ud:
			touch.ud[uid] = False
			return super().on_touch_move(touch)

		if not touch.ud[uid]:
			return super().on_touch_move(touch)

		if touch.grab_current is not self:
			return False

		return self.drag_move(touch)

	def on_touch_up(self, touch):
		uid = self._touch_uid()
		if uid not in touch.ud:
			touch.ud[uid] = False
			return super().on_touch_up(touch)

		if not touch.ud[uid]:
			return super().on_touch_up(touch)

		if touch.grab_current is not self:
			return False

		touch.ungrab(self)
		self._drag_touch = None

		return self.drag_up(touch)

	def drag_down(self, touch):
		self.clean_dragging()
		self.prepare_preview_widget(touch)
		self.touch_dx = self.touch_dy = 0
		self.dragging = False
		self.preview_widget.canvas.opacity = 0
		
		Window.add_widget(self.preview_widget)
		self.start_widget_pos = self.to_window(*self.pos)
		self.preview_widget.pos = self.start_widget_pos
		return False

	def drag_move(self, touch):
		if not self.dragging:
			self.touch_dx += abs(touch.dx)
			self.touch_dy += abs(touch.dy)

			if (self.touch_dx ** 2 + self.touch_dy ** 2) ** 0.5 > self.drag_distance:
				self.dragging = True
				self.preview_widget.canvas.opacity = 0.4
				touch.ud['drag_cls'] = self.drag_cls
				touch.ud['drag_widget'] = self
				self.parent.remove_widget(self)
			else:
				return False

		x, y = self.start_widget_pos
		x += (touch.x - touch.ox)
		y += (touch.y - touch.oy)
		self.preview_widget.pos = [x, y]
		return False

	def drag_up(self, touch):
		self.clean_dragging()
		if not self.dragging:
			return False

		self.clean_dragging()
		self.dragging = False
		return False

	def prepare_preview_widget(self, touch):
		fbo = Fbo(size=self.size, with_stencilbuffer=True)
		with fbo:
			ClearColor(0, 0, 0, 0)
			ClearBuffers()
			Scale(1, -1, 1)
			Translate(-self.x, -self.y - self.height, 0)

		fbo.add(self.canvas)
		fbo.draw()
		fbo.texture.flip_vertical()

		self.preview_widget.size = self.size
		self.preview_widget.texture = fbo.texture

	def clean_dragging(self):
		"""Removes the drag widget preview.
		"""
		self.preview_pixels = None
		if self.preview_widget.parent:
			self.preview_widget.parent.remove_widget(self.preview_widget)


class DraggableLayoutBehavior(Widget):

	spacer_widget = ObjectProperty(None)

	drag_classes = ListProperty([])

	drag_append_end = BooleanProperty(False)

	def __init__(self, *args, **kwargs):
		self.spacer_widget = SpacerWidget()
		super().__init__(*args, **kwargs)

	def _touch_uid(self):
		return '{}.{}'.format(self.__class__.__name__, self.uid)

	def compare_pos_to_widget(self, widget, pos):
		return 'before'

	def get_widget_under_drag(self, x, y):
		for widget in self.children:
			if widget.collide_point(x, y):
				return widget
		
		return None

	def handle_drag_release(self, index, drag_widget, touch):
		self.add_widget(drag_widget, index)

	def get_drop_insertion_index_move(self, x, y):
		spacer = self.spacer_widget
		widget = self.get_widget_under_drag(x, y)

		if widget in (spacer, None):
			return None

		i = self.children.index(widget)
		j = None
		if self.compare_pos_to_widget(widget, (x, y)) == 'before':
			if i == len(self.children) - 1 or self.children[i + 1] != spacer:
				j = i + 1
		else:
			if not i or self.children[i - 1] != spacer:
				j = i
		return j

	def get_drop_insertion_index_up(self, x, y):
		spacer = self.spacer_widget
		widget = self.get_widget_under_drag(x, y)
		
		if widget == spacer:
			index = self.children.index(spacer)
		elif widget == None:
			index = 0
		else:
			if self.compare_pos_to_widget(widget, (x, y)) == 'before':
				index = self.children.index(widget) + 1
			else:
				index = self.children.index(widget)

		if spacer.parent:
			i = self.children.index(spacer)
			self.remove_widget(spacer)
			if i < index:
				index -= 1
		
		return index

	def on_touch_move(self, touch):
		spacer = self.spacer_widget
		preview_widget = touch.ud.get('drag_widget')
		if preview_widget != None:
			spacer.size = preview_widget.size

			pw = preview_widget.preview_widget
			spacer.outline_color = pw.outline_color
			spacer.outline_width = pw.outline_width
		
		x, y = touch.pos
		if touch.grab_current is not self:
			if not touch.ud.get(self._touch_uid()):
				# we haven't dealt with this before
				if self.collide_point(*touch.pos) and \
						touch.ud.get('drag_cls') in self.drag_classes:
					if super().on_touch_move(touch):
						return True
					touch.grab(self)
					touch.ud[self._touch_uid()] = True
				else:
					return super().on_touch_move(touch)
			else:
				# we have dealt with this touch before, do it when grab_current
				return True
		else:
			if touch.ud.get('drag_cls') not in self.drag_classes or \
					not self.collide_parent_tree(x, y):
				touch.ungrab(self)
				del touch.ud[self._touch_uid()]
				if spacer.parent:
					self.remove_widget(spacer)
				return False
			if super().on_touch_move(touch):
				touch.ungrab(self)
				del touch.ud[self._touch_uid()]
				if spacer.parent:
					self.remove_widget(spacer)
				return True

		if self.drag_append_end:
			if not spacer.parent:
				self.add_widget(spacer)
			return True

		j = self.get_drop_insertion_index_move(x, y)
		if j is not None:
			if spacer.parent:
				i = self.children.index(spacer)
				self.remove_widget(spacer)
				if i < j:
					j -= 1
			self.add_widget(spacer, index=j)
		
		return True

	def on_touch_up(self, touch):
		spacer = self.spacer_widget
		if touch.grab_current is not self:
			if not touch.ud.get(self._touch_uid()):
				# we haven't dealt with this before
				if self.collide_point(*touch.pos) and \
						touch.ud.get('drag_cls') in self.drag_classes:
					if super().on_touch_up(touch):
						return True
					x, y = touch.pos
				else:
					return super().on_touch_up(touch)
			else:
				# we have dealt with this touch before, do it when grab_current
				return True
		else:
			touch.ungrab(self)
			del touch.ud[self._touch_uid()]
			x, y = touch.pos
			if touch.ud.get('drag_cls') not in self.drag_classes or \
					not self.collide_parent_tree(x, y):
				if spacer.parent:
					self.remove_widget(spacer)
				return False
			if super().on_touch_up(touch):
				if spacer.parent:
					self.remove_widget(spacer)
				return True

		if self.drag_append_end:
			if spacer.parent:
				self.remove_widget(spacer)
			
			self.handle_drag_release(0, touch.ud['drag_widget'], touch)
			return True

		index = self.get_drop_insertion_index_up(x, y)
		self.handle_drag_release(index, touch.ud['drag_widget'], touch)
		return True
	
	def collide_parent_tree(self, x, y):
		"""Returns whether (x, y) collide with the widget and all its parents.
		"""
		if not self.collide_point(x, y):
			return False

		parent = self.parent
		while parent and hasattr(parent, 'to_parent'):
			x, y = parent.to_parent(x, y)  # transform to parent's parent's
			if not parent.collide_point(x, y):
				return False

			parent = parent.parent
		
		return True

