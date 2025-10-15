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


class Match_OrientOnCrv:
    def __init__(self ,Target ):
        self.Targets = []
        #self.Crv = None
        self.AimVector = None
        self.WorldVector  = None

        self.UnpackDic = {}

        try:
            self.string_type = basestring
        except NameError:
            self.string_type = str
        '''
        if cmds.objectType(Crv) == "transform":
            Shp = cmds.listRelatives(Crv , s =1 , type = "nurbsCurve")
            if Shp:
                self.Crv = Shp[0]
            else:
                raise ValueError("Crv is not Curve ")
        if cmds.objectType(Crv) == "nurbsCurve":
            self.Crv = Crv
        if self.Crv is None :
            raise ValueError("Crv is not Curve ")
        '''



        if isinstance(Target , self.string_type) and cmds.objExists(Target) == True:
            self.Targets.append(Target)

        if isinstance(Target , list) and all(cmds.objExists(x)== True for x in Target ):
            self.Targets = Target

    def Add_Target(self, Target):


        if isinstance(Target , self.string_type) and cmds.objExists(Target) == True:
            self.Targets.append(Target)
        if isinstance(Target , list) and all(cmds.objExists(x)== True for x in Target ):
            self.Targets += Target


    def set_AimVector(self , AimVector = (1,0,0)):
        if not isinstance(AimVector , tuple) and len(AimVector) ==3 and all(isinstance(x , (float, int) ) for x in AimVector):
            raise TypeError("Invalid input. Expected a tuple of 3 floats.")
        else:
            self.UnpackDic["aimVector"] = AimVector


    def set_UpVector(self , UpVector = (0,1,0)):
        if not isinstance(UpVector , tuple) and len(UpVector) ==3  and all(isinstance(x , (float, int) ) for x in UpVector):
            raise TypeError("Invalid input. Expected a tuple of 3 floats.")
        else:
            self.UnpackDic["upVector"]= UpVector 
    def set_WorldVector(self , WorldVector = (0,1,0)):
        if not isinstance(WorldVector , tuple) and len(WorldVector) ==3  and all(isinstance(x , (float, int) ) for x in WorldVector):
            raise TypeError("Invalid input. Expected a tuple of 3 floats.")
        else:
            self.UnpackDic["worldUpVector"] = WorldVector

    def set_Type(self , Type = "scene" , Object = None):
        
        isTypes = [ "scene" , "object" , "objectrotation"  ,"vector" , "none" ]
        if not Type in isTypes:
            raise TypeError("Invalid Type. Must be one of 'scene', 'object', 'objectrotation', 'vector', or 'none'.")
        
        self.UnpackDic["worldUpType"] = Type
        if cmds.objExists(Object) and Type == "objectrotation":
            self.UnpackDic["worldUpObject"] = Object

    def set_Option(self, **kwargs):
        self.UnpackDic.update(kwargs)


    def Build(self , Parent = False):
        self.UnpackDic["maintainOffset"] = False

        OldTarget = None
        for i , Target in enumerate(self.Targets):

            if OldTarget:
                Grp = cmds.createNode("transform" , n = "{}_Grp" .format(Target))
                cmds.delete(cmds.parentConstraint(Target , Grp , mo =0))
                cmds.parent(Target , Grp)

                #if i == 0:
                AimC = cmds.aimConstraint(OldTarget ,  Grp , **self.UnpackDic )
                cmds.delete(AimC)
                if i == len(self.Targets):
                    OldTargetRotate = cmds.xform(OldTarget , q =1 , ro =1 , ws =1)
                    for  n , ax in enumerate("XYZ"):
                        cmds.setAttr("{}.rotate{}" .format(Grp , ax) ,OldTargetRotate[n])

                cmds.parent(Target , world=1)
                cmds.delete(Grp)


            if Parent and i >0:
                
                cmds.parent(Target , OldTarget)

            OldTarget = Target