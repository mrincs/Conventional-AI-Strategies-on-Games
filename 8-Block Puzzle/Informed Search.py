import Queue;

#*********************Generic functions used both by uninformed and informed search ****************************
board =[[" "," "," "],
		[" "," "," "],
		[" "," "," "]]

#Return an array of integers
def makeState(nw, n, ne, w, c, e, sw, s, se):
	state = [0,0,0,0,0,0,0,0,0]
	state[0] = nw
	state[1] = n
	state[2] = ne
	state[3] = w
	state[4] = c
	state[5] = e
	state[6] = sw
	state[7] = s
	state[8] = se
	# Last index contains the position of the blank
	# so that we don't have to check position of the blank
	# as all the operators operates on blank
	idx = state.index("blank")
	state[idx] = 0
	return state

#Construct a 2-D array for original puzzle board formation
def makeBoard(stateArray, board):
	board[0][0] = stateArray[0]
	board[0][1] = stateArray[1]
	board[0][2] = stateArray[2]
	board[1][0] = stateArray[3]
	board[1][1] = stateArray[4]
	board[1][2] = stateArray[5]
	board[2][0] = stateArray[6]
	board[2][1] = stateArray[7]
	board[2][2] = stateArray[8]
	return board

#Display 2-D board array
def displayState(board):
	for i in range(0,3):
		print "*",
		for j in range(0,3):
			if board[i][j] == 0:
				print " ",
			else:
				print board[i][j],
			if j != 2:
				print "|",
			else:
				print ""

# Program Input printer
def print_program_input(initialState):
	print "     Program Input"
	print "========================"
	print "Initial State"
	tempArray = initialState[:]
	displayState(makeBoard(tempArray, board))
	print "Goal State"
	tempArray = [1, 2, 3, 4, 5, 6, 7, 8, 0]
	displayState(makeBoard(tempArray, board))

# Backtrace and display full solution path starting from root state
def display_solution_path(solution_path, curNode):
	print "Solution Path: "
	print "========================="
	#curNode contains goal State
	#Back trace to root node and construct solution path
	level = 0
	backtracePath = Queue.LifoQueue()
	backtracePath.put(getState(curNode))
	while is_root_node(curNode) != True:
		#print backtracePath
		parent = getParent(curNode)
		curNode = search_for_parent_node_in_search_list(solution_path, parent)
		if curNode != []:
			backtracePath.put(getState(curNode))
		else:
			print "Back trace Error"

	while not backtracePath.empty():
		state = backtracePath.get()
		level += 1
		displayState(makeBoard(state[0:9], board))
		print "-----------------"
	#(level-1) because root is considered as level 0
	print "Depth of the Solution: ",(level-1)

def search_for_parent_node_in_search_list(solution_path, parent):
	for node in solution_path:
		if getState(node) == parent:
			return node
	return []


def makeNode(state, parent, depth, cost):
	return [state, parent, depth, cost]

def getState(curNode):
	return curNode[0]

def getParent(curNode):
	return curNode[1]

def getDepth(curNode):
	return curNode[2]

def getCost(curNode):
	return curNode[3]

def is_root_node(curNode):
	if getParent(curNode) == []:
		return True
	return False

#Find blank position in array
def find_blank_position(state):
	pos = 0
	for i in state:
		if i == 0:
			return pos
		pos += 1
	return -1

#Check whether goal is achieved
def is_goal_state(curState, goalState):
	if (curState) != (goalState):
		return False
	else:
		return True


# Operators
# curState is present state that is to be expanded
# successorState is the node that came from expanding curState node
def move_blank_left(curState):
	successorState = []
	blank_pos = curState[len(curState)-1]
	if blank_pos not in [0,3,6]:
		successorState = curState[:]
		successorState[blank_pos] = successorState[blank_pos-1]
		successorState[blank_pos-1] = 0
		successorState[len(successorState)-1] = blank_pos-1
	return successorState

