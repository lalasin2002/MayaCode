import maya.cmds as cmds
import maya.api.OpenMaya as om # Maya API 2.0 사용
import math


def SetAttr_HideLockVectorAttr(item, lock=True, TurnOnKeyable= False):
    """오브젝트의 translate , rotate , scale  하이드 앤 락"""
    if TurnOnKeyable :
        KeyableBool = True
    else:
        KeyableBool = False
    Axis = ['X', 'Y', 'Z']
    Attr = ['.translate', '.rotate', '.scale']
    try:
        for y in Attr:
            for z in Axis:
                
                cmds.setAttr(item + y + z, keyable=KeyableBool)
                cmds.setAttr(item + y + z, channelBox = TurnOnKeyable)
                cmds.setAttr(item + y + z,  lock=lock )
    except:
        pass

def SetAttr_ObjectsVis(Type, Turn_Bool=False):
    """ 타입별 오브젝트 하이드"""
    All = cmds.ls(type=Type)
    for x in All:
        cmds.setAttr(x + '.visibility', Turn_Bool)


def SetAttr_CleanJntOrient(Jnt):
    """ 조인트 로테이션 => 조인트 오리엔트 , 식으로 초기화"""
    ParentObj = None
    IsParent = cmds.listRelatives(Jnt, p =1)
    if IsParent:
        ParentObj = IsParent[0]
       
    JntRotateDeg = cmds.getAttr("{}.rotate".format(Jnt))[0]
    for x in "XYZ":
        cmds.setAttr("{}.rotate{}".format(Jnt,x) , 0)
        
    Grp = cmds.createNode("transform" , n = Jnt + "_FixGrp")
    Prime = cmds.createNode("transform" , n = Jnt + "_FixPrime")
    
    cmds.parent(Grp , Prime)
    cmds.delete(cmds.parentConstraint(Jnt , Prime , mo = 0))
    cmds.parent(Jnt , Grp)
    
    for  i , x in enumerate( "XYZ"):
        cmds.setAttr("{}.rotate{}".format(Grp,x) , JntRotateDeg[i])
        
    cmds.parent(Jnt , world = 1)
    if ParentObj:
        cmds.parent(Jnt , ParentObj)
    cmds.delete(Prime)

#----------------------------------------------------------------------------------Cnt

def Cnt_MatchAttr(Source, Target):
    '''같은 Attr가 있을때 서로 연결'''
    source_attrs = cmds.listAttr(Source, k=1, ud=1) or []
    target_attrs = cmds.listAttr(Target, k=1, ud=1) or []

    for attr in source_attrs:
        if attr in target_attrs:
            source_plug = '{}.{}'.format(Source, attr)
            target_plug = '{}.{}'.format(Target, attr)

            if not cmds.isConnected(source_plug, target_plug):
                cmds.connectAttr(source_plug, target_plug, f=1)


def Cnt_VectorAttr(Source, Target , Attrs = [".translate" , ".rotate" , ".scale"] , Axis = "XYZ"):
    for Attr in Attrs:
        for V in Axis:
            cmds.connectAttr("{}{}{}" .format(Source , Attr , V) , "{}{}{}" .format(Target , Attr , V) ,f =1)