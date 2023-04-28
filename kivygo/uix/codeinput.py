'''
[ Future ]:
	lbl = Label
	lbl.text ='Clique [b][ref=aqui]aqui[/ref][/b] para testar!'
	lbl.bind(on_ref_press=self.processaClique
	def processaClique(self,instance, value):
		print ("Usuario clicou sobre o link " , value)

[ IMPORTANTE ] | Adicionar seta de escrita quando estiver com focus == True |
[ BUGS ] Rolagem | Seleção | Canvas ViewPort |

'''

from kivy.app import runTouchApp
from kivy.core.text.markup import MarkupLabel as CoreLabel
from kivy.core.text import DEFAULT_FONT
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import (
	ListProperty, NumericProperty,
	StringProperty, AliasProperty,
	BooleanProperty, ColorProperty
)
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.graphics import Rectangle
from kivy.core.clipboard import Clipboard
from kivy.lang.builder import Builder
from functools import partial


meta_carac = {
	# specials keys
	8 : 'backspace',
	9 : 'tab',
	13 : 'enter',
	127 : 'delete',
	271 : 'enter',
	273 : 'up',
	274 : 'down',
	275 : 'right',
	276 : 'left',
	278 : 'home',
	279 : 'end',
	280 : 'pageup',
	281 : 'pagedown',
	301 : 'capslock',
	303 : 'lshift',
	304 : 'rshift',
	305 : 'lctrl',
	306 : 'rctrl',
	# 307 : 'alt-gr',
	307 : 'ralt',
	308 : 'lalt',
}


Builder.load_string("""


<CodeInput>:
	canvas.before:
		Color:
			rgba: self.background
		Rectangle:
			pos: self.pos
			size: self.size
		Color:
			rgba: self.text_color
	
	canvas.after:
		Color:
			rgba: self._cursor_color
		Rectangle:
			pos: self._cursor_pos
			size: self.cursor_size
		
		Color:
			rgba: self.selection_color[:-1] + [0.4]

""")


