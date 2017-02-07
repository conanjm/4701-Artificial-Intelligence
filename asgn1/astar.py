import sys, time, resource, heapq
from math import sqrt, fabs
from collections import deque
from copy import deepcopy

def h(board):
	res, length = 0, int(sqrt(len(board)))
	for curPos, goalPos in enumerate(board):
		if goalPos:
			r1, c1, r2, c2 = curPos/length, curPos%length, goalPos/length, goalPos%length
			res += int(fabs(r1-r2)+ fabs(c1-c2) )
	return res

def getMove(move):
	if move == 'Up':
		return 0
	elif move == 'Down':
		return 1
	elif move == 'Left':
		return 2
	else:
		return 3

class Node:
	# move: the move takes from its parent to itself
	def __init__(self, board, idx, move, parent, depth):
		self.board = board
		self.idx = idx
		self.move = move
		self.parent = parent
		self.depth = depth

	def __cmp__(self, other):
		gself, gother = self.depth + h(self.board), other.depth + h(other.board)
		if gself < gother or (gself == gother and getMove(self.move) < getMove(other.move) ):
			return -1
		return 1
		

def up( node,  length):
	if node.idx - length >= 0:
		newBoard = list(node.board)
		newBoard[node.idx], newBoard[node.idx-length] = newBoard[node.idx-length], newBoard[node.idx] 
		return tuple(newBoard)
	return None
		# newBoard = tuple(newBoard)
		# if newBoard not in fset and newBoard not in explored:
		# 	child = Node(newBoard, node.idx-length, 'Up', node, node.depth+1 )
		# 	fset.add(child.board)
		# 	return child
		# return None
			# frontier.append(child)
			# return True
	# return False

def down( node, length):
	if node.idx + length < len(node.board):
		newBoard = list(node.board)
		newBoard[node.idx], newBoard[node.idx+length] = newBoard[node.idx+length], newBoard[node.idx] 
		return tuple(newBoard)
	return None
		# newBoard = tuple(newBoard)
		# if newBoard not in fset and newBoard not in explored:
		# 	child = Node(newBoard, node.idx+length, 'Down', node, node.depth+1 )
		# 	fset.add(child.board)
		# 	return child
		# return None
	# 		frontier.append(child)
	# 		return True
	# return False

def left(node,  length):
	if node.idx % length:
		newBoard = list(node.board)
		newBoard[node.idx], newBoard[node.idx-1] = newBoard[node.idx-1], newBoard[node.idx] 
		return tuple(newBoard)
	return None
		# newBoard = tuple(newBoard)
		# return newBoard
		# if newBoard not in fset and newBoard not in explored:
		# 	child = Node(newBoard, node.idx-1, 'Left', node, node.depth+1 )
		# 	fset.add(child.board)
		# 	return child
		# return None
	# 		frontier.append(child)
	# 		return True
	# return False

def right( node, length):
	if (node.idx+1) % length:
		newBoard = list(node.board)
		newBoard[node.idx], newBoard[node.idx+1] = newBoard[node.idx+1], newBoard[node.idx] 
		return tuple(newBoard)
	return None
		# newBoard = tuple(newBoard)
		# if newBoard not in fset and newBoard not in explored:
		# 	child = Node(newBoard, node.idx+1, 'Right', node, node.depth+1 )
		# 	fset.add(child.board)
		# 	return child
		# elif newBoard 
		# return None
	# 		frontier.append(child)
	# 		return True
	# return False


def dfs(initBoard, goalBoard):
	max_fringe_size, max_search_depth, nodes_expanded = 1, 0, 0
	frontier, fset, explored = [Node(initBoard, initBoard.index(0), '', None, 0)], {initBoard}, set()	
	length = int(sqrt(len(initBoard)))
	
	while len(frontier):
		node = frontier.pop()
		fset.remove(node.board)
		explored.add(node.board)

		if node.board == goalBoard:
			path = []
			tmp = node
			while tmp.parent is not None:
				path.append(tmp.move)
				tmp = tmp.parent
			path.reverse()
			print 'path_to_goal: ', list(path)
			print 'cost_of_path: ', len(path)
			print 'nodes_expanded:', nodes_expanded
			print 'fringe_size:', len(frontier)
			print 'max_fringe_size: {}'.format(max_fringe_size)
			print 'search_depth: {}'.format(node.depth)
			print 'max_search_depth: {}'.format(max_search_depth)
			print 'running_time: {}'.format(time.time() - startTime )
			print 'max_ram_usage: {}'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / float(1024**2))
			return

		nodes_expanded += 1

		newBoard = right( node, length)
		if newBoard is not None and newBoard not in fset and newBoard not in explored:
			child = Node(newBoard, node.idx+1, 'Right', node, node.depth+1 )
			frontier.append(child)
			fset.add(child.board)
			max_search_depth = max(max_search_depth, frontier[-1].depth)

		newBoard = left( node, length)
		if newBoard is not None and newBoard not in fset and newBoard not in explored:
			child = Node(newBoard, node.idx-1, 'Left', node, node.depth+1 )
			frontier.append(child)
			fset.add(child.board)
			max_search_depth = max(max_search_depth, frontier[-1].depth)

		newBoard = down( node, length)
		if newBoard is not None and newBoard not in fset and newBoard not in explored:
			child = Node(newBoard, node.idx+length, 'Down', node, node.depth+1 )
			frontier.append(child)
			fset.add(child.board)
			max_search_depth = max(max_search_depth, frontier[-1].depth)
		
		newBoard = up( node, length)
		if newBoard is not None and newBoard not in fset and newBoard not in explored:
			child = Node(newBoard, node.idx-length, 'Up', node, node.depth+1 )
			frontier.append(child)
			fset.add(child.board)
			max_search_depth = max(max_search_depth, frontier[-1].depth)

		max_fringe_size = max( max_fringe_size, len(frontier))


def astar(initBoard, goalBoard):
	max_fringe_size, max_search_depth, nodes_expanded = 1, 0, 0
	frontier, fset, explored = [], {initBoard},  set()
	heuristic = h(initBoard)
	heapq.heappush(frontier, (heuristic, Node(initBoard, initBoard.index(0), '', None, 0 ) ))

	while len(frontier):
		node = heapq.heappop(frontier)
		fset.remove(node.board)
		explored.add(node.board)

		if node.board == goalBoard:
			print 'SUCCESS'

		nodes_expanded += 1

		child = up(frontier, node, fset, explored, length)
		if child is not None:
			heapq.heappush(frontier,child)

		child = down(frontier, node, fset, explored, length)
		if child is not None:
			heapq.heappush(frontier,child)

		child = left(frontier, node, fset, explored, length)
		if child is not None:
			heapq.heappush(frontier,child)

		child = right(frontier, node, fset, explored, length)
		if child is not None:
			heapq.heappush(frontier,child)
			








if __name__ == '__main__':
	startTime = time.time()
	method, initBoard = sys.argv[1], tuple(map(int, sys.argv[2].split(',')))
	goalBoard = tuple(range(len(initBoard)))
	dfs(initBoard, goalBoard)

