import maya.cmds as cmds
import random



def startCell(cellSize):
	'''
	Input: cell Size

		- Create the first cell
	
	Output: cell name, centerPosition
	'''

	print('cellSize: {}'.format(cellSize))

	# create object: startCell
	cell = cmds.polyPlane(n='cell', w=cellSize, h=cellSize, sx=1, sy=1)
	
	# get objectCenter
	XYZ = cmds.objectCenter(cell[0], gl=True)		
	x = str(int(XYZ[0]))
	z = str(int(XYZ[2]))
	xz = x +' ' +z
	print('startCell position: {}'.format(xz))

	output = (cell[0], xz)
	return output


def addCell(cellSize, cellList, setList):
	'''
	Input: cellSize, list of cells and list of cell positions
	
		- selects a random cell and checks for neigbours
		- a neighbours cell is created
	'''

	con = True
	while con:

		# shuffle list
		random.shuffle(cellList)

		cell = cellList[0]
		XYZ = cmds.objectCenter(cell, gl=True)		
		posX = XYZ[0]
		posZ = XYZ[2]
		print('\ncheck neighbouers')
		print('list size: {}'.format(len(cellList)))
		print('random index: {}'.format(0))
		print('selected cell: {}'.format(cell))
		print('cell posX: {}'.format(posX))
		print('cell posZ: {}'.format(posZ))


		# Calculate neighbours position
		topCellX = str(int(posX))
		topCellZ = str(int(posZ + cellSize))
		bottomCellX = str(int(posX))
		bottomCellZ = str(int(posZ - cellSize))
		leftCellX = str(int(posX + cellSize))
		leftCellZ = str(int(posZ))
		rightCellX = str(int(posX - cellSize))
		rightCellZ = str(int(posZ))
		print('topCell    X: {}   Z: {}'.format(topCellX, topCellZ))
		print('bottomCell X: {}   Z: {}'.format(bottomCellX, bottomCellZ))
		print('leftCell   X: {}   Z: {}'.format(leftCellX, leftCellZ))
		print('rightCell  X: {}   Z: {}'.format(rightCellX, rightCellZ))

		# Concatenate values
		topxz = topCellX +' ' +topCellZ
		bottomxz = bottomCellX +' ' + bottomCellZ
		leftxz = leftCellX +' ' +leftCellZ
		rightxz = rightCellX +' ' +rightCellZ
		print(topxz)
		print(bottomxz)
		print(leftxz)
		print(rightxz)

		# Set neighbours position
		neighbours = {topxz, bottomxz, leftxz, rightxz}
		newNeighours = list(neighbours.difference(setList)) 
		print('set newnewNeighours: {}'.format(newNeighours))
		

		if len(newNeighours) != 0:

			# Select random neihgours position
			rand = random.randint(0, len(newNeighours)-1)
			neighbour = newNeighours[0].split()
		
			con = False


	neighbourX = neighbour[0]
	neighbourZ = neighbour[1]
	print('neighbourX: {}'.format(neighbourX))
	print('neighbourZ: {}'.format(neighbourZ))

	# Generate new cell
	cell = cmds.polyPlane(n='cell', w=cellSize, h=cellSize, sx=1, sy=1)
	cmds.move(neighbourX, 0, neighbourZ) 

	# Concatenate Position
	xz = neighbourX +' ' +neighbourZ

	output = (cell[0], xz)
	return output