import maya.cmds as cmds
import re #regular expression
import math


# OLD VERSION

def getNormalDirOLD(obj):
		# get number of faces
		faceNum = cmds.polyEvaluate(obj, face=True)
		
		for x in range(faceNum):
			
			# face select
			cmds.select( '{}.f[{}:{}]'.format(obj,x,x) ) # select face 0
			print('{}.f[0:{}]'.format(obj,x))

			# get the current selection
			selection = cmds.ls(sl=True)

			# trying to get the face normal angles of the current selection
			polyInfo = cmds.polyInfo(selection, fn=True)
			
			# convert the string to array with regular expression
			polyInfoArray = re.findall(r"[\w.-]+", polyInfo[0]) 
			polyInfoX = float(polyInfoArray[2])
			polyInfoY = float(polyInfoArray[3])
			polyInfoZ = float(polyInfoArray[4])

			# deselect current selection
			cmds.select(d=True )

			print str(polyInfoX) + ', ' + str(polyInfoY) + ', ' + str(polyInfoZ)


def facesDel(obj):
	"""
	delete faces point up or downward
	- firt get number of faces
	- loop throught all faces
	- check for there normal direction
	- if normal Y is not 0, a face to list
	- delete al faces in list
	"""
	faces = []

	# get number of faces
	faceNum = cmds.polyEvaluate(obj, face=True)
	
	for x in range(faceNum):
		
		# select face number
		face = '{}.f[{}]'.format(obj,x)

		# get normal Y value
		polyInfo = cmds.polyInfo(face, fn=True)
		polyInfoArray = re.findall(r"[\w.-]+", polyInfo[0]) 
		polyInfoY = float(polyInfoArray[3])

		# append face
		if not polyInfoY == 0.0:
			faces.append(face)

	# delete faces in list
	cmds.delete(faces)


def layoutUV(obj, type=0):

	totalFaces = cmds.polyEvaluate(obj, face=True)
	
	oneThird = totalFaces/3
	
	if (type == 0):
		startFace = 0
		endFace = oneThird - 1
		cmds.polyProjection(obj + '.f[' + str(startFace) + ':' + str(endFace) + ']',type="planar")

	if (type == 1):
		startFace = oneThird
		endFace = (oneThird * 2) - 1
		cmds.polyProjection(obj + '.f[' + str(startFace) + ':' + str(endFace) + ']',type="cylindrical")

	if (type == 2):
		startFace = (oneThird * 2)
		endFace = totalFaces - 1
		cmds.polyProjection(obj + '.f[' + str(startFace) + ':' + str(endFace) + ']',type="spherical")

	if (type == 3):		
		cmds.polyCylindricalProjection(obj + '.f[*]')
		cmds.polyMapCut( obj +'.e[17]' ) # WARNING: this does not always select a verticle edge as a cut line
		cmds.unfold(obj +'.map[*]', i=5000, ss=0.001, gb=0, gmb=0.5, pub=0, ps=0,oa=2, us=False) 


def getPolyData(ojb):
	'''
	Input: object
		- get number of vertecies
		- get number of edges
		- get number of faces
	Output: tuple
	'''
	
	# get number of vertexes
	vertNum = cmds.polyEvaluate(obj, vertex=True)    
	print('Vertex Number: ',vertNum)    
	
	# get number of edges
	edgeNum = cmds.polyEvaluate(obj, edge=True)    
	print('Edge Number: ', edgeNum)    
	
	# get number of faces
	faceNum = cmds.polyEvaluate(obj, face=True)    
	print('Face Number: ',faceNum)

	polyData = ( vertNum, edgeNum, faceNum )
	return polyData


def getFaceVertices(obj, face=0):
	info = cmds.polyInfo(fv=True)
	info = info[face].replace('FACE','').replace('{}:'.format(face,'' ), '').replace('\n', '').split(' ')
	verList = filter(None, info)
	print('face vertices: {}'.format(verList))
	return verList


def getVertexPos(obj, verNum):    
	verPos = cmds.xform( obj[0] +'.vtx[{}]'.format(verNum), q=True, objectSpace=True, t=True)
	print(verPos)
	return verPos # tuple(x, y, z)


def pointsDistance(x1, y1, z1, x2, y2, z2):
	d = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
	print('distance between point a and b = {}'.format(d))
	return d


# OLD VERSION
def getGreaterFaces(obj, max):
	'''
	Input: object, greater face size)
	return a list of all the faces of an object, with a greater square root (max)
	Output: list
	'''
	greaterList = []
	
	# get number of faces
	faceNum = cmds.polyEvaluate(obj, face=True)    
	print('Face Number: ',faceNum)
	
	for i in range(faceNum-1):
		# create temp face
		temp = cmds.duplicate( obj, n='temp' )
		sel = cmds.select(temp[0] + '.f[*]' )
		cmds.select(temp[0] + '.f[{}]'.format(i), d=True )
		cmds.delete()
		cmds.select(temp[0])
		bound = cmds.polyEvaluate(b=True)
		print(bound)
		cmds.delete()
		
		# calculate square root
		x = bound[0][0] - bound[0][1]
		z = bound[2][0] - bound[2][1]
		sqr = "{:.2f}".format(x*z)
		print(sqr)
		
		# get greater faces
		if (float(sqr) > float(max)):
			greaterList.append(i)
				
	print(greaterList)
	return greaterList

