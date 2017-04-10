import sys, heapq
from collections import deque

def revise(board, domain, i, j):
	removed = set()
	for vi in domain[i]:
		available = False
		for vj in domain[j]:
			if vi != vj:
				available = True
				break
		if not available:
			removed.add(vi)

	if not removed:
		return False

	for num in removed:
		domain[i].remove(num)
	return True


def ac_3(board):
	# initialize queue, arcs and domains
	q, domain = deque(), {}
	for i in xrange(81):
		domain[i] = set([board[i]]) if board[i] != 0 else set(range(1,10))
		row, col = i/9, i%9
		# arc for same row and same col
		for v in xrange(9):
			if v != col:
				q.append((i, row * 9 + v))
			if v != row:
				q.append((i, v * 9 + col))
		# arc for same region (other than those in the same row or same col)
		idx = 3 * (row / 3) + col / 3	# this is the idx for the region
		for r in xrange((idx / 3 ) * 3, (idx / 3) * 3 + 3):
			for c in xrange((idx % 3)* 3, (idx % 3) * 3 + 3):
				if r != row and c != col:
					q.append((i, r * 9 + c))

	while len(q):
		i, j = q.popleft()

		if revise(board, domain, i, j):
			if not domain[i]:
				return False
			# add each of i's neighbors other than j
			row, col = i/9, i%9
			
			for v in xrange(9):
				# neighbor for same row ( row, v)
				k = row * 9 + v
				if k != j and v != col:
					q.append((k, i))
				# neighbor for same col ( v, col)
				k = v * 9 + col
				if k != j and v != row:
					q.append((k, i))
				# neighbor for same region (other than same row/col)
				idx = 3 * (row / 3) + col / 3
				for r in xrange((idx / 3 ) * 3, (idx / 3) * 3 + 3):
					for c in xrange((idx % 3)* 3, (idx % 3) * 3 + 3):
						if r != row and c != col and r * 9 + c != j:
							q.append((r * 9 + c, i))
	return True

















def printBoard(board):
	print '================='
	for i in xrange(81):
		print board[i],
		if i % 9 == 8:
			print
	print '================='


def mrv(domain, unassigned):
	minIdx, minVal = -1, float('inf')
	for i in unassigned:
		if len(domain[i]) < minVal:
			minVal = len(domain[i])
			minIdx = i
	return minIdx


def backtrace(board, domain, unassigned):

	if not unassigned:
		return True

	# pick out the variable with minimum remaining values
	i = mrv(domain, unassigned)
	unassigned.remove(i)

	row, col = i/9, i%9
	
	for val in domain[i]:
		removed = {}	# this 'removed' variables is to restore to original domains when encounter a failure assignment
		board[i] = val
		
		tryNextVal = False

		# perform forward checking on every unassigned variables
		# forward check on same row and same col
		for v in xrange(9):
		
			# check same row unassigned elements [row, v]
			if v != col and row*9+v in unassigned and val in domain[row*9+v]:

				if len(domain[row*9+v])==1:

					unassigned.add(i)
					board[i] = 'x'
					tryNextVal = True
					break

				domain[row*9+v].remove(val)
				if row*9+v not in removed:
					removed[row*9+v] = set()
				removed[row*9+v].add(val)

			# check same col unassigned elements [v, col]
			if v != row and v*9+col in unassigned and val in domain[v*9+col]:
				
				if len(domain[v*9+col])==1:
					
					for rm in removed:
						for v in removed[rm]:
							domain[rm].add(v)

					unassigned.add(i)
					board[i] = 'x'
					tryNextVal = True
					break

				domain[v*9+col].remove(val)
				if v*9+col not in removed:
					removed[v*9+col] = set()
				removed[v*9+col].add(val)


		if tryNextVal == True:
			continue

		# forward checking for same region unassigned elements [r,c]
		idx = 3 * (row / 3) + col / 3
		for r in xrange((idx / 3 ) * 3, (idx / 3) * 3 + 3):
			for c in xrange((idx % 3)* 3, (idx % 3) * 3 + 3):
				if r != row and c != col and r*9+c in unassigned and val in domain[r*9+c]:
					if len(domain[r*9+c])==1:
						for rm in removed:
							for v in removed[rm]:
								domain[rm].add(v)
						unassigned.add(i)
						board[i] = 'x'
						tryNextVal = True
						break

					domain[r*9+c].remove(val)
					if r*9+c not in removed:
						removed[r*9+c] = set()
					removed[r*9+c].add(val)

		if tryNextVal == True:
			continue

		res = backtrace(board, domain, unassigned)
		if res:
			return True

		for rm in removed:
			for v in removed[rm]:
				domain[rm].add(v)

	unassigned.add(i)
	board[i] = 'x'
	return False








def isConsistent(board, idx, val):
	row, col = idx/9, idx%9
	for v in xrange(9):
		# check same row elements [row, v]
		if board[row*9+v] == val:
			return False
		# check same col elements [v, col]
		if board[v*9+col] == val:
			return False
	idx = 3 * (row / 3) + col / 3
	for r in xrange((idx / 3 ) * 3, (idx / 3) * 3 + 3):
		for c in xrange((idx % 3)* 3, (idx % 3) * 3 + 3):
			if board[r*9+c] == val:
				return False
	return True



def plainbacktrace(board, idx):
	if idx==81:
		return True

	if board[idx] == 0:
		for i in xrange(1, 10):
			if isConsistent(board, idx, i):
				board[idx] = i
				if plainbacktrace(board, idx+1):
					return True
				board[idx] = 0
		return False

	else:
		return plainbacktrace(board, idx+1)




def backtrack(board):
	domain = {}
	# initialize domain for all variables
	for i in board:
		domain[i] = set([board[i]]) if board[i] != 0 else set(range(1, 10))

	# printBoard(board)

	return plainbacktrace(board, 0)

	# return backtrace(board, domain, set(range(81)))


if __name__ == '__main__':

	# with open(sys.argv[1]) as ifile:
	# 	for line in ifile:
	board = {}
	for i, ch in enumerate(sys.argv[1]):
		if i < 81:
			board[i] = int(ch)

	if not backtrack(board):
		printBoard(board)
		print 'not solvable'
	else:
		printBoard(board)
		print 'ok'

