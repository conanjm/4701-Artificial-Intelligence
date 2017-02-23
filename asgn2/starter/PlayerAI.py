from random import *
from BaseAI import BaseAI

vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)

class PlayerAI(BaseAI):

	def numberOfSameTiles(self, grid):
		count = 0
		for i in xrange(4):
			for j in xrange(4):
				if grid[i][j] == 0:
					continue;
				if j+1 < 4 and grid[i][j] == grid[i][j+1]:
					count += 1
				if i+1 < 4 and grid[i][j] == grid[i+1][j]:
					count += 1
		return float(count) / 25

	def numberOfEmptyTiles(self, grid):
		count = 0
		for i in xrange(4):
			for j in xrange(4):
				if grid[i][j] == 0:
					count += 1
		return float(count) / 16

	def monotonic(self, grid):
		lrIncreCnt, lrDecreCnt, udIncreCnt, udDecreCnt = 0,0,0,0
		for i in xrange(4):
			for j in xrange(4):
				lrIncre, lrDecre, udIncre, udDecre = False, False, False, False
				if x[i][j] != 0:
					if j+1 < 4 and x[i][j+1] > x[i][j]:
						lrIncre = True
					if i+1 < 4 and x[i][j] < x[i+1][j]:
						udIncre = True
				if j+1 < 4 and x[i][j+1] != 0 and x[i][j] > x[i][j+1]:
					lrDecre = True
				if i+1 < 4 and x[i+1][j] != 0 and s[i][j] > x[i+1][j]:
					upDecre = True

			if lrIncre == True and lrDecre == False:
				lrIncreCnt += 1
			else if lrIncre == False and lrDecre == True:
				lrDecreCnt += 1
			else:
				pass
			if upIncre == True and upDecre == False:
				upIncreCnt += 1
			else if upIncre == False and upDecre == False:
				upDecreCnt += 1
			else:
				pass
		return float(max(lrIncreCnt, max(lrDecreCnt, max(udIncreCnt, udDecreCnt)))) / 8


	def terminal_test(self, grid):

	def h(self, grid):

	def getChildren(self, moves):
		children = []
		for move in moves:
			gridClone = grid.clone()
			if move == 0:
				gridClone.moveUD(False)
				children.append(gridClone)
			elif move == 1:
				gridClone.moveUD(True)
			elif move == 2:
				gridClone.moveLR(False)
			else:
				gridClone.moveLR(True)
			children.append(gridClone)
		return children


	def maximize(self, grid, a, b):

		if terminal_test(grid):
			return None, h(grid)

		moves = grid.getAvailableMoves(range(4))
		children = getChildren(moves)

		maxMove, maxUtility = None, -float("inf")

		for i, child in enumerate(children):
			_, utility = minimize(child, a, b)

			if utility > maxUtility:
				maxMove, maxUtility = moves[i], utility

			if maxUtility >= b:
				break
			
			if maxUtility > a:
				a = maxUtility
		
		return maxMove, maxUtility

	def minimize(self, grid, a, b):

		if terminal_test(grid):
			return None, h(grid)

		moves = grid.getAvailableMoves(range(4))
		children = getChildren(moves)

		minMove, minUtility = None, float("inf")

		for i, child in enumerate(children):
			move, utility = maximize(child, a, b)

			if utility < minUtility:
				minMove, minUtility = moves[i], utility

			if minUtility <= a:
				break;

			if minUtility < b:
				b = minUtility
		
		return minMove, minUtility


	def getMove(self, grid):
		a, b = -float(inf), float(inf)
		move, utility = maximize(grid, a, b)
		return move