def move_blank_right(curState):
	successorState = []
	blank_pos = curState[len(curState)-1]
	if blank_pos not in [2,5,8]:
		successorState = curState[:]
		successorState[blank_pos] = successorState[blank_pos+1]
		successorState[blank_pos+1] = 0
		successorState[len(successorState)-1] = blank_pos+1
	return successorState

def move_blank_up(curState):
	successorState = []
	blank_pos = curState[len(curState)-1]
	if blank_pos not in [0,1,2]:
		successorState = curState[:]
		successorState[blank_pos] = successorState[blank_pos-3]
		successorState[blank_pos-3] = 0
		successorState[len(successorState)-1] = blank_pos-3
	return successorState

def move_blank_down(curState):
	successorState = []
	blank_pos = curState[len(curState)-1]
	if blank_pos not in [6,7,8]:
		successorState = curState[:]
		successorState[blank_pos] = successorState[blank_pos+3]
		successorState[blank_pos+3] = 0
		successorState[len(successorState)-1] = blank_pos+3
	return successorState

#********************Informed Search Strategy specific functions ***************************

#Best Search Heuristics 1: Greedy Approach
#h1(n) = Number of misplaced tiles. To show the effect of choosing a bad heuristic function
#h2(n) = Manhattan distance of all misplaced tiles..

#Calculate heuristic function value
def calculate_heuristic_value(curState, heuristic_func, costFromRoot):
	# Option 1 is BSH1 : h(n) = Number of misplaced tiles
	if heuristic_func == 1:
		return count_misplaced_tiles(curState)
	# Option 2 is BSH2 : h(n) = Manhattan distance of all misplaced tiles
	elif heuristic_func == 2:
		return sum_of_manhattan_distance(curState)
	# Option 3 is A*: f(n) = h(n) + g(n) where h(n) = Manhattan distance and f(n) = Depth of the node
	elif heuristic_func == 3:
		return sum_of_manhattan_distance(curState)+costFromRoot
	else:
		return 0

#Return Number of Misplaced Tiles: Heuristic Function 1
def count_misplaced_tiles(curState):
	misplaced_tiles = 0
	for i in range(0,8):
		if curState[i] != i+1:
			misplaced_tiles += 1
	return misplaced_tiles



#Return sum of Manhattan Distance of all tiles: Heuristic Function 2
def sum_of_manhattan_distance(curState):
	sum_dist = 0
	makeBoard(curState, board)
	for i in range(0,3):
		for j in range(0,3):
			tile_number = board[i][j]
			if tile_number != 0:
				exp_i = (tile_number-1)/3
				exp_j = (tile_number-1)%3
				sum_dist += abs(i-exp_i)
				sum_dist += abs(j-exp_j)
	return sum_dist


#Choose next best state. Greedy approach. Used by best-first and A* search strategy
def search_for_next_best_state(curNode, state_list, visited_states, heuristic_func):
	#initialize successor state queue to hold expanded nodes
	successor_state_list = []
	curState = getState(curNode)
	successorState = move_blank_left(curState)
	if successorState:
		successor_state_list.append(successorState)
	successorState = move_blank_right(curState)
	if successorState:
		successor_state_list.append(successorState)
	successorState = move_blank_up(curState)
	if successorState:
		successor_state_list.append(successorState)
	successorState = move_blank_down(curState)
	if successorState:
		successor_state_list.append(successorState)
	#Calculate Heuristic function's value for each generated states
	for state_idx in range(0, len(successor_state_list)):
		if successor_state_list[state_idx] not in visited_states:
			cur_heuristic_value = calculate_heuristic_value(successor_state_list[state_idx], heuristic_func, getDepth(curNode)+1)
			state_list.append(makeNode(successor_state_list[state_idx], curState, getDepth(curNode)+1, cur_heuristic_value))



