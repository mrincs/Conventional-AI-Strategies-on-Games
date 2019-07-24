import time
import gamePlay
from copy import deepcopy

def eval_func(board, player):

	opponent = flip_player(player)
	weighted_sum_player = 0
	weighted_sum_opp = 0
	location_wt = [[-22, -18, -14, -12, -12, -14, -18, -22],
					[-18, -5, -1, 1, 1, -1, -5, -18],
					[-14, -1, 10, 12, 12, 10, -1, -14],
					[-12, 1, 12, 22, 22, 12, 1, -12],
					[-12, 1, 12, 22, 22, 12, 1, -12],
					[-14, -1, 10, 12, 12, 10, -1, -14],
					[-18, -5, -1, 1, 1, -1, -5, -18],
					[-22, -18, -14, -12, -12, -14, -18, -22]]
	for i in range(8):
		for j in range(8):
			if board[i][j] == player:
				weighted_sum_player += location_wt[i][j]
			elif board[i][j] == opponent:
				weighted_sum_opp += location_wt[i][j]
	if (weighted_sum_player + weighted_sum_opp) != 0:
		#combined_heuristic_value = eval_func2(board, player)
		#print "Combined Eval Func : ", combined_heuristic_value
		#print "Weighted Eval Func : ", 100 * (weighted_sum_player - weighted_sum_opp) / (weighted_sum_player + weighted_sum_opp)
		return 100 * (weighted_sum_player - weighted_sum_opp) / (weighted_sum_player + weighted_sum_opp) +  eval_func2(board, player)
	else:
		return eval_func2(board, player)

def eval_func2(board, player):

	opponent = flip_player(player)
	player_count = 0
	opponent_count = 0
	player_possible_moves = 0
	opponent_possible_moves =0
	player_corners_cnt = 0
	opponent_corners_cnt = 0
	for i in range(8):
		for j in range(8):
			if board[i][j] == player:
				player_count += 1
				if i == 0:
					if j == 0:
						player_corners_cnt += 1
					if j == 7:
						player_corners_cnt += 1
				if i == 7:
					if j == 0:
						player_corners_cnt += 1
					if j == 7:
						player_corners_cnt += 1

			elif board[i][j] == opponent:
				opponent_count += 1
				if i == 0:
					if j == 0:
						opponent_corners_cnt += 1
					if j == 7:
						opponent_corners_cnt += 1
				if i == 7:
					if j == 0:
						opponent_corners_cnt += 1
					if j == 7:
						opponent_corners_cnt += 1
			if gamePlay.valid(board, player, (i,j)):
				player_possible_moves += 1
			if gamePlay.valid(board, opponent, (i,j)):
				opponent_possible_moves += 1
	if (player_count + opponent_count) != 0:
		coin_diff_heuristic_value =  100 * (player_count - opponent_count) / (player_count + opponent_count)
	else:
		coin_diff_heuristic_value = 0
	if (player_possible_moves + opponent_possible_moves) != 0:
		mobility_heuristic_value = 100 * (player_possible_moves - opponent_possible_moves) / (player_possible_moves + opponent_possible_moves)
	else:
		mobility_heuristic_value = 0
	if (player_corners_cnt + opponent_corners_cnt) != 0:
		corners_heuristic_value = 100 * (player_corners_cnt - opponent_corners_cnt) / (player_corners_cnt + opponent_corners_cnt)
	else:
		corners_heuristic_value = 0
	#print coin_diff_heuristic_value, mobility_heuristic_value, corners_heuristic_value
	combined_heuristic_value = (coin_diff_heuristic_value + mobility_heuristic_value + corners_heuristic_value) / 3
	return combined_heuristic_value

def eval_func1(board, player):
	combined_heuristic_value = coin_parity(board, player) + mobility(board, player) + corners(board, player)
	return combined_heuristic_value/3

# Heuristic component 1
def coin_parity(board, player):

	opponent = flip_player(player)
	player_count = 0
	opponent_count = 0
	for i in range(8):
		for j in range(8):
			if board[i][j] == player:
				player_count += 1
			elif board[i][j] == opponent:
				opponent_count += 1
	heuristic_value =  100 * (player_count - opponent_count) / (player_count + opponent_count)
	#print gamePlay.printBoard(board)
	#print "[White, Black, Heuristic]: " ,whites, blacks, heuristic_value
	return heuristic_value

# Heuristic component 2
def mobility(board, player):

	opponent = flip_player(player)
	player_possible_moves = 0
	opponent_possible_moves =0
	for i in range(8):
		for j in range(8):
			if gamePlay.valid(board, player, (i,j)):
				player_possible_moves += 1
			if gamePlay.valid(board, opponent, (i,j)):
				opponent_possible_moves += 1
	if (player_possible_moves + opponent_possible_moves) != 0:
		heuristic_value = 100 * (player_possible_moves - opponent_possible_moves) / (player_possible_moves + opponent_possible_moves)
	else:
		heuristic_value = 0
	return heuristic_value

