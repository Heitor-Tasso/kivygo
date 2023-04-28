
from kivy.properties import (
	OptionProperty, ObjectProperty,
	BooleanProperty, NumericProperty,
)

from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.config import Config
from weakref import ref
from time import time
from kivy.app import App


class ButtonBehavior(Widget):

	state = OptionProperty('normal', options=('normal', 'down'))
	'''
	The state is 'down' only when the button is currently touched/clicked,
	otherwise its 'normal'.
	'''

	last_touch = ObjectProperty(None)
	'''
	Contains the last relevant touch received by the Button. This is
	used in `on_press` and `on_release` to know which touch dispatched the event.
	'''

	min_state_time = NumericProperty(0)
	'''
	The minimum period of time which the widget must remain in the
	`'down'` state. `min_state_time` is a float and defaults to 0.035.
	This value is taken from `kivy.config.Config`.
	'''

	always_release = BooleanProperty(False)
	'''
	This determines whether or not the widget fires an `on_release` event if
	the touch_up is outside the widget.
	'''

	up_elevation = NumericProperty(3)
	"""
	Elevation level when the button is in the up state.
	"""

	down_elevation = NumericProperty(1)
	"""
	Elevation level when the button is in the down state.
	"""

	pressed = BooleanProperty(False)
	"""
	Read only property that represents if the button is pressed or not.
	"""

	do_text_shrink = BooleanProperty(True)
	"""
	When set to `True`, text on a button will shrink when the button is pressed.
	This is done to mimic the effect that the text is going into the screen on press.
	The amount of change in font size can be adjusted using the property `text_shrink_amount`.

	If you have created a custom widget and want to use this effect in a widget. Set the `id`
	value of your text(which is inside the widget) to `label`. The effect will apply to to any
	label with id = 'label'.
	"""

	text_shrink_amount = NumericProperty(1)
	"""
	Amount to decrease the font_size on button press. Will only work if `do_text_shrink` is `True`.
	You can try setting this to a negative value to make the text shrink.
	If `text_shrink_amount = 1` then the font_size will decrease by '1sp'.
	"""

	disabled = BooleanProperty(False)
	"""
	Whether the widget has been disabled or not
	"""

	def on_press(self, *args):
		pass

	def on_release(self, *args):
		pass

	def __init__(self, **kwargs):
		self.register_event_type('on_press')
		self.register_event_type('on_release')
		if 'min_state_time' not in kwargs:
			self.min_state_time = float(Config.get('graphics',
												   'min_state_time'))
		
		super().__init__(**kwargs)
		self.__state_event = None
		self.__touch_time = None
		self.fbind('state', self.cancel_event)
		Clock.schedule_once(self.elevation_setter, 0)

	def elevation_setter(self, *args):
		self.elev = self.up_elevation

	def _do_press(self):
		self.state = 'down'

	def _do_release(self, *args):
		self.state = 'normal'

	def cancel_event(self, *args):
		if self.__state_event:
			self.__state_event.cancel()
			self.__state_event = None

	def on_touch_down(self, touch):
		if touch.is_mouse_scrolling:
			return False
		
		if not self.collide_point(touch.x, touch.y):
			return False
		
		if self in touch.ud:
			return False
	
		if self.collide_point(*touch.pos) and not self.disabled:
			self.pressed = True
			self.elev = self.down_elevation
			self.dispatch("on_press")

			if "label" in self.ids and self.do_text_shrink:
				self.ids.label.font_size -= self.text_shrink_amount
		
		touch.grab(self)
		touch.ud[self] = True
		self.last_touch = touch
		self.__touch_time = time()
		self._do_press()

		if App._running_app:
			self.dispatch('on_press')
		
		return True

	def on_touch_move(self, touch):
		if touch.grab_current is self:
			return True
		
		if super().on_touch_move(touch):
			return True
		
		return (self in touch.ud)

	def on_touch_up(self, touch):
		if touch.grab_current is not self:
			return super().on_touch_up(touch)
		
		assert(self in touch.ud)
		touch.ungrab(self)
		self.last_touch = touch

		if (not self.always_release and
				not self.collide_point(*touch.pos)):
			self._do_release()
			return None

		if self.pressed and not self.disabled:
			self.elev = self.up_elevation
			self.pressed = False
			self.dispatch("on_release")

			if "label" in self.ids and self.do_text_shrink:
				self.ids.label.font_size += self.text_shrink_amount

		touchtime = time() - self.__touch_time
		if touchtime < self.min_state_time:
			self.__state_event = Clock.schedule_once(
				self._do_release, self.min_state_time - touchtime)
		else:
			self._do_release()
		
		if App._running_app:
			self.dispatch('on_release')
		
		return True

	def trigger_action(self, duration=0.1):
		'''Trigger whatever action(s) have been bound to the button by calling
		both the on_press and on_release callbacks.

		This is similar to a quick button press without using any touch events,
		but note that like most kivy code, this is not guaranteed to be safe to
		call from external threads. If needed use `kivy.clock.Clock` to safely
		schedule this function and the resulting callbacks to be called
		from the main thread.

		Duration is the length of the press in seconds. Pass 0 if you want
		the action to happen instantly.
		'''

		self._do_press()
		self.dispatch('on_press')

		def trigger_release(dt):
			self._do_release()
			self.dispatch('on_release')
		
		if not duration:
			trigger_release(0)
		else:
			Clock.schedule_once(trigger_release, duration)


