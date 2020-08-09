import pygame, sys, random, math
from pygame.locals import *
from copy import deepcopy
from time import sleep
pygame.font.init()

# COLOURS
#             R    G    B
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)

class AI:
	def __init__(self, game, color, method='alpha_beta', depth=1):
		'''Initialise the AI player.'''
		
		# pass method in main
		# defaults to 'alpha_beta' (optimal)
		# 'minimax' / 'alpha_beta'
		self.method = method

		# mid evaluation
		self.mid = self.pnl
		# end evaluation
		self.end = self.sum_dist
		
		self.depth = depth
		self.game = game
		self.color = color

		self.eval_colour = color
		
		# initialise opponent colour
		if self.color == BLACK:
			self.opp_color = WHITE
		else:
			self.opp_color = BLACK
		
		# current evaluation
		self.currentv = self.mid
		# bool to store check for endgame evaluation
		self.end_bool = False
		self.node_counter = 0

	def compute(self, board, return_node_counter=False):
		'''Carries out the algorithm for the turn, using defined evaluation functions.'''
		self.node_counter = 0
		if(self.end is not None and not self.end_bool):
			# if only kings, end evaluation in effect
			if self.kings(board):
				# end eval
				self.end_bool = True
				self.currentv = self.end
		if self.method == 'minimax':
			self.minimax(board)
		elif self.method == 'alpha_beta':
			self.alphabeta(board)
		if return_node_counter:
			return self.node_counter

	def minimax(self, board):
		# temp to store max/min value generated for algorithm
		mm_move, mm_decision, temp = self.mm(self.depth - 1, board, 'max')
		self.move(mm_move, mm_decision, board)

	def alphabeta(self, board):
		# temp to store max/min value generated for algorithm
		# -inf and +inf passed as initial values for alpha and beta
		ab_move, ab_decision, temp = self.ab(self.depth - 1, board, 'max', alpha=-float('inf'), beta=float('inf'))
		self.move(ab_move, ab_decision, board)
	
	# minimax
	def mm(self, depth, board, player):
		'''Minimax Algorithm.'''
		if depth == 0:
			if player == 'max':
				max_val = -float("inf")
				opt_pos = None
				opt_move = None
				for moves in self.gen_move(board):
					for mv in moves[2]:
						# copy board to avoid overwrites
						board_copy = deepcopy(board)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						self.move_on_board(board_copy, moves, mv)
						self.node_counter += 1
						heur_val = self.currentv(board_copy)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color

						if heur_val > max_val:
							max_val = heur_val
							opt_pos = moves
							opt_move = (mv[0], mv[1])
						elif heur_val == max_val and random.random() <= 0.5:
							max_val = heur_val
							opt_pos = (moves[0], moves[1])
							opt_move = (mv[0], mv[1])
						if(heur_val == -float("inf") and opt_pos is  None):
							opt_pos = (moves[0], moves[1])
							opt_move = (mv[0], mv[1])
				return opt_pos, opt_move, max_val
			else:
				min_val = float("inf")
				opt_pos = None
				opt_move = None
				for moves in self.gen_move(board):
					for mv in moves[2]:
						# copy board to avoid overwrites
						board_copy = deepcopy(board)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						self.node_counter += 1
						self.move_on_board(board_copy, moves, mv)
						heur_val = self.currentv(board_copy)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						if heur_val < min_val:
							min_val = heur_val
							opt_pos = moves
							opt_move = mv
						elif heur_val == min_val and random.random() <= 0.5:
							min_val = heur_val
							opt_pos = moves
							opt_move = mv
						if(heur_val == float("inf") and opt_pos is  None):
							opt_pos = (moves[0], moves[1])
							opt_move = (mv[0], mv[1])
				return opt_pos, opt_move, min_val
		else:
			if player == 'max':
				max_val = -float("inf")
				opt_pos = None
				opt_move = None
				for moves in self.gen_move(board):
					for mv in moves[2]:
						# copy board to avoid overwrites
						board_copy = deepcopy(board)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						self.move_on_board(board_copy, moves, mv)
						self.node_counter += 1
						if self.endgame(board_copy):
							heur_val = float("inf")
						else:
							temp, temp, heur_val = self.mm(depth - 1, board_copy, 'min')
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						if(heur_val is None):
							continue
						if heur_val > max_val:
							max_val = heur_val
							opt_pos = moves
							opt_move = mv
						elif heur_val == max_val and random.random() <= 0.5:
							max_val = heur_val
							opt_pos = moves
							opt_move = mv
						if(heur_val == -float("inf") and opt_pos is  None):
							opt_pos = (moves[0], moves[1])
							opt_move = (mv[0], mv[1])
				return opt_pos, opt_move, max_val
			else:
				min_val = float("inf")
				opt_pos = None
				opt_move = None
				for moves in self.gen_move(board):
					for mv in moves[2]:
						# copy board to avoid overwrites
						board_copy = deepcopy(board)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						self.node_counter += 1
						self.move_on_board(board_copy, moves, mv)
						if self.endgame(board_copy):
							heur_val = -float("inf")
						else:
							temp, temp, heur_val = self.mm( depth - 1, board_copy, 'max')
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						if(heur_val is None):
							continue
						if heur_val < min_val:
							min_val = heur_val
							opt_pos = (moves[0], moves[1])
							opt_move = (mv[0], mv[1])
						elif heur_val == min_val and random.random() <= 0.5:
							min_val = heur_val
							opt_pos = moves
							opt_move = mv
						if(heur_val == float("inf") and opt_pos is  None):
							opt_pos = (moves[0], moves[1])
							opt_move = (mv[0], mv[1])
				return opt_pos, opt_move, min_val
	
	# alphabeta
	def ab(self, depth, board, player, alpha, beta):
		'''Alpha-beta Pruning.'''
		if depth == 0:
			if player == 'max':
				max_val = -float("inf")
				opt_pos = None
				opt_move = None
				for moves in self.gen_move(board):
					for mv in moves[2]:
						# copy board to avoid overwrites
						board_copy = deepcopy(board)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						self.node_counter += 1
						self.move_on_board(board_copy, moves, mv)
						heur_val = self.currentv(board_copy)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						if heur_val > max_val:
							max_val = heur_val
							opt_pos = moves
							opt_move = (mv[0], mv[1])
						elif heur_val == max_val and random.random() <= 0.5:
							max_val = heur_val
							opt_pos = (moves[0], moves[1])
							opt_move = (mv[0], mv[1])
						if(heur_val == -float("inf") and opt_pos is  None):
							opt_pos = (moves[0], moves[1])
							opt_move = (mv[0], mv[1])
						alpha = max(alpha, max_val)
						if alpha > beta:
							# beta cutoff
							break
					if alpha > beta:
						# beta cutoff
						break
				return opt_pos, opt_move, max_val
			else:
				min_val = float("inf")
				opt_pos = None
				opt_move = None
				for moves in self.gen_move(board):
					for mv in moves[2]:
						# copy board to avoid overwrites
						board_copy = deepcopy(board)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						self.move_on_board(board_copy, moves, mv)
						self.node_counter += 1
						heur_val = self.currentv(board_copy)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						if heur_val < min_val:
							min_val = heur_val
							opt_pos = moves
							opt_move = mv
						elif heur_val == min_val and random.random() <= 0.5:
							min_val = heur_val
							opt_pos = moves
							opt_move = mv
						if(heur_val == float("inf") and opt_pos is  None):
							opt_pos = (moves[0], moves[1])
							opt_move = (mv[0], mv[1])
						beta = min(beta, min_val)
						if alpha > beta:
							# alpha cutoff
							break
					if alpha > beta:
						# alpha cutoff
						break
				return opt_pos, opt_move, min_val
		else:
			if player == 'max':
				max_val = -float("inf")
				opt_pos = None
				opt_move = None
				for moves in self.gen_move(board):
					for mv in moves[2]:
						# copy board to avoid overwrites
						board_copy = deepcopy(board)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						self.move_on_board(board_copy, moves, mv)
						self.node_counter += 1
						if self.endgame(board_copy):
							heur_val = float("inf")
						else:
							temp, temp, heur_val = self.ab(depth - 1, board_copy, 'min', alpha, beta)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						if(heur_val is None):
							continue
						if heur_val > max_val:
							max_val = heur_val
							opt_pos = moves
							opt_move = mv
						elif heur_val == max_val and random.random() <= 0.5:
							max_val = heur_val
							opt_pos = moves
							opt_move = mv
						if(heur_val == -float("inf") and opt_pos is  None):
							opt_pos = (moves[0], moves[1])
							opt_move = (mv[0], mv[1])
						alpha = max(alpha, max_val)
						if alpha >= beta:
							# beta cutoff
							break
					if alpha > beta:
						# alpha cutoff
						break
				return opt_pos, opt_move, max_val
			else:
				min_val = float("inf")
				opt_pos = None
				opt_move = None
				for moves in self.gen_move(board):
					for mv in moves[2]:
						# copy board to avoid overwrites
						board_copy = deepcopy(board)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						self.node_counter += 1
						self.move_on_board(board_copy, moves, mv)
						if self.endgame(board_copy):
							heur_val = -float("inf")
						else:
							temp, temp, heur_val = self.ab( depth - 1, board_copy, 'max', alpha, beta)
						self.color, self.opp_color = self.opp_color, self.color
						self.game.turn = self.color
						if(heur_val is None):
							continue
						if heur_val < min_val:
							min_val = heur_val
							opt_pos = (moves[0], moves[1])
							opt_move = (mv[0], mv[1])
						elif heur_val == min_val and random.random() <= 0.5:
							min_val = heur_val
							opt_pos = moves
							opt_move = mv
						if(heur_val == float("inf") and opt_pos is  None):
							opt_pos = (moves[0], moves[1])
							opt_move = (mv[0], mv[1])
						beta = min(beta, min_val)
						if alpha > beta:
							# alpha cutoff
							break
					if alpha > beta:
						# alpha
						break
				return opt_pos, opt_move, min_val
	
	def move(self, start_pos, end_pos, board):
		'''Computer move function.'''
		if start_pos is None:
			self.game.end_turn()
		
		# if no where to go, end game
		if end_pos is None:
			self.end_game = True

		if not self.game.hop and end_pos is not None:
			# if not a hop
			if board.location(end_pos[0], end_pos[1]).occupant != None and board.location(end_pos[0], end_pos[1]).occupant.color == self.game.turn:
				start_pos = end_pos
			
			# otherwise, if 
			elif start_pos != None and end_pos in board.legal_moves(start_pos[0], start_pos[1]):
				# move piece
				board.mv_piece(
					start_pos[0], start_pos[1], end_pos[0], end_pos[1])

				if end_pos not in board.adjacent(start_pos[0], start_pos[1]):
					
					# remove piece (capture)
					board.rm_piece(start_pos[0] + (end_pos[0] - start_pos[0]) // 2, start_pos[1] + (end_pos[1] - start_pos[1]) // 2)

					self.game.hop = True
					start_pos = end_pos
					end_pos = board.legal_moves(start_pos[0], start_pos[1], True)
					if end_pos != []:
						# hop
						self.move(start_pos, end_pos[0], board)
					self.game.end_turn()

		if self.game.hop:
			if start_pos != None and end_pos in board.legal_moves(start_pos[0], start_pos[1], self.game.hop):
				
				# move piece
				board.mv_piece(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
				
				# remove piece (capture)
				board.rm_piece(start_pos[0] + (end_pos[0] - start_pos[0]) // 2, start_pos[1] + (end_pos[1] - start_pos[1]) // 2)

			if board.legal_moves(end_pos[0], end_pos[1], self.game.hop) == []:
				self.game.end_turn()
			else:
				start_pos = end_pos
				end_pos = board.legal_moves(start_pos[0], start_pos[1], True)
				if end_pos != []:
					# hop
					self.move(start_pos, end_pos[0], board)
				self.game.end_turn()
		if not self.game.hop:
			self.game.turn = self.opp_color
	
	# move piece
	def move_on_board(self, board, start_pos, end_pos, hop=False):
		if not hop:
			if board.location(end_pos[0], end_pos[1]).occupant != None and board.location(end_pos[0], end_pos[1]).occupant.color == self.game.turn:
				start_pos = end_pos

			elif start_pos != None and end_pos in board.legal_moves(start_pos[0], start_pos[1]):

				# move piece
				board.mv_piece(
					start_pos[0], start_pos[1], end_pos[0], end_pos[1])

				if end_pos not in board.adjacent(start_pos[0], start_pos[1]):
					
					# remove piece (capture)
					board.rm_piece(start_pos[0] + (end_pos[0] - start_pos[0]) // 2, start_pos[1] + (end_pos[1] - start_pos[1]) // 2)

					hop = True
					start_pos = end_pos
					end_pos = board.legal_moves(start_pos[0], start_pos[1], True)
					if end_pos != []:
						# hop
						self.move_on_board(board, start_pos, end_pos[0],hop=True)
		else:
			if start_pos != None and end_pos in board.legal_moves(start_pos[0], start_pos[1], hop):

				# move piece
				board.mv_piece(start_pos[0], start_pos[1], end_pos[0], end_pos[1])

				# remove piece (capture)
				board.rm_piece(start_pos[0] + (end_pos[0] - start_pos[0]) // 2, start_pos[1] + (end_pos[1] - start_pos[1]) // 2)

			if board.legal_moves(end_pos[0], end_pos[1], self.game.hop) == []:
				return
			else:
				start_pos = end_pos
				end_pos = board.legal_moves(start_pos[0], start_pos[1], True)
				if end_pos != []:
					# hop
					self.move_on_board(board, start_pos, end_pos[0],hop=True)
	
	# generate a potential move
	def gen_move(self, board):
		for i in range(8):
			for j in range(8):
				if(board.legal_moves(i, j, self.game.hop) != [] and board.location(i, j).occupant != None and board.location(i, j).occupant.color == self.game.turn):
					yield (i, j, board.legal_moves(i, j, self.game.hop))

	# mid game evaluation function
	# piece and location heuristic
	def pnl(self, board):
		'''
		Mid game evaluation. Piece and Location.
		+1 : Piece in own half.
		+2 : Piece in opponent's half.
		+3 : For every King piece.
		'''
		score = 0
		if(self.eval_colour == WHITE):
			for i in range(8):
				for j in range(8):
					occupant = board.location(i, j).occupant
					if(occupant is not None):
						if occupant.color == self.eval_colour and occupant.king:
							score += 3
						elif occupant.color != self.eval_colour and occupant.king:
							score -= 3
						elif occupant.color == self.eval_colour and j < 4:
							score += 1
						elif occupant.color != self.eval_colour and j < 4:
							score -= 2
						elif occupant.color == self.eval_colour and j >= 4:
							score += 2
						elif occupant.color != self.eval_colour and j >= 4:
							score -= 1
		else:
			for i in range(8):
				for j in range(8):
					occupant = board.location(i, j).occupant
					if(occupant is not None):
						if occupant.color == self.eval_colour and occupant.king:
							score += 3
						elif occupant.color != self.eval_colour and occupant.king:
							score -= 3
						elif occupant.color == self.eval_colour and j < 4:
							score += 2
						elif occupant.color != self.eval_colour and j < 4:
							score -= 1
						elif occupant.color == self.eval_colour and j >= 4:
							score += 2
						elif occupant.color != self.eval_colour and j >= 4:
							score -= 1
		return score
	
	# check if board contains only king pieces
	def kings(self, board):
		'''Returns True if only Kings on board, otherwise returns False.'''
		for i in range(8):
			for j in range(8):
				occupant = board.location(i, j).occupant
				if(occupant is not None and not occupant.king):
					return False
		return True
	
	# distance formula
	def dist(self, x1, y1, x2, y2):
		'''Calculate distance between two points.'''
		return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
	
	# end evaluation
	def sum_dist(self, board):
		'''Sum of distances between player 1 and player 2 King pieces.'''
		player_1, player_2 = self.locate_all(board)
		t_dist = 0
		for moves in player_1:
			for opp in player_2:
				t_dist += self.dist(moves[0], moves[1], opp[0], opp[1])
		if(len(player_1) >= len(player_2)):
			t_dist *= -1
		return t_dist

	# location of pieces
	def locate_all(self, board):
		'''Returns and stores all pieces locations.'''
		player_1 = []
		player_2 = []
		for i in range(8):
			for j in range(8):
				occupant = board.location(i, j).occupant
				if(occupant is not None):
					if(occupant.color == self.eval_colour):
						player_1.append((i, j))
					else:
						player_2.append((i, j))
		return player_1, player_2
	
	# check if endgame
	def endgame(self, board):
		'''Checks if any legal moves left. Returns True if no legal moves otherwise returns False.'''
		for x in range(8):
			for y in range(8):
				if board.location(x, y).color == BLACK and board.location(x, y).occupant != None and board.location(x, y).occupant.color == self.game.turn:
					if board.legal_moves(x, y) != []:
						return False
		return True
