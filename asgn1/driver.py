import sys, time, resource, heapq
from math import sqrt, fabs
from collections import deque

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
	def __init__(self, board, idx, move, parent, depth, seq=0):
		self.board = board
		self.idx = idx
		self.move = move
		self.parent = parent
		self.depth = depth
		self.seq = seq;

	def __cmp__(self, other):
		gself, gother = self.depth + h(self.board), other.depth + h(other.board)
		if gself < gother or (gself == gother and getMove(self.move) < getMove(other.move) ) or (gself == gother and getMove(self.move) == getMove(other.move) and self.seq < other.seq ):
			return -1
		return 1
		
def up(node,  length):
	if node.idx - length >= 0:
		newBoard = list(node.board)
		newBoard[node.idx], newBoard[node.idx-length] = newBoard[node.idx-length], newBoard[node.idx] 
		return tuple(newBoard)
	return None

def down( node, length):
	if node.idx + length < len(node.board):
		newBoard = list(node.board)
		newBoard[node.idx], newBoard[node.idx+length] = newBoard[node.idx+length], newBoard[node.idx] 
		return tuple(newBoard)
	return None

def left(node,  length):
	if node.idx % length:
		newBoard = list(node.board)
		newBoard[node.idx], newBoard[node.idx-1] = newBoard[node.idx-1], newBoard[node.idx] 
		return tuple(newBoard)
	return None

def right( node, length):
	if (node.idx+1) % length:
		newBoard = list(node.board)
		newBoard[node.idx], newBoard[node.idx+1] = newBoard[node.idx+1], newBoard[node.idx] 
		return tuple(newBoard)
	return None

def output(node, nodes_expanded, frontier, max_fringe_size, max_search_depth):
	f = open('output.txt', 'wb')
	path = []
	tmp = node
	while tmp.parent is not None:
		path.append(tmp.move)
		tmp = tmp.parent
	path.reverse()
	f.write('path_to_goal: {}\n'.format(list(path)) )
	f.write ('cost_of_path: {}\n'.format(len(path)) )
	f.write ('nodes_expanded: {}\n'.format(nodes_expanded))
	f.write ('fringe_size: {}\n'.format(len(frontier)))
	f.write ('max_fringe_size: {}\n'.format(max_fringe_size))
	f.write ('search_depth: {}\n'.format(node.depth))
	f.write ('max_search_depth: {}\n'.format(max_search_depth))
	f.write ('running_time: {}\n'.format(time.time() - startTime ))
	f.write ('max_ram_usage: {}\n'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / float(1024**2)))
	f.close()
	return

def bfs(initBoard, goalBoard):
	max_fringe_size, max_search_depth, nodes_expanded, initIdx = 1, 0, 0, initBoard.index(0)
	frontier, fset, explored = deque([Node(initBoard, initBoard.index(0), '', None, 0)]), {initBoard},  set()

	while len(frontier):
		node = frontier.popleft()
		fset.remove(node.board)
		explored.add(node.board)

		if node.board == goalBoard:
			output(node, nodes_expanded, frontier, max_fringe_size, max_search_depth)
			return

		nodes_expanded += 1
		length = int(sqrt(len(node.board)))

		# right
		newBoard = up( node, length )
		if newBoard is not None and newBoard not in fset and newBoard not in explored:
			child = Node(newBoard, node.idx-length, 'Up', node, node.depth+1 )
			frontier.append(child)
			fset.add(child.board)
			max_search_depth = max(max_search_depth, frontier[-1].depth)

		newBoard = down( node, length )
		if newBoard is not None and newBoard not in fset and newBoard not in explored:
			child = Node(newBoard, node.idx+length, 'Down', node, node.depth+1 )
			frontier.append(child)
			fset.add(child.board)
			max_search_depth = max(max_search_depth, frontier[-1].depth)

		newBoard = left( node, length )
		if newBoard is not None and newBoard not in fset and newBoard not in explored:
			child = Node(newBoard, node.idx-1, 'Left', node, node.depth+1 )
			frontier.append(child)
			fset.add(child.board)
			max_search_depth = max(max_search_depth, frontier[-1].depth)

		newBoard = right( node, length )
		if newBoard is not None and newBoard not in fset and newBoard not in explored:
			child = Node(newBoard, node.idx+1, 'Right', node, node.depth+1 )
			frontier.append(child)
			fset.add(child.board)
			max_search_depth = max(max_search_depth, frontier[-1].depth)

		max_fringe_size = max( max_fringe_size, len(frontier))

	return 'Failure'

