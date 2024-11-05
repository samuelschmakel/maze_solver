from cell import Cell
import random
import time

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed
        if not self._seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
    
    def _draw_cell(self, i, j):
        x1 = self._x1 + (i * self._cell_size_x)
        x2 = x1 + self._cell_size_x
        y1 = self._y1 + (j * self._cell_size_y)
        y2 = y1 + self._cell_size_y

        self._cells[i][j].draw(x1,y1,x2,y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        row_index = len(self._cells[0]) - 1
        col_index = len(self._cells) - 1
        self._cells[col_index][row_index].has_bottom_wall = False
        self._draw_cell(col_index, row_index)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            # Check right
            if i != len(self._cells)-1 and self._cells[i+1][j].visited == False:
                to_visit.append((i+1,j, "right"))

            # Check down
            if j != len(self._cells[0])-1 and self._cells[i][j+1].visited == False:
                to_visit.append((i,j+1, "down"))

            # Check left
            if i != 0 and self._cells[i-1][j].visited == False:
                to_visit.append((i-1,j, "left"))

            # Check up
            if j != 0 and self._cells[i][j-1].visited == False:
                to_visit.append((i,j-1, "up"))

            # If we've reached a dead end, return
            if not to_visit:
                self._draw_cell(i, j)
                return
            
            #print(f"to_visit: {to_visit}")
            # Pick a random direction
            c = random.choice(to_visit)

            if c[2] == "right":
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False
            if c[2] == "down":
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False
            if c[2] == "left":
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False
            if c[2] == "up":
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False

            self._break_walls_r(c[0],c[1])

    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[0])):
                self._cells[i][j].visited = False
        print("Done!")

    def solve(self):
        return self._solve_r(0,0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == len(self._cells)-1 and j == len(self._cells[0])-1:
            return True
        # Checking bottom
        if j != len(self._cells[0])-1:
            if self._cells[i][j].has_bottom_wall == False and not self._cells[i][j+1].visited:
                self._cells[i][j].draw_move(self._cells[i][j+1])
                if self._solve_r(i, j+1):
                    return True
                self._cells[i][j].draw_move(self._cells[i][j+1], True)

        # Checking right
        if i != len(self._cells)-1:
            if self._cells[i][j].has_right_wall == False and not self._cells[i+1][j].visited:
                self._cells[i][j].draw_move(self._cells[i+1][j])
                if self._solve_r(i+1, j):
                    return True
                self._cells[i][j].draw_move(self._cells[i+1][j], True)

        # Checking left
        if i != 0:
            if self._cells[i][j].has_left_wall == False and not self._cells[i-1][j].visited:
                self._cells[i][j].draw_move(self._cells[i-1][j])
                if self._solve_r(i-1, j):
                    return True
                self._cells[i][j].draw_move(self._cells[i-1][j], True)

        # Checking top
        if j != 0:
            if self._cells[i][j].has_top_wall == False and not self._cells[i][j-1].visited:
                self._cells[i][j].draw_move(self._cells[i][j-1])
                if self._solve_r(i, j-1):
                    return True
                self._cells[i][j].draw_move(self._cells[i][j-1], True)

        print("At ending False")
        print(f"i, j: {i}, {j}")
        return False