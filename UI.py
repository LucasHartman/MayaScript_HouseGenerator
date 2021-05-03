import maya.cmds as cmds


def showUI():  
	'''UI window'''
	myWin = cmds.window(title="Simple Window", widthHeight=(300, 200))
	cmds.columnLayout()    
	cmds.text(label="Hello, Maya!")
	cmds.button(label="Make Cube", command=buttonFunction)
	cmds.showWindow(myWin)

def buttonFunction(args):
	''' showUI button function, create a poly cube'''
	cmds.polyCube()





