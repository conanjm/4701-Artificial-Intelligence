from random import *
from BaseAI import BaseAI
import time, math

vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)

class PlayerAI(BaseAI):

	def numberOfMerges(self, grid):
		ud, lr = 0,0
		for i in xrange(4):
			for j in xrange(4):
				if grid.map[i][j] == 0:
					continue
				if j+1 < 4 and grid.map[i][j] == grid.map[i][j+1]:
					lr += 1
				if i+1 < 4 and grid.map[i][j] == grid.map[i+1][j]:
					ud += 1
		return max(ud, lr)

	def smooth(self, grid):
		res = 0
		for i in xrange(4):
			for j in xrange(4):
				if grid.map[i][j] != 0:
					val = math.log(grid.map[i][j], 2)
					if j+1 < 4 and grid.map[i][j+1] != 0:
						right = math.log(grid.map[i][j+1], 2)
						res -= abs(right - val)
					if i+1 < 4 and grid.map[i+1][j] != 0:
						down = math.log(grid.map[i+1][j], 2)
						res -= abs(down - val)
		return res

	def numberOfEmptyTiles(self, grid):
		count = 0
		for i in xrange(4):
			for j in xrange(4):
				if grid.map[i][j] == 0:
					count += 1
		return math.log(count, 2)

	def smooth(self, grid):
		res = 0
		for i in xrange(4):
			for j in xrange(4):
				if j+1 < 4:
					res += abs( (0 if grid.map[i][j]==0 else math.log(grid.map[i][j], 2)) - (0 if grid.map[i][j+1]==0 else math.log(grid.map[i][j+1], 2)))
				if i+1 < 4:
					res += abs( (0 if grid.map[i][j]==0 else math.log(grid.map[i][j], 2)) - (0 if grid.map[i+1][j]==0 else math.log(grid.map[i+1][j], 2)))
		return res

	def maxVal(self, grid):
		res = -float("inf")
		for i in xrange(4):
			for j in xrange(4):
				if grid.map[i][j] > res:
					res = grid.map[i][j]
		return math.log(res, 2)

	def monotonic(self, grid):
		rIncre, rDecre, dIncre, dDecre = 0,0,0,0

		for i in xrange(4):
			for j in xrange(4):
				cur = 0 if grid.map[i][j]==0 else math.log( grid.map[i][j] ,2 )
				if j+1 < 4:
					right = 0 if grid.map[i][j+1]==0 else math.log( grid.map[i][j+1] ,2 )
					if cur < right:
						rIncre += cur - right
					elif cur > right:
						rDecre += right - cur
					else:
						pass
				if i+1 < 4:
					down = 0 if grid.map[i+1][j]==0 else math.log( grid.map[i+1][j] , 2 )
					if cur < down:
						dIncre += cur - down 
					elif cur > down:
						dDecre += down - cur
					else:
						pass
		return max(rIncre, rDecre) + max(dIncre, dDecre)

	# def monotonic(self, grid):
	# 	lrIncreCnt, lrDecreCnt, udIncreCnt, udDecreCnt = 0,0,0,0
	# 	for i in xrange(4):
	# 		for j in xrange(4):
	# 			lrIncre, lrDecre, udIncre, udDecre = False, False, False, False
	# 			if grid.map[i][j] != 0:
	# 				if j+1 < 4 and grid.map[i][j+1] > grid.map[i][j]:
	# 					lrIncre = True
	# 				if i+1 < 4 and grid.map[i][j] < grid.map[i+1][j]:
	# 					udIncre = True
	# 			if j+1 < 4 and grid.map[i][j+1] != 0 and grid.map[i][j] > grid.map[i][j+1]:
	# 				lrDecre = True
	# 			if i+1 < 4 and grid.map[i+1][j] != 0 and grid.map[i][j] > grid.map[i+1][j]:
	# 				udDecre = True

	# 		if lrIncre == True and lrDecre == False:
	# 			lrIncreCnt += 1
	# 		elif lrIncre == False and lrDecre == True:
	# 			lrDecreCnt += 1
	# 		else:
	# 			pass
	# 		if udIncre == True and udDecre == False:
	# 			udIncreCnt += 1
	# 		elif udIncre == False and udDecre == False:
	# 			udDecreCnt += 1
	# 		else:
	# 			pass
	# 	return max(lrIncreCnt, max(lrDecreCnt, max(udIncreCnt, udDecreCnt)))

	def h(self, grid):
		return  self.monotonic(grid)
		+ 2.7 * math.log(grid.getAvailableCells(), 2) 
		+ 0.1 * self.smooth(grid) 
		+ self.maxVal(grid)

	def getChildren(self, moves, grid):
		children = []
		for move in moves:
			gridClone = grid.clone()
			if move == 0:
				gridClone.moveUD(False)
			elif move == 1:
				gridClone.moveUD(True)
			elif move == 2:
				gridClone.moveLR(False)
			else:
				gridClone.moveLR(True)
			children.append(gridClone)
		return children

	def terminal_test(self, grid, curDepth, depth):
		if curDepth == depth:
			return True
		return False

		# if time.clock() - preTime >= 0.00002:
		# 	preTime = time.clock()
		# 	return True
		# return False

	def maximize(self, grid, a, b, curDepth, depth):

		if self.terminal_test(grid, curDepth, depth):
			return None, self.h(grid)

		moves = grid.getAvailableMoves(range(4))
		children = self.getChildren(moves, grid)

		maxMove, maxUtility = None, -float("inf")

		for i, child in enumerate(children):
			_, utility = self.minimize(child, a, b, curDepth + 1, depth)

			if utility > maxUtility:
				maxMove, maxUtility = moves[i], utility

			if maxUtility >= b:
				break
			
			if maxUtility > a:
				a = maxUtility
		
		return maxMove, maxUtility

	def minimize(self, grid, a, b, curDepth, depth):

		if self.terminal_test(grid, curDepth, depth):
			return None, self.h(grid)

		moves = grid.getAvailableMoves(range(4))
		children = self.getChildren(moves, grid)

		minMove, minUtility = None, float("inf")

		for i, child in enumerate(children):
			_, utility = self.maximize(child, a, b, curDepth + 1, depth)

			if utility < minUtility:
				minMove, minUtility = moves[i], utility

			if minUtility <= a:
				break;

			if minUtility < b:
				b = minUtility
		
		return minMove, minUtility


	def getMove(self, grid):
		a, b = -float("inf"), float("inf")
		preTime, depth = time.clock(), 0
		move = randint(0,3)
		startTime, preTime = time.clock(), time.clock()
		while 0.2 - (time.clock()-startTime) > 4 * ( time.clock() - preTime ):
			depth += 1
			preTime = time.clock()
			move, utility = self.maximize(grid, a, b, 0, depth)
		return move