class CodeInput(Widget):
	
	cursor_color = ListProperty([[1, 0, 0, 1], [0, 1, 0, 1]])
	_cursor_color = ColorProperty([0, 0, 0, 0])
	
	cursor_size = ListProperty([sp(1), sp(18)])

	_cursor_pos = ListProperty([0, 0])
	cursor_interval = NumericProperty(0.6)
	_labels = ListProperty([])
	background = ColorProperty('#282a36')
	text_color = ColorProperty('#FFFFFF')
	selection_color = ColorProperty('#636672')

	tab_width = NumericProperty(4)

	font_name = StringProperty(DEFAULT_FONT)
	font_size = NumericProperty(sp(15))
	font_context = StringProperty(None, allownone=True)
	font_family = StringProperty(None, allownone=True)

	auto_indent = BooleanProperty(False)
	focus = BooleanProperty(False)


	# Index of the `end` & `init` visible labels on the viewport
	label_init = 0
	label_end = 0

	# Number of lines in all text -> len(lines)
	_n_labels = 0

	# Number of lines in the viewport -> viewport_height / line_height
	max_lines = 0
	
	# True if the key is pressed and False if not
	shift_pressed = False
	ctrl_pressed = False
	capslock_pressed = False
	alt_pressed = False

	# The position of the top line on viewport
	top_line_y = 0

	# Indicates if the input has a selection	
	in_selection = False

	# `Window.request_keyboard` to bind and get the normal keys
	_keyboard = None


	def _set_text(self, text:str) -> None:
		n_text = text.splitlines()
		self._labels.clear()
		self._rectangles.clear()
		self._n_labels = 0
		Clock.schedule_once(partial(self.insert_lines, n_text, True))

	def _get_text(self):
		return ''.join([f'{lbl.text}\n' for lbl in self._labels])
	
	text = AliasProperty(_get_text, _set_text, bind=('_labels',), cache=True)


	def __init__(self, **kwargs):
		self.selected = [0, 0]
		self.touch_down_pos = [[0, 0], [0, 0]]
		self.last_cursor_pos = [0, 0]
		self._cursor = [0, 0]
		self._selection = []
		self._rectangles = []
		
		super().__init__(**kwargs)
		self.cursor_clock = Clock.schedule_interval(self.change_cursor_color, self.cursor_interval)
		self.fbind('font_name', self.update_text_options)
		self.fbind('font_size', self.update_text_options)
		
		Window.bind(on_key_down=self.key_down, on_key_up=self.key_up)
		self.bind(size=self._update_graph, pos=self._update_graph)

		Clock.schedule_once(self.start)

	def start(self, *args) -> None:
		self._cursor_pos = [self.x, self.top_line_y]
		self.change_cursor_color("hide")

	def _update_graph(self, *args):
		self.update_values()
		self._update_lines()
	
	def _keyboard_unbind(self):
		if self._keyboard:
			self._keyboard.unbind(on_textinput=self.keyboard_on_textinput)
			self._keyboard.release()
			self._keyboard = None

	def _keyboard_bind(self):
		if not self._keyboard:
			self._keyboard = Window.request_keyboard(self._keyboard_unbind, self, 'text')
			self._keyboard.bind(on_textinput=self.keyboard_on_textinput)


	def change_cursor_color(self, dt, *args):
		color = self.get_color(self.cursor_color, 0)
		if self.in_selection:
			self._cursor_color = color
		
		elif self.focus:	
			if self._cursor_color != color or dt == "show":
				self._cursor_color = color
			else:
				self._cursor_color = self.get_color(self.cursor_color, 1, [*color[:-1], 0])
				
		self.cursor_clock.timeout = self.cursor_interval

	def update_text_options(self, *args):
		self.update_values()
		self._rectangles = []
		self._labels = []
		top_line_y = self.top_line_y

		for i_lbl in range(self._n_labels):
			label, texture, size = self.make_label(
											self._labels[i_lbl].text,
											self._label_kwargs)
			self._labels.append(label)
			self._rectangles.append(
				Rectangle(texture=texture, size=size, pos=[self.x, top_line_y])
			)
			top_line_y -= self.cursor_size[1]
		
		self.label_end = (self.label_init + self.max_lines)
		self._update_lines()

	def _update_lines(self, *args):
		if not self._labels:
			return None
		
		cur_y = self._cursor[1]
		cur_sh = self.cursor_size[1]
		new_max_lines = (self.label_init + self.max_lines)
		top_line_y = self.top_line_y

		if new_max_lines < self._n_labels:
			self.label_end = new_max_lines

		elif self.label_end < new_max_lines:
			if self.label_init > 0:
				self.label_init -= 1

			if self.label_end < self._n_labels:
				self.label_end += 1
		
		self.canvas.clear()
		for rect in self._rectangles[self.label_init:self.label_end]:
			rect.pos = [self.x, top_line_y]
			self.canvas.add(rect)
			top_line_y -= cur_sh
		
		y = self._rectangles[cur_y].pos[1]
		if self.label_init > cur_y:
			y = ( self.top_line_y + ( (self.label_init - cur_y) * cur_sh ) )

		elif self.label_end <= cur_y:
			y = ( top_line_y + cur_sh - ( (cur_y - self.label_end + 1) * cur_sh ) )

		self._cursor_pos = [self._x_cursor_by_index(*self._cursor), y]
		self.update_selection()

	def get_color(self, object, index, default=None):
		if isinstance(object, (list, tuple)):
			if len(object) == 2 and index > -1 and index < 3:
				color = object[index]
				if isinstance(color, str):
					color = get_color_from_hex(color)
				return color
		
		if index == 1 and default != None:
			return default
		return object

	def update_values(self, *args):
		self.cursor_size = [ dp(1), (1.2 * self.font_size) ]
		cur_sh = self.cursor_size[1]
		self.max_lines = int(round((self.height / cur_sh), 0))
		self.top_line_y = (self.y + self.height - cur_sh)

	def move_cursor_left(self, cur_sw, cur_sh, cur_x, cur_y, cur_px, cur_py):

		if (self.x + cur_sw) >= cur_px and cur_y > 0:
			if cur_y == self.label_init:
				self._scroll_down()
				cur_py -= cur_sh
			
			cur_y -= 1
			cur_x = self.get_len_str(cur_y)
			cur_px = (self.x + cur_sw + self._rectangles[cur_y].size[0])
			cur_py += cur_sh
		
		elif cur_px > (self.x + cur_sw):
			if self.ctrl_pressed:
				cur_px, cur_x = self.last_word()
			else:
				cur_x -= 1
				cur_px = self._x_cursor_by_index(cur_x, cur_y)
		
		self.ctrl_selection([cur_x, cur_y], [cur_px, cur_py])
	
	def move_cursor_right(self, largs):
		cur_sw, cur_sh, cur_x, cur_y, cur_px, cur_py = largs

		n_lbl = self._n_labels-1
		if self._rectangles:
			size_rec = (self._rectangles[cur_y].size[0] + self.x)
			if size_rec <= cur_px and cur_y < n_lbl:
				cur_y += 1
				cur_x = 0
				cur_px, cur_py = self.x, cur_py-cur_sh
				
			elif cur_y <= n_lbl and cur_px <= size_rec:
				if size_rec == 1:
					if cur_y < n_lbl:
						cur_y += 1
						cur_py -= cur_sh
				elif self.ctrl_pressed:
					cur_px, cur_x = self.next_word(cur_y)
				else:
					cur_x += 1
					get_pos = self._x_cursor_by_index(cur_x, cur_y)
					if get_pos != cur_px:
						cur_px = get_pos
					else:
						cur_x -= 1
			
			if cur_y == self.label_end:
				self._scroll_up()
				cur_py += cur_sh

		self.ctrl_selection([cur_x, cur_y], [cur_px, cur_py])
	
	def move_cursor_up(self, largs):
		cur_sw, cur_sh, cur_x, cur_y, cur_px, cur_py = largs

		if cur_y > 0:
			if cur_y == self.label_init:
				self._scroll_down()
			else:
				cur_py += cur_sh
			cur_y -= 1
			cur_px = (self._x_cursor_by_index(cur_x, cur_y) + self.x)
			if cur_x >= self.get_len_str(cur_y):
				cur_x = self.get_len_str(cur_y)

		self.ctrl_selection([cur_x, cur_y], [cur_px, cur_py])
	
	def move_cursor_down(self, largs):
		cur_sw, cur_sh, cur_x, cur_y, cur_px, cur_py = largs

		if cur_y < self._n_labels-1:
			if cur_y == self.label_end-1:
				self._scroll_up()
			else:
				cur_py -= cur_sh
			cur_y += 1
			cur_px = (self._x_cursor_by_index(cur_x, cur_y) + self.x)
			if cur_x >= self.get_len_str(cur_y):
				cur_x = self.get_len_str(cur_y)
				
		self.ctrl_selection([cur_x, cur_y], [cur_px, cur_py])

	def ctrl_selection(self, cursor, cursor_pos):
		self._cursor = [*cursor]
		
		if self.ctrl_pressed:
			self.last_cursor_pos = [*cursor_pos]
			self.do_selection()

		self._cursor_pos = [*cursor_pos]

	def update_selection(self):
		self.canvas.after.remove_group('selection')
		
		for i in self._selection:
			rect, index = i[0], i[1][0]
			if index >= self.label_init and index < self.label_end:
				rect.pos = [rect.pos[0], self._rectangles[index].pos[1]]
				rect.size = [rect.size[0], self.cursor_size[1]]
				self.canvas.after.add(rect)

	def do_selection(self, *args):
		if not self._labels:
			return None
		

		last_cursor_pos, last_cursor = self.get_cursor_by_touch(*self.last_cursor_pos, False)
		_cursor_pos, _cursor = self.touch_down_pos
		
		cur_y = self._cursor[1]
		largs = [
			last_cursor[1], _cursor[1],
			last_cursor_pos[0], last_cursor[0],
			_cursor_pos[0], _cursor[0]
		]

		if not self._selection:
			rect = Rectangle(size=[0, 0], pos=[0, 0], group='selection')
			self._selection.append([rect, [_cursor[1], self.x]])
			self.selected[1] += 1
			self.do_selection()
			self.selected[0] = cur_y
			return None
		
		self.remove_selection(False)
		l_select = max(_cursor[1], cur_y)
		first_index = min(_cursor[1], cur_y)
		total_select = len(self._selection)-1
		
		if total_select > 0:
			if l_select == self.max_lines-1:
				l_select = self.label_end-1
			if first_index == self.max_lines-1-self.label_init:
				first_index = self.label_init

		total_indexs = (l_select - first_index)

		for n, index in enumerate(range(first_index, l_select+1)):

			if index < self.label_init or index > self.label_end:
				continue

			lbl = self._labels[index]
			width, pos_x = lbl.size[0], self.x
			
			if total_indexs == 0:
				width, pos_x = self.direction_first_select(lbl, largs)
			
			elif index == first_index:
				x, px = self.direction_select(largs, last_select=False)
				width = lbl.get_extents(lbl.text[x:])[0]
				pos_x = px
			
			elif index == l_select:
				x, px = self.direction_select(largs, last_select=True)
				width = lbl.get_extents(lbl.text[:x])[0]

			try:
				if index == (self.label_end - 1) or index == (self.label_init + 1):
					rect = Rectangle(
								size=[width, self.cursor_size[1]],
								pos=[pos_x, self._rectangles[index].pos[1]],
								group='selection'
					)
					self._selection.append([rect, [index, pos_x]])
					self.selected[1] += 1
				else:
					rect = self._selection[n][0]
					self._selection[n] = [rect, [index, pos_x]]
					rect.size = [width, self.cursor_size[1]]
					rect.pos = [pos_x, self._rectangles[index].pos[1]]
			except IndexError:
				rect = Rectangle(
							size=[width, self.cursor_size[1]],
							pos=[pos_x, self._rectangles[index].pos[1]],
							group='selection'
				)
				self._selection.append([rect, [index, pos_x]])
				self.selected[1] += 1
			
			self.canvas.after.add(rect)
		
		self._selection = self._selection[:total_indexs+1]
		self.selected[0] = (cur_y - 1)

	def direction_first_select(self, lbl, largs):
		last_y, touch_y, last_px, last_x, touch_px, touch_x = largs
		
		if last_x < touch_x:
			width = lbl.get_extents(lbl.text[last_x:touch_x])[0]
			pos_x = last_px
		else:
			width = lbl.get_extents(lbl.text[touch_x:last_x])[0]
			pos_x = touch_px

		return [width, pos_x]

	def direction_select(self, largs, last_select):
		last_y, touch_y, last_px, last_x, touch_px, touch_x = largs
		if last_select:
			if last_y > touch_y:
				return [last_x, self.x]
			else:
				return [touch_x, self.x]
		else:
			if last_y < touch_y:
				return [last_x, last_px]
			else:
				return [touch_x, touch_px]
			
	def remove_selection(self, remov=True):
		self.canvas.after.remove_group('selection')
		if remov:
			self._selection = []
			self.touch_down_pos = [[0, 0], [0, 0]]
			self.last_cursor_pos = [0, 0]
			self.selected = [0, 0]

	def get_len_str(self, cur_y):
		if not self._labels:
			return 0
		
		return len(self._labels[cur_y].text)

	def _x_cursor_by_index(self, cur_x, cur_y):
		if not self._labels:
			return self.x
		
		lbl = self._labels[cur_y]
		width = lbl.get_extents(lbl.text[:cur_x])[0]
		return (self.x + width) 
	
	def insert_lines(self, lines, set_text=False, *args):
		if not lines:
			return None
	
		lbl_txt = ''
		lbls = []
		recs = []
		cur_sh = self.cursor_size[1]
		cur_py = self._cursor_pos[1]
		cur_x, cur_y = self._cursor
		self.canvas.clear()

		if self._labels:
			lbl_txt = self._labels[cur_y].text[:cur_x]
			lines[-1] += self._labels[cur_y].text[cur_x:]
		
		l_lines = len(lines)
		
		for n in range(l_lines):
			text = ((lbl_txt if n == 0 else '') + lines[n])
			label, texture, size = self.make_label(text, self._label_kwargs)
			lbls.append(label)
			recs.append(Rectangle(texture=texture, size=size,
								  pos=[self.x, cur_py]))
			cur_py -= cur_sh
		
		self._n_labels += (l_lines - 1) if self._labels else (l_lines)
		self._rectangles = (self._rectangles[:cur_y] + recs + self._rectangles[cur_y+1:])
		self._labels = (self._labels[:cur_y] + lbls + self._labels[cur_y+1:])
		
		if self._n_labels <= self.max_lines:
			self.label_end = (self.label_init + self._n_labels)
			self._cursor[1] += (l_lines - 1)
			self._cursor[0] = len(lbls[-1].text)
		else:
			self.label_init = (self.label_end - self.max_lines)
			self.label_end = (cur_y + l_lines)
			self._cursor[0] = [len(lbls[-1].text), (self.label_end - 1)]

			if self.label_init < 0:
				self._cursor[1] = self.label_end
				self.label_init = 0
				self.label_end = self.max_lines
		
		if set_text:
			self._cursor = [0, 0]
			self.label_init = 0
			self.label_end = l_lines

			if l_lines > self.max_lines:
				self.label_end = self.max_lines
				
		self._update_lines()

	def ctrl_v(self):
		lines = Clipboard.paste().splitlines()
		self.insert_lines(lines)

	def ctrl_c(self):
		pass

	def ctrl_z(self):
		pass

	def ctrl_x(self):
		pass

	def do_redo(self):
		pass

	def backspace(self):
		cur_sw, cur_sh = self.cursor_size
		cur_px, cur_py = self._cursor_pos
		x_before, y_before = self._cursor
		
		self.move_cursor_left(cur_sw, cur_sh, *self._cursor, cur_px, cur_py)
		
		cur_x, cur_y = self._cursor
		lbls, recs = self._labels, self._rectangles
		
		if lbls and x_before > 0:
			t_label = lbls[y_before].text
			n_text = t_label[:cur_x] + t_label[x_before:]
			self.change_line(n_text, y_before, self._label_kwargs)
		
		elif y_before > 0:
			n_text = lbls[cur_y].text[:cur_x] + lbls[y_before].text[x_before:]
			self.change_line(n_text, cur_y, self._label_kwargs)
			
			del lbls[y_before]
			del recs[y_before]
			self._n_labels -= 1
			self.label_end -= 1
			
			if self.label_end == self._n_labels and self.label_init > 0:
				self.label_init -= 1
			
			self._update_lines()

	def enter(self):
		cur_x, cur_y = self._cursor
		text = self._labels[cur_y].text
		self._cursor = [0, (cur_y + 1)]
		n_text = ''

		if self.auto_indent:
			tabs = self.identation(0, cur_y)
			n_text = ' ' * tabs
			self._cursor[0] = tabs

		if text[cur_x:] == '':
			cur = (-1) if self._cursor[1] > self._n_labels else (self._cursor[1])
			self.insert_string(n_text, cur)
		else:
			self.change_line(text[:cur_x], cur_y, self._label_kwargs)
			self.insert_string((n_text + text[cur_x:]), self._cursor[1])
		
		self._update_lines()
	
	def identation(self, cur_x, cur_y):
		for n, x in enumerate(self._labels[cur_y].text):
			if x != ' ':
				return n
		return cur_x

	def next_word(self, cur_y):
		label  = self._labels[cur_y]
		text = label.text

		for n, i in enumerate(text):
			if n > self._cursor[0] and i == ' ':
				w_text = label.get_extents(text[:n])[0]
				return [(self.x + w_text), len(text[:n])]
		
		line_height = (self.x + self._rectangles[cur_y].size[0])
		return [(self.x + line_height), self.get_len_str(cur_y)]
	
	def last_word(self):
		label  = self._labels[self._cursor[1]]
		get_ext = label.get_extents
		text = label.text
		l_txt = local = len(text)

		for n, i in enumerate(label.text[::-1]):
			local = (l_txt - n - 1)
			if self._cursor[0] > local and i == ' ':
				lbl_w = get_ext(text[:local])[0]
				return [(self.x + lbl_w), len(text[:local])]
		
		lbl_w = get_ext(text[:local])[0]
		return [(self.x + lbl_w), len(text[:local])]
		
	
	def _scroll_up(self):
		cur_sh = self.cursor_size[1]
		recs = self._rectangles
		pos_i = (self.y + self.height - cur_sh)
		
		if self.label_end >= self._n_labels:
			return None
		
		self.canvas.remove(recs[self.label_init])
		
		for rect in recs[ (self.label_init + 1) : (self.label_end + 1) ]:
			rect.pos = [self.x, pos_i]
			pos_i -= cur_sh

		self.canvas.add(recs[self.label_end])

		self.label_init += 1
		self.label_end += 1
		self._cursor_pos[1] += cur_sh
		self.update_selection()

		if self.in_selection:
			self.do_selection()

	def _scroll_down(self):
		if self.label_init == 0:
			return None
		
		cur_sh = self.cursor_size[1]
		recs = self._rectangles
		pos_i = (self.y + self.height - cur_sh)
	
		rect1 = recs[self.label_init-1]
		self.canvas.remove(recs[self.label_end-1])

		for rect in recs[self.label_init:self.label_end-1]:
			pos_i -= cur_sh
			rect.pos = [self.x, pos_i]

		rect1.pos = [ self.x, (self.y + self.height - self.cursor_size[1]) ]
		self.canvas.add(rect1)

		self.label_init -= 1
		self.label_end -= 1
		self._cursor_pos[1] -= cur_sh
		self.update_selection()

		if self.in_selection:
			self.do_selection()

	def key_up(self, window, key, *args):
		if not self.focus:
			return False

		chr_key = ( meta_carac[key] ) if key in meta_carac else ( chr(key) )
		
		if chr_key in {'rshift', 'lshift'}:
			self.shift_pressed = False
		
		elif chr_key in {'rctrl', 'lctrl'}:
			self.ctrl_pressed = False

		elif chr_key in {'ralt', 'lalt', 'alt-gr'}:
			self.alt_pressed = False
		
		return True

	def key_down(self, window, key, *args):
		if not self.focus:
			return False

		chr_key = ( meta_carac[key] ) if key in meta_carac else ( chr(key) )
		
		if chr_key in ['backspace', 'delete']:
			self.backspace()

		elif chr_key == 'enter':
			self.enter()

		elif self.ctrl_pressed and self.shift_pressed and chr_key == 'z':
			self.do_redo()

		elif self.ctrl_pressed and chr_key in ['v', 'c', 'z', 'x']:
			if self.focus:
				func = getattr(self, f'ctrl_{chr_key}')
				func()
		
		elif chr_key in ['up', 'down', 'left', 'right']:
			move_cursor = getattr(self, f'move_cursor_{chr_key}')
			move_cursor([*self.cursor_size, *self._cursor, *self._cursor_pos])
		
		elif chr_key in ['rshift', 'lshift', 'rctrl', 'lctrl']:
			setattr(self, chr_key[1:], True)
		
		elif chr_key in {'ralt', 'lalt', 'alt-gr'}:
			setattr(self, chr_key, True)
		
		elif chr_key == 'capslock':
			self.capslock_pressed = not self.capslock_pressed
		
		elif chr_key in ['tab']:
			self.insert_string(u'\t')
		
		elif chr_key in ['pageup', 'pagedown', 'end', 'home']:
			pass

		self.cursor_clock.timeout = (self.cursor_interval + 1.4)
		self.change_cursor_color("show")
		return True
	
	def keyboard_on_textinput(self, window, chr_key):
		if not self.focus:
			return False
		
		cur_sw, cur_sh = self.cursor_size 

		if self._cursor_pos[0] > (self.x + self.width):
			self._cursor_pos = [ (self.x + cur_sw), (self._cursor_pos[1] - cur_sh) ]
			self._cursor[1] += 1
			self._cursor[0] = 0
		
		self.insert_string(chr_key)

	def _scroll_to(self, cur_y):
		if not self._labels:
			return None
		
		if self.label_init < cur_y:
			lbl_init = (cur_y - self.max_lines + 1)
			lbl_end = (cur_y + 1)
			cur_p = (lbl_end - 1)
		
		elif self.label_init > cur_y:
			lbl_init = cur_y
			lbl_end = (cur_y + self.max_lines)
			cur_p = lbl_init

		self.label_init = lbl_init
		self.label_end = lbl_end
		self._cursor_pos[1] = self._rectangles[cur_p].pos[1]
		self._cursor[1] = cur_y
		self._update_lines()

	@property
	def _label_kwargs(self):
		return {
			'font_size': self.font_size,
			'font_name': self.font_name,
			'font_context': self.font_context,
			'font_family': self.font_family,
			'markup': True,
		}

	def change_line(self, n_text, y_cur, kw):
		label, texture, size = self.make_label(n_text, kw)
		self._labels[y_cur] = label

		self.canvas.remove(self._rectangles[y_cur])
		self._rectangles[y_cur] = Rectangle(texture=texture, size=size,
											pos=[self.x, self._cursor_pos[1]])
		self.canvas.add(self._rectangles[y_cur])

	def make_label(self, text, kwargs):
		n_text = text.replace(u'[', u'&bl;').replace(u']', u'&br;')
		# n_text = ''.join((u'[color=#FF0000]', n_text, u'[/color]'))
		label = CoreLabel(text=n_text, **kwargs)
		label.refresh()
		label.text = text
		return [label, label.texture, label.texture.size]

	def insert_string(self, string, p=-1):
		cur_x, cur_y = self._cursor
		cur_sh = self.cursor_size[1]
		new_cur_y = (self._cursor_pos[1] + cur_sh)

		if self.capslock_pressed or self.shift_pressed and p != -1:
			string = string.upper()

		if string.find(u'\t') != -1:
			string = string.replace(u'\t', u' '*self.tab_width)
			self._cursor[0] += (len(string) - 1)

		if self._n_labels > 0 and self._n_labels > cur_y and p == -1:
			text = self._labels[cur_y].text
			n_text = text[:cur_x] + string + text[cur_x:]
			self.change_line(n_text, cur_y, self._label_kwargs)
		else:
			label, texture, size = self.make_label(string, self._label_kwargs)
			self._labels.insert(p, label)
			self._n_labels += 1

			if self._n_labels <= self.max_lines:
				self.label_end = self._n_labels

			rect = Rectangle(texture=texture, size=size,
		    				 pos=[self.x, self._cursor_pos[1]])
			self._rectangles.insert(p, rect)
			self.canvas.add(rect)

		if p == -1:
			self._cursor[0] += 1
		
		self._cursor_pos[0] = self._x_cursor_by_index(*self._cursor)

		if self._rectangles[self._cursor[1]].pos[1] < self.y or p != -1:
			self._scroll_up()
		
		if string == '' or p != -1:
			self._cursor_pos[1] -= self.cursor_size[1]
		
		if new_cur_y > ( self.y + self.height + cur_sh ) or \
			new_cur_y < ( self.y + (cur_sh * 2) ):
			self._scroll_to(cur_y)

	def change_focus(self, in_focus):
		if in_focus:
			return None
		
		self.focus = in_focus
		self.change_cursor_color("hide")
		self._keyboard_unbind()

	def on_touch_up(self, touch):
		if self.in_selection:
			self.in_selection = False
			self.change_cursor_color("show")
			self.cursor_clock.cancel()
			self.cursor_clock()

		if not self.collide_point(*touch.pos):
			self.change_focus(False)
			return False

	def on_touch_down(self, touch):
		if not self.collide_point(*touch.pos):
			self.change_focus(False)
			return False

		if super().on_touch_down(touch):
			return True

		if self._keyboard == None:
			self._keyboard_bind()

		self.cursor_clock.timeout = (self.cursor_interval + 1.4)
		self.change_cursor_color("show")

		if 'button' in touch.profile and touch.button.startswith('scroll'):
			scroll_type = touch.button[6:]

			if scroll_type == 'down':
				self._scroll_down()
			
			elif scroll_type == 'up':
				self._scroll_up()
		
		elif self.focus:
			self.in_selection = False
			self.remove_selection()
			
			self.get_cursor_by_touch(*touch.pos)
			self.last_cursor_pos = [*self._cursor_pos]
			self.touch_down_pos = [[*self._cursor_pos], [*self._cursor]]
			self.selected = [self._cursor[1], 0]

		self.focus = True
		return True
	
	def on_touch_move(self, touch):
		if not self.focus:
			return None
		
		print("touch.pos -=> ", touch.pos)
		self.get_cursor_by_touch(*touch.pos)
		self.last_cursor_pos = [*self._cursor_pos]
		self.in_selection = True

		if touch.pos[1] <= ( self.y + (self.cursor_size[1] / 2) ):
			self._scroll_up()
		
		elif touch.pos[1] >= ( self.y + self.height - (self.cursor_size[1] / 2) ):
			self._scroll_down()
		
		else:
			self.do_selection()
		

	def get_cursor_by_touch(self, x, y, change=True):
		if not self._labels:
			return None
		
		cur_sh = self.cursor_size[1]
		cur_y = int(round( (( (y - self.y) / cur_sh ) + 0.3), 0 ))
		cur_y = (self.max_lines - cur_y + self.label_init)

		if cur_y >= self._n_labels:
			return None
		
		lbl = self._labels[cur_y]
		l_txt = len(lbl.text)
		width = lbl.size[0]
		divisor = ( max(width, 1) / max(l_txt, 1) )
		cur_x = min( int(round( ((x - self.x) / divisor), 0 )), l_txt)
		
		cur_p = ( self.y + self.height - ( (cur_y - self.label_init) * cur_sh ) - cur_sh )
		if cur_p < self.y:
			cur_p = self._cursor_pos[1]
		
		pos = (self.x + lbl.get_extents(lbl.text[:cur_x])[0])
		if change:
			self._cursor_pos = [pos, cur_p]
			self._cursor = [cur_x, cur_y]

		print("by -=> ", x, y)
		print("position -=> ", [[pos, cur_p], [cur_x, cur_y]])
		return [[pos, cur_p], [cur_x, cur_y]]



if __name__ == '__main__':

	path = r'C:\Users\heito\AppData\Local\Programs\Python\Python39\Lib\site-packages\kivy\uix\textinput.py'
	from kivy.uix.textinput import TextInput

	with open(path, 'r') as file:
		text = ""
		text = file.read()
		# inp = TextInput()
		inp = CodeInput()
		inp.text = text
		runTouchApp(inp)
