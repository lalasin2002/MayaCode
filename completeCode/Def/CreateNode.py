import maya.cmds as cmds


def Create_Node(name, nodeTyp='transform'):
    node = cmds.createNode(nodeTyp, n=name)
    return node


def Create_BlendcolorNode(Name):
    node = cmds.createNode('blendColors', n=Name)
    for x in "RGB":
        cmds.setAttr("{}.color1{}".format(node, x), 0)
        cmds.setAttr("{}.color2{}".format(node, x), 0)
    return node


def Create_SetrangeNode(Name):
    node = cmds.createNode('setRange', n=Name)
    return node


def Create_MdNode(Name, operation=1):
    node = cmds.createNode('multiplyDivide', n=Name)
    cmds.setAttr("{}.operation".format(node), operation)
    return node


def Create_MdlNode(Name, Input_Value=0):
    node = cmds.createNode('multDoubleLinear', n=Name)
    cmds.setAttr("{}.input2".format(node), Input_Value)
    return node


def Create_AdlNode(Name, Input_Value=0):
    node = cmds.createNode('addDoubleLinear', n=Name)
    cmds.setAttr("{}.input2".format(node), Input_Value)
    return node


def Create_DmNode(Name, Target, input='inputMatrix'):
    node = cmds.createNode('decomposeMatrix', n=Name)
    cmds.connectAttr("{}.worldMatrix".format(Target), "{}.{}".format(node, input))
    return node


def Create_ConditionNode(Name, operation=0):
    node = cmds.createNode('condition', n=Name)
    cmds.setAttr("{}.operation".format(node), operation)
    return node


def Create_CrvinfoNode(Name, Crv=None):
    node = cmds.createNode('curveInfo', n=Name)
    if Crv:
        Shp = Crv
        if not cmds.objectType(Crv) == "nurbsCurve":
            Shp = cmds.listRelatives(Crv, s=1)[0]
        cmds.connectAttr("{}.worldSpace[0]".format(Shp), "{}.inputCurve".format(node), f=1)
    return node


def Create_PocifNode(Name, CrvName="", Parameter=0, TurnOnPercentage=True):
    POCIF = cmds.createNode('pointOnCurveInfo', n=Name)
    cmds.setAttr("{}.turnOnPercentage".format(POCIF), TurnOnPercentage)
    cmds.setAttr("{}.parameter".format(POCIF), Parameter)

    if cmds.objExists(CrvName):
        cmds.connectAttr("{}.worldSpace[0]".format(CrvName), "{}.inputCurve".format(POCIF), f=1)

    return POCIF


def Create_NpocNode(Name, CrvName="", inPositionTGT="", inPositionAttrName="translate"):
    NPOC = cmds.createNode("nearestPointOnCurve", n=Name)

    if cmds.objExists(CrvName):
        cmds.connectAttr("{}.worldSpace[0]".format(CrvName), "{}.inputCurve".format(NPOC), f=1)

    if cmds.objExists(inPositionTGT):
        if cmds.attributeQuery(inPositionAttrName, node=inPositionTGT, ex=True):
            for Axis in "XYZ":
                cmds.connectAttr(
                    "{}.{}{}".format(inPositionTGT, inPositionAttrName, Axis),
                    "{}.inPosition{}".format(NPOC, Axis),
                    f=True
                )

    return NPOC

def Create_Loc(Name , ShpScale =1 , NolistBool = True):
    ReturnTgt = None
    Loc = cmds.spaceLocator(n = Name)[0]
    Shp = cmds.listRelatives(Loc , s =1)[0]
    for x in "XYZ":                
        cmds.setAttr(Shp  + ".localScale{}" .format(x) ,ShpScale )

    if NolistBool:
        ReturnTgt = Loc
    else:
        ReturnTgt = [Loc , Shp]
        
    return ReturnTgt 


def Create_Jnt(Name , CP_Target = None):
    cmds.select(cl =1)
    Jnt = cmds.joint(n = Name )
    if not CP_Target is None:
        PreGrp = cmds.createNode('transform', n=Jnt + "_PreGrp")
        cmds.parent(Jnt, PreGrp)
        CP = cmds.parentConstraint(CP_Target, PreGrp)

        cmds.parent(Jnt, w=1)
        cmds.delete(CP)
        cmds.delete(PreGrp)

    return Jnt

def Create_Crv(Name , Poslist , degree =1 ):

    Crv = cmds.curve(n = Name , p = Poslist , d= 1)
    reCrv = cmds.rebuildCurve(Crv , ch =1  , rpo =1 , rt = 0 , end = 1 , kr = 0, kcp = 0 , kep =1 , kt =0 , s= len(Poslist) ,d =degree )
    Shp = cmds.listRelatives(Crv , s= 1)
    ReName = cmds.rename("{}Shape" .format(Name) , Shp[0] )
    return reCrv


def Create_ANT(Name , CP_Target = None , Cnt_Target  = None , NonSelect = True ):
    ReTurn_lst = None
    Node = cmds.createNode("annotationShape" , n = Name + "Shape")
    Find_Transform = cmds.listRelatives(Node , p =1)[0]
    TransForm = cmds.rename(Find_Transform , "{}" .format(Name))
    
    if NonSelect :
        cmds.setAttr(Node + ".overrideEnabled" , 1)
        cmds.setAttr(Node + ".overrideDisplayType" ,2)
    
    if Cnt_Target :
        cmds.connectAttr("{}.{}" .format(Cnt_Target , "worldMatrix[0]") , "{}.{}" .format(Node , "dagObjectMatrix[0]" ,f =1) )
    if CP_Target:
        cmds.pointConstraint(CP_Target , TransForm  , mo =0)
        
    ReTurn_lst = [TransForm , Node]
    
    return ReTurn_lst


def Create_TextCrv(Name , TextString ,CenterPivotBool = True , FontSizePt = 27.8 , Font = "Lucida Sans Unicode"):
    FontOption = "{}, {}pt" .format(Font , str(FontSizePt))
    Text = cmds.textCurves( n = "__PreFix__{}" .format(Name) , t = TextString ,f = FontOption)[0]
    DulicateText = cmds.duplicate(Text , n = Name ,rc =1)[0]
    cmds.delete(Text)
    
    ChildTransform = cmds.listRelatives(DulicateText  ,ad =1,c =1,  type = "transform")
    ChildCrv = cmds.listRelatives(DulicateText  ,ad =1,c =1  , type = "nurbsCurve")
    for x in ChildTransform:
        cmds.makeIdentity(x ,apply = 1,  s= 1, t =1, r =1)
    
    
    for i, x in enumerate(ChildCrv):
        cmds.parent(x , DulicateText  ,r =1, s =1)
        RE = cmds.rename(x , "{}{}shape" .format(Name , str(i+1)))
        
        
    cmds.delete(ChildTransform )
    
    if CenterPivotBool:
       center = cmds.objectCenter(DulicateText, gl = True)
       
       CV = cmds.ls("{}*shape.cv[*]" .format(Name) ,fl =1 )
       cmds.select(CV)
       cmds.move( -center[0] ,0 ,0 , r =1 , os =1 , wd =1 )
       
    return DulicateText