
from kivy.animation import Animation
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.properties import (
	ListProperty, NumericProperty,
	ObjectProperty, StringProperty,
	BooleanProperty, ColorProperty
)
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivygo.widgets.icon import GoIconButton
from kivygo.layouts.floatlayout import GoFloatChild

Builder.load_string("""

					
<GoInputBox>:
	padding: [dp(10)+self.outline_width] * 4
	background_color: GoColors.primary_default
	outline_color: GoColors.primary_border
	label_defaut_color: GoColors.at_primary_default if self.state_label == "in" else GoColors.background_default
	
	box_size:
		[\
		[self.x + self.padding[0] + root.outline_width, self.y + self.padding[3] + root.outline_width],\
		[self.width - self.padding[0] - self.padding[2] - (root.outline_width*2), self.height - self.padding[1] - self.padding[3] - (root.outline_width*2)]\
		]

	canvas:
		Color:
			rgba: root.outline_color
		Line:
			rounded_rectangle: (\
				list(map(lambda x: x-root.outline_width, self.box_size[0]))\
				 + list(map(lambda x: x+(root.outline_width*2), self.box_size[1]))\
				 + root.radius + [100])
			width: root.outline_width

	canvas.before:
		Color:
			rgba: root.background_color
		RoundedRectangle:
			pos: self.box_size[0]
			size: self.box_size[1]
			radius: root.radius
	
	GoFloatChild:
		size: 0, 0
		pos: 0, 0
		Label:
			id: label
			x: root.x
			size_hint_x: None
			text: root.label_text
			color: root.label_defaut_color
			width: label.texture_size[0] + dp(140)

<GoInputForBox>:
	background_color: [1, 1, 1, 0]

<GoInputLeftIcon>:
	size_hint_y: None
	height: dp(50)
	outline_width: dp(1.01)
	GoIconButtonFade:
		size_hint_x: None
		width: dp(24)
	GoInputForBox:
					
""")


class GoInputBox(BoxLayout):

	radius = ListProperty([0, 0, 0, 0])
	box_size = ListProperty([[0, 0], [0, 0]])
	background_color = ColorProperty()
	outline_color = ColorProperty()
	outline_width = NumericProperty(1.01)

	label_text = StringProperty("")
	label_font_size_in = NumericProperty(sp(16))
	label_font_size_out = NumericProperty(sp(12))
	label_defaut_color = ColorProperty()

	state_label = StringProperty("in")
	label_in = ListProperty([0, 0])
	label_out = ListProperty([0, 0])

	_widgets = None

	def __init__(self, **kwargs):
		self._widgets = {
			"left_icon": None,
			"mid_input": None,
			"right_icon": None
		}
		
		super().__init__(**kwargs)
		Clock.schedule_once(self.config)

	def config(self, *args):
		self.ids.label.font_size = self.label_font_size_in

		self.on_children()

	def on_children(self, *args):
		left_icon, mid_input, right_icon = None, None, None

		stack = [self]
		while stack:
			current_widget = stack[0]
			del stack[0]

			stack.extend(current_widget.children)
			if not hasattr(current_widget, "type_widget"):
				continue

			if current_widget.type_widget == "Input":
				mid_input = current_widget
				
			elif current_widget.type_widget == "Icon":
				if mid_input == None and right_icon == None:
					right_icon = current_widget
				else:
					left_icon = current_widget


		self._widgets["left_icon"] = left_icon
		self._widgets["mid_input"] = mid_input
		self._widgets["right_icon"] = right_icon


	def on_touch_down(self, touch):
		if touch.is_mouse_scrolling:
			return False

		if self._widgets["mid_input"] != None:
			if self._widgets["mid_input"].collide_point(*touch.pos):
				self.anima(True)

		return super().on_touch_down(touch)
	
	def on_touch_up(self, touch):
		if touch.is_mouse_scrolling:
			return False

		if self._widgets["mid_input"] != None:
			if not self._widgets["mid_input"].collide_point(*touch.pos):
				if self._widgets["mid_input"].text == "":
					self.anima(False)
		
		return super().on_touch_up(touch)

	def on_pos(self, *args):
		left_icon = self._widgets["left_icon"]

		if left_icon != None:
			self.label_in = (self.x-dp(40)+left_icon.width, self.center_y-(self.ids.label.height/2))
		else:
			self.label_in = (self.x-dp(40), self.center_y-(self.ids.label.height/2))

		radius_left = self.radius[0] if self.radius[0] > self.radius[3] else self.radius[3] 
		if radius_left <= dp(13):
			radius_left = dp(13)
		
		self.label_out = (self.x-dp(50)+self.radius[-1]/2.5, self.top)

		if self.state_label == 'in':
			self.ids.label.pos = self.label_in
		elif self.state_label == 'out':
			self.ids.label.pos = self.label_out

	def anima(self, pos_widget, *args):
		if pos_widget:
			self.state_label = 'out'
			newpos = self.label_out
			font = self.label_font_size_out
		else:
			self.state_label = 'in'
			newpos = self.label_in
			font = self.label_font_size_in
		
		anim = Animation(pos=(newpos), font_size=font, d=.1, t='out_sine')
		anim.start(self.ids.label)


