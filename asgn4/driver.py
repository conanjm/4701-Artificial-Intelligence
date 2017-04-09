import sys
from collections import deque

def revise(board, domain, i, j):
	removed = set()
	for vi in domain[i]:
		res = False
		for vj in domain[j]:
			if vi != vj:
				res = True
				break
		if not res:
			removed.add(vi)

	if not removed:
		return True

	for num in removed:
		domain[i].remove(num)
	return False


def ac_3(board):
	# initialize queue, arcs and domains
	q, domain = deque(), {}
	for i in xrange(81):
		domain[i] = set([board[i]]) if board[i] != 0 else set([range(1,10)])
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

if __name__ == '__main__':

	with open(sys.argv[1]) as ifile:
		for line in ifile:
			board = {}
			for i, ch in enumerate(line):
				board[i] = ch

			if ac_3(board):
				print "OK"
			else:
				print "Not solvable"
