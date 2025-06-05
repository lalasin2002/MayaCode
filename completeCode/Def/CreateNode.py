import maya.cmds as cmds
def Create_Node(name, nodeTyp='transform'):
    node = cmds.createNode(nodeTyp, n=name)
    return node


def CreateBlendColor_Node(Name):
    node = cmds.createNode('blendColors', n=Name)
    for x in "RGB":
        cmds.setAttr(node + ".color1{}" .format(x) ,0 )
        cmds.setAttr(node + ".color2{}" .format(x) ,0 )
    return node


def CreateSetRange_Node(Name):
    node = cmds.createNode('setRange', n=Name)
    return node


def CreateMD_Node(Name, operation=1):
    node = cmds.createNode('multiplyDivide', n=Name)
    cmds.setAttr(node + '.operation', operation)
    return node


def CreateMDL_Node(Name, Input_Value=0):
    node = cmds.createNode('multDoubleLinear', n=Name)
    cmds.setAttr(node + '.input2', Input_Value)
    return node


def CreateADL_Node(Name, Input_Value=0):
    node = cmds.createNode('addDoubleLinear', n=Name)
    cmds.setAttr(node + '.input2', Input_Value)
    return node


def CreateDM_Node(Name, Target, input='inputMatrix'):
    node = cmds.createNode('decomposeMatrix', n=Name)
    cmds.connectAttr(Target + '.worldMatrix', node + '.inputMatrix')
    return node


def CreateCondition_Node(Name, operation=0):
    node = cmds.createNode('condition', n=Name)
    cmds.setAttr(node + '.operation', operation)
    return node

def CreateCrvInfo_Node(Name , Crv = None):
    node = cmds.createNode('curveInfo', n = Name)
    if Crv:
        Shp = Crv
        if not cmds.objectType(Crv) == "nurbsCurve":
            Shp = cmds.listRelatives(Crv ,s =1)[0]
        cmds.connectAttr(Shp + '.worldSpace[0]' , node + '.inputCurve' ,f=1)
    return node

def CreatePOCIF_Node(Name , CrvName = "" , Parameter = 0, TurnOnPercentage = True):
    ReturnTgt = None
    POCIF = cmds.createNode('pointOnCurveInfo' , n = Name)
    
    
    cmds.setAttr(POCIF  + ".turnOnPercentage", TurnOnPercentage)
    cmds.setAttr(POCIF  + '.parameter', Parameter)
    if cmds.objExists(CrvName) == True:
        cmds.connectAttr(CrvName + ".worldSpace[0]" , POCIF + '.inputCurve', f=1)    
    
    return POCIF

def CreateNPOC_Node(Name , CrvName = "" , inPositionTGT = "" , inPositionAttrName = "translate"):

    
    NPOC = cmds.createNode("nearestPointOnCurve" , n = Name )
    if cmds.objExists(CrvName) == True:
        cmds.connectAttr(CrvName + ".worldSpace[0]" , NPOC + '.inputCurve', f=1)
    if cmds.objExists(inPositionTGT) == True:
        if cmds.attributeQuery(inPositionAttrName , node = inPositionTGT , ex =1):
            for Axis in "XYZ":
                cmds.connectAttr("{}.{}{}".format(inPositionTGT , inPositionAttrName , Axis) ,  "{}.inPosition{}".format(NPOC , Axis) , f=1)
    return NPOC