class GoInputForBox(TextInput):
	window_root = ObjectProperty(None)
	def insert_text(self, substring, from_undo=False):
		r =  super().insert_text(substring, from_undo=from_undo)

		if self.window_root != None:
			self.window_root.dispatch('on_input_text', substring, from_undo)
		return r


class GoInputLeftIcon(GoInputBox):
	pass

# class GoInputIcon(AnchorLayout):
# 	outline_color = ListProperty([0]*4)
# 	line_color_pos = ListProperty([0]*4)
# 	color_line = ListProperty([0]*4)
# 	outline_width = NumericProperty(1.01)

# 	background_color = ListProperty([0]*4)
# 	multiline = BooleanProperty(False)
# 	radius = ListProperty([dp(15), dp(15), dp(15), dp(15)])

# 	icon_left = ObjectProperty(None)
# 	icon_left_state = StringProperty('toggle')#'toggle' or 'button'
# 	icon_left_color = ListProperty([1, 1, 1, 1])
# 	icon_left_pos_source = StringProperty('')
# 	icon_left_source = StringProperty('')
# 	icon_left_color_pos = ListProperty([-1, -1, -1, -1])
# 	icon_left_state_sources = ListProperty(['', ''])
# 	icon_left_size = ListProperty([dp(30), dp(23)])
# 	icon_left_effect_color = ListProperty([0, 0, 0, 0])

# 	icon_right = ObjectProperty(None)
# 	icon_right_state = StringProperty('toggle')#'toggle' or 'button'
# 	icon_right_color = ListProperty([1, 1, 1, 1])
# 	icon_right_pos_source = StringProperty('')
# 	icon_right_state_sources = ListProperty(['', ''])
# 	icon_right_source = StringProperty('')
# 	icon_right_color_pos = ListProperty([-1, -1, -1, -1])
# 	icon_right_size = ListProperty([dp(30), dp(23)])
# 	icon_right_effect_color = ListProperty([0, 0, 0, 0])

# 	label_text = StringProperty('')
# 	label_font_size = NumericProperty(dp(16))
# 	label_defaut_color = ListProperty([0]*4)
# 	label_pos_color = ListProperty([0]*4)
# 	state_label = StringProperty('')

# 	input = ObjectProperty(None)
# 	hide = ObjectProperty(False)
# 	text_input_color = ListProperty([0]*4)
# 	input_text = StringProperty("")

# 	__events__ = ('on_icon_right_state', 'on_icon_right_press', 'on_icon_right_release', 'on_icon_left_state', 'on_icon_left_press',
# 				  'on_icon_left_release', 'on_input_press', 'on_input_release', 
# 				  'on_input_text', 'on_init_input', 'on_icon_right_pos',
# 				  'on_icon_right_pos_release', 'on_enter')

# 	def __init__(self, **kwargs):
# 		super().__init__(**kwargs)
# 		self.pdentro = (0, 0)
# 		self.pfora = (0, 0)
# 		Clock.schedule_once(self.config)

# 	def on_icon_right_state(self, *args):
# 		pass
	
# 	def on_icon_left_state(self, *args):
# 		pass

# 	def select(self, *args):
# 		self.input.focus = True
# 		touch = MouseMotionEvent(None, 123, args=(1, 1))  # args are device, id, spos
# 		touch.button = 'left'
# 		touch.pos = [self.center_x, self.center_y]
# 		self.dispatch('on_touch_down', touch)
	
# 	def un_select(self, *args):
# 		self.input.focus = False
# 		touch = MouseMotionEvent(None, 123, args=(1, 1))  # args are device, id, spos
# 		touch.button = 'left'
# 		touch.pos = [self.center_x, self.center_y]
# 		self.dispatch('on_touch_up', touch)

# 	def config(self, *args):
# 		self.pads()
# 		self.color_line = self.outline_color
# 		self.icon_right = self.ids.button_right
# 		self.icon_left = self.ids.button_left
# 		self.input = self.ids.input

# 		if not self.icon_left_source and not self.icon_left_state_sources[0] and not self.icon_left_pos_source:
# 			self.ids.box.remove_widget(self.ids.anchor_left)
# 			self.icon_left_size = [0, 0]
# 			self.icon_left = False
# 		if not self.icon_right_source and not self.icon_right_state_sources[0] and not self.icon_right_pos_source:
# 			self.ids.box.remove_widget(self.ids.anchor_right)
# 			self.icon_right_size = [0,0]
# 			self.icon_right = False
# 		self.dispatch('on_init_input')

