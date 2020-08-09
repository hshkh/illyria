import pygame, sys
from pygame.locals import *
from time import sleep

pygame.font.init()

# COLOURS
#             R    G    B
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
HL_COL   = (144, 238, 144)
PINK	 = (222, 165, 164)
PURPLE   = (177, 156, 217)

# DIRECTIONS
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"

class Game:
	'''Main game + attributes.'''
	def __init__(self, loop_mode):
		self.graphics = Graphics()
		self.board = Board()
		self.end_game = False
		self.turn = BLACK
		self.selected_piece = None # a board location.
		self.hop = False
		self.loop_mode = loop_mode
		self.selected_legal_moves = []

	def setup(self):
		'''Initialises the window and board at game start.'''
		self.graphics.setup_window()

	def player_turn(self):
		'''
		Event triggers.
		i.e. Mouse clicks and exiting window.
		'''
		mouse_pos = tuple(map(int, pygame.mouse.get_pos()))
		# mouse loc on board
		self.mouse_pos = tuple(map(int, self.graphics.board_coords(mouse_pos[0], mouse_pos[1])))
		if self.selected_piece != None:
			self.selected_legal_moves = self.board.legal_moves(self.selected_piece[0], self.selected_piece[1], self.hop)

		for event in pygame.event.get():
			
			# 'QUIT' being the 'x' on window bar
			if event.type == QUIT:
				self.terminate_game()
			
			# mouse click event
			if event.type == MOUSEBUTTONDOWN:
				if self.hop == False:
					if self.board.location(self.mouse_pos[0], self.mouse_pos[1]).occupant != None and self.board.location(self.mouse_pos[0], self.mouse_pos[1]).occupant.color == self.turn:
						self.selected_piece = self.mouse_pos

					elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece[0], self.selected_piece[1]):

						self.board.mv_piece(self.selected_piece[0], self.selected_piece[1], self.mouse_pos[0], self.mouse_pos[1])

						if self.mouse_pos not in self.board.adjacent(self.selected_piece[0], self.selected_piece[1]):
							self.board.rm_piece(self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) // 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) // 2)

							self.hop = True
							self.selected_piece = self.mouse_pos
						else:
							self.end_turn()

				if self.hop == True:
					if self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece[0], self.selected_piece[1], self.hop):
						self.board.mv_piece(self.selected_piece[0], self.selected_piece[1], self.mouse_pos[0], self.mouse_pos[1])
						self.board.rm_piece(self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) // 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) // 2)

					if self.board.legal_moves(self.mouse_pos[0], self.mouse_pos[1], self.hop) == []:
							self.end_turn()

					else:
						self.selected_piece = self.mouse_pos


	def update(self):
		'''Calls graphics class and updates display.'''
		self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)
		self.board.capture = False

	def terminate_game(self):
		'''Quits pygame and closes window.'''
		pygame.quit()
		sys.exit()

		while True: # main game loop
			self.player_turn()
			self.update()

	def end_turn(self):
		'''
		Upon a capture.
		End turn and switch player.
		Check for end game and reset class attributes.
		'''
		if self.turn == BLACK:
			self.turn = WHITE
		else:
			self.turn = BLACK

		# reset class attributes
		self.selected_piece = None
		self.selected_legal_moves = []
		self.hop = False

		self.board.capture = True

	def check_for_endgame(self):
		'''If a player has run out of moves or pieces return True otherwise return False.'''
		for x in range(8):
			for y in range(8):
				if self.board.location(x, y).color == BLACK and self.board.location(x, y).occupant != None and self.board.location(x, y).occupant.color == self.turn:
					if self.board.legal_moves(x, y) != []:
						return False
		return True
	
	def check_for_drawgame(self, turn_counter):
		'''If the game has 100 consecutive turns with no captures return True otherwise return False.'''
		if turn_counter == 100 and not self.check_for_endgame():
			return True
		else:
			return False

