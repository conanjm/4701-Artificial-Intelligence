from random import *
from BaseAI import BaseAI
import time, math

vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)

class PlayerAI(BaseAI):

	def __init__(self):
		self.level = 0

	def smooth(self, grid):
		num, denom = 0, 0
		for i in xrange(4):
			for j in xrange(4):
				if grid.map[i][j] != 0:
					if j+1<4:
						denom += 1
						if grid.map[i][j+1] == grid.map[i][j]:
							num += 1
						# if abs(math.log(grid.map[i][j+1],2) if grid.map[i][j+1]!=0 else 0 - math.log(grid.map[i][j], 2) if grid.map[i][j]!=0 else 0) <2:
						# 	num += 1
					if i+1<4:
						denom += 1
						if grid.map[i+1][j] == grid.map[i][j]:
							num += 1
						# if abs(math.log(grid.map[i+1][j], 2) if grid.map[i+1][j]!=0 else 0 - math.log(grid.map[i][j],2) if grid.map[i][j]!=0 else 0) < 2:
						# 	num += 1
		if num == 0:
			return 0
		return float(num) / denom

	def numberOfEmptyTiles(self, grid):
		count = 0
		for i in xrange(4):
			for j in xrange(4):
				if grid.map[i][j] == 0:
					count += 1
		return float(count) / 15

	def snake(self, grid):
		order = []
		for i in xrange(4):
			if grid.map[i][0] >= grid.map[i][1] and grid.map[i][1] >= grid.map[i][2] and grid.map[i][2] >= grid.map[i][3]:
				order.append(1)
			elif grid.map[i][0] <= grid.map[i][1] and grid.map[i][1] <= grid.map[i][2] and grid.map[i][2] <= grid.map[i][3]:
				order.append(-1)
			else:
				order.append(0)
		return order[0]==-order[1] and order[1] == -order[2] and order[2] == -order[3]


	def monotonic(self, grid):
		lrIncre, lrDecre, udIncre, udDecre = 0,0,0,0

		for i in xrange(4):
			if grid.map[i][0] <= grid.map[i][1] and grid.map[i][1] <= grid.map[i][2] and grid.map[i][2] <= grid.map[i][3]:
				lrIncre += 1
			if grid.map[i][0] >= grid.map[i][1] and grid.map[i][1] >= grid.map[i][2] and grid.map[i][2] >= grid.map[i][3]:
				lrDecre += 1
			if grid.map[0][i] <= grid.map[1][i] and grid.map[1][i] <= grid.map[2][i] and grid.map[2][i] <= grid.map[3][i]:
				udIncre += 1
			if grid.map[0][i] >= grid.map[1][i] and grid.map[1][i] >= grid.map[2][i] and grid.map[2][i] >= grid.map[3][i]:
				udDecre += 1

		return float(max(lrIncre, lrDecre) + max(udIncre, udDecre)) / 8

	def maxInCorner(self, grid):
		maxTile = grid.getMaxTile()
		return (grid.map[0][0]==maxTile) or (grid.map[0][3]==maxTile) or (grid.map[3][0]==maxTile) or (grid.map[3][3]==maxTile) 

	def maxInUL(self, grid):
		return grid.getMaxTile() == grid.map[0][0]

	def h(self, grid):
		#return  0.46 * self.numberOfEmptyTiles(grid) +  0.22 * self.snake(grid) + 0.27 * self.smooth(grid) + 0.05 * self.maxInCorner(grid)
		return  0.46 * self.numberOfEmptyTiles(grid) +  0.22 * self.monotonic(grid) + 0.27 * self.smooth(grid) + 0.05 * self.maxInCorner(grid)
		# return  0.5 * self.numberOfEmptyTiles(grid) + 0.05 * self.monotonic(grid) + 0.45 * self.smooth(grid) 



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

	def minimize(self, grid, a, b, preTime, depth):

		if time.clock() - preTime >= 0.00011:
			preTime = time.clock()
			return None, self.h(grid)

		moves = grid.getAvailableMoves(range(4))
		children = self.getChildren(moves, grid)

		minMove, minUtility = None, float("inf")

		for i, child in enumerate(children):
			move, utility = self.maximize(child, a, b, preTime, depth+1)

			if utility < minUtility:
				minMove, minUtility = moves[i], utility

			if minUtility <= a:
				break;

			if minUtility < b:
				b = minUtility
		
		return minMove, minUtility

	def maximize(self, grid, a, b, preTime, depth):

		if time.clock() - preTime >= 0.0001:
			preTime = time.clock()
			return None, self.h(grid)

		moves = grid.getAvailableMoves(range(4))
		children = self.getChildren(moves, grid)

		maxMove, maxUtility = None, -float("inf")

		for i, child in enumerate(children):
			_, utility = self.minimize(child, a, b, preTime, depth+1)

			if utility > maxUtility:
				maxMove, maxUtility = moves[i], utility

			if maxUtility >= b:
				break
			
			if maxUtility > a:
				a = maxUtility
		
		return maxMove, maxUtility

	def getMove(self, grid):
		a, b = -float("inf"), float("inf")

		move, utility = self.maximize(grid, a, b, time.clock(), 0)
		return move