# 	def pads(self, *args):
# 		radius_left = self.radius[0] if self.radius[0] > self.radius[3] else self.radius[3] 
# 		radius_right = self.radius[1] if self.radius[1] > self.radius[2] else self.radius[2]
		
# 		if radius_left > 13:
# 			one_pad_x = radius_left-radius_left/2
# 			two_pad_x = -one_pad_x/1.4
# 			self.ids.anchor_left.padding = [one_pad_x, 1, two_pad_x, 1]
# 			self.ids.anchor_input.padding = [one_pad_x, 1, one_pad_x, 1]
# 		else:
# 			self.ids.anchor_left.padding = [7, 1, 15, 1]
		
# 		if radius_right > dp(13):
# 			one_pad_x = radius_right-radius_right/2
# 			two_pad_x = -one_pad_x/1.7
# 			self.ids.anchor_right.padding = [two_pad_x, 1, one_pad_x, 1]
# 			# self.ids.anchor_input.padding = [one_pad_x, 1, two_pad_x, 1]
# 		else:
# 			self.ids.anchor_left.padding = [7, 1, -3, 1]
# 			# self.ids.anchor_input.padding = [5, 1, 2, 1]

# 	def on_touch_down(self, touch):
# 		if touch.is_mouse_scrolling:
# 			return False

# 		if self.ids.anchor_input.collide_point(*touch.pos):
# 			self.anima(True)
# 			self.dispatch('on_input_press')
			
# 		if self.icon_right:
# 			if self.icon_right.collide_point(*touch.pos):
# 				# self.icon_down(self.icon_right)
# 				self.dispatch('on_icon_right_press')
# 		if self.icon_left:
# 			if self.icon_left.collide_point(*touch.pos):
# 				#se .icon_down(self.icon_left)
# 				self.dispatch('on_icon_left_press')

# 		return super().on_touch_down(touch)
	
# 	def on_touch_up(self, touch):
# 		if touch.is_mouse_scrolling:
# 			return False

# 		if not self.ids.anchor_input.collide_point(*touch.pos):
# 			self.dispatch('on_input_release')
# 			if self.ids.input.text == '':
# 				self.anima(False)
# 		if self.icon_right:
# 			if self.icon_right.collide_point(*touch.pos):
# 				# self.icon_up(self.icon_right)
# 				self.dispatch('on_icon_right_release')
# 		if self.icon_left:
# 			if self.icon_left.collide_point(*touch.pos):
# 				# self.icon_up(self.icon_left)
# 				self.dispatch('on_icon_left_release')
# 		return super().on_touch_up(touch)

# 	def on_icon_right_press(self): pass
# 	def on_icon_right_release(self): pass
# 	def on_icon_right_pos(self, *args): pass
# 	def on_icon_right_pos_release(self, *args): pass
	
# 	def on_icon_left_press(self): pass
# 	def on_icon_left_release(self): pass

# 	def on_input_press(self): pass
# 	def on_input_release(self): pass

# 	def on_init_input(self): pass
# 	def on_input_text(self, substring, from_undo): pass
# 	def on_enter(self, *args): pass

# 	def on_pos(self, *args):
# 		self.pdentro = (self.x-dp(50)+self.radius[-1]/2.5, self.y+dp(40))
# 		radius_left = self.radius[0] if self.radius[0] > self.radius[3] else self.radius[3] 
# 		if radius_left <= dp(13):
# 			radius_left = dp(13)
# 		if self.icon_left_size[0] == 0:
# 			self.pfora = (self.x-dp(40)+radius_left, self.y+dp(10))
# 		else:
# 			self.pfora = (self.x-dp(40)+self.icon_left_size[0]+(radius_left/2), self.y+dp(10))

# 		if self.state_label == 'pdentro':
# 			self.ids.lbl.pos = self.pdentro
# 		elif self.state_label == 'pfora':
# 			self.ids.lbl.pos = self.pfora
# 		else:
# 			self.ids.lbl.pos = self.pfora

# 	def anima(self, pos_widget, *args):
# 		if pos_widget:
# 			self.state_label = 'pdentro'
# 			newpos = self.pdentro
# 			font = sp(12)
# 			if self.line_color_pos != [0, 0, 0, 0]:
# 				self.color_line = self.line_color_pos
# 			self.ids.lbl.color = self.label_pos_color
# 		if not pos_widget:
# 			self.state_label = 'pfora'
# 			newpos = self.pfora
# 			font = sp(16)
# 			self.color_line = self.outline_color
# 			self.ids.lbl.color = self.label_defaut_color
		
# 		anim = Animation(pos=(newpos), font_size=font, d=.1, t='out_sine')
# 		anim.start(self.ids.lbl)