class ToggleButtonBehavior(ButtonBehavior):
	
	__groups = {}

	group = ObjectProperty(None, allownone=True)
	'''
	Group of the button. If `None`, no group will be used (the button will be
	independent). `group` must be a hashable object, like a string.
	Only one button in a group can be in a 'down' state.
	'''

	allow_no_selection = BooleanProperty(True)
	'''
	This specifies whether the widgets in a group allow no selection i.e.
	everything to be deselected.
	'''

	def __init__(self, **kwargs):
		self._previous_group = None
		super().__init__(**kwargs)

	def on_group(self, *largs):
		groups = ToggleButtonBehavior.__groups
		if self._previous_group:
			group = groups[self._previous_group]
			for item in group[:]:
				if item() is self:
					group.remove(item)
					break
		
		group = self._previous_group = self.group
		if group not in groups:
			groups[group] = []
		r = ref(self, ToggleButtonBehavior._clear_groups)
		groups[group].append(r)

	def _release_group(self, current):
		if self.group is None:
			return None
		
		group = self.__groups[self.group]
		for item in group[:]:
			widget = item()
			if widget is None:
				group.remove(item)
			
			if widget is current:
				continue
			
			widget.state = 'normal'

	def _do_press(self):
		if not self.allow_no_selection:
			return None
	
		if self.group and self.state == 'down':
			return None

		self._release_group(self)
		self.state = 'normal' if self.state == 'down' else 'down'

	def _do_release(self, *args):
		pass

	@staticmethod
	def _clear_groups(wk):
		# auto flush the element when the weak reference have been deleted
		groups = ToggleButtonBehavior.__groups
		for group in list(groups.values()):
			if wk in group:
				group.remove(wk)
				break

	@staticmethod
	def get_widgets(groupname):
		'''
		Return a list of the widgets contained in a specific group. If the
		group doesn't exist, an empty list will be returned.
		
		.. note:
			Always release the result of this method! Holding a reference to
			any of these widgets can prevent them from being garbage collected.
			If in doubt, do::
				l = ToggleButtonBehavior.get_widgets('mygroup')
				# do your job
				del l
		
		.. warning:
			It's possible that some widgets that you have previously
			deleted are still in the list. The garbage collector might need
			to release other objects before flushing them.
		'''
		groups = ToggleButtonBehavior.__groups
		if groupname not in groups:
			return []
		return [x() for x in groups[groupname] if x()][:]
