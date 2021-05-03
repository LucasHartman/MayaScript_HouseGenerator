import maya.cmds as cmds

def wallShader( obj, colorFile, normalFile, repeatUV=3 ):
	# create Nodes
	placeTexture = cmds.shadingNode('place2dTexture', asUtility=True)
	imageTexture = cmds.shadingNode('file', asTexture=True) # input image

	imageNormal = cmds.shadingNode('file', asTexture=True) # input image
	bump = cmds.shadingNode('aiBump2d', asTexture=True) # Bump
	normal = cmds.shadingNode('aiNormalMap', asTexture=True) # Normal
	shaderNode = cmds.shadingNode('aiStandardSurface', asShader=True) # shader

	# connect nodes
	cmds.connectAttr(placeTexture + '.outUV', imageTexture + '.uvCoord')
	cmds.connectAttr(imageTexture + '.outColor', shaderNode + '.baseColor')
	cmds.connectAttr(placeTexture + '.outUV', imageNormal + '.uvCoord')
	cmds.connectAttr(imageNormal + '.outAlpha', bump + '.bumpMap')
	cmds.connectAttr(bump + '.outValue', normal + '.input')
	cmds.connectAttr(normal + '.outValue', shaderNode + '.normalCamera')

	# import file
	#colorFile = 'C://Users//12213119//Documents//maya//2020//scripts//Lab//genHouse//tex//brick09_low.jpg'
	cmds.setAttr( imageTexture+'.fileTextureName',  colorFile, type = "string")
	#normalFile = 'C://Users//12213119//Documents//maya//2020//scripts//Lab//genHouse//tex//brick09_low_d.jpg'
	cmds.setAttr( imageNormal+'.fileTextureName',  normalFile, type = "string")

	# modify attribute
	cmds.setAttr(placeTexture + '.repeatU', repeatUV)
	cmds.setAttr(placeTexture + '.repeatV', repeatUV)

	# apply shader to object
	cmds.select( obj )
	cmds.hyperShade( assign=shaderNode )
