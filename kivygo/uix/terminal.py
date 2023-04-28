from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.codeinput import CodeInput
from kivy.uix.textinput import TextInput
from kivy.core.text.markup import MarkupLabel as CoreLabel
from kivy.properties import (
	ObjectProperty, StringProperty,
	BooleanProperty, ColorProperty,
	NumericProperty
)
from kivy.clock import Clock
from kivy.metrics import dp
from pygments.styles import get_style_by_name


Builder.load_string("""

<CodeEditor>:
	id: scroller
	code: text_code
	effect_cls: 'ScrollEffect'
	bar_width: '15dp'
	input_minimum_height: text_code.minimum_height
	TextCode:
		id: text_code
		size_hint: [None, None]
		on_text: scroller.update_width_code()
		height: max(self.minimum_height, scroller.height)
		font_size: root.font_size
		style: root.style
		background_color: [1, 1, 1, 0]
		text: root.text


<InputEditor>:
	id: scroller
	code: text_code
	effect_cls: 'ScrollEffect'
	bar_width: '15dp'
	input_minimum_height: text_code.minimum_height
	InputTerminal:
		id: text_code
		size_hint: None, None
		on_text: scroller.update_width_code()
		height: max(self.minimum_height, scroller.height)
		font_size: root.font_size
		style: root.style
		background_color: [1, 1, 1, 0]
		text: root.text
		foreground_color: root.text_color

		
""")


class InputTerminal(TextInput):

	can_scroll = True

	def on_touch_down(self, touch):
		if not self.can_scroll:
			# Não posso rolar
			return False
		return super().on_touch_down(touch)

	def on_touch_move(self, touch):
		if not self.can_scroll:
			# Não posso rolar
			return False
		return super().on_touch_move(touch)


class TextCode(CodeInput, InputTerminal):
	pass


class CodeEditorBase(ScrollView):
	
	code = ObjectProperty(None)
	bar_move = ''
	change_width = ObjectProperty(True)
	touch_pos = [0, 0]
	style = ObjectProperty(get_style_by_name('monokai'))
	text = StringProperty("")
	clickable = BooleanProperty(True)
	cursor_color = ColorProperty([1, 0, 0, 1])
	font_size = NumericProperty("12sp")
	text_color = ColorProperty([1, 1, 1, 1])
	input_minimum_height = NumericProperty(0)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.bind(size=self.update_width_code)
		self.bind(pos=self.update_width_code)
		Clock.schedule_once(self.start)

	
	def start(self, *args):
		self.code.cursor_color = self.cursor_color
		self.update_width_code()
		self.on_clickable()
	

	def on_clickable(self, *args):
		if not self.clickable:
			self.code.cursor_color = [0, 0, 0, 0]
			return None
		
		self.code.cursor_color = self.cursor_color


	# def on_touch_up(self, touch):
	#     if not self.clickable:
	#         return None
		
	#     return super().on_touch_up(touch)
	
	def on_touch_down(self, touch):
		self.touch_pos = touch.pos
		if not self.collide_point(*touch.pos):
			return False

		self.code.can_scroll = False
		if touch.x >= (self.x + self.width - self.bar_width):
			self.bar_move = 'left'
			return True
		elif touch.y <= (self.y + self.bar_width):
			self.bar_move = 'bottom'
			return True

		self.bar_move = ''
		self.code.can_scroll = True

		# if not self.clickable:
		#     return None
		
		return super().on_touch_down(touch)

	def maximum_text(self):
		label = CoreLabel(**self.code._get_line_options())
		lines = self.code.text.splitlines()
		max_width = 0
		for i in range(len(lines)):
			max_width = max(label.get_extents(lines[i])[0], max_width)
		return max_width + dp(20)

	def update_width_code(self, *args):
		if self.code is None or len(self.code._cursor) < 2:
			return None

		labels = self.code._lines_labels
		if not labels:
			return None
		
		if not self.change_width:
			self.code.width = self.width
			return None
		
		if self.code._cursor[1] >= len(labels):
			self.code._cursor = (0, 0)

		max_width = max(self.maximum_text(), self.width)
		if max_width != self.code.width:
			self.code.width = max_width
			self.scroll_x = 1
		

		current_label = labels[self.code._cursor[1]]
		if current_label.width > self.width:
			if self.scroll_x <= 0.5:
				self.scroll_x += 0.5
		else:
			self.scroll_x = 0
		
		if self.code.height <= self.height:
			self.scroll_y = 0
	
	def decrise_scroll(self, dt, direction):
		name = f'scroll_{direction}'
		n_scroll = getattr(self, name)
		
		if n_scroll >= dt:
			setattr(self, name, (n_scroll - dt))
		elif n_scroll > 0:
			setattr(self, name, 0)

	def incrise_scroll(self, dt, direction):
		name = f'scroll_{direction}'
		n_scroll = getattr(self, name)
		
		if n_scroll <= (1 - dt):
			setattr(self, name, (n_scroll + dt))
		elif n_scroll < 1:
			setattr(self, name, 1)

	def on_touch_move(self, touch):
		if self.code == None:
			return None
		
		if not self.collide_point(*touch.pos):
			return None
		
		if self.code._selection:
			# Desce ou sobe de acordo com a seleção
			x, y = touch.pos
			
			dt = (1 / self.code.height) * dp(40)
			if y < (self.y + dp(40)):
				self.decrise_scroll(dt, 'y')
			elif y > (self.y + self.height - dp(40)):
				self.incrise_scroll(dt, 'y')

			dt = (1 / self.code.width) * dp(40)
			if x < (self.x + dp(40)):
				self.decrise_scroll(dt, 'x')
			elif x > (self.x + self.width - dp(40)):
				self.incrise_scroll(dt, 'x')

		if not self.code.can_scroll:
			last_pos = self.touch_pos
			self.touch_pos = touch.pos

			cfd = (last_pos[1] - touch.y)
			distance = abs(cfd * (len(self.code._lines) * dp(17) / dp(185)) / 2.2)
			dt = round((1 / self.code.height * distance), 2)
			if self.bar_move == 'left':
				if cfd > dp(5):
					# Movimentar bar para baixo
					self.decrise_scroll(dt, 'y')
				elif cfd < dp(-5):
					# Movimentar bar para cima
					self.incrise_scroll(dt, 'y')
				else:
					self.touch_pos = last_pos
			
			cfd = (last_pos[0] - touch.x)
			dt = dp(7) * (1 / (self.code.width/max(abs(cfd), 1)))
			if self.bar_move == 'bottom':
				if cfd > dp(5):
					# Movimentar bar para esquerda
					self.decrise_scroll(dt, 'x')
				elif cfd < dp(-5):
					# Movimentar bar para a direita
					self.incrise_scroll(dt, 'x')
				else:
					self.touch_pos = last_pos
			return True

		# if not self.clickable:
		#     return None
	
		return super().on_touch_move(touch)


class InputEditor(CodeEditorBase):
	pass


class CodeEditor(CodeEditorBase):
	pass

