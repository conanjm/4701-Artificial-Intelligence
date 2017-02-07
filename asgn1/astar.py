import sys, time, resource, heapq
from math import sqrt, fabs
from collections import deque
from copy import deepcopy

class Node:
	# move: the move takes from its parent to itself
	def __init__(self, board, idx, move, parent, depth):
		self.board = board
		self.idx = idx
		self.move = move
		self.parent = parent
		self.depth = depth

def up(tree, node, fset, explored, length):
	if node.idx - length >= 0:
		newBoard = list(node.board)
		newBoard[node.idx], newBoard[node.idx-length] = newBoard[node.idx-length], newBoard[node.idx] 
		newBoard = tuple(newBoard)
		if newBoard not in fset and newBoard not in explored:
			child = Node(newBoard, node.idx-length, 'Up', node, node.depth+1 )
			tree.append(child)
			fset.add(newBoard)
			return True
	return False


def down(tree, node, fset, explored, length):
	if node.idx + length < len(node.board):
		newBoard = list(node.board)
		newBoard[node.idx], newBoard[node.idx+length] = newBoard[node.idx+length], newBoard[node.idx] 
		newBoard = tuple(newBoard)
		if newBoard not in fset and newBoard not in explored:
			child = Node(newBoard, node.idx+length, 'Down', node, node.depth+1 )
			tree.append(child)
			fset.add(newBoard)
			return True
	return False

def left(tree, node, fset, explored, length):
	if node.idx % length:
		newBoard = list(node.board)
		newBoard[node.idx], newBoard[node.idx-1] = newBoard[node.idx-1], newBoard[node.idx] 
		newBoard = tuple(newBoard)
		if newBoard not in fset and newBoard not in explored:
			child = Node(newBoard, node.idx-1, 'Left', node, node.depth+1 )
			tree.append(child)
			fset.add(newBoard)
			return True
	return False


def right(tree, node, fset, explored, length):
	if (node.idx+1) % length:
		newBoard = list(node.board)
		newBoard[node.idx], newBoard[node.idx+1] = newBoard[node.idx+1], newBoard[node.idx] 
		newBoard = tuple(newBoard)
		if newBoard not in fset and newBoard not in explored:
			child = Node(newBoard, node.idx+1, 'Right', node, node.depth+1 )
			tree.append(child)
			fset.add(newBoard)
			return True
	return False


def dfs(initBoard, goalBoard):
	max_fringe_size, max_search_depth, nodes_expanded, initIdx = 1, 0, 0, initBoard.index(0)
	tree, fset, explored = [Node(initBoard, initIdx, '', None, 0)], {initBoard}, set()	
	length = int(sqrt(len(initBoard)))
	
	while len(tree):
		node = tree.pop()
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
			print 'fringe_size:', len(tree)
			print 'max_fringe_size: {}'.format(max_fringe_size)
			print 'search_depth: {}'.format(node.depth)
			print 'max_search_depth: {}'.format(max_search_depth)
			print 'running_time: {}'.format(time.time() - startTime )
			print 'max_ram_usage: {}'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / float(1024**2))
			return

		nodes_expanded += 1
		print nodes_expanded

		if right(tree, node, fset, explored, length):
			max_search_depth = max(max_search_depth, tree[-1].depth)
		if left(tree, node, fset, explored, length):
			max_search_depth = max(max_search_depth, tree[-1].depth)
		if down(tree, node, fset, explored, length):
			max_search_depth = max(max_search_depth, tree[-1].depth)
		if up(tree, node, fset, explored, length):
			max_search_depth = max(max_search_depth, tree[-1].depth)

		max_fringe_size = max( max_fringe_size, len(tree))


def h(board):
	res, length = 0, int(sqrt(len(board)))
	for curPos, goalPos in enumerate(board):
		if goalPos:
			r1, c1, r2, c2 = curPos/length, curPos%length, goalPos/length, goalPos%length
			res += int(fabs(r1-r2)+ fabs(c1-c2) )
	return res

def astar(initBoard, goalBoard):
	max_fringe_size, max_search_depth, nodes_expanded, initIdx = 1, 0, 0, initBoard.index(0)
	frontier, fidx, fset, explored = [], [], {initBoard},  set()
	heuristic = h(initBoard)
	heapq.heappush(frontier, (heuristic, initBoard ) )
	heapq.heappush(fidx, (heuristic, initIdx))
	tree = []
	heapq.heappush(tree, (heuristic, Node('', None, 0) ))

	while len(frontier):
		curBoard = heapq.heappop(frontier)
		fset.remove(initBoard)
		idx = heapq.heappop(fidx)
		explored.add(curboard)
		node = heapq.heappop(tree)

		if curBoard == goalBoard:
			print 'SUCCESS'


if __name__ == '__main__':
	startTime = time.time()
	method, initBoard = sys.argv[1], tuple(map(int, sys.argv[2].split(',')))
	goalBoard = tuple(range(len(initBoard)))
	dfs(initBoard, goalBoard)


