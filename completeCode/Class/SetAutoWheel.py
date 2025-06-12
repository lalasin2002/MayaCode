# -*- coding: utf-8 -*-
import maya.cmds as cmds
import re , os , sys , pprint 


class SetAutoWheel:
    '''
    --------------------------------------------------------------------------------\n
    >>             클래스 매개변수             -\n
    
    CenterPivotTarget = 실제로 굴러갈 오브젝트 \n
    GeoTarget = 바퀴 지오메트리 오브젝트 (반지름 구하는데 필요) \n
    FrontDirect = 실제로 굴러갈 오브젝트의 주로 이동되는 방향 ex) translateX , translateY, ... \n
    RotateDirect = 실제로 굴러갈 오브젝트의 회전 방향 ex) rotateX , rotateY , ... \n
    --------------------------------------------------------------------------------\n
    >>             클래스 인스턴스 변수              -\n
    
    self.FunctionTarget = 결과물로써 회전되는 오브젝트 \n
    self.GeoTarget = 바퀴 지오메트리 \n
    self.OldPos=  거리계산에 필요한 첫번째 위치오브젝트 \n
    self.NewPos = 거리계산에 필요한 갱신 위치오브젝트 \n
    self.DirPos = 굴러가는 주방향을 계산하는 벡터오브젝트(dotProduct 사용) \n
    self.ExpressionNode= 만들어진 익스프레션 노드 \n

    --------------------------------------------------------------------------------\n
    >>             추가정보              -\n
    
    Attrbute Auto , Offset , radius의 위치는 CenterPivotTarget에 있음\n
    현 클래스로 만들어지는 오브젝트의 이름은 CenterPivotTarget의 이름을 가져옴 \n
    GeoTarget 변형인자는 오로지 지오메트리의 반지름에 구하는데에만 쓰이기에 실질적 리깅은 없음 따로 해줘야함\n

    
    '''
    
    def __init__(self , CenterPivotTarget, GeoTarget , FrontDirect = "translateZ" , RotateDirect = "rotateX"):
            
            Radius = 0
            WheelOldPos = None
            WheelNewPos = None
            WheelDirPos = None

            self.FunctionTarget = None
            self.GeoTarget = None
            self.OldPos= None
            self.NewPos = None
            self.DirPos = None
            self.ExpressionNode= None

        
            #-------------------------------------------------------------------------------------FindValue for Radius

            PreTransformList = []
            AttrNameList= ["Auto" , "WheelRadius" , "Offset"]

            Lattice = cmds.lattice(dv = (2,2,2) , oc =1 , n = "{}_Lattice" .format(GeoTarget))
            BtnLatticePt = ["{}.pt[0:1][0][0]".format(Lattice [1]) , "{}.pt[0:1][0][1]".format(Lattice [1])]
            cmds.select(BtnLatticePt)
            Cls = cmds.cluster( BtnLatticePt, n = "Btn{}_Cls" .format(Lattice[0]))

            CenterPos = cmds.xform(CenterPivotTarget ,q =1, ws =1 , t =1)
            ClsPos = cmds.xform(Cls , q =1 , rp =1)

            Radius = round(((CenterPos[0] - ClsPos[0])**2 + (CenterPos[1]- ClsPos[1] )**2 + (CenterPos[2]- ClsPos[2])**2 )**0.5 , 3)
            cmds.delete(Cls)
            cmds.delete(Lattice)

            #-------------------------------------------------------------------------------------CreateNode and MakeAttr

            CenterPivotTarget , CenterPivotTargetGrps = self.Grping(CenterPivotTarget , 2)

            
            for WheelPos in ["WheelOldPos" , "WheelNewPos" , "WheelDirPos"]:
                Name = "{}_{}" .format(CenterPivotTarget , WheelPos) 
                WheelTransForm = cmds.createNode("transform" , n = Name)
                self.d_Match_CP(CenterPivotTarget , WheelTransForm)
                PreTransformList.append(WheelTransForm)

            WheelOldPos = PreTransformList[0]
            WheelNewPos = PreTransformList[1]
            WheelDirPos = PreTransformList[2]

            cmds.parent(WheelDirPos  , CenterPivotTargetGrps[-1] , WheelNewPos)
            cmds.setAttr( "{}.{}".format(WheelDirPos , FrontDirect)  , Radius)

            for i , AttrName in enumerate( AttrNameList):
                AttrFind = cmds.attributeQuery(AttrName , node= CenterPivotTarget , exists = True)

                if AttrFind == False:

                    cmds.addAttr(CenterPivotTarget , ln = AttrName , at='double' , k=1)
                    if i == 0:
                        cmds.addAttr("{}.{}" .format(CenterPivotTarget , AttrName ) , e =1 , min= 0 , max= 1 ,)
                    if i == 1:
                        cmds.setAttr("{}.{}" .format(CenterPivotTarget , AttrName ) , k = 0, cb =1)
                        cmds.setAttr("{}.{}" .format(CenterPivotTarget , AttrName ) , Radius)

            #----------------------------------------------------------------------------------------------Expression Work

            cmds.connectAttr("{}.{}" .format(CenterPivotTarget ,AttrNameList[2] ) , "{}.{}"  .format(CenterPivotTargetGrps[0] ,RotateDirect ) ,f =1 )

            ExpressionString =""

            VarSting = "$AutoWheel = {center}.{autoAttr};\n$AutoWheelOffset = {center}.{offsetAttr};\n$Radius = {center}.{radius};\n".format(center = CenterPivotTarget , autoAttr =  AttrNameList[0] ,offsetAttr = AttrNameList[2], radius = AttrNameList[1])
            VectorVarString = "vector $WheelOldPos = `xform -q -ws -t \"{wheelOldpos}\"`;\nvector $WheelNewPos = `xform -q -ws -t \"{wheelNewPos}\"`;\nvector $WheelDirPos = `xform -q -ws -t \"{wheelDirPos}\"`;\n" .format(wheelOldpos = WheelOldPos ,wheelNewPos = WheelNewPos , wheelDirPos = WheelDirPos )
            FuncVarString = "vector $WheelDir = ($WheelDirPos - $WheelNewPos);\nvector $WheelMoveMent =  ($WheelNewPos - $WheelOldPos );\nfloat $WheelDistacne = mag($WheelMoveMent);\n$WheelDot = dotProduct($WheelMoveMent , $WheelDir  , 1);\n"
            AutoWheelFuncString = "{center}.{rotDirect} = $AutoWheel * ({center}.{rotDirect} + 360/((3.14 *2 ) * $Radius) * ($WheelDot *$WheelDistacne ));\n" .format(center = CenterPivotTarget , rotDirect = RotateDirect)

            MatchFuncString = "matchTransform {old} {new};\n" .format(old = WheelOldPos , new = WheelNewPos)


            ExpressionString += VarSting
            ExpressionString += VectorVarString
            ExpressionString += FuncVarString
            ExpressionString += AutoWheelFuncString
            ExpressionString += MatchFuncString 


            Exp = cmds.expression(s = ExpressionString , n = "Exp_{}_Auto" .format(CenterPivotTarget))


            self.FunctionTarget = CenterPivotTarget
            self.GeoTarget = GeoTarget
            self.OldPos= WheelOldPos
            self.NewPos = WheelNewPos
            self.DirPos = WheelDirPos
            self.ExpressionNode= Exp 


    def Grping(self , Target , Count ):
        Grp_Suffix = ["_Grp" , "_Offset" , "_Prime" , '_GrpPrime']
        Count = int(Count)
        Groups =[]
        Parent_Group = None
        for i , x in enumerate(Grp_Suffix[:Count]):
            Group = cmds.createNode("transform" , n = "{}{}" .format(Target ,x))

            if Parent_Group:
                cmds.parent( Parent_Group ,Group )
            Parent_Group = Group
            Groups.append(Group)
        cmds.delete(cmds.parentConstraint(Target, Groups[-1]))
        cmds.parent(Target ,  Groups[0])

        return  Target , Groups

    def d_Match_CP(self ,Staric, Target, Bool_Point=True, Bool_Orient=True, Bool_Scale=False):

        if Bool_Point == True:
            Po = cmds.pointConstraint(Staric, Target, mo=0)
            cmds.delete(Po)
        if Bool_Orient == True:
            Or = cmds.orientConstraint(Staric, Target, mo=0)
            cmds.delete(Or)
        if Bool_Scale == True:
            Scale = cmds.scaleConstraint(Staric, Target, mo=0)
            cmds.delete(Scale)

    


'''
sel = cmds.ls(sl =1)

Test = c_Set_AutoWheel(sel[0] ,sel[1])

'''

