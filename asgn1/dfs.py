import sys, copy, time, resource
from math import sqrt
from collections import deque

def dfs(initBoard, goalBoard, initIdx, nodes_expanded):
	frontier, fset, fidx, explored = [initBoard], {initBoard}, [initIdx], set()

	while len(frontier):
		curBoard = frontier.pop()
		fset.remove(curBoard)
		idx = fidx.pop()
		explored.add(curBoard)

		if curBoard == goalBoard:
			print 'success'
			return

		nodes_expanded += 1
		print nodes_expanded

		delta = int(sqrt(len(curBoard)))

		# right
		if (idx+1) % delta:
			neighbor = list(curBoard)
			neighbor[idx], neighbor[idx+1] = neighbor[idx+1] ,neighbor[idx]
			neighbor = tuple(neighbor)
			if neighbor not in fset and neighbor not in explored:
				frontier.append(neighbor)
				fset.add(neighbor)
				fidx.append(idx+1)

		#left
		if idx % delta:
			neighbor = list(curBoard)
			neighbor[idx], neighbor[idx-1] =neighbor[idx-1], neighbor[idx]
			neighbor = tuple(neighbor)
			if neighbor not in fset and neighbor not in explored:
				frontier.append(neighbor)
				fset.add(neighbor)
				fidx.append(idx-1)

		#down
		if idx + delta < len(curBoard):
			neighbor = list(curBoard)
			neighbor[idx], neighbor[idx+delta] = neighbor[idx+delta], neighbor[idx]
			neighbor = tuple(neighbor)
			if neighbor not in fset and neighbor not in explored:
				frontier.append(neighbor)
				fset.add(neighbor)
				fidx.append(idx+delta)

		#up
		if idx - delta >=0:
			neighbor = list(curBoard)
			neighbor[idx], neighbor[idx-delta] = neighbor[idx-delta], neighbor[idx]
			neighbor = tuple(neighbor)
			if neighbor not in fset and neighbor not in explored:
				frontier.append(neighbor)
				fset.add(neighbor)
				fidx.append(idx-delta)

	return 'Failure'



if __name__ == '__main__':
	method, initBoard = sys.argv[1], tuple(map(int, sys.argv[2].split(',')))
	goalBoard = tuple(range(len(initBoard)))
	dfs(initBoard, goalBoard, initBoard.index(0), 0)