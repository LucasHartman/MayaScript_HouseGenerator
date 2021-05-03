import maya.cmds as cmds
import sys
import random


import Utilities

sys.path.append('C:/Users\12213119/Documents/maya/2020/scripts/Lab/genHouse')
reload(Utilities)



def genFloors(numFloors, floorHeight, cellList, setList):
	'''
	if (number of floors > 0)

	z = 1
	for x in range(numFloors)
		
		step 2: Create a number of floors

			- floorList = setList
			- rooflist = setLIst
			- remove a RANDOM number of items from lists
			- create polyPlanes using position from floorList +z

			- combine copy cells
			- merge points
			- extrude copy cells
			- delete top/bottom faces

			- z=z+1
	'''

	floorList = setList
	rooflist = cellList

	print('floorList: {}'.format(floorList))
	print('rooflist: {}'.format(rooflist))

	# generate ground floor
	if (numFloors != 0):
		
		print('Ground Foor')

		# move Roofs 1 level
		sel = cmds.select( 'Roof_:*' )
		objects = cmds.ls(sl=True, g=True)
		cmds.move(floorHeight, y=True)
		cmds.select( clear=True )

		# copy cells
		sel = cmds.select( 'Cell_:*' )
		objects = cmds.ls(sl=True, g=True)
		cmds.duplicate(n='cell')
		cmds.select( clear=True )

		# create ground floor
		sel = cmds.select( 'Floor_:*' )
		objects = cmds.ls(sl=True, g=True)
		cmds.polyUnite(ch=False, n='GroundFloor' )
		cmds.polyMergeVertex( d=0.15 )
		cmds.polyExtrudeFacet(ty=floorHeight)
		cmds.select( clear=True )

		# delete top/down faces
		sel = cmds.select( 'Floor_:*' )
		objects = cmds.ls(sl=True, g=True)
		Utilities.facesDel(objects[0])
		#cmds.select( clear=True )

		# layout UV
		Utilities.layoutUV(objects[0],3)
		cmds.select( clear=True )


	# generate upper floors
	if (numFloors > 0):

		for x in range(numFloors):
			
			print('Floor_{}'.format(x+1))



def genWindow(h=8):
	
	# create: Glass Mesh
	#base = cmds.polyPlane(n='base', w=h/2, h=h, sx=1, sy=1)

	# create: Frame Mesh
	frame = cmds.polyPlane(n='frame', w=h/2, h=h, sx=1, sy=1)
	cmds.polyExtrudeEdge(kft=True,lty=h/h)
	cmds.delete(frame[0]+'.f[0]')
	cmds.polyExtrudeFacet(kft=True,ltz=float(h)/10.0/4.0)
	sel = cmds.select(frame[0]+'.f[9]',frame[0]+'.f[11]',frame[0]+'.f[13]',frame[0]+'.f[15]')
	cmds.polyExtrudeFacet(kft=True, ltz=float(h)/20.0)
	sel = cmds.select(frame[0]+'.f[17]',frame[0]+'.f[19]',frame[0]+'.f[21]',frame[0]+'.f[23]')
	cmds.polyExtrudeFacet(kft=True, ltz=float(h)/40.0)
	cmds.polyBevel3(frame[0]+'.f[0:63]', offset= float(h)/1000.0 )

	# create: Deco Mesh
	deco = cmds.polyPlane(n='deco', w=h/2, h=h, sx=2, sy=h/(h/4))
	cmds.polyBevel3(deco[0]+'.e[*]', offset= float(h)/100.0 )
	
	# list: big faces
	selList = []
	for x in range(cmds.polyEvaluate(deco[0], face=True)-1):
		faceSize = Utilities.getFaceSqr(deco[0],x)
		if (faceSize > float(h)/4.0): # delete big face size
			selList.append(deco[0]+'.f[{}]'.format(x))
			print('faceSize: {}'.format(faceSize))

	# delete faces
	cmds.polyDelFacet( selList )

	# exrude: deco Mesh
	cmds.polyExtrudeFacet(deco[0], kft=True, ltz=float(h)/40.0)
	numFaces= cmds.polyEvaluate(deco[0], face=True)

	window = cmds.polyUnite(frame[0], deco[0], name='window', ch=0, mergeUVSets=1)
	cmds.xform( p=True, ro=[90,0,0] ) 
	cmds.makeIdentity(apply=True, rotate=True ) # freeTransformation


def genDoor(h, floorH=15):
    base = cmds.polyPlane(sx=1, sy=1, h=h, w=h/2, n='tempdoor')
    cmds.polyExtrudeFacet(base[0]+'.f[*]', ltz= float(h/h)/4.0 )
    
    frame = cmds.polyPlane(sx=1, sy=1, h=h, w=h/2, n='frame')
    sel = cmds.select(frame[0]+'.e[1:3]')
    cmds.polyExtrudeEdge( kft=True, lty=float(h)/20.0)
    
    getVertex4 = cmds.xform(  frame[0]+'.vtx[4]', q=True, objectSpace=True, t=True)
    getVertex5 = cmds.xform(  frame[0]+'.vtx[5]', q=True, objectSpace=True, t=True)
    cmds.polyMoveVertex( frame[0]+'.vtx[4]', tx=-getVertex4[0]+getVertex5[0] )
    getVertex6 = cmds.xform(  frame[0]+'.vtx[6]', q=True, objectSpace=True, t=True)
    getVertex7 = cmds.xform(  frame[0]+'.vtx[7]', q=True, objectSpace=True, t=True)
    cmds.polyMoveVertex( frame[0]+'.vtx[6]', tx=-getVertex6[0]+getVertex7[0] )    
    cmds.delete(frame[0]+'.f[0]')
    cmds.polyExtrudeFacet(frame[0]+'.f[*]', ltz=float(h/h)/2.0 )
    
    door = cmds.polyUnite(frame[0], base[0], name='door', ch=0, mergeUVSets=1)
    cmds.xform( p=True, ro=[90,0,0] )
    cmds.makeIdentity(apply=True, rotate=True ) # freeTransformation
    cmds.move(0,h/2,0)


def addWindows(obj, doorHeight, maxDoors):

	# get number of faces
	faceNum = cmds.polyEvaluate(obj, face=True)

	for x in range(faceNum):

		setwindow = [0,1,1,1]
		random.shuffle(setwindow)
		#print('random value: {}'.format(setwindow[0]))

		# get face center position
		face = Utilities.faceCenter(obj,x)
		print(face)

		# get face Normal Direction
		normals = Utilities.getFaceNormal(obj,x)

		# get rot, besed on face normal direction
		if (int(float(normals[0])) == 1):
			rotY = 90
			print('rot: {}'.format(90))
		elif (int(float(normals[0])) == -1):
			rotY = -90
			print('rot: {}'.format(-90))
		elif (int(float(normals[2])) == -1):
			rotY = 180
			print('rot: {}'.format(-90))
		else:
			rotY = 0


		if (setwindow[0] == 1):
			# gen instance: window
			instWindow = cmds.instance('Window_:window', n='instWindow' )
			cmds.xform(instWindow[0], t=[face[0], face[1], face[2]], ro=[0 ,rotY, 0])
		else:
			if (maxDoors > 0):
				Door = cmds.instance('Window_:door', n='door' )
				cmds.xform(Door[0], t=[face[0], 0+(doorHeight/2), face[2]], ro=[0 ,rotY, 0])
				print('create door')
				maxDoors = maxDoors-1

