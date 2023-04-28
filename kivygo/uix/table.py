from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from functools import partial
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.metrics import dp
from math import ceil
from time import time


Builder.load_string("""

<Table>:
	canvas:
		Color:
			rgba:[1, 1, 1, 1]
		Rectangle:
			pos: self.pos
			size: self.size
	
	TableScrollView:
		id: scroll
		effect_cls: 'ScrollEffect'
		on_scroll_y: root.update_grid_y()
		table: root
		
		BoxLayout:
			orientation: 'vertical'
			size_hint: [None, None]
			size: self.minimum_width, self.minimum_height
			
			Widget:
				size_hint: [None, None]
				size: header.size
			
			GridWidget:
				id: body
				size_hint: [None, None]
				cols: 1
				height: self.minimum_height
				table: root
				name: 'body'
	
	FloatLayout:
		size_hint: [None, None]
		size: [0, 0]
		
		ScrollView:
			effect_cls: 'ScrollEffect'
			scroll_x: scroll.scroll_x
			size_hint: [None, None]
			size: [scroll.width, header.height]
			pos: [scroll.x, ( scroll.y + scroll.height-header.height ) ]
			canvas.before:
				Color:
					rgba:[1, 1, 1, 1]
				Rectangle:
					pos: self.pos
					size: self.size
			BoxLayout:
				id: header
				size_hint: [None, None]
				height: self.minimum_height
				table: root
				name: 'header'

<Celula>:
	size_hint: [None, None]
	size: ['100dp', '35dp']
	color: [0, 0, 0, 1]
	canvas.after:
		Color:
			rgba:[0, 0, 0, 1]
		Line:
			rectangle: [*self.pos, *self.size]
			width:dp(1.5)

""")


class GridWidget(GridLayout):
	
	def remove_widget(self, widget, n_widget=None, i_col=0):
		if widget not in self.children:
			return

		funbind = widget.funbind
		funbind('size', self._trigger_layout)
		funbind('size_hint', self._trigger_layout)
		funbind('size_hint_max', self._trigger_layout)
		funbind('size_hint_min', self._trigger_layout)

		if widget.canvas in self.canvas.children:
			self.canvas.remove(widget.canvas)
		
		elif widget.canvas in self.canvas.after.children:
			self.canvas.after.remove(widget.canvas)
		
		elif widget.canvas in self.canvas.before.children:
			self.canvas.before.remove(widget.canvas)
		
		widget.parent = None
		widget.dec_disabled(self._disabled_count)

		for i, child in enumerate(self.children):
			if child == widget:
				self.children.pop(i)
				if n_widget:
					self.add_widget(n_widget, i+i_col)
				break


class Celula(ButtonBehavior, Label):
	def __init__(self, text='', col=0, row=0, **kwargs):
		super().__init__(**kwargs)
		self.text = str(text)
		self.row = row
		self.col = col

	def on_press(self, *args):
		table = self.parent.table
		name = self.parent.name
		if name == 'body':
			table.dispatch('on_cell_body_press', self.row, self.col)
		elif name == 'header':
			table.dispatch('on_cell_haeder_press', self.row, self.col)