def dfs(initBoard, goalBoard):
	max_fringe_size, max_search_depth, nodes_expanded = 1, 0, 0
	frontier, fset, explored = [Node(initBoard, initBoard.index(0), '', None, 0)], {initBoard}, set()	
	length = int(sqrt(len(initBoard)))
	
	while len(frontier):
		node = frontier.pop()
		fset.remove(node.board)
		explored.add(node.board)

		if node.board == goalBoard:
			output(node, nodes_expanded, frontier, max_fringe_size, max_search_depth)
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

def ast(initBoard, goalBoard):
	seq = 0
	max_fringe_size, max_search_depth, nodes_expanded, length = 1, 0, 0, (int(sqrt(len(initBoard))))
	frontier, explored = [], { initBoard }
	heapq.heappush(frontier, Node(initBoard, initBoard.index(0), '', None, 0, seq ) )
	seq += 1
	fdict = {initBoard:frontier[0]}

	while len(frontier):
		node = heapq.heappop(frontier)
		del fdict[node.board]
		explored.add(node.board)

		if node.board == goalBoard:
			output(node, nodes_expanded, frontier, max_fringe_size, max_search_depth)
			return

		nodes_expanded += 1

		newBoard = up( node, length)
		if newBoard is not None:
			if newBoard not in fdict.keys() and newBoard not in explored:
				child = Node(newBoard, node.idx-length, 'Up', node, node.depth+1, seq )
				seq += 1
				heapq.heappush(frontier, child )
				max_fringe_size = max( max_fringe_size, len(frontier))
				fdict[newBoard] = child
				max_search_depth = max(max_search_depth, child.depth)
			elif newBoard in fdict.keys():
				child = fdict[newBoard]
				if node.depth+1 < child.depth:
					child.depth = node.depth+1
					frontier.remove(child)
					heapq.heappush(frontier, child)
			else:
				pass

		newBoard = down( node, length)
		if newBoard is not None:
			if newBoard not in fdict.keys() and newBoard not in explored:
				child = Node(newBoard, node.idx+length, 'Down', node, node.depth+1 , seq)
				seq += 1
				heapq.heappush(frontier, child )
				max_fringe_size = max( max_fringe_size, len(frontier))
				fdict[newBoard] = child
				max_search_depth = max(max_search_depth, child.depth)
			elif newBoard in fdict.keys():
				child = fdict[newBoard]
				if node.depth+1 < child.depth:
					child.depth = node.depth+1
					frontier.remove(child)
					heapq.heappush(frontier,child)
			else:
				pass

		newBoard = left( node, length)
		if newBoard is not None:
			if newBoard not in fdict.keys() and newBoard not in explored:
				child = Node(newBoard, node.idx-1, 'Left', node, node.depth+1, seq )
				seq += 1
				heapq.heappush(frontier, child )
				max_fringe_size = max( max_fringe_size, len(frontier))
				fdict[newBoard] = child
				max_search_depth = max(max_search_depth, child.depth)
			elif newBoard in fdict.keys():
				child = fdict[newBoard]
				if node.depth+1 < child.depth:
					child.depth = node.depth+1
					frontier.remove(child)
					heapq.heappush(frontier, child)
			else:
				pass

		newBoard = right( node, length)
		if newBoard is not None: 
			if newBoard not in fdict.keys() and newBoard not in explored:
				child = Node(newBoard, node.idx+1, 'Right', node, node.depth+1, seq )
				seq += 1
				heapq.heappush(frontier, child )
				max_fringe_size = max( max_fringe_size, len(frontier))
				fdict[newBoard] = child
				max_search_depth = max(max_search_depth, child.depth)
			elif newBoard in fdict.keys():
				child = fdict[newBoard]
				if node.depth+1 < child.depth:
					child.depth = node.depth+1
					frontier.remove(child)
					heapq.heappush(frontier, child)
			else:
				pass

	return 'Failure'

