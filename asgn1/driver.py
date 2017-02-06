import sys, copy, time, resource
from math import sqrt
from collections import deque

nodes_expanded, max_fringe_size, max_search_depth = 0, 0, 0
start_time = time.time();

class State():
	def __init__(self, board, path, depth, idx):
		self.board = board
		self.length = int(sqrt(len(board)))
		self.path = path
		self.depth = depth
		# idx: the index of '0'
		self.idx = idx

	def up(self):
		# first check whether the '0' is in the first row
		if self.idx - self.length < 0:
			return None

		newBoard, newPath = copy.deepcopy(self.board), copy.deepcopy(self.path)
		newPath.append('Up')
		newBoard[self.idx], newBoard[self.idx-self.length] = newBoard[self.idx-self.length], newBoard[self.idx]
		return tuple(newBoard), newPath, self.idx-self.length

	def down(self):
		# first check whether the '0' is in the last row
		if self.idx + self.length >= len(self.board)
			return None

		newBoard, newPath = copy.deepcopy(self.board), copy.deepcopy(self.path)
		newPath.append('Down')
		newBoard[self.idx], newBoard[checkIdx] = newBoard[checkIdx], newBoard[self.idx]
		return newBoard, newPath, self.idx+self.length

	def left(self):
		# first check whether the '0' is in the first column
		if self.idx % sqrt(self.length) == 0:
			return None

		newBoard, newPath = copy.deepcopy(self.board), copy.deepcopy(self.path)
		newPath.append('Left')
		newBoard[self.idx], newBoard[self.idx-1] = newBoard[self.idx-1], newBoard[self.idx]
		return newBoard, newPath, int(self.idx % sqrt(self.length))

	def right(self):
		# first check whether the '0' is in the last column
		if (self.idx+1) % sqrt(self.length) == 0:
			return None

		newBoard, newPath = copy.deepcopy(self.board), copy.deepcopy(self.path)
		newPath.append('Right')
		newBoard[self.idx], newBoard[self.idx+1] = newBoard[self.idx+1], newBoard[self.idx]
		return newBoard, newPath, int((self.idx+1) % sqrt(self.length))

# def notInFrontier(frontier, childBoard):
# 	for state in frontier:
# 		if state.board == childBoard:
# 				return False
# 	return True

def bfs(initBoard, goalBoard):
	# frontier: deque of State
	# explored: set of tuple of board
	frontier, explored = deque([State(initBoard, [], 0)]), set()

	while len(frontier):

		curState = frontier.popleft()
		explored.add(tuple(curState.board))

		# print 
		# print 'curBoard: ', curState.board
		# print '================================'
		
		global nodes_expanded, max_fringe_size, max_search_depth

		if curState.board == goalBoard:
			print 'path_to_goal: {}'.format(curState.path)
			print 'cost_of_path: {}'.format(len(curState.path))
			print 'nodes_expanded: {}'.format(nodes_expanded)
			print 'fringe_size: {}'.format(len(frontier))
			print 'max_fringe_size: {}'.format(max_fringe_size)
			print 'search_depth: {}'.format(curState.depth)
			print 'max_search_depth: {}'.format(max_search_depth)
			print 'running_time: {}'.format(time.time()-start_time)
			print 'max_ram_usage: {}'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / float(1024**2))
			return 

		nodes_expanded += 1

		# Up
		move = curState.up()
		if move is not None:
			childBoard, childPath = move
			if notInFrontier(frontier, childBoard) and tuple(childBoard) not in explored:
				# print 'up', childBoard
				frontier.append(State(childBoard, childPath, curState.depth+1))
				max_fringe_size, max_search_depth = max(max_fringe_size, len(frontier)), max(max_search_depth, curState.depth+1)
		# Down
		move = curState.down()
		if move is not None:
			childBoard, childPath = move
			if notInFrontier(frontier, childBoard) and tuple(childBoard) not in explored:
				# print 'down', childBoard
				frontier.append(State(childBoard, childPath, curState.depth+1))
				max_fringe_size, max_search_depth = max(max_fringe_size, len(frontier)),  max(max_search_depth, curState.depth+1)

		# left
		move = curState.left()
		if move is not None:
			childBoard, childPath = move
			if notInFrontier(frontier, childBoard) and tuple(childBoard) not in explored:
				# print 'left', childBoard
				frontier.append(State(childBoard, childPath, curState.depth+1))
				max_fringe_size,max_search_depth = max(max_fringe_size, len(frontier)),  max(max_search_depth, curState.depth+1)

		# right
		move = curState.right()
		if move is not None:
			childBoard, childPath = move
			if notInFrontier(frontier, childBoard) and tuple(childBoard) not in explored:
				# print 'right', childBoard
				frontier.append(State(childBoard, childPath, curState.depth+1))
				max_fringe_size, max_search_depth = max(max_fringe_size, len(frontier)),  max(max_search_depth, curState.depth+1)

	return 'Failure'

