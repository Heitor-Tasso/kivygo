from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivygo.behaviors.drag_and_drop import GoDraggableLayoutBehavior
from kivy.lang.builder import Builder
from kivygo.colors import GoColorBase, GoBackgroundColor
from kivy.uix.layout import Layout
from kivy.properties import BoundedNumericProperty, ListProperty, NumericProperty, VariableListProperty


class NotEnoughCellsException(Exception):
	pass


Builder.load_string("""

<GoGridLayout>:
	background_color: GoColors.no_color
	background_disabled: GoColors.no_color


<GoGridLayoutColor>:
	background_color: GoColors.background_default
	background_hover: GoColors.background_hover
	border_color: GoColors.background_border
	border_hover: GoColors.no_color
	border_disabled: GoColors.no_color

<GoAutoGridLayout>:
		    
<GoAutoGridLayoutColor>:
		    
<GoDraggableGridLayout>:
		    
<GoDraggableGridLayoutColor>:
		    
<GoDynamicGridLayout>:
		    
<GoDynamicGridLayoutColor>:
		    
""")


class GoGridLayout(GoBackgroundColor, GridLayout):
	pass


class GoGridLayoutColor(GoColorBase, GoGridLayout):
	pass


class GoAutoGridLayout(GoGridLayout):

	max_size = ListProperty([dp(235), dp(250)])

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.config)
	
	def config(self, *args):
		Window.bind(on_flip=self.set_grid_cols)
		self.set_grid_cols()


	def on_size(self, *args):
		Clock.schedule_once(self.set_grid_cols)

	def set_grid_cols(self, *args):
		w1, w2 = self.max_size
		tc = max(2, len(self.children)+1)

		for i in range(1, tc):
			w = round(self.width/i)

			if (w > w1 and w < w2) or w < w1:

				self.cols =  i - (1 if w < w1 and i > 1 else 0)
				break

			elif i == (tc - 1):
				
				self.cols = i
				break
		
		self.padding = 0
		self.spacing = 0
		Clock.schedule_once(self.check_max_width)
	
	def check_max_width(self, *args):
		if not self.children:
			return None

		w1, w2 = self.max_size

		if self.cols >= len(self.children):

			if self.children[0].width > (w2+dp(20)):

				t = int( (self.children[0].width - w2) / 2 )
				self.padding = [t, 0, t, 0]
				self.spacing = t
				return None
		
		self.padding = dp(10)
		self.spacing = dp(10)


class GoAutoGridLayoutColor(GoGridLayoutColor, GoAutoGridLayout):
	pass


class GoDraggableGridLayout(GoGridLayout, GoDraggableLayoutBehavior):

	def compare_pos_to_widget(self, widget, pos):
		x, y = pos

		if y > widget.top:
			return 'before'

		elif y < widget.y:
			return 'after'

		elif x > widget.right:
			return 'after'

		elif x < widget.x:
			return 'before'

		else:
			spacer = self.spacer_widget
			if widget.parent is spacer.parent:

				children = widget.parent.children
				if children.index(spacer) > children.index(widget):
					return 'after'

		return 'before'


class GoDraggableGridLayoutColor(GoGridLayoutColor, GoDraggableGridLayout):
	pass


class GoDynamicGridLayout(GoBackgroundColor, Layout):

	cols = BoundedNumericProperty(None, min=0, allownone=True)
	rows = BoundedNumericProperty(None, min=0, allownone=True)
	_grid = ListProperty([])
	
	spacing = NumericProperty(0)

	padding = VariableListProperty([0, 0, 0, 0])
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.bind(
			children=self._trigger_layout,
			size=self._trigger_layout,
			pos=self._trigger_layout
		)

	def add_widget(self, widget):
		if not hasattr(widget, 'colspan'):
			widget.colspan = 1  # TODO warning, not defined as property.

		if not hasattr(widget, 'rowspan'):
			widget.rowspan = 1  # TODO warning, not defined as property.

		return super().add_widget(widget)

	def on_children(self, *args):
		children_cells = sum([c.rowspan * c.colspan for c in self.children])
		total_cells = self.cols * self.rows if not None in {self.cols, self.rows} else None

		if total_cells and children_cells > total_cells:
			raise NotEnoughCellsException(f"Available cells: {total_cells}. Requested cells: {children_cells}. Increase cols and/or rows")

	def do_layout(self, *largs):
		if not self.children:
			return None

		lp, tp, rp, bp = self.padding
		
		cols_width = (self.width - (self.spacing * (self.cols - 1)) - (lp + rp)) / self.cols
		rows_height = (self.height - (self.spacing * (self.rows - 1)) - (tp + bp)) / self.rows
		

		grid = [[0 for j in range(self.cols)] for i in range(self.rows)]
		# A grid with size cols x rows.
		# each position represents a cell. zero means the cell is available,
		
		for c in self.children[::-1]:
			c.width = (cols_width * c.colspan) + (self.spacing * (c.colspan - 1))
			c.height = (rows_height * c.rowspan) + (self.spacing * (c.rowspan - 1))
			# Find next available cell
			cur_row, cur_col = self._next_cell(grid)
			if cur_row == None or cur_col == None:  # TODO raise exception?
				break

			# fill cell or cells in grid according to rowspan, colspan
			for ry in range(c.rowspan):
				# if rowspan > 1 we need to put the widget at the lowest row
				last_row = cur_row + ry
				for rx in range(c.colspan):
					grid[cur_row + ry][cur_col + rx] = c
		
			c.x = (self.x + ((tp + bp)/2) + (cols_width + self.spacing)  * cur_col)
			c.y = (self.y - ((tp + bp)/2) + self.height - rows_height - (rows_height + self.spacing) * last_row)

		self._grid = grid

	def cell(self, row, col):
		"""Returns widget at pos (row, col) in the grid"""
		return self._grid[row - 1][col - 1]

	def _next_cell(self, grid):
		# TODO optimize
		for y in range(len(grid)):
			for x in range(len(grid[0])):
				if grid[y][x] == 0:
					return y, x
		
		return [None, None]


class GoDynamicGridLayoutColor(GoColorBase, GoDynamicGridLayout):
	pass