# Heuristic component 3
def corners(board, player):

	opponent = flip_player(player)
	player_corners_cnt = 0
	opponent_corners_cnt = 0
	if board[0][0] == player:
		player_corners_cnt += 1
	elif board[0][0] == opponent:
		opponent_corners_cnt += 1
	if board[0][7] == player:
		player_corners_cnt += 1
	elif board[0][7] == opponent:
		opponent_corners_cnt += 1
	if board[7][0] == player:
		player_corners_cnt += 1
	elif board[7][0] == opponent:
		opponent_corners_cnt += 1
	if board[7][7] == player:
		player_corners_cnt += 1
	elif board[7][7] == opponent:
		opponent_corners_cnt += 1
	if (player_corners_cnt + opponent_corners_cnt) != 0:
		heuristic_value = 100 * (player_corners_cnt - opponent_corners_cnt) / (player_corners_cnt + opponent_corners_cnt)
	else:
		heuristic_value = 0

	return heuristic_value



# Modify the board to add to search state sets
def modify_board(board, player, move):
	board[move[0]][move[1]] = player
	return board

# Change player
def flip_player(player):
	if player == "W" or player == "w":
		player = "B"
	else:
		player = "W"
	return player


# Generate all valid moves
def generate_possible_moves(board, player):

	moves = []
	for i in range(8):
		for j in range(8):
			if gamePlay.valid(board, player, (i,j)):
				moves.append((i,j))
	return moves

#Minimax Algorithm specific functions
#------------------------------------
def min_stage(board, depth_limit, cur_depth, player):

	#Base case of recursive call
	if cur_depth == depth_limit:
		return eval_func(board, player)
	#print "Inside Min Stage: Player", player

	# Find all possible moves
	moves = generate_possible_moves(board, player)

	#No possible moves. Game over. Return to find the winner
	if len(moves) == 0:
		return "pass"
	else:
		lowest_minimax_value = float('inf')
		best_move = moves[0]
		for move in moves:
			#print "Move Min:" , move, cur_depth
			cur_board = deepcopy(board)
			gamePlay.doMove(cur_board, player, move)
			#Recursive call to minimax_strategy to go to deeper node
			cur_minimax_value = max_stage(cur_board, depth_limit, (cur_depth+1), flip_player(player))
			#print "Current Min: ", cur_minimax_value
			if cur_minimax_value < lowest_minimax_value :
				#print "Selected Min: ", cur_minimax_value
				lowest_minimax_value = cur_minimax_value
				best_move = move

		#print "Final Choice Min:", lowest_minimax_value, cur_depth
		return lowest_minimax_value

def max_stage(board, depth_limit, cur_depth, player):

	#Base case of recursive call
	if cur_depth == depth_limit:
		return eval_func(board, player)
	#print "Inside Max Stage: Player ", player

	# Find all possible moves
	moves = generate_possible_moves(board, player)

	#No possible moves. Game over. Return to find the winner
	if len(moves) == 0:
		return "pass"
	else:
		highest_minimax_value = float('-inf')
		best_move = moves[0]
		for move in moves:
			#print "Move Max: ", move, cur_depth
			cur_board = deepcopy(board)
			gamePlay.doMove(cur_board, player, move)
			#Recursive call to minimax_strategy to go to deeper node
			cur_minimax_value = min_stage(cur_board, depth_limit, (cur_depth+1), flip_player(player))
			#print "Current Max: ",cur_minimax_value
			if cur_minimax_value > highest_minimax_value:
				#print "Selected Max: ", cur_minimax_value
				highest_minimax_value = cur_minimax_value
				best_move = move

		#print "Final Choice Max:" , highest_minimax_value, cur_depth
		return highest_minimax_value

def minimax_strategy(board, depth_limit, cur_depth, player):

	#print "Inside minimax_strategy"
	# Find all possible moves
	moves = generate_possible_moves(board, player)

	#No possible moves. Game over. Return to find the winner
	if len(moves) == 0:
		return "pass"
	else:
		best_minimax_value = float('-inf')
		best_move = moves[0]
		for move in moves:
			cur_board = deepcopy(board)
			gamePlay.doMove(cur_board, player, move)
			#print "Move:" , move
			#Recursive call to minimax_strategy to go to deeper node
			cur_minimax_value = min_stage(cur_board, depth_limit, (cur_depth+1), flip_player(player))
			#cur_minimax_value = minimax_strategy(cur_board, depth_limit, (cur_depth+1), best_minimax_value, flip_player(player))

			if cur_minimax_value > best_minimax_value:
				best_minimax_value = cur_minimax_value
				best_move = move

		return best_move

