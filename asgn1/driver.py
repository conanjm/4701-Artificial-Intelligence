import sys, copy, time, resource
from math import sqrt
from collections import deque

nodes_expanded, search_depth, max_fringe_size, max_search_depth = 0, 0, 0, 0
start_time = time.time();

class State():
	def __init__(self, board, path):
		self.board = board
		self.length = len(board)
		self.idx = self.board.index(0)
		self.path = path

	def up(self):
		# first check whether the '0' is in the first row
		checkIdx = self.idx-int(sqrt(self.length))
		if checkIdx < 0:
			return None

		newBoard, newPath = copy.deepcopy(self.board), copy.deepcopy(self.path)
		newPath.append('Up')
		newBoard[self.idx], newBoard[checkIdx] = newBoard[checkIdx], newBoard[self.idx]
		return newBoard, newPath

	def down(self):
		# first check whether the '0' is in the last row
		checkIdx = self.idx+int(sqrt(self.length))
		if checkIdx >= self.length:
			return None

		newBoard, newPath = copy.deepcopy(self.board), copy.deepcopy(self.path)
		newPath.append('Down')
		newBoard[self.idx], newBoard[checkIdx] = newBoard[checkIdx], newBoard[self.idx]
		return newBoard, newPath

	def left(self):
		# first check whether the '0' is in the first column
		if self.idx % sqrt(self.length) == 0:
			return None

		newBoard, newPath = copy.deepcopy(self.board), copy.deepcopy(self.path)
		newPath.append('Left')
		newBoard[self.idx], newBoard[self.idx-1] = newBoard[self.idx-1], newBoard[self.idx]
		return newBoard, newPath

	def right(self):
		# first check whether the '0' is in the last column
		if (self.idx+1) % sqrt(self.length) == 0:
			return None

		newBoard, newPath = copy.deepcopy(self.board), copy.deepcopy(self.path)
		newPath.append('Right')
		newBoard[self.idx], newBoard[self.idx+1] = newBoard[self.idx+1], newBoard[self.idx]
		return newBoard, newPath

def notInFrontier(frontier, childBoard):
	for state in frontier:
		if state.board == childBoard:
				return False
	return True

def bfs(initBoard, goalBoard):
	# frontier: deque of State
	# explored: set of tuple of board
	frontier = deque([State(initBoard, [])])
	explored = set()

	while len(frontier):
		curState = frontier.popleft()
		explored.add(tuple(curState.board))

		print 
		print 'curBoard: ', curState.board
		print '================================'
		
		global nodes_expanded

		if curState.board == goalBoard:
			print 'path_to_goal: {}'.format(curState.path)
			print 'cost_of_path: {}'.format(len(curState.path))
			print 'nodes_expanded: {}'.format(nodes_expanded)
			print 'fringe_size: {}'.format(len(frontier))
			print 'max_fringe_size: {}'.format(max_fringe_size)
			print 'search_depth: {}'.format(search_depth)
			print 'max_search_depth: {}'.format(max_search_depth)
			print 'running_time: {}'.format(time.time()-start_time)
			print 'max_ram_usage: {}'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / float(1024**2))
			return 

		nodes_expanded += 1

		# Up Down Left Right
		move = curState.up()
		if move is not None:
			childBoard, childPath = move
			if notInFrontier(frontier, childBoard) and tuple(childBoard) not in explored:
				print 'up', childBoard
				frontier.append(State(childBoard, childPath))

		move = curState.down()
		if move is not None:
			childBoard, childPath = move
			if notInFrontier(frontier, childBoard) and tuple(childBoard) not in explored:
				print 'down', childBoard
				frontier.append(State(childBoard, childPath))

		move = curState.left()
		if move is not None:
			childBoard, childPath = move
			if notInFrontier(frontier, childBoard) and tuple(childBoard) not in explored:
				print 'left', childBoard
				frontier.append(State(childBoard, childPath))

		move = curState.right()
		if move is not None:
			childBoard, childPath = move
			if notInFrontier(frontier, childBoard) and tuple(childBoard) not in explored:
				print 'right', childBoard
				frontier.append(State(childBoard, childPath))

	return 'Failure'

if __name__ == '__main__':
	start_time = time.time()
	method, initBoard = sys.argv[1], map(int, sys.argv[2].split(','))
	if method == 'bfs':
		bfs(initBoard, range(len(initBoard)))

	# fo = open('output.txt', 'wb')
	# fo.write(str(initBoard))
	# fo.close()
