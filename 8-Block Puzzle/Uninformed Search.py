import Queue

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

#*********************Uninformed Search Strategy Specific Functions **********************************

#Expand and include all possible states. Used by BFS and DFS
def search_for_all_possible_next_states(curNode, queue, visited_states):
	#initialize successor state queue to hold expanded nodes
	successor_state_queue = Queue.Queue()
	curState = getState(curNode)
	successorState = move_blank_left(curState)
	if successorState:
		successor_state_queue.put(successorState)
	successorState = move_blank_right(curState)
	if successorState:
		successor_state_queue.put(successorState)
	successorState = move_blank_up(curState)
	if successorState:
		successor_state_queue.put(successorState)
	successorState = move_blank_down(curState)
	if successorState:
		successor_state_queue.put(successorState)
	#Append successor states to the end of the main state queue
	while not successor_state_queue.empty():
		temp = successor_state_queue.get()
		if temp not in visited_states:
			queue.put(makeNode(temp, curState, getDepth(curNode)+1, getDepth(curNode)+1))

#Uninformed Search Strategy main function. Used by BFS and DFS
def UninformedSearch(queue, visited_states, solution_path, goalState, limit):

	while queue.qsize() > 0 and limit > 0:
		curNode = queue.get()
		curState = getState(curNode)
		visited_states.append(curState)
		solution_path.append(curNode)
		limit -= 1
		if is_goal_state(curState, goalState) == True:
			while not queue.empty():
				queue.get()
			display_solution_path(solution_path, curNode)
			return True
		else:
			#Expand all the nodes in current level
			search_for_all_possible_next_states(curNode, queue, visited_states)
	return False


def testBFS(initialState, goalState, limit):

	#Queue represents set of states
	queue = Queue.Queue()

	initialState.append(find_blank_position(initialState))
	goalState.append(find_blank_position(goalState))
	solution_path = []
	visited_states = []
	curState = initialState[:]
	#Enqueue initial node
	queue.put(makeNode(curState, [], 0, 0))
	print_program_input(initialState)
	print "          BFS"
	print "========================"
	if UninformedSearch(queue, visited_states, solution_path, goalState, limit) != True:
		print "Goal Not Found"

def testDFS(initialState, goalState, limit):

	#Queue represents set of states
	queue = Queue.LifoQueue()

	initialState.append(find_blank_position(initialState))
	goalState.append(find_blank_position(goalState))
	num_steps = 0
	solution_path = []
	visited_states = []
	curState = initialState[:]
	queue.put(makeNode(curState, [], 0, 0))
	print_program_input(initialState)
	print "          DFS"
	print "========================"
	if UninformedSearch(queue, visited_states, solution_path, goalState, limit) != True:
		print "Goal Not Found"


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
initialState =  initialState8
limit = 100000

#Initializations

#testBFS(initialState, goalState, limit)
#testDFS(initialState, goalState, limit)
