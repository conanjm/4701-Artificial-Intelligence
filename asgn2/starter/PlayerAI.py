from random import *
from BaseAI import BaseAI
import time

vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)

class PlayerAI(BaseAI):

	def __init__(self):
		self.level = 0

	def numberOfSameTiles(self, grid):
		count = 0
		for i in xrange(4):
			for j in xrange(4):
				if grid.map[i][j] == 0:
					continue;
				if j+1 < 4 and grid.map[i][j] == grid.map[i][j+1]:
					count += 1
				if i+1 < 4 and grid.map[i][j] == grid.map[i+1][j]:
					count += 1
		return float(count) / 25

	def numberOfEmptyTiles(self, grid):
		count = 0
		for i in xrange(4):
			for j in xrange(4):
				if grid.map[i][j] == 0:
					count += 1
		return float(count) / 16

	def monotonic(self, grid):
		lrIncreCnt, lrDecreCnt, udIncreCnt, udDecreCnt = 0,0,0,0
		for i in xrange(4):
			for j in xrange(4):
				lrIncre, lrDecre, udIncre, udDecre = False, False, False, False
				if grid.map[i][j] != 0:
					if j+1 < 4 and grid.map[i][j+1] > grid.map[i][j]:
						lrIncre = True
					if i+1 < 4 and grid.map[i][j] < grid.map[i+1][j]:
						udIncre = True
				if j+1 < 4 and grid.map[i][j+1] != 0 and grid.map[i][j] > grid.map[i][j+1]:
					lrDecre = True
				if i+1 < 4 and grid.map[i+1][j] != 0 and grid.map[i][j] > grid.map[i+1][j]:
					udDecre = True

			if lrIncre == True and lrDecre == False:
				lrIncreCnt += 1
			elif lrIncre == False and lrDecre == True:
				lrDecreCnt += 1
			else:
				pass
			if udIncre == True and udDecre == False:
				udIncreCnt += 1
			elif udIncre == False and udDecre == False:
				udDecreCnt += 1
			else:
				pass
		return float(max(lrIncreCnt, max(lrDecreCnt, max(udIncreCnt, udDecreCnt)))) / 8

	def h(self, grid):
		return 0.1 * self.monotonic(grid) + 0.5 * self.numberOfEmptyTiles(grid) + 0.4 * self.numberOfSameTiles(grid)

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

	def terminal_test(self, grid, preTime):
		if time.clock() - preTime >= 0.0002:
			preTime = time.clock()
			return True
		return False

	def maximize(self, grid, a, b, preTime):

		if self.terminal_test(grid, preTime):
			return None, self.h(grid)

		moves = grid.getAvailableMoves(range(4))
		children = self.getChildren(moves, grid)

		maxMove, maxUtility = None, -float("inf")

		for i, child in enumerate(children):
			_, utility = self.minimize(child, a, b, preTime)

			if utility > maxUtility:
				maxMove, maxUtility = moves[i], utility

			if maxUtility >= b:
				break
			
			if maxUtility > a:
				a = maxUtility
		
		return maxMove, maxUtility

	def minimize(self, grid, a, b, preTime):

		if self.terminal_test(grid, preTime):
			return None, self.h(grid)

		moves = grid.getAvailableMoves(range(4))
		children = self.getChildren(moves, grid)

		minMove, minUtility = None, float("inf")

		for i, child in enumerate(children):
			move, utility = self.maximize(child, a, b, preTime)

			if utility < minUtility:
				minMove, minUtility = moves[i], utility

			if minUtility <= a:
				break;

			if minUtility < b:
				b = minUtility
		
		return minMove, minUtility


	def getMove(self, grid):
		a, b = -float("inf"), float("inf")
		move, utility = self.maximize(grid, a, b, time.clock())
		return move