class TableScrollView(ScrollView):

	table = None

	def update_from_scroll(self, *largs):
		'''Force the reposition of the content, according to current value of
		:attr:`scroll_x` and :attr:`scroll_y`.

		This method is automatically called when one of the :attr:`scroll_x`,
		:attr:`scroll_y`, :attr:`pos` or :attr:`size` properties change, or
		if the size of the content changes.
		'''
		if not self._viewport:
			self.g_translate.xy = self.pos
			return None
		
		vp = self._viewport

		# update from size_hint
		if vp.size_hint_x is not None:
			
			w = vp.size_hint_x * self.width
			
			if vp.size_hint_min_x is not None:
				w = max(w, vp.size_hint_min_x)
			
			if vp.size_hint_max_x is not None:
				w = min(w, vp.size_hint_max_x)
			
			vp.width = w

		if vp.size_hint_y is not None:
			
			h = vp.size_hint_y * self.height
			
			if vp.size_hint_min_y is not None:
				h = max(h, vp.size_hint_min_y)
			
			if vp.size_hint_max_y is not None:
				h = min(h, vp.size_hint_max_y)
			
			vp.height = h

		if vp.width > self.width or self.always_overscroll:
			
			sw = vp.width - self.width
			x = self.x - self.scroll_x * sw
		else:
			x = self.x

		if vp.height > self.height or self.always_overscroll:
			
			sh = vp.height - self.height
			y = self.y - self.scroll_y * sh
		else:
			y = self.top - vp.height

		# from 1.8.0, we now use a matrix by default, instead of moving the
		# widget position behind. We set it here, but it will be a no-op most
		# of the time.
		vp.pos = 0, 0
		
		if self.table is not None:
			do_scroll_x = self.table.do_scroll_x
			
			if do_scroll_x == -1:
				x += dp(80)
			
			elif do_scroll_x == 1:
				x -= dp(80)
			else:
				self.table.do_scroll_x = None
		
		self.g_translate.xy = [x, y]

		# New in 1.2.0, show bar when scrolling happens and (changed in 1.9.0)
		# fade to bar_inactive_color when no scroll is happening.
		ev = self._bind_inactive_bar_color_ev
		
		if ev is None:
			tr = Clock.create_trigger(self._bind_inactive_bar_color, 0.5)
			ev = self._bind_inactive_bar_color_ev = tr
		
		self.funbind('bar_inactive_color', self._change_bar_color)
		Animation.stop_all(self, '_bar_color')
		self.fbind('bar_color', self._change_bar_color)
		self._bar_color = self.bar_color
		ev()