def dfs(initBoard, goalBoard):
	# frontier: deque of State
	# explored: set of tuple of board
	frontier, frontier_set, explored = [State(initBoard, [], 0, initBoard.index(0))], {tuple(initBoard)}, set()
	# count = 0
	# while count < 10:
	while len(frontier):
		# count += 1
		curState = frontier.pop()
		frontier_set.remove(tuple(curState.board))
		explored.add(tuple(curState.board))

		global nodes_expanded, max_fringe_size, max_search_depth

		if curState.board == goalBoard:
			print 'path_to_goal: {}'.format(curState.path)
			print 'cost_of_path: {}'.format(len(curState.path))
			print 'nodes_expanded: {}'.format(nodes_expanded)
			print 'fringe_size: {}'.format(len(frontier))
			print 'max_fringe_size: {}'.format(max_fringe_size)
			print 'search_depth: {}'.format(curState.depth)
			print 'max_search_depth: {}'.format(max_search_depth)
			print 'running_time: {}'.format(time.time()-start_time)
			print 'max_ram_usage: {}'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / float(1024**2))
			return 

		nodes_expanded += 1
		if nodes_expanded % 100 == 0:
			print "nodes_expanded = {}".format(nodes_expanded)

		# print 
		# print 'currentBoard', curState.board
		# print '====================================='

		# right
		move = curState.right()
		if move is not None:
			childBoard, childPath, idx = move
			if tuple(childBoard) not in frontier_set  and tuple(childBoard) not in explored:
				# print 'right', childBoard
				frontier.append(State(childBoard, childPath, curState.depth+1, idx))
				frontier_set.add(tuple(childBoard))
				max_fringe_size,max_search_depth = max(max_fringe_size, len(frontier)),  max(max_search_depth, curState.depth+1)

		# left
		move = curState.left()
		if move is not None:
			childBoard, childPath, idx = move
			if tuple(childBoard) not in frontier_set and tuple(childBoard) not in explored:
				# print 'left', childBoard
				frontier.append(State(childBoard, childPath, curState.depth+1, idx))
				frontier_set.add(tuple(childBoard))
				max_fringe_size,max_search_depth = max(max_fringe_size, len(frontier)),  max(max_search_depth, curState.depth+1)

		# down
		move = curState.down()
		if move is not None:
			childBoard, childPath, idx = move
			if tuple(childBoard) not in frontier_set and tuple(childBoard) not in explored:
				# print 'down', childBoard
				frontier.append(State(childBoard, childPath, curState.depth+1, idx))
				frontier_set.add(tuple(childBoard))
				max_fringe_size,max_search_depth = max(max_fringe_size, len(frontier)),  max(max_search_depth, curState.depth+1)

		# up
		move = curState.up()
		if move is not None:
			childBoard, childPath, idx = move
			if tuple(childBoard) not in frontier_set and tuple(childBoard) not in explored:
				# print 'up', childBoard
				frontier.append(State(childBoard, childPath, curState.depth+1, idx))
				frontier_set.add(tuple(childBoard))
				max_fringe_size,max_search_depth = max(max_fringe_size, len(frontier)),  max(max_search_depth, curState.depth+1)

	return 'Failure'


if __name__ == '__main__':
	start_time = time.time()
	method, initBoard = sys.argv[1], map(int, sys.argv[2].split(','))
	if method == 'bfs':
		bfs(initBoard, range(len(initBoard)))
	elif method == 'dfs':
		dfs(initBoard, range(len(initBoard)))

	# fo = open('output.txt', 'wb')
	# fo.write(str(initBoard))
	# fo.close()
