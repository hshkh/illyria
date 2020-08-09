import pygame, sys
from pygame.locals import *
import draughts
import illyria
from datetime import datetime
import argparse

# COLOURS
#             R    G    B
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)

def main():
	'''Main method.'''

	parser = inputhandler()

	args = vars(parser.parse_args())
	'''Default to watching the computer play.'''
	if args['gamemode'] is None:
		args['gamemode'] = 's'

	game_counter = 50
	game_number = 0

	if args['gamemode'] == 's':

		print('To play, add the following command line argument:')
		print('-g p')

		while game_counter != 0:
			turn_counter = 0
			start = datetime.now()
			game_number += 1
			n_steps = 0
			game = draughts.Game(loop_mode=True)
			game.setup()

			bot = illyria.AI(game, BLACK, method='alpha_beta', depth=3)

			bot2 = illyria.AI(game, WHITE, method='alpha_beta', depth=3)
			
			while True:

				for event in pygame.event.get():
							if event.type == QUIT:
								game.terminate_game()

				if game.turn == BLACK:

					turn_counter += 1

					_ = bot.compute(game.board, True)
					
					if game.board.capture:
						turn_counter = 0

					if game.check_for_drawgame(turn_counter):
						print('DRAW GAME.')
						game.graphics.draw_message("DRAW GAME.")
						if(game.loop_mode):
							game.end_game = True
					
					if game.check_for_endgame():
						if game.turn == BLACK:
							print('WHITE WINS!')
							game.graphics.draw_message("WHITE WINS!")
						elif game.turn == WHITE:
							print('BLACK WINS!')
							game.graphics.draw_message("BLACK WINS!")
						else:
							print('DRAW GAME.')
							game.graphics.draw_message("DRAW GAME.")
						
						if(game.loop_mode):
							game.end_game = True

					game.update()

				else:

					turn_counter += 1

					_ = bot2.compute(game.board, True)

					if game.board.capture:
						turn_counter = 0
					
					if game.check_for_drawgame(turn_counter):
						print('DRAW GAME.')
						game.graphics.draw_message("DRAW GAME.")
						if(game.loop_mode):
							game.end_game = True
					
					if game.check_for_endgame():
						if game.turn == BLACK:
							print('WHITE WINS!')
							game.graphics.draw_message("WHITE WINS!")
						elif game.turn == WHITE:
							print('BLACK WINS!')
							game.graphics.draw_message("BLACK WINS!")
						else:
							print('DRAW GAME.')
							game.graphics.draw_message("DRAW GAME.")
						
						if(game.loop_mode):
							game.end_game = True
					
					game.update()
				if game.end_game:
					end = datetime.now()
					# testing : print duration of game (hh:mm:ss.ms)
					# print('game {} : game duration : {}'.format(game_number, end - start))
					while game.end_game:
						for event in pygame.event.get():
							if event.type == QUIT:
								game.terminate_game()
							if event.type == MOUSEBUTTONDOWN:
								game.end_game = False
								break
					break

	if args['gamemode'] == 'p':

		print('To spectate, add the following command line argument:')
		print('-g s')

		while game_counter != 0:
			turn_counter = 0
			start = datetime.now()
			game_number += 1
			n_steps = 0
			game = draughts.Game(loop_mode=True)
			game.setup()

			bot = illyria.AI(game, WHITE, method='alpha_beta', depth=3)
			
			while True:
				if game.turn == BLACK:

					game.player_turn()

					if game.board.capture:
						turn_counter = 0
					
					if game.check_for_endgame():
						if game.turn == BLACK:
							print('WHITE WINS!')
							game.graphics.draw_message("WHITE WINS!")
						elif game.turn == WHITE:
							print('BLACK WINS!')
							game.graphics.draw_message("BLACK WINS!")
						else:
							print('DRAW GAME.')
							game.graphics.draw_message("DRAW GAME.")
						
						if(game.loop_mode):
							game.end_game = True

					game.update()
				else:

					turn_counter += 2

					_ = bot.compute(game.board, True)

					if game.board.capture:
						turn_counter = 0
					
					if game.check_for_drawgame(turn_counter):
						print('DRAW GAME.')
						game.graphics.draw_message("DRAW GAME.")
						if(game.loop_mode):
							game.end_game = True
					
					if game.check_for_endgame():
						if game.turn == BLACK:
							print('WHITE WINS!')
							game.graphics.draw_message("WHITE WINS!")
						elif game.turn == WHITE:
							print('BLACK WINS!')
							game.graphics.draw_message("BLACK WINS!")
						else:
							print('DRAW GAME.')
							game.graphics.draw_message("DRAW GAME.")
						
						if(game.loop_mode):
							game.end_game = True
					
					game.update()
				if game.end_game:
					end = datetime.now()
					# testing : print duration of game (hh:mm:ss.ms)
					# print('game {} : game duration : {}'.format(game_number, end - start))
					while game.end_game:
						for event in pygame.event.get():
							if event.type == QUIT:
								game.terminate_game()
							if event.type == MOUSEBUTTONDOWN:
								game.end_game = False
								break
					break
		

def inputhandler():
	'''User input handler.'''
	parser = argparse.ArgumentParser(description='Set a game mode.')
	parser.add_argument(
		'-g', '--gamemode', help='Type "p" to play or "s" to spectate.', required=False
	)
	return parser

if __name__ == "__main__":
	main()
	pass
