import maya.cmds as cmds
import os

def roofPattern(cellSize, cellList, setList):
		"""
		Input: cellSize, list of cells and list of cell positions

			- A cell is selected
			- base of its positions it checks for neighboring cells
			- based on the number of neighbors and the neighbors position,
			the right roof-object is selected, with the polyRoof Function
		"""

		# get cellListst
		print('cellList: {}\n'.format(cellList))

		# convert: List to Set
		setList = set(setList)


		# create xz pos
		xzList = []
		for i in cellList:
			print('\n------------------------------------------------------------- createRoof_{}'.format(i.replace('Cell_:','')))
			
			name = 'roof{}'.format(i.replace('Cell_:cell',''))

			# get position
			XYZ = cmds.objectCenter(i, gl=True)
			x = XYZ[0]
			z = XYZ[2]
			xzItem = str(int(x)) +' ' +str(int(z))
			xzList.append(xzItem)
			print('{}.tx: {} \n{}.tz: {}'.format(i,x,i,z))

			# calculate neigbours pos
			topZ = str(int(z + cellSize))
			bottomZ = str(int(z - cellSize))
			leftX =  str(int(x + cellSize))
			rightX = str(int(x - cellSize))
			print('\ntopZ: {}\nbottomZ: {}\nleftX: {}\nrightX: {}'.format(topZ,bottomZ,leftX,rightX))
			
			# concatenate
			top = str(int(x)) +' ' +topZ
			bottom = str(int(x)) +' ' +bottomZ
			left = leftX +' ' +str(int(z))
			right = rightX +' ' +str(int(z))
			
			# find actual neighbours
			setNeighbours = {top, bottom, left, right}
			foundNeighbours = list( setList.intersection(setNeighbours))
			print('\nsim neighbours:   {}'.format(setNeighbours))
			print('all cell pos:     {}'.format(setList))
			print('found neighbours: {}\n'.format(foundNeighbours))
			

			# get names of the neighbours
			c = 0
			for a in xzList:
				for b in foundNeighbours:
					if a == b:
						print('{} neigbour: {}'.format(i, cellList[c]))
				c = c+1
		
			# get right roof type
			non = len(foundNeighbours)
			neighbourOrder = {99}
			print('')
			for i in foundNeighbours:
				pos = i.split()
				nx = int(pos[0])
				nz = int(pos[1])

				# top
				if nz > z:
					a = 1
					neighbourOrder.add(a)
					print('found top neighbour')
				# left
				if nx > x:
					b = 2
					neighbourOrder.add(b)
					print('found left neighbour')
				# bottom
				if nz < z:
					c = 3
					neighbourOrder.add(c)
					print('found bottom neighbour')
				# right
				if nx < x:
					d = 4
					neighbourOrder.add(d)
					print('found right neighbour')
	
			# find roof patterns
			print('')

			if non == 1:
				t = {1}
				l = {2}
				b = {3}
				r = {4}
				if t.issubset(neighbourOrder):
					print('generate top roof')
					polyRoof(name,1, x,z,0)
				if l.issubset(neighbourOrder):
					print('generate left roof')
					polyRoof(name,1, x,z,90)
				if b.issubset(neighbourOrder):
					print('generate bottom roof')
					polyRoof(name,1, x,z,0)
				if r.issubset(neighbourOrder):
					print('generate right roof')
					polyRoof(name,1, x,z,90)
			if non == 2:
				tl = {1,2} # top/left
				lb = {2,3} # left/bottom
				br = {3,4} # bottom/right
				rt = {1,4} # top/right
				rl = {2,4} # right/left
				tb = {1,3} # top/bottom
				if tl.issubset(neighbourOrder):
					print('generate top/left roof')
					polyRoof(name,2, x,z,0)
				if lb.issubset(neighbourOrder):
					print('generate left/bottom roof')
					polyRoof(name,2, x,z,90)
				if br.issubset(neighbourOrder):
					print('generate bottom/right roof')
					polyRoof(name,2, x,z,180)
				if rt.issubset(neighbourOrder):
					print('generate top/right roof')
					polyRoof(name,2, x,z,270)
				if rl.issubset(neighbourOrder):
					print('generate left/right roof')
					polyRoof(name,1, x,z,90)
				if tb.issubset(neighbourOrder):
					print('generate top/bottom roof')
					polyRoof(name,1, x,z,0)

			if non == 3:
				tlb = {1,2,3}
				lbr = {2,3,4}
				brt = {3,4,1}
				rtl = {4,1,2}
				if tlb.issubset(neighbourOrder):
					print('generate top/left/bottom roof')
					polyRoof(name,3, x,z, 0)
				if lbr.issubset(neighbourOrder):
					print('generate left/bottom/right roof')
					polyRoof(name,3, x,z, 90)
				if brt.issubset(neighbourOrder):
					print('generate bottom/right/top roof')
					polyRoof(name,3, x,z, 180)
				if rtl.issubset(neighbourOrder):
					print('generate top/right/ roof')
					polyRoof(name,3, x,z,270)	
			
			if non == 4:
				tlbr = {1,2,3,4}
				if tlbr.issubset(neighbourOrder):
					print('generate top/left/bottom/right roof')
					polyRoof(name, 4, x,z, 0)