class Graphics:
	def __init__(self):
		'''Setting window specifications.'''
		self.caption = "Illyria"

		self.icon = pygame.image.load('resources/illyria.png')
		self.screen = pygame.display.set_icon(self.icon)

		# set the fps of the game to 120
		self.fps = 120
		self.clock = pygame.time.Clock()

		self.window_size = 600
		self.screen = pygame.display.set_mode((self.window_size, self.window_size))
		self.background = pygame.image.load('resources/board.png')

		self.square_size = self.window_size // 8
		self.piece_size = self.square_size // 2

		self.message = False

	def setup_window(self):
		'''Initialises window.'''
		pygame.init()
		pygame.display.set_caption(self.caption)

	def update_display(self, board, legal_moves, selected_piece):
		'''Updates display.'''
		self.screen.blit(self.background, (0,0))

		self.highlight_squares(legal_moves, selected_piece)
		self.draw_board_pieces(board)

		if self.message:
			self.screen.blit(self.text_surface_obj, self.text_rect_obj)
			self.screen.blit(self.sec_msg, self.sec_text_rect)

		pygame.display.update()
		self.clock.tick(self.fps)

	def draw_board_squares(self, board):
		'''Draws the sqaures. These are visible when selecting a piece.'''
		for x in range(8):
			for y in range(8):
				pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )

	def draw_board_pieces(self, board):
		'''Draws the pieces on the board.'''

		# load crown
		crown_img = pygame.image.load('resources/crown.png')
		crown_img_s = pygame.transform.scale(crown_img, (30,30))

		for x in range(8):
			for y in range(8):
				if board.matrix[x][y].occupant != None:
					pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color, tuple(map(int, self.pixel_coords((x, y)))), int(self.piece_size))

					if board.location(x,y).occupant.king == True:
						# draws crown to centre of King piece
						self.screen.blit(crown_img_s, (tuple(map(int, self.pixel_coords((x-0.2, y-0.2))))))

	def pixel_coords(self, board_coords):
		'''Returns centre location of passed board_coords.'''
		return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

	def board_coords(self, pixel_x, pixel_y):
		'''Returns square of passed pixel_coords.'''
		return (pixel_x // self.square_size, pixel_y // self.square_size)

	def highlight_squares(self, squares, selected):
		'''Colours the squares (legal moves) and highlights the squares the selected piece can move to.'''
		for square in squares:
			pygame.draw.rect(self.screen, HL_COL, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))

		if selected != None:
			pygame.draw.rect(self.screen, HL_COL, (selected[0] * self.square_size, selected[1] * self.square_size, self.square_size, self.square_size))

	def draw_message(self, message):
		'''Draws message to the screen.'''
		self.message = True
		self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
		self.text_surface_obj = self.font_obj.render(message, True, PINK, BLACK)
		self.text_rect_obj = self.text_surface_obj.get_rect()
		self.text_rect_obj.center = (self.window_size // 2, self.window_size // 2)

		self.sec_font = pygame.font.Font('freesansbold.ttf', 22)
		self.sec_msg = self.sec_font.render('(click to continue)', True, PURPLE)
		self.sec_text_rect = self.sec_msg.get_rect()
		self.sec_text_rect.center = (self.window_size // 2, self.window_size // 2 + 53)

class Board:

	capture = False

	def __init__(self):
		'''Initialise a new board as a matrix.'''
		self.matrix = self.new_board()

	def new_board(self):
		'''Create a new board matrix.'''

		# initialize squares and place them in matrix
		matrix = [[None] * 8 for i in range(8)]
		for x in range(8):
			for y in range(8):
				if (x % 2 != 0) and (y % 2 == 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 != 0) and (y % 2 != 0):
					matrix[y][x] = Square(BLACK)
				elif (x % 2 == 0) and (y % 2 != 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 == 0) and (y % 2 == 0):
					matrix[y][x] = Square(BLACK)

		# initialize the pieces and put them in the appropriate squares
		for x in range(8):
			for y in range(3):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(WHITE)
			for y in range(5, 8):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(BLACK)

		return matrix

	def board_string(self, board):
		'''
		Takes a board and returns a matrix of the board space colors. Used for testing new_board()
		'''

		board_string = [[None] * 8] * 8

		for x in range(8):
			for y in range(8):
				if board[x][y].color == WHITE:
					board_string[x][y] = "WHITE"
				else:
					board_string[x][y] = "BLACK"


		return board_string

	def rel(self, direction, x, y):
		'''
		Returns the coordinates one square in a different direction to (x,y).
		'''
		if direction == NORTHWEST:
			return (x - 1, y - 1)
		elif direction == NORTHEAST:
			return (x + 1, y - 1)
		elif direction == SOUTHWEST:
			return (x - 1, y + 1)
		elif direction == SOUTHEAST:
			return (x + 1, y + 1)
		else:
			return 0

	def adjacent(self, x, y):
		'''Returns a list of squares locations that are diagonally adjacent to (x,y).'''

		return [self.rel(NORTHWEST, x,y), self.rel(NORTHEAST, x,y),self.rel(SOUTHWEST, x,y),self.rel(SOUTHEAST, x,y)]

	def location(self, x, y):
		'''
		Takes a set of coordinates as arguments and returns self.matrix[x][y]
		This can be faster than writing something like self.matrix[coords[0]][coords[1]]
		'''
		x = int(x)
		y = int(y)
		return self.matrix[x][y]

	def blind_legal_moves(self, x, y):
		'''
		Returns a list of blind legal move locations from a set of coordinates (x,y) on the board.
		If that location is empty, then blind_legal_moves() return an empty list.
		'''

		if self.matrix[x][y].occupant != None:

			if self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == BLACK:
				blind_legal_moves = [self.rel(NORTHWEST, x, y), self.rel(NORTHEAST, x, y)]

			elif self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == WHITE:
				blind_legal_moves = [self.rel(SOUTHWEST, x, y), self.rel(SOUTHEAST, x, y)]

			else:
				blind_legal_moves = [self.rel(NORTHWEST, x, y), self.rel(NORTHEAST, x, y), self.rel(SOUTHWEST, x, y), self.rel(SOUTHEAST, x, y)]

		else:
			blind_legal_moves = []

		return blind_legal_moves

	def legal_moves(self, x, y, hop = False):
		'''
		Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
		If that location is empty, then legal_moves() returns an empty list.
		'''
		blind_legal_moves = self.blind_legal_moves(x, y)
		legal_moves = []

		if hop == False:
			for move in blind_legal_moves:
				if hop == False:
					if self.on_board(move[0], move[1]):
						if self.location(move[0], move[1]).occupant == None:
							legal_moves.append(move)

						elif self.location(move[0], move[1]).occupant.color != self.location(x, y).occupant.color and self.on_board(move[0] + (move[0] - x), move[1] + (move[1] - y)) and self.location(move[0] + (move[0] - x), move[1] + (move[1] - y)).occupant == None: # is this location filled by an enemy piece?
							legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		else: # hop == True
			for move in blind_legal_moves:
				if self.on_board(move[0], move[1]) and self.location(move[0], move[1]).occupant != None:
					if self.location(move[0], move[1]).occupant.color != self.location(x, y).occupant.color and self.on_board(move[0] + (move[0] - x), move[1] + (move[1] - y)) and self.location(move[0] + (move[0] - x), move[1] + (move[1] - y)).occupant == None: # is this location filled by an enemy piece?
						legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		return legal_moves

	def rm_piece(self, x, y):
		'''Removes a piece from the board at coords (x,y).'''
		self.matrix[x][y].occupant = None

	def mv_piece(self, start_x, start_y, end_x, end_y):
		'''Moves a piece from coords start(x,y) to end(x,y)'''

		self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
		self.rm_piece(start_x, start_y)

		self.king(end_x, end_y)

	def on_board(self, x, y):
		'''If the passed coords are on the board, return True. Otherwise, return false.'''

		if x < 0 or y < 0 or x > 7 or y > 7:
			return False
		else:
			return True


	def king(self, x, y):
		'''Promotes a Man to a King upon advancing to back line.'''
		if self.location(x, y).occupant != None:
			if (self.location(x, y).occupant.color == BLACK and y == 0) or (self.location(x, y).occupant.color == WHITE and y == 7):
				self.location(x, y).occupant.crown()

class Piece:
	def __init__(self, color, king = False):
		'''Initialise Piece attributes.'''
		self.color = color
		self.king = king
		self.value = 1

	def crown(self):
		'''Initialise King attribute.'''
		self.king = True
		self.value = 2

class Square:
	def __init__(self, color, occupant = None):
		'''Initialise Square attributes.'''
		self.color = color # color is either BLACK or WHITE
		self.occupant = occupant # occupant is a Square object