def ida(initBoard, goalBoard):

	length = int(sqrt(len(initBoard)))
	initHeuristic = h(initBoard)
	threshold = initHeuristic
	max_fringe_size, max_search_depth = 1, 0
	while True:
		nodes_expanded = 0
		frontier, fset, explored  = [ Node(initBoard, initBoard.index(0), '', None, 0, initHeuristic )], {initBoard}, { }
		delta = float('inf')
		while len(frontier):
			node = frontier.pop()
			fset.remove(node.board)
			explored[node.board] = node.depth

			if node.board == goalBoard:
				output(node, nodes_expanded, frontier, max_fringe_size, max_search_depth)
				return

			nodes_expanded += 1

			newBoard = right( node, length)
			if newBoard is not None and newBoard not in fset:
				heuristic = h(newBoard)
				if node.depth +1+ heuristic <= threshold and ( newBoard not in explored.keys() or explored[newBoard]>node.depth ):
					child = Node(newBoard, node.idx+1, 'Right', node, node.depth+1)
					frontier.append(child)
					fset.add(child.board)
					max_search_depth = max(max_search_depth, frontier[-1].depth)
				# else:
				# 	delta = min(delta, node.depth+1+h(newBoard))

			newBoard = left(node, length)
			if newBoard is not None and newBoard not in fset:
				heuristic = h(newBoard)
				if node.depth +1+ heuristic <= threshold and ( newBoard not in explored.keys() or explored[newBoard]>node.depth ):
					child = Node(newBoard, node.idx-1, 'Left', node, node.depth+1 )
					frontier.append(child)
					fset.add(child.board)
					max_search_depth = max(max_search_depth, frontier[-1].depth)
				# else:
				# 	delta = min(delta, node.depth+1+h(newBoard))

			newBoard = down( node, length)
			if newBoard is not None and newBoard not in fset:
				heuristic = h(newBoard)
				if node.depth +1+ heuristic <= threshold and ( newBoard not in explored.keys() or explored[newBoard]>node.depth ):
					child = Node(newBoard, node.idx+length, 'Down', node, node.depth+1 )
					frontier.append(child)
					fset.add(child.board)
					max_search_depth = max(max_search_depth, frontier[-1].depth)
				# else:
				# 	delta = min(delta, node.depth+1+h(newBoard))
			
			newBoard = up( node, length)
			if newBoard is not None and newBoard not in fset:
				heuristic = h(newBoard)
				if node.depth +1+ heuristic <= threshold and ( newBoard not in explored.keys() or explored[newBoard]>node.depth ):
					child = Node(newBoard, node.idx-length, 'Up', node, node.depth+1 )
					frontier.append(child)
					fset.add(child.board)
					max_search_depth = max(max_search_depth, frontier[-1].depth)
				# else:
				# 	delta = min(delta, node.depth+1+h(newBoard))

			max_fringe_size = max( max_fringe_size, len(frontier))

		threshold += 1

if __name__ == '__main__':
	startTime = time.time()
	method, initBoard = sys.argv[1], tuple(map(int, sys.argv[2].split(',')))
	goalBoard = tuple(range(len(initBoard)))
	if method == 'bfs':
		bfs(initBoard, goalBoard)
	elif method == 'dfs':
		dfs(initBoard, goalBoard)
	elif method == 'ast':
		ast(initBoard, goalBoard)
	elif method == 'ida':
		ida(initBoard, goalBoard)
	else:
		"Please check your input"

