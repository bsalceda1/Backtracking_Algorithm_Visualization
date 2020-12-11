import pygame as pg
import time

pg.init()
pg_time = pg.time.Clock()

class Grid:
	sodoku_board = [
		[0,0,2,8,0,0,3,0,0],
		[0,0,0,0,0,9,0,2,0],
		[4,3,7,2,5,6,0,0,0],  
		[1,0,0,0,0,0,0,0,4],
		[3,0,4,0,1,0,6,0,7],
		[5,0,6,4,0,7,0,1,0],
		[6,0,8,1,0,2,4,7,9],
		[0,0,3,5,0,0,0,6,0],
		[0,9,0,7,0,4,0,3,8],
	]

	def __init__(self, rows, cols, height, width):
		self.rows = rows
		self.cols = cols 
		self.height = height
		self.width = width
		self.cubes = [[Cube(self.sodoku_board[y][x], y, x, width, height) for x in range(cols)] for y in range(rows)]

	def draw(self, screen):
		#Fill Background Color
		screen.fill(pg.Color("White"))

		#Draw Grid Lines
		gap = self.width / 9
		for i in range(self.rows+1):
			line_thickness = 4 if i % 3 == 0 else 1
			pg.draw.line(screen, pg.Color("Black"), (0, i*gap), (self.width, i*gap), line_thickness)
			pg.draw.line(screen, pg.Color("Black"), (i*gap, 0), (i*gap, self.width), line_thickness)

		#Draw Cubes
		for y in range(self.rows):
			for x in range(self.rows):
				self.cubes[y][x].draw(screen)

	def find_empty_cube(self):
		for y in range(9):
			for x in range(9):
				if self.cubes[y][x].value == 0:
					return (y, x)

	#Check if new val doesnt break sodoku rule
	def is_valid(self, cube, pos, val):
		#check row
		for x in range(self.rows):
			if self.cubes[pos[0]][x].value == val and x != pos[1]:
				return False
		#check column 
		for y in range(self.cols):
			if self.cubes[y][pos[1]].value == val and y != pos[0]:
				return False

		#check mini box 
		y_mini = pos[0] // 3
		x_mini = pos[1] // 3
		
		for y in range(y_mini*3, y_mini*3 + 3):
			for x in range(x_mini*3, x_mini*3 + 3):
				if self.cubes[y][x].value == val and [y,x] != pos:
					return False

		return True

	def solve_cubes(self):
		#Return True if no more empty spot
		if not self.find_empty_cube():
			return True

		empty = self.find_empty_cube()
		y,x = empty

		for i in range(1,10):
			if self.is_valid(self.cubes, (y,x), i):
				self.cubes[y][x].being_solved = True
				self.cubes[y][x].value = i
				update_board(screen, board)
				pg.display.update()
				print(i, " valid")

				#Solve until it's done
				if self.solve_cubes():
					return True

			self.cubes[y][x].value = 0
			update_board(screen, board)
			pg.display.update()

		return False
				

class Cube:
	def __init__(self, value, row, col, width, height):
		self.value = value
		self.row = row 
		self.col = col
		self.width = width 
		self.height = height
		self.being_solved = False

	def draw(self, screen):
		font = pg.font.SysFont(None, 50)
		gap = self.width / 9
		x = self.col * gap
		y = self.row * gap

		if self.value != 0:
			fnt_color = "Black" if self.being_solved == False else "Red"
			text = font.render(str(self.value), 1, pg.Color(fnt_color))
			screen.blit(text ,(x +(gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/ 2)))


def draw_board(screen , board):
	board.draw(screen)
	board.solve_cubes()

def update_board(screen, board):
	board.draw(screen)

def main_loop():
	global screen, board
	width = 610
	screen_size = width, width
	screen = pg.display.set_mode(screen_size)
	board = Grid(9, 9, width, width)
	run = True
	while run:

		for event in pg.event.get():
			if event.type == pg.QUIT: run = False

		draw_board(screen, board)
		pg.display.update()



if __name__ == "__main__":
	main_loop() 
