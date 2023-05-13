
from kivy.uix.layout import Layout
from kivy.properties import BoundedNumericProperty, ListProperty


class NotEnoughCellsException(Exception):
    pass


class SimpleTableLayout(Layout):

    cols = BoundedNumericProperty(None, min=0, allownone=True)
    rows = BoundedNumericProperty(None, min=0, allownone=True)
    _grid = ListProperty([])

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
        total_cells = self.cols * \
            self.rows if self.cols is not None and self.rows is not None else None

        if total_cells and children_cells > total_cells:
            raise NotEnoughCellsException(f"Available cells: {total_cells}. Requested cells: {children_cells}. Increase cols and/or rows")

    def do_layout(self, *largs):
        if not self.children:
            return None

        cols_width = self.width / self.cols
        rows_height = self.height / self.rows

        grid = [[0 for x in range(self.cols)] for y in range(self.rows)]
        # A grid with size cols x rows.
        # each position represents a cell. zero means the cell is available,
        
        for c in self.children[::-1]:
            c.size = cols_width * c.colspan, rows_height * c.rowspan
            # Find next available cell
            cur_row, cur_col = self._next_cell(grid)
            if cur_row is None or cur_col is None:  # TODO raise exception?
                break

            # fill cell or cells in grid according to rowspan, colspan
            for ry in range(c.rowspan):
                # if rowspan > 1 we need to put the widget at the lowest row
                last_row = cur_row + ry
                for rx in range(c.colspan):
                    grid[cur_row + ry][cur_col + rx] = c
            
            c.x = (self.x + cols_width * cur_col)
            c.y = (self.y + self.height - rows_height - rows_height * last_row)

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