# NEW VERSION
def getFaceSqr(obj, FacNum):
	'''
	arg: object, object face number
	Calculate the square root of a face
	return: square root of selected face
	'''
	# print object name
	#print('object:   ' + obj)
	
	# get number of faces
	faceNum = cmds.polyEvaluate(obj, face=True)    
	#print('face num: {} '.format(faceNum))
	
	# get face vertices
	info = cmds.polyInfo(obj+ '.f[{}]'.format(FacNum), fv=True) # get vertecies
	info = info[0].replace('FACE','').replace('{}:'.format(FacNum), '').replace('\n', '').split(' ') # edit output
	verList = filter(None, info) # face vertices = [ 0, 1, 2, 3 ]
	#print('vertex 0: '+ verList[0])
	#print('vertex 1: '+ verList[1])
	#print('vertex 2: '+ verList[2])
	#print('vertex 3: '+ verList[3])
	
	# get vertex pos
	verPos0 = cmds.xform(  obj+'.vtx[{}]'.format(verList[0]), q=True, objectSpace=True, t=True)
	verPos1 = cmds.xform(  obj+'.vtx[{}]'.format(verList[1]), q=True, objectSpace=True, t=True)
	verPos2 = cmds.xform(  obj+'.vtx[{}]'.format(verList[2]), q=True, objectSpace=True, t=True)
	verPos3 = cmds.xform(  obj+'.vtx[{}]'.format(verList[3]), q=True, objectSpace=True, t=True)
	#print('vertex 0: {}'.format(verPos0) )
	#print('vertex 1: {}'.format(verPos1) )
	#print('vertex 2: {}'.format(verPos2) )

	# cal point to point distance
	disA = math.sqrt((verPos1[0]-verPos0[0])**2+(verPos1[1]-verPos0[1])**2+(verPos1[2]-verPos0[2])**2)
	disB = math.sqrt((verPos2[0]-verPos1[0])**2+(verPos2[1]-verPos1[1])**2+(verPos2[2]-verPos1[2])**2)	
	disC = math.sqrt((verPos3[0]-verPos2[0])**2+(verPos3[1]-verPos2[1])**2+(verPos3[2]-verPos2[2])**2)
	disD = math.sqrt((verPos0[0]-verPos3[0])**2+(verPos0[1]-verPos3[1])**2+(verPos0[2]-verPos3[2])**2)
	#print('vertex0 and vertex1: {}'.format(disA))
	#print('vertex1 and vertex2: {}'.format(disB))
	#print('vertex2 and vertex3: {}'.format(disC))
	#print('vertex3 and vertex0: {}'.format(disD))

	# cal square root
	faceSqr = ((disA+disB)/2) * ((disC+disD)/2)
	#print( 'face square root:    {}'.format(faceSqr))
	
	return faceSqr


def faceCenter(obj, face):
	'''
	arg: object, object face
	return: center position of the face
	'''
	info = cmds.polyInfo(obj+ '.f[{}]'.format(face), fv=True) # get vertecies
	info = info[0].replace('FACE','').replace('{}:'.format(face), '').replace('\n', '').split(' ') # edit output
	verList = filter(None, info) # face vertices = [ 0, 1, 2, 3 ]

	# get vertex pos
	verPos0 = cmds.xform(  obj+'.vtx[{}]'.format(verList[0]), q=True, objectSpace=True, t=True)
	verPos1 = cmds.xform(  obj+'.vtx[{}]'.format(verList[1]), q=True, objectSpace=True, t=True)
	verPos2 = cmds.xform(  obj+'.vtx[{}]'.format(verList[2]), q=True, objectSpace=True, t=True)
	verPos3 = cmds.xform(  obj+'.vtx[{}]'.format(verList[3]), q=True, objectSpace=True, t=True)

	# cal center pos
	centerX = (verPos0[0] + verPos1[0] + verPos2[0] + verPos3[0])/4
	centerY = (verPos0[1] + verPos1[1] + verPos2[1] + verPos3[1])/4
	centerZ = (verPos0[2] + verPos1[2] + verPos2[2] + verPos3[2])/4
	centerPos = (centerX, centerY ,centerZ)
	#print(centerPos)

	# location marker
	#cmds.polySphere()
	#cmds.xform(t=[centerX, centerY, centerZ])

	return centerPos

# NEW VERSION
def getFaceNormal(obj, face):
	'''
	arg: object, object face
	return normal direction list
	'''
	# get object face, normal dir
	faceDir = cmds.polyInfo(obj+ '.f[{}]'.format(face), fn=True)
	#print(faceDir)
	
	# edit String
	faceDir = faceDir[0].replace('FACE_NORMAL', '').replace('{}:'.format(face), '').replace('\n', '').split(' ')
	faceDir = filter(None, faceDir)
	
	return faceDir
