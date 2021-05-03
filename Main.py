import maya.cmds as cmds
import pymel.core as pm
import sys
import random

import UI
import Cells
import Roof
import Floor
import Shaders
import Utilities


# ========================================================================= Execute

'''
Maya/Script Editor/Python Execute Scrip:

import sys

#add folder to PythonPath
sys.path.append('c:/Users/12213119/Documents/maya/2020/scripts/Lab/genHouse')

# print PythonPaths
from pprint import pprint
sys.path
pprint(sys.path)

# import file
import Main

# refresh file
reload(Main)

# call script
Main.Main()
'''

# ========================================================================= Cleanup

sys.path.append('C:/Users\12213119/Documents/maya/2020/scripts/Lab/genHouse')
reload(UI)
reload(Cells)
reload(Roof)
reload(Floor)
reload(Shaders)
reload(Utilities)

# remove existing namespaces
defaults = ['UI', 'shared']
namespaces = (ns for ns in pm.namespaceInfo(lon=True) if ns not in defaults)
namespaces = (pm.Namespace(ns) for ns in namespaces)
for ns in namespaces:
    ns.remove()

# delete empyt groups
transforms =  cmds.ls(type='transform')
deleteList = []
for tran in transforms:
    if cmds.nodeType(tran) == 'transform':
        children = cmds.listRelatives(tran, c=True) 
        if children == None:
            print '%s, has no childred' %(tran)
            deleteList.append(tran)
            
cmds.delete(deleteList)

# ========================================================================= Settings

# Input
cellSize = 20
numbercell = int(random.uniform(3, 9))
numFloors = 3
floorHeight = 15
repeatUV = 3
windowHeight = 8
doorHeight = 10
maxDoors = 2

# Directory
meshDir = 'C:/Users/12213119/Documents/maya/2020/scripts/Lab/genHouse/mesh/'
colorFile = 'C:/Users/12213119/Documents/maya/2020/scripts/Lab/genHouse/tex/brick09_low.jpg'
normalFile = 'C:/Users/12213119/Documents/maya/2020/scripts/Lab/genHouse/tex/brick09_low_d.jpg'

# Lists
cellList = []
setList = []

# Namespaces
cmds.namespace( add='Import_' )
cmds.namespace( add='Cell_' )
cmds.namespace( add='Roof_' )
cmds.namespace( add='Floor_' )
cmds.namespace( add='Window_' )


# ========================================================================= Class

class Main:

	print('\n------------------------------------------------------------- Create UI')

	# Create UI
	#UI.showUI()



	print('\n------------------------------------------------------------- startCell')
	
	#set Namespace: CELL
	cmds.namespace( set='Cell_' )

	# Create object: START CELL
	startCell = Cells.startCell(cellSize)
	print('startCell output: {}'.format(startCell))

	cellList.append(startCell[0])
	print('cellList: {}'.format(cellList))

	setList.append(startCell[1])
	print('setList: {}'.format(setList))

	
	# Create objects: Cells
	for x in range(numbercell):
	
		print('\n------------------------------------------------------------- addCell_{}'.format(x))

		addCell = Cells.addCell(cellSize, cellList, setList)
		print('addCell outtput {}'.format(addCell))

		cellList.append(addCell[0])
		print('cellList: {}'.format(cellList))

		setList.append(addCell[1])
		print('setList: {}'.format(setList))

	# set Namaespace: ROOT
	cmds.namespace( set=':' )

	# group: Cells
	sel = cmds.select( 'Cell_:*' )
	objects = cmds.ls(sl=True, g=True)
	cmds.group( objects, n='Cell_Grp' )
	cmds.select( clear=True )



	print('\n------------------------------------------------------------- Roof')

	cmds.namespace( set='Import_' )

	# import: Base Roof Objects
	Roof.roofObjs(meshDir)
	
	sel = cmds.select( 'Import_:*' )
	cmds.xform(sel, r=True, s=(cellSize,cellSize,cellSize) )
	cmds.select( clear=True )

	cmds.namespace( set=':' )

	# set namaespace
	cmds.namespace( set='Roof_')
	
	# generate: Roof
	Roof.roofPattern(cellSize, cellList, setList)

	# set Namaespace: ROOT
	cmds.namespace( set=':' )

	# group: ROOF
	sel = cmds.select( 'Roof_:*' )
	objects = cmds.ls(sl=True, g=True)
	cmds.group( objects, n='Roof_Grp' )
	cmds.select( clear=True )

	# group: IMPORT
	sel = cmds.select( 'Import_:*' )
	objects = cmds.ls(sl=True, g=True)
	cmds.group( objects, n='Import_Grp' )
	cmds.hide( cmds.ls(sl=True))
	cmds.select( clear=True )



	print('\n------------------------------------------------------------- Floor')

	cmds.namespace( set='Floor_' )

	# Create object: Ground Floor
	Floor.genFloors(numFloors, floorHeight, cellList, setList)
	
	# set Namaespace: ROOT
	cmds.namespace( set=':' )

	# group: Floor
	sel = cmds.select( 'Floor_:*' )
	objects = cmds.ls(sl=True, g=True)
	cmds.group( objects, n='Floor_Grp' )
	cmds.select( clear=True )

	# Assign Shader
	sel = cmds.select( 'Floor_:*' )
	objects = cmds.ls(sl=True, g=True)
	Shaders.wallShader( objects[0], colorFile, normalFile, repeatUV )


	print('\n------------------------------------------------------------- Window')

	'''
	- select walls
	- get pos & normal direction: wall faces
	- add data: nested wall tuple
	- select a pattern of faces
	- generate window instaces and position
	'''
	# set NameSpace: Window
	cmds.namespace( set='Window_' )

	Floor.genWindow(8)
	Floor.genDoor(10)

	# create: Windows
	Floor.addWindows('Floor_:GroundFloor', doorHeight, maxDoors)

	# set Namaespace: ROOT
	cmds.namespace( set=':' )

	# group: WINDOW
	sel = cmds.select( 'Window_:*' )

