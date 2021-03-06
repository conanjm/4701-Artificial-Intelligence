import sys, time, resource
from math import sqrt
from collections import deque
from copy import deepcopy

startTime = time.time()

class Node:
	# move: the move takes from its parent to itself
	def __init__(self, move, parent, depth):
		self.move = move
		self.parent = parent
		self.depth = depth

def up( curBoard, idx, fset, explored, frontier, fidx, tree, delta, node ):
	if idx - delta >=0:
		neighbor = list(curBoard)
		neighbor[idx], neighbor[idx-delta] = neighbor[idx-delta], neighbor[idx]
		neighbor = tuple(neighbor)
		if neighbor not in fset and neighbor not in explored:
			frontier.append(neighbor)
			fset.add(neighbor)
			fidx.append(idx-delta)
			tree.append(Node('Up', node, node.depth+1))
			return True
	return False

def down( curBoard, idx, fset, explored, frontier, fidx, tree, delta, node ):
	if idx + delta < len(curBoard):
		neighbor = list(curBoard)
		neighbor[idx], neighbor[idx+delta] = neighbor[idx+delta], neighbor[idx]
		neighbor = tuple(neighbor)
		if neighbor not in fset and neighbor not in explored:
			frontier.append(neighbor)
			fset.add(neighbor)
			fidx.append(idx+delta)
			tree.append(Node('Down', node, node.depth+1))
			return True
	return False

def left( curBoard, idx, fset, explored, frontier, fidx, tree, delta, node ):
	if idx % delta:
		neighbor = list(curBoard)
		neighbor[idx], neighbor[idx-1] =neighbor[idx-1], neighbor[idx]
		neighbor = tuple(neighbor)
		if neighbor not in fset and neighbor not in explored:
			frontier.append(neighbor)
			fset.add(neighbor)
			fidx.append(idx-1)
			tree.append(Node('Left', node, node.depth+1))
			return True
	return False

def right( curBoard, idx, fset, explored, frontier, fidx, tree, delta, node ):
	if (idx+1) % delta:
		neighbor = list(curBoard)
		neighbor[idx], neighbor[idx+1] = neighbor[idx+1] ,neighbor[idx]
		neighbor = tuple(neighbor)
		if neighbor not in fset and neighbor not in explored:
			frontier.append(neighbor)
			fset.add(neighbor)
			fidx.append(idx+1)
			tree.append(Node('Right', node, node.depth+1))
			return True
	return False

def bfs(initBoard, goalBoard):
	max_fringe_size, max_search_depth, nodes_expanded, initIdx = 1, 0, 0, initBoard.index(0)
	frontier, fset, fidx, explored = deque([initBoard]), {initBoard}, deque([initIdx]), set()
	tree = deque([Node('', None, 0)])

	while len(frontier):
		curBoard = frontier.popleft()
		fset.remove(curBoard)
		idx = fidx.popleft()
		explored.add(curBoard)
		node = tree.popleft()

		if curBoard == goalBoard:
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
		delta = int(sqrt(len(curBoard)))

		# right
		if up( curBoard, idx, fset, explored, frontier, fidx, tree, delta, node ):
			max_search_depth = max(max_search_depth, tree[-1].depth)	

		if down( curBoard, idx, fset, explored, frontier, fidx, tree, delta, node ):
			max_search_depth = max(max_search_depth, tree[-1].depth)

		if left( curBoard, idx, fset, explored, frontier, fidx, tree, delta, node ):
			max_search_depth = max(max_search_depth, tree[-1].depth)

		if right( curBoard, idx, fset, explored, frontier, fidx, tree, delta, node ):
			max_search_depth = max(max_search_depth, tree[-1].depth)

		max_fringe_size = max( max_fringe_size, len(frontier))

	return 'Failure'





def dfs(initBoard, goalBoard):
	max_fringe_size, max_search_depth, nodes_expanded, initIdx = 1, 0, 0, initBoard.index(0)
	frontier, fset, fidx, explored = [initBoard], {initBoard}, [initIdx], set()
	tree = [Node('', None, 0)]

	while len(frontier):
		curBoard = frontier.pop()
		fset.remove(curBoard)
		idx = fidx.pop()
		explored.add(curBoard)
		node = tree.pop()

		if curBoard == goalBoard:
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
		# print nodes_expanded

		delta = int(sqrt(len(curBoard)))

		# right
		if right( curBoard, idx, fset, explored, frontier, fidx, tree, delta, node ):
			max_search_depth = max(max_search_depth, tree[-1].depth)	

		if left( curBoard, idx, fset, explored, frontier, fidx, tree, delta, node ):
			max_search_depth = max(max_search_depth, tree[-1].depth)

		if down( curBoard, idx, fset, explored, frontier, fidx, tree, delta, node ):
			max_search_depth = max(max_search_depth, tree[-1].depth)

		if up( curBoard, idx, fset, explored, frontier, fidx, tree, delta, node ):
			max_search_depth = max(max_search_depth, tree[-1].depth)



		# if (idx+1) % delta:

		# 	neighbor = list(curBoard)
		# 	neighbor[idx], neighbor[idx+1] = neighbor[idx+1] ,neighbor[idx]
		# 	neighbor = tuple(neighbor)
		# 	if neighbor not in fset and neighbor not in explored:
		# 		frontier.append(neighbor)
		# 		fset.add(neighbor)
		# 		fidx.append(idx+1)
		# 		tree.append(Node('Right', node, node.depth+1))
		# 		max_search_depth = max(max_search_depth, tree[-1].depth)

		# #left
		# if idx % delta:
		# 	neighbor = list(curBoard)
		# 	neighbor[idx], neighbor[idx-1] =neighbor[idx-1], neighbor[idx]
		# 	neighbor = tuple(neighbor)
		# 	if neighbor not in fset and neighbor not in explored:
		# 		frontier.append(neighbor)
		# 		fset.add(neighbor)
		# 		fidx.append(idx-1)
		# 		tree.append(Node('Left', node, node.depth+1))
		# 		max_search_depth = max(max_search_depth, tree[-1].depth)

		# #down
		# if idx + delta < len(curBoard):
		# 	neighbor = list(curBoard)
		# 	neighbor[idx], neighbor[idx+delta] = neighbor[idx+delta], neighbor[idx]
		# 	neighbor = tuple(neighbor)
		# 	if neighbor not in fset and neighbor not in explored:
		# 		frontier.append(neighbor)
		# 		fset.add(neighbor)
		# 		fidx.append(idx+delta)
		# 		tree.append(Node('Down', node, node.depth+1))
		# 		max_search_depth = max(max_search_depth, tree[-1].depth)
				
		# #up
		# if idx - delta >=0:
		# 	neighbor = list(curBoard)
		# 	neighbor[idx], neighbor[idx-delta] = neighbor[idx-delta], neighbor[idx]
		# 	neighbor = tuple(neighbor)
		# 	if neighbor not in fset and neighbor not in explored:
		# 		frontier.append(neighbor)
		# 		fset.add(neighbor)
		# 		fidx.append(idx-delta)
		# 		tree.append(Node('Up', node, node.depth+1))
		# 		max_search_depth = max(max_search_depth, tree[-1].depth)

		max_fringe_size = max( max_fringe_size, len(frontier))

	return 'Failure'


if __name__ == '__main__':
	method, initBoard = sys.argv[1], tuple(map(int, sys.argv[2].split(',')))
	goalBoard = tuple(range(len(initBoard)))
	if method == 'bfs':
		bfs(initBoard, goalBoard)
	elif method == 'dfs':
		dfs(initBoard, goalBoard)