class Table(BoxLayout):

	header_data = []
	body_data = []
	celulas = []
	header = []
	resizable = True
	data_setted = False
	index_x = 0
	index_y = 0
	do_scroll_x = None
	body_cols = 0
	body_rows = 0

	touch_x = 0
	touch_y = 0

	__events__ = ('on_cell_haeder_press', 'on_cell_body_press')

	def __init__(self, header_data=[], body_data=[], **kwargs):
		super().__init__(**kwargs)
		
		Clock.schedule_once(partial(self.set_data, header_data, body_data))
	
	def set_data(self, header_data, body_data, *args):
		# self.data_setted = True
		self.ids.body.clear_widgets()
		self.ids.header.clear_widgets()

		self.body_cols = int(ceil((self.width)/dp(80.0))) + 6
		self.body_rows = int(ceil((self.height)/dp(40.0))) + 6
		self.ids.body.cols = self.body_cols
		print(self.body_rows, self.body_cols)

		cols = len(header_data)
		rows = len(body_data)
		self.body_data = body_data
		self.header_data = header_data

		max_width = self.get_max_width()
		minus = True if max_width < self.width and self.resizable else False
		width = self.width/dp(80)

		tmp = time()
		
		col_w = self.body_cols
		row_h = self.body_rows

		print(self.ids.body.rows,self.ids.body.cols)
		print(col_w, row_h, self.get_celula_size(minus, 0, width))

		for n_row in range(rows):
			co = []
			for n_col in range(cols):
				size = self.get_celula_size(minus, n_col, width)
				celula = Celula(body_data[n_row][n_col], n_col, n_row, size=size)
				co.append(celula)
				if col_w > 0:
					self.ids.body.add_widget(celula)
					col_w -= 1
			
			if row_h > 0:
				col_w = self.body_cols
				row_h -= 1
			
			self.celulas.append(co)

		print(time()-tmp)
		print(self.ids.body.rows, self.ids.body.cols)

		col_w = self.body_cols
		
		for n_col in range(cols):
			
			size = self.get_celula_size(minus, n_col, width)
			celula = Celula(header_data[n_col]['text'], n_col, size=size)
			self.header.append(celula)
			
			if col_w > 0:
				self.ids.header.add_widget(celula)
				col_w -= 1

		self.ids.header.width = sum(map(lambda x: x.width, self.ids.header.children))
		self.ids.body.width = sum(map(lambda x: x.width, self.ids.header.children))
		
		if not args:
			Clock.schedule_once(self.update_size)

	def on_size(self, *args):
		if not self.get_root_window():
			return None
		# Clock.schedule_once(self.update_size)

	def get_celula_size(self, minus, col, width):
		size = self.header_data[col].get('size')
		
		if size is None or minus:
			return (width, dp(40))
		
		return size

	def get_max_width(self):
		if self.header_data[0].get('size') is not None:
			return sum(map(lambda x: x['size'][0], self.header_data))
		else:
			return self.width

	def update_size(self, *args):
		if not self.data_setted and not self.resizable:
			return None
		else:
			self.data_setted = False
		
		print('Redimensionando')
		width = self.get_max_width()
		minus = True if width < self.width and self.resizable else False
		
		self.ids.header.width = width
		self.ids.body.width = width
		width = self.width/self.ids.body.cols

		for child in self.ids.body.children[::-1]:
			child.size = self.get_celula_size(minus, child.col, width)

		for child in self.ids.header.children[::-1]:
			child.size = self.get_celula_size(minus, child.col, width)

	def on_touch_down(self, touch):
		if not self.collide_point(*touch.pos):
			return False
		
		self.touch_x = touch.x
		return super().on_touch_down(touch)

	def on_touch_move(self, touch):
		dif = touch.x - self.touch_x
		if dif <= -dp(80):
			self.mais_update_grid_x()
			self.touch_x = touch.x
			self.do_scroll_x = -1
		
		elif dif >= dp(80):
			self.menos_update_grid_x()
			self.touch_x = touch.x
			self.do_scroll_x = 1
		
		return super().on_touch_move(touch)
	
	def on_touch_up(self, touch):
		return super().on_touch_up(touch)

	def menos_update_grid_x(self, *args):
		n_header = len(self.header)
		if self.index_x <= 0:
			return None
		
		if not self.get_root_window():
			return None

		for _ in range(1):
			self.index_x -= 1
			for i in range(self.body_rows+1):
				icol = (self.index_x + self.body_cols)
				line = self.celulas[(self.index_y + i)]
				# remove o ultimo e adiciona outro widget no inicio da coluna
				self.ids.body.remove_widget(line[icol], line[self.index_x], self.body_cols-1)
			
			wid = self.header[self.index_x]
			self.ids.header.remove_widget(self.header[icol])
			self.ids.header.add_widget(wid, n_header)

			if self.index_x <= 0:
				break

		self.ids.header.width = sum(map(lambda x: x.width, self.ids.header.children))
		self.ids.body.width = sum(map(lambda x: x.width, self.ids.header.children))

	def mais_update_grid_x(self, *args):
		n_header = len(self.header)
		if self.index_x >= n_header-self.body_cols:
			return None
		
		if not self.get_root_window():
			return None
		
		for _ in range(1):
			
			icol = (self.index_x + self.body_cols)
			
			for i in range(self.body_rows+1):
				line = self.celulas[(self.index_y + i)]
				# remove o primeiro e adiciona outro widget no final da coluna
				self.ids.body.remove_widget(line[self.index_x], line[icol], -(self.body_cols))
			
			wid = self.header[self.index_x]
			self.ids.header.remove_widget(wid)
			self.ids.header.add_widget(self.header[icol])

			self.index_x += 1
			if self.index_x >= n_header-self.body_cols:
				break

		# self.ids.header.width = sum(map(lambda x: x.width, self.ids.header.children))
		# self.ids.body.width = sum(map(lambda x: x.width, self.ids.header.children))

	def update_grid_y(self, *args):
		#0.16
		if not self.get_root_window():
			return None
		# print(self.ids.scroll.scroll_y)

	def on_cell_haeder_press(self, row, col, *args):
		print('Clicou na celula header: ', row, col)    
	
	def on_cell_body_press(self, row, col, *args):
		print('Clicou na celula body: ', row, col)

if __name__ == '__main__':
	from kivy.app import App
	
	columns = tuple({'text':f'Coluna {x}', 'size':(dp(80), dp(40))} for x in range(50))
	data = tuple(tuple(f'Celula {x}' for x in range(50)) for _ in range(50))

	# columns = (
	#     {'text':'ID', 'size':(dp(40), dp(35))}, {'text':'Nome', 'size':(dp(150), dp(35))},
	#     {'text':'Senha', 'size':(dp(180), dp(35))}
	# )
	# data = (('1', 'Heitor', '1234'), ('2', 'SrGambiarra', '4321'), ('3', 'Pitoco', 'bagunceiro'), ('4', 'OK', 'teste'))

	class TableApp(App):
		def build(self):
			return Table(columns, data)
	
	TableApp().run()
