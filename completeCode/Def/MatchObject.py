# -*- coding: utf-8 -*-
import maya.cmds as cmds

def Match_ConstraintObject(Staric, Target, Bool_Point=True, Bool_Orient=True, Bool_Scale=False):
    ''' 
    Constraint maintainoffset = False 를 이용한 오브젝트 매치 \n
    Staric :: Constrain의 Parent 오브젝트 \n
    Target :: Constrain를 받고자 하는 오브젝트 \n
    
    각 Bool_(Point , Orient , Scale) 은 Constrain의 타입사용을 의미함
    '''
    if Bool_Point == True:
        Po = cmds.pointConstraint(Staric, Target, mo=0)
        cmds.delete(Po)
    if Bool_Orient == True:
        Or = cmds.orientConstraint(Staric, Target, mo=0)
        cmds.delete(Or)
    if Bool_Scale == True:
        Scale = cmds.scaleConstraint(Staric, Target, mo=0)
        cmds.delete(Scale)

def Match_PointOnCrv(Target , Crv ,Parameter , Percentage = 1 ):
    CrvShp = None
    if cmds.objectType(Crv) == "transform":
        Shp = cmds.listRelatives(Crv , s =1 , type = "nurbsCurve")
        if Shp:
            CrvShp = Shp[0]
        else:
            raise ValueError("Crv is not Curve ")
    if cmds.objectType(Crv) == "nurbsCurve":
        CrvShp = Crv

    POICF = cmds.createNode('pointOnCurveInfo', n=Target + '_POCIF')
    
    cmds.setAttr(POICF + '.turnOnPercentage',  Percentage )
    cmds.setAttr(POICF + '.parameter', Parameter)
    cmds.connectAttr(CrvShp + '.worldSpace[0]', POICF + '.inputCurve', f=1)
    cmds.connectAttr(POICF + '.result.position ', Target + '.translate', f=1)
    Target_Pos = cmds.xform(Target, q=1, ws =1, t =1)
    cmds.delete(POICF)
    cmds.xform(Target , ws= 1, t =Target_Pos)