def polyRoof(name, type, x, z, r):
		"""
		Input: RoofType, position, rotation

			- Each rooftype has a value,
			base on the value a roof-Object is selected
			and placed correclty in the scene
		"""

		if type == 1:
			roof = cmds.duplicate( 'Import_:roof_F_001', n=name )
			if r == 90:
				cmds.xform(roof[0], r=True,t=(x,0,z), ro=(0, 90, 0))
			else:
				cmds.xform(roof[0], r=True,t=(x,0,z), ro=(0, 0, 0) )
		if type == 2:
			roof = cmds.duplicate( 'Import_:roof_FL_001', n=name )
			if r == 0:
				cmds.xform(roof[0], r=True, t=(x,0,z))
			if r == 90:
				cmds.xform(roof[0], r=True, t=(x,0,z), ro=(0, 90, 0))
			if r == 180:
				cmds.xform(roof[0], r=True, t=(x,0,z), ro=(0, 180, 0))
			if r == 270:
				cmds.xform(roof[0], r=True, t=(x,0,z), ro=(0, 270, 0))
		if type == 3:
			roof = cmds.duplicate( 'Import_:roof_FLR_001', n=name )
			if r == 0:
				cmds.xform(roof[0], r=True, t=(x,0,z), ro=(0, 90, 0))
			if r == 90:
				cmds.xform(roof[0], r=True, t=(x,0,z), ro=(0, 180, 0))
			if r == 180:
				cmds.xform(roof[0], r=True, t=(x,0,z), ro=(0, 270, 0))
			if r == 270:
				cmds.xform(roof[0], r=True, t=(x,0,z), ro=(0, 0, 0))
		if type == 4:
			roof = cmds.duplicate( 'Import_:roof_FLBR_001', n=name )
			cmds.xform(roof[0], r=True, t=(x,0,z), ro=(0, 0, 0))



def roofObjs(meshDir):
	'''
	input: dircortory of the base Roof Obj-files

		- Import obj-files
	'''
	fileType = 'OBJ'


	objFiles = cmds.getFileList(folder = meshDir, filespec = '*.%s' % fileType)

	for item in objFiles:
		fname = os.path.join(meshDir, item)
		objName, ext = os.path.splitext(os.path.basename(fname))
		# import each file
		imported_objects = cmds.file(fname, i=True, rnn=True) 
		transforms = cmds.ls(imported_objects, type='transform')
		
		for i, object in enumerate(transforms):
			# rename it
			goodName = '%s_%s' % (objName, str(i+1).zfill(3))
			cmds.rename(object, goodName)
