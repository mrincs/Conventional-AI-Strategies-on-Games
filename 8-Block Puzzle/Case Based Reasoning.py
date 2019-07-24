import Queue;
import random

#*********************Generic functions used both by uninformed and informed search ****************************
board =[[" "," "," "],
		[" "," "," "],
		[" "," "," "]]

curBoard =[[" "," "," "],
			[" "," "," "],
			[" "," "," "]]

targetBoard =[[" "," "," "],
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
def construct_solution_path(solution_path, curNode):
	#curNode contains goal State
	#Back trace to root node and construct solution path
	level = 0
	solutionPath = []
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
		solutionPath.append(state)
		level += 1
		#displayState(makeBoard(state[0:9], board))
		#print "-----------------"
	return solutionPath
	#(level-1) because root is considered as level 0
	#print "Depth of the Solution: ",(level-1)

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
def calculate_heuristic_value(curState, goalState, heuristic_func, costFromRoot):
	# Option 1 is BSH1 : h(n) = Number of misplaced tiles
	if heuristic_func == 1:
		return count_misplaced_tiles(curState)
	# Option 2 is BSH2 : h(n) = Manhattan distance of all misplaced tiles
	elif heuristic_func == 2:
		return sum_of_manhattan_distance(curState)
	# Option 3 is A*: f(n) = h(n) + g(n) where h(n) = Manhattan distance and f(n) = Depth of the node
	elif heuristic_func == 3:
		return modified_sum_of_manhattan_distance(curState, goalState)+costFromRoot
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
def search_for_next_best_state(curNode, goalState, state_list, visited_states, heuristic_func):
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
			cur_heuristic_value = calculate_heuristic_value(successor_state_list[state_idx], goalState, heuristic_func, getDepth(curNode)+1)
			state_list.append(makeNode(successor_state_list[state_idx], curState, getDepth(curNode)+1, cur_heuristic_value))

#Informed Search main function. Used by A* and Best First Search
def InformedSearch(start_state, goalState, limit, heuristic_func):

	state_list = []
	solution_path = []
	visited_states = []
	state_list.append(makeNode(start_state, [], 0, calculate_heuristic_value(start_state, goalState, heuristic_func, 0)))
	while len(state_list) > 0 or limit > 0:

		curNode = state_list.pop(0)
		curState = getState(curNode)
		visited_states.append(curState)
		solution_path.append(curNode)
		limit -= 1

		search_for_next_best_state(curNode, goalState, state_list, visited_states, heuristic_func)

		if is_goal_state(curState, goalState) == True:
			while len(state_list) > 0:
				state_list.pop()
			solutionPath = construct_solution_path(solution_path, curNode)
			return solutionPath

	return null

def testInformedSearch(initialState, goalState, limit, heuristic_func):
	initialState.append(find_blank_position(initialState))
	curState = initialState[:]
	goal_state = goalState
	goal_state.append(find_blank_position(goalState))
	#A node will represent (state, parent state, depth, costToGoal)
	curNode = makeNode(curState, [], 0, calculate_heuristic_value(curState, goalState, heuristic_func, 0))

	if scan_CBRrules(initialState, goal_state, limit, heuristic_func, CBRrules) != True:
		print "Goal Not Found"

def testInformedSearch1(initialState, goalState, limit):
	return testInformedSearch(initialState, goalState, limit, 1)

def testInformedSearch2(initialState, goalState, limit):
	return testInformedSearch(initialState, goalState, limit, 2)

def testAStarSearch(initialState, goalState, limit):
	return testInformedSearch(initialState, goalState, limit, 3)

limit = 10000


#testInformedSearch1(initialState, goalState, limit)
#testInformedSearch2(initialState, goalState, limit)
#testAStar(initialState, goalState, limit)



#############################################################################
################Case-Based Reasoning Systems modifications###################
#############################################################################

#Modified Manhattan distance which compares start_state with variable goal state.
#Previous implementation was for a fixed goal state
def modified_sum_of_manhattan_distance(curState, targetState):
	sum_dist = 0
	makeBoard(curState, curBoard)
	makeBoard(targetState, targetBoard)
	for i in range(0,3):
		for j in range(0,3):
			tile_number = curBoard[i][j]
			if tile_number != 0:
				for k in range(0,3):
					for l in range(0,3):
						elem = targetBoard[k][l]
						if elem == tile_number:
							exp_i = (k-i)
							exp_j = (l-j)
							sum_dist += abs(exp_i)
							sum_dist += abs(exp_j)
							#print "[elm, Abs_exp_i, Abs_exp_j]", elem, abs(exp_i), abs(exp_j)
	#print sum_dist
	return sum_dist

#Case based Reasoning APIs
def makeRules(start_state, goal_state, solution_path):
	return [start_state, goal_state, solution_path]

def getStartStateFromRule(rule):
	return rule[0]

def getGoalStateFromRule(rule):
	return rule[1]

def getSolutionPathFromRule(rule):
	return rule[2]

# Scanning through the system to find exact or near matches whose solution can be utilized
def scan_CBRrules(start_state, goalState, limit, heuristic_func, CBRrules):

	flag = False
	minSimilarityIndex = 10000
	minStart = 10000
	minGoal = 10000
	similarRule = []
	idx = 0
	if len(CBRrules) != 0:
		print "Similarity Index with Existing Cases in system:"
		print "-----------------------------------------------"
	for rule in CBRrules:
		start_state_distance = modified_sum_of_manhattan_distance(start_state, getStartStateFromRule(rule))
		goal_state_distance = modified_sum_of_manhattan_distance(goalState, getGoalStateFromRule(rule))
		similarityIndex  = start_state_distance + goal_state_distance

		idx += 1
		print "Case ", idx
		print similarityIndex
		if (similarityIndex <= 4 and minSimilarityIndex > similarityIndex):
			similarRule = rule
			minSimilarityIndex = similarityIndex
			minStart = start_state_distance
			minGoal = goal_state_distance
	if len(CBRrules) != 0 and minSimilarityIndex != 10000:
		print "Selected Rule:", similarRule
		print "Similarity Index: ", minSimilarityIndex
	# Found an exact match
	if (minSimilarityIndex) == 0:
		print "Found an exact match in CBR!!!"
		flag = True
		return flag
	# Found an approximate match in rule based system.
	# We're selecting only the rules for which total sum of manhattan distance of start state of the problem and start state of rule
	# and goal state of problem and goal state of the rule is less than five. Other rules are discarded
	elif (minSimilarityIndex) <= 4:
		flag = True
		constructPath = []
		constructRule = []
		if minStart == 0:
			# Find route from rules goal state to problem goal state
			solutionPath = InformedSearch(getGoalStateFromRule(similarRule), goalState, limit, heuristic_func)
			constructPath = getSolutionPathFromRule(similarRule)
			constructPath = constructPath + solutionPath[1:]
			constructRule = makeRules(start_state, goalState, constructPath)
			CBRrules.append(constructRule)
		elif minGoal == 0:
			# Find route from problem start state to rule start state
			solutionPath = InformedSearch(start_state, getStartStateFromRule(similarRule), limit, heuristic_func)
			constructPath = solutionPath
			constructPath = constructPath + getSolutionPathFromRule(similarRule)[1:]
			constructRule = makeRules(start_state, goalState, constructPath)
			CBRrules.append(constructRule)
		else:
			# Rule goal state constructs a part of problem state
			# It handles the case below:
			#		  If P does not exactly solve the problem, adapt P into a solution path, by concatenating it with two new paths:
			#			 Ps, from S0 to S1, and
			#			 Pg, from G1 to G0.
			# Find route from problem start state to rule start state and rule goal state to problem goal state
			solutionPath = InformedSearch(start_state, getStartStateFromRule(similarRule), limit, heuristic_func)
			constructPath = solutionPath
			constructPath = constructPath + getSolutionPathFromRule(similarRule)[1:]
			solutionPath = InformedSearch(getGoalStateFromRule(similarRule), goalState, limit, heuristic_func)
			constructPath = constructPath + solutionPath[1:]
			constructRule = makeRules(start_state, goalState, constructPath)
			CBRrules.append(constructRule)
		return flag
	# Doesn't match with existing problems. Solve and store in CBR
	solutionPath = InformedSearch(start_state, goalState, limit, heuristic_func)
	if len(solutionPath) != 0:
		print "New Problem Found !!!"
		constructRule = makeRules(start_state, goalState, solutionPath)
		CBRrules.append(constructRule)
		flag = True
	return flag


# First caller function according to Project specification
def testCaseBasedSearch(initialState, goalState, limit):
	return testInformedSearch(initialState, goalState, limit, 3)

# Display CBR Systems
def displayCBR(CBRrules):
	print "CBR System:"
	print "------------"
	for rule in CBRrules:
		print rule

#System to store rules
CBRrules = []

############### Problem States ###################
### Problem Instance = <Initial, Goal>
### For experiments , use manually selected problems
def manual_problem_instances():

	problemInstances = [[makeState(2, "blank", 3, 1, 5, 6, 4, 7, 8), makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")],
						[makeState(2, 3, 6, 1, 4, "blank", 7, 5, 8), makeState(1, 2, 3, 4, 5, "blank", 7, 8, 6)],
						[makeState(2, 3, 6, 1, "blank", 8, 7, 4, 5), makeState(1, 2, 3, 4, 5, "blank", 7, 8, 6)],
						[makeState(2, 3, 6, "blank", 1, 8, 7, 4, 5), makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")],
						[makeState(3, "blank", 6, 2, 1, 8, 7, 4, 5), makeState(1, 2, 3, 4, "blank", 5, 7, 8, 6)],
						[makeState(2, "blank", 3, 1, 5, 6, 4, 7, 8), makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")],
						[makeState(2, "blank", 3, 1, 5, 6, 4, 7, 8), makeState(1, 2, 3, 4, 5, "blank", 7, 8, 6)],
						[makeState(3, 1, "blank", 2, 8, 6, 7, 4, 5), makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")]]
	run_problemSet(problemInstances)

#Generate random test problems
def generateTestProblems(testCaseNumber):
	testProblemsCount = 0
	testProblem = []
	while(testProblemsCount < testCaseNumber):
		# Generate random start states
		testProblemsCount += 1
		problemInstance = []
		counter = 0
		curAddlist = []
		curRemoveList = range(0, 9)
		while (counter < 9):
			counter += 1
			numberToAdd = random.choice(curRemoveList)
			curRemoveList.remove(numberToAdd)
			curAddlist.append(numberToAdd)
		problemInstance.append(curAddlist)
		# Generate random goal states
		counter = 0
		curAddlist = []
		curRemoveList = range(0, 9)
		while (counter < 9):
			counter += 1
			numberToAdd = random.choice(curRemoveList)
			curRemoveList.remove(numberToAdd)
			curAddlist.append(numberToAdd)
		problemInstance.append(curAddlist)
		testProblem.append(problemInstance)
	print testProblem
	run_problemSet(testProblem)

def run_problemSet(problemInstances):
	for idx in range(0,len(problemInstances)-1):
		initialState = problemInstances[idx][0]
		goalState = problemInstances[idx][1]
		print "##########"
		print "Problem ", (idx+1)
		print "##########"
		print "Input : "
		displayState(makeBoard(initialState, board))
		print "Goal :"
		displayState(makeBoard(goalState, board))
		testCaseBasedSearch(initialState, goalState, 10000)
		displayCBR(CBRrules)

# Entry call of the program
manual_problem_instances()
#generateTestProblems(3)