#Alpha Beta Pruning Algorithm specific functions
#------------------------------------
def min_stage_with_pruning(board, depth_limit, cur_depth, player, alpha, beta, time_lmt, start_time):

	cur_time = time.time()
	#Base case of recursive call
	if cur_depth == depth_limit or (cur_time - start_time) > (time_lmt - 1):
		return eval_func(board, player)
	#print "Inside Min Stage: Player", player

	# Find all possible moves
	moves = generate_possible_moves(board, player)

	#No possible moves. Game over. Return to find the winner
	if len(moves) == 0:
		return "pass"
	else:
		lowest_minimax_value = float('inf')
		best_move = moves[0]
		for move in moves:
			#print "Move Min:" , move, cur_depth
			cur_board = deepcopy(board)
			gamePlay.doMove(cur_board, player, move)
			#Recursive call to minimax_strategy to go to deeper node
			cur_minimax_value = max_stage_with_pruning(cur_board, depth_limit, (cur_depth+1), flip_player(player), alpha, beta, time_lmt, start_time)
			#print "Current Min: ", cur_minimax_value
			if cur_minimax_value < lowest_minimax_value:
				#print "Selected Min: ", cur_minimax_value
				lowest_minimax_value = cur_minimax_value
				best_move = move
			cur_time = time.time()
			if lowest_minimax_value <= alpha or (cur_time - start_time) > (time_lmt - 1):
				return lowest_minimax_value
			beta = min(beta, lowest_minimax_value)

		#print "Final Choice Min:", lowest_minimax_value, cur_depth
		return lowest_minimax_value


def max_stage_with_pruning(board, depth_limit, cur_depth, player, alpha, beta, time_lmt, start_time):

	cur_time = time.time()
	#Base case of recursive call
	if cur_depth == depth_limit or (cur_time - start_time) > (time_lmt - 1):
		return eval_func(board, player)
	#print "Inside Max Stage: Player ", player

	# Find all possible moves
	moves = generate_possible_moves(board, player)

	#No possible moves. Game over. Return to find the winner
	if len(moves) == 0:
		return "pass"
	else:
		highest_minimax_value = float('-inf')
		best_move = moves[0]
		for move in moves:
			#print "Move Max: ", move, cur_depth
			cur_board = deepcopy(board)
			gamePlay.doMove(cur_board, player, move)
			#Recursive call to minimax_strategy to go to deeper node
			cur_minimax_value = min_stage_with_pruning(cur_board, depth_limit, (cur_depth+1), flip_player(player), alpha, beta, time_lmt, start_time)
			#print "Current Max: ",cur_minimax_value
			if cur_minimax_value > highest_minimax_value:
				#print "Selected Max: ", cur_minimax_value
				highest_minimax_value = cur_minimax_value
				best_move = move
			cur_time = time.time()
			if highest_minimax_value >= beta or (cur_time - start_time) > (time_lmt - 1):
				return highest_minimax_value
			alpha = max(highest_minimax_value, alpha)

		#print "Final Choice Max:" , highest_minimax_value, cur_depth
		return highest_minimax_value


def alpha_beta_pruning_strategy(board, depth_limit, cur_depth, player, itime):

	time_lmt = itime
	start_time = time.time()
	alpha = float('-inf')
	beta = float('inf')
	#print "Inside minimax_strategy"
	# Find all possible moves
	moves = generate_possible_moves(board, player)

	#No possible moves. Game over. Return to find the winner
	if len(moves) == 0:
		return "pass"
	else:
		best_minimax_value = float('-inf')
		best_move = moves[0]
		for move in moves:
			cur_board = deepcopy(board)
			gamePlay.doMove(cur_board, player, move)
			#print "Move:" , move
			#Recursive call to minimax_strategy to go to deeper node
			cur_minimax_value = min_stage_with_pruning(cur_board, depth_limit, (cur_depth+1), flip_player(player), alpha, beta, time_lmt, start_time)
			#cur_minimax_value = minimax_strategy(cur_board, depth_limit, (cur_depth+1), best_minimax_value, flip_player(player))

			if cur_minimax_value > best_minimax_value:
				best_minimax_value = cur_minimax_value
				best_move = move
			cur_time = time.time()
			if best_minimax_value >= beta or (cur_time - start_time) > (time_lmt - 1):
				return best_move
			alpha = max(best_minimax_value, alpha)
		return best_move



def nextMove(board, color, itime):

	# Searching for next move without alpha beta pruning
	#return minimax_strategy(board, 4, 0, color)
	# Searching for next move with alpha beta pruning
	return alpha_beta_pruning_strategy(board, 4, 0, color, itime)


init_board =	[['.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', 'W', 'B', '.', '.', '.'],
['.', '.', '.', 'B', 'W', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.'],
['.', '.', '.', '.', '.', '.', '.', '.']]
sumOfTimes = 0
#player = "W"
#opponent = "B"
#eval_func(board)
#generate_game_tree(board, player, 2)
#result = minimax_strategy(init_board, 2, 0, 0, player)
#result = nextMove(init_board, "W", 0)
#print "Final Result: ", result