#Informed Search main function. Used by A* and Best First Search
def InformedSearch(state_list, visited_states, solution_path, goalState, limit, heuristic_func):

	while len(state_list) > 0 and limit > 0:

		curNode = state_list.pop(0)
		curState = getState(curNode)
		visited_states.append(curState)
		solution_path.append(curNode)
		limit -= 1

		search_for_next_best_state(curNode, state_list, visited_states, heuristic_func)
		if heuristic_func == 3:
			state_list.sort(key=lambda tup: tup[3]+tup[2])
		else:
			state_list.sort(key=lambda tup: tup[3])
		if getCost(curNode) < getCost(state_list[0]):
			if is_goal_state(curState, goalState) == True:
				while len(state_list) > 0:
					state_list.pop()
				display_solution_path(solution_path, curNode)
				return True

	return False

def testInformedSearch(initialState, goalState, limit, heuristic_func):

	#State_list represents set of states in fringe
	state_list = []
	initialState.append(find_blank_position(initialState))
	goalState.append(find_blank_position(goalState))
	solution_path = []
	visited_states = []
	curState = initialState[:]
	#A node will represent (state, parent state, depth, costToGoal)
	curNode = makeNode(curState, [], 0, calculate_heuristic_value(curState, heuristic_func, 0))
	#Enqueue initial node
	state_list.append(curNode)
	print_program_input(initialState)

	if InformedSearch(state_list, visited_states, solution_path, goalState, limit, heuristic_func) != True:
		print "Goal Not Found"

def testInformedSearch1(initialState, goalState, limit):
	return testInformedSearch(initialState, goalState, limit, 1)

def testInformedSearch2(initialState, goalState, limit):
	return testInformedSearch(initialState, goalState, limit, 2)

def testAStarSearch(initialState, goalState, limit):
	return testInformedSearch(initialState, goalState, limit, 3)

# First group of test cases - should have solutions with depth <= 5
initialState1 = makeState(2, "blank", 3, 1, 5, 6, 4, 7, 8)
initialState2 = makeState(1, 2, 3, "blank", 4, 6, 7, 5, 8)
initialState3 = makeState(1, 2, 3, 4, 5, 6, 7, "blank", 8)
initialState4 = makeState(1, "blank", 3, 5, 2, 6, 4, 7, 8)
initialState5 = makeState(1, 2, 3, 4, 8, 5, 7, "blank", 6)


# Second group of test cases - should have solutions with depth <= 10
initialState6 = makeState(2, 8, 3, 1, "blank", 5, 4, 7, 6)
initialState7 = makeState(1, 2, 3, 4, 5, 6, "blank", 7, 8)
initialState8 = makeState("blank", 2, 3, 1, 5, 6, 4, 7, 8)
initialState9 = makeState(1, 3, "blank", 4, 2, 6, 7, 5, 8)
initialState10 = makeState(1, 3, "blank", 4, 2, 5, 7, 8, 6)


# Third group of test cases - should have solutions with depth <= 20
initialState11 = makeState("blank", 5, 3, 2, 1, 6, 4, 7, 8)
initialState12 = makeState(5, 1, 3, 2, "blank", 6, 4, 7, 8)
initialState13 = makeState(2, 3, 8, 1, 6, 5, 4, 7, "blank")
initialState14 = makeState(1, 2, 3, 5, "blank", 6, 4, 7, 8)
initialState15 = makeState("blank", 3, 6, 2, 1, 5, 4, 7, 8)


# Fourth group of test cases - should have solutions with depth <= 50
initialState16 = makeState(2, 6, 5, 4, "blank", 3, 7, 1, 8)
initialState17 = makeState(3, 6, "blank", 5, 7, 8, 2, 1, 4)
initialState18 = makeState(1, 5, "blank", 2, 3, 8, 4, 6, 7)
initialState19 = makeState(2, 5, 3, 4, "blank", 8, 6, 1, 7)
initialState20 = makeState(3, 8, 5, 1, 6, 7, 4, 2, "blank")

#Initializations
goalState = makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")
initialState =  initialState20
limit = 10000


#testInformedSearch1(initialState, goalState, limit)
#testInformedSearch2(initialState, goalState, limit)
#testAStar(initialState, goalState, limit)
