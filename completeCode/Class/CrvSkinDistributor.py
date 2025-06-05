# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import maya.cmds as cmds
from collections import OrderedDict

class CrvSkinDistributor:
    def __init__(self, items ):
        '''
        Crv에 여러조인트의 스킨값을 균일하게 넣기위한 클래스\n
        
        =======================메서드 설명========================\n
        =\n
        __init__ : 조인트 리스트를 지정하는 메서드\n
        InputCrv : 커브를 지정하기위한 메서드\n
        GetItemParameter : 커브위의 오브젝트의 파라미터를 구하는 메서드 \n
        ReBuildCrvParameter : 지정 커브의 minValue , maxValue 가 0 ,1 이 아닐경우 사용 \n

        Calculate : 조인트 리스트 , 커브가 지정되었으면 SkinParcent를 구하기위한 계산 \n
        Skinning : 커브에 조인트를 스키닝하고 계산된 스킨값을 넣음 \n

        =\n
        =======================배개변수 설명========================\n

        item :: 조인트 리스트 를 넣는 매개변수 최소 요소 2개 이상 \n
        
        '''

        self.items = None
        self.Crv = None
        self.CrvShp = None
        self.SkinData = None
        self.SkinCluterNode = None

        if isinstance(items , list):
            if len(items ) > 1 and any(cmds.objectType(x) == "joint" for x in items):
                self.items = items

    def InputCrv(self , Crv):
        '''
        Crv :: 커브오브젝트 매개변수\n
        Transform 이든 shape이든 \n
        결과적으로 "nurbsCurve" 맞다면 무얼넣어도 상관없음\n

        '''

        if cmds.objectType(Crv) == "transform":
            ShpFinds = cmds.listRelatives(Crv , s =1)
            if ShpFinds:
                if cmds.objectType(ShpFinds[0]) == "nurbsCurve":
                    self.Crv = Crv
                    self.CrvShp = ShpFinds[0]
                
        if cmds.objectType(Crv) == "nurbsCurve":
            self.CrvShp = Crv
            TransformFinds = cmds.listRelatives(Crv , p =1)
            if TransformFinds:
                if cmds.objectType(TransformFinds[0]) == "transform":
                    self.Crv = TransformFinds[0]

    def Calculate(self , Print = True):
        '''
        __init__ , InputCrv 메서드에 의해 지정된 조인트리스트, 커브를 대상으로\n
        스킨값 계산하는 메서드\n
        =\n
        Print :: 스크립트 에디터에 스킨값을 출력하기위한 변수임 Flase시 출력하지 않음 \n
        
        '''

        self.SkinData = OrderedDict()
        Cvlist = cmds.ls(self.Crv + ".cv[*]" , fl =1)
        Cvlist = [x for x in Cvlist]

        
        OldItemParam = None
        OldItem = None
        
        for NewItem in self.items :
            NewItemParam = self.GetItemParameter(NewItem , self.CrvShp)
            if OldItem:
                OldItemParam = self.GetItemParameter(OldItem, self.CrvShp)
                #OldCvParam = None
                CvCount = 0
                for  i, Cv in enumerate(Cvlist):
                    NewCvParam = self.GetItemParameter(Cv , self.CrvShp)
                    if OldItemParam <= NewCvParam <=NewItemParam:
                        DiffParam = round( NewItemParam - OldItemParam ,3)
                        
                        if DiffParam == 0:
                            RebuildCvParam = 0 
                        else:
                            RebuildCvParam = round((NewItemParam -  NewCvParam) /DiffParam , 3)
                        
                        r_RebuildCvParam = 1.0 - RebuildCvParam
                        self.SkinData[Cv] = [(OldItem  , RebuildCvParam) , ( NewItem, r_RebuildCvParam)]


            OldItem = NewItem
        
        if Print :
            StringForPrint ="> SkinData :: {} to {} \n" .format(self.items , self.CrvShp)
            for x ,y in self.SkinData.items():
                StringForPrint += "   Cv =  {}  Values = {} \n" .format(x ,y)

            print (StringForPrint )

    def Skinning(self):
        '''
        계산된 스킨 데이터를 대상으로 스키닝됨
        
        '''

        SkinCluterNode = None
        if isinstance(self.SkinData , dict) and self.items and self.CrvShp:
            SkinCluterNode = cmds.skinCluster(self.items , self.CrvShp )[0]

            for Cv , Values in self.SkinData.items():
                cmds.skinPercent(SkinCluterNode , Cv , transformValue= Values)

        self.SkinCluterNode = SkinCluterNode
        return self.SkinCluterNode

    def ReBuildCrvParameter(self):
        if self.CrvShp:
            RebuildCrv = cmds.rebuildCurve(self.CrvShp , kr = 0 ,end =1 , kcp =1 )[0]
            getMin = cmds.getAttr(RebuildCrv + ".minValue")
            getMax = cmds.getAttr(RebuildCrv + ".maxValue")

            if getMin == 0 and getMax == 1:
                FindShp = cmds.listRelatives(RebuildCrv , s =1)[0]
                self.CrvShp =  FindShp
            
    @staticmethod
    def GetItemParameter( item, CrvShp ,roundCount =3 ):
        '''
        item :: 오브젝트 \n
        CrvShp :: 커브"쉐입" \n
        roundCount :: 파라미터값 반환시 소수점 제한수 기본 3 \n

        =\n

        반환시 오로지 파라미터값만 반환\n
        
        
        '''

        Get = None

        if cmds.objExists(item) and CrvShp:

            Pos = cmds.xform(item , ws =1 , q =1, t =1)
            NPOC = cmds.createNode("nearestPointOnCurve" , n = "{}_Cal_NPOC" .format("__PreSet"))
            for i, Axis in enumerate("XYZ"):
                cmds.setAttr(NPOC + ".inPosition{}" .format(Axis) , Pos[i])

            cmds.connectAttr(CrvShp + ".worldSpace[0]" , NPOC + ".inputCurve" ,f =1)
            Get = round( cmds.getAttr(NPOC + ".parameter" ) ,roundCount )

            cmds.delete(NPOC)

        return Get 


#Test 
#sel = cmds.ls(type = "joint")
#Test = CrvSkinDistributor(sel)
#Test.InputCrv("Tail_Crv")
#Test.ReBuildCrvParameter()
#Test.Calculate()
#Test.Skinning()