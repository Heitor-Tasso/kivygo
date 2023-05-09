"""
To use this class, you must define two methods for it:
:attr:`HoverBehavior.on_cursor_enter` and :attr:`HoverBehavior.on_cursor_leave`,
which will be automatically called when the mouse cursor is over the widget
and when the mouse cursor goes beyond the widget.

.. note::

	:class:`~HoverBehavior` will by default check to see if the current Widget is visible
	(i.e. not covered by a modal or popup and not a part of a Relative Layout, MDTab or Carousel
	that is not currently visible etc) and will only issue events if the widget is visible.

	To get the legacy behavior that the events are always triggered, you can set `detect_visible
	on the Widget to `False`.

"""
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import (
	BooleanProperty, ObjectProperty,
	ListProperty
)


class HoverBehavior(Widget):

	hovering = BooleanProperty(False)
	"""
	`True`, if the mouse cursor is within the borders of the widget.

	Note that this is set and cleared even if the widget is not visible
	"""

	hover_visible = BooleanProperty(False)
	"""
	`True` if hovering is True AND is the current widget is visible
	"""

	enter_point = ObjectProperty(allownone=True)
	"""
	Holds the last position where the mouse pointer crossed into the Widget
	if the Widget is visible and is currently in a hovering state
	"""

	detect_visible = BooleanProperty(True)
	"""
	Should this widget perform the visibility check?
	"""

	cursor_pos = ListProperty([0, 0])
	repeat_callback = BooleanProperty(False)

	_last_parent = ObjectProperty(None)
	__resizes = []


	def on_cursor_enter(self, *args):
		"""Called when mouse enters the bbox of the widget AND the widget is visible."""
		pass

	def on_cursor_leave(self, *args):
		"""Called when the mouse exits the widget AND the widget is visible."""
		pass


	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.register_event_type("on_cursor_enter")
		self.register_event_type("on_cursor_leave")

		if not HoverBehavior.__resizes:
			Window.bind(mouse_pos=self.on_mouse_update)
			Window.bind(on_cursor_leave=self.window_cursor_leave)
		
		HoverBehavior.__resizes.append(self)

	def on_parent(self, *args):
		if self.parent != None:
			self._last_parent = self.parent
		
		if self.parent == None and HoverBehavior.__resizes:
			if HoverBehavior.__resizes[0] is self:
				Window.unbind(mouse_pos=self.on_mouse_update)
				Window.unbind(on_cursor_leave=self.window_cursor_leave)
				del HoverBehavior.__resizes[0]
				
				if HoverBehavior.__resizes:
					Window.bind(mouse_pos=HoverBehavior.__resizes[0].on_mouse_pos)
					Window.bind(on_cursor_leave=HoverBehavior.__resizes[0].window_cursor_leave)
			else:
				HoverBehavior.__resizes.remove(self)

	def window_cursor_leave(self, *args):
		for wid in HoverBehavior.__resizes:
			if wid.hover_visible or wid.repeat_callback:
				wid.do_cursor_leave()

	def do_cursor_leave(self, *args):
		self.hovering = False
		self.enter_point = None
		if self.hover_visible or self.repeat_callback:
			self.hover_visible = False
			self.dispatch("on_cursor_leave")
	
	def do_cursor_enter(self, *args):
		if self.hover_visible:
			self.enter_point = self.cursor_pos
			self.dispatch("on_cursor_enter")

	def new_dispatch(self, *args):
		"""
			ARGS:
			 `option`: 'leave' or 'enter'
		"""
		if not self.hovering:
			self.dispatch("on_cursor_leave")
		else:
			self.dispatch("on_cursor_enter")

	def on_mouse_update(self, *args):
		if not self.get_root_window():
			return None
		
		for wid in HoverBehavior.__resizes:
			
			pos = args[1]
			wid.cursor_pos = pos
			#  If widget not in the same position: on_exit event if needed
			if not wid.collide_point(*wid.to_widget(*pos)):
				wid.do_cursor_leave()
				continue

			# | The pointer is in the same position as the widget

			if wid.hovering and not wid.repeat_callback:
				#  nothing to do here. Not - this does not handle the case where
				#  a popup comes over an existing hover event.
				#  This seems reasonable
				continue
			
			wid.hovering = True

			# | We need to traverse the tree to see if the Widget is visible
			
			# This is a two stage process:
			# - first go up the tree to the root Window.
			#   At each stage - check that the Widget is actually visible
			# - Second - At the root Window check that there is not another branch
			#   covering the Widget

			wid.hover_visible = True
			if wid.detect_visible:
				widget = wid
				while 1:
					# Walk up the Widget tree from the target Widget
					parent = widget.parent
					try:
						# See if the mouse point collides with the parent
						# using both local and global coordinates to cover absolut and relative layouts
						pinside = parent.collide_point(*parent.to_widget(*pos)) or parent.collide_point(*pos)
					except Exception:
						# The collide_point will error when you reach the root Window
						break
					if not pinside:
						wid.hover_visible = False
						break
					# Iterate upwards
					widget = parent

				#  parent = root window
				#  widget = first Widget on the current branch
				children = parent.children
				for child in children:
					# For each top level widget - check if is current branch
					# If it is - then break.
					# If not then - since we start at 0 - this widget is visible

					# Check to see if it should take the hover
					if child == widget:
						# this means that the current widget is visible
						break
					if child.collide_point(*pos):
						#  this means that the current widget is covered by a modal or popup
						wid.hover_visible = False
						break
					
			wid.do_cursor_enter()

