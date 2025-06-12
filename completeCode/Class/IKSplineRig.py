# -*- coding: utf-8 -*-
import maya.cmds as cmds
from collections import OrderedDict

class IKspline:
    def __init__(self , Jntlst , PrefixName = None):
        '''
        지정된 조인트 체인에 IK Spline을 세팅.\n
        스트레치 및 볼륨 유지 기능까지 포함.\n
        리깅자체는 expression 활용.\n

        [메서드 설명]
        - __init__: 조인트 리스트와 네이밍을 설정합
            - Jntlst (list): IK Spline을 적용할 조인트 리스트 요소가 3개 이상있어야함
            - PrefixName (str, optional): 생성되는 조인트 및 노드의 접두사 (기본값: None)\n
        [메서드 종류]
        - setAxis : 조인트 체인의 주 방향 설정, 스트래치 및 볼륨메 설정에 필요.
        - setScaleDefault : 스트레치 및 볼륨메 스케일조정 오브젝트 생성.
        - createCrv : 조인트들 위치에 커브 생성됨
        - setStretch : 스트래치 설정 Root조인트에 Attr 생성됨,리깅자체는 setIKBuild메서드에 세팅됨
        - setVolume : 볼륨메 설정 Root조인트에 Attr 생성됨,리깅자체는 setIKBuild메서드에 세팅됨
        - setIKBuild : 위 메서드를 통해 설정값을 받고 리깅빌드됨
        

        '''
        self.Jntlst = Jntlst
        self.Crv = None
        self.Root = None
        self.IK = None
        self.AxisDic = {"Axis" : "X" , "axis" : "x"}
        self.AxisOtherDic = {"Axis" : ["Y" ,"Z"] , "axis" : ["y" , "z"]}

        
        self.IsStretch = False
        self.IsVolume = False
        self.IsVolumeOffset = False
        self.IsFold = False

        self.ScaleDefault = None
        self.ScaleDefaultExpDic = None

        self.StretchAttrName = None
        self.StretchAttrExpDic = None
        self.StretchFuncExpDic = None

        self.VolumeAttrName = None 
        self.VolumeAttrExpDic = None
        self.VolumeFuncExpDic = None
        self.VolumeOffsetName = None


        self.FoldAttrName = None
        self.FoldOffsetName = None
        self.FoldAttrExpDic = None
        self.FoldFuncExpDic = None
        self.FoldOffsetAttrExpDic = None

        self.NamingFormat = "NoneName_" + "{count}{name}"
        self.IsNamingFormat = True

        if PrefixName:
            self.NamingFormat = PrefixName + "{count}{name}"
            



        self.ExpTotal = ""
        
        

        

        self.ExpFuncSetRange = r"global proc float setRangeFunc (float $value , float $oldMin , float $oldMax , float $Min , float $Max  ) {"
        self.ExpFuncSetRange += "\n"
        self.ExpFuncSetRange += r"   float $Func = clamp($Min , $Max , $Min + ((($value  -$oldMin  )/($oldMax -$oldMin ) )  * ($Max -  $Min)       )     );"
        self.ExpFuncSetRange += "\n"
        self.ExpFuncSetRange += r"  return  $Func;"
        self.ExpFuncSetRange += "\n"
        self.ExpFuncSetRange += r"}"
        self.ExpFuncSetRange += "\n"
        self.ExpFuncBlend = r"global proc float BlendFunc (float $blender , float $color1 , float $color2) {"
        self.ExpFuncBlend += "\n"
        self.ExpFuncBlend += r"  float $output = ((1.0- $blender)*  $color1) + ($blender *  $color2);"
        self.ExpFuncBlend += "\n"
        self.ExpFuncBlend += r"  return $output;"
        self.ExpFuncBlend += "\n"
        self.ExpFuncBlend += r"}"
        self.ExpFuncBlend += "\n"

        self.ExpTotal += self.ExpFuncSetRange
        self.ExpTotal += self.ExpFuncBlend

        reNameJnts= []
        for i , x in enumerate(self.Jntlst):
            #print (x)
            reNameString = self.NamingFormat.format(count = "_" + str(i +1).zfill(2) , name ="_Jnt" )
            Jnt = cmds.rename(x ,reNameString )
            reNameJnts.append(Jnt)

        self.Jntlst = reNameJnts
        if len(self.Jntlst) > 0 and cmds.objectType(self.Jntlst[0]) == "joint":
            self.Root = self.Jntlst[0]

    def setAxis(self , Axis = "X"):
        '''
        [메서드 설명]
        - setAxis : 조인트체인의 주 방향을 설정하는 메서드로 스트래치 및 볼륨메에 필수적
            - Axis : 주방향 매개변수 오로지 XYZ 중 하나만
        
        
        '''

        upperAxisOtherlst = []
        lowAxisOtherlst = []
        for x in "XYZ":
            if x == Axis:
                self.AxisDic["Axis"] = x
                self.AxisDic["axis"] = x.lower()
            else:
                upperAxisOtherlst.append(x)
                lowAxisOtherlst.append(x.lower())

        self.AxisOtherDic["Axis"] = upperAxisOtherlst
        self.AxisOtherDic["axis"] = lowAxisOtherlst
            
    def setScaleDefault(self , ScaleDefault = None):
        '''
        [메서드 설명]
        - setScaleDefault : 스트래치 및 볼륨메 scaling 설정
            - ScaleDefault : 이미 만들어진 ScaleDefault가 있다면 입력
        
        
        '''
        if self.IsNamingFormat:
            if   ScaleDefault and cmds.objExists(ScaleDefault):
                self.ScaleDefault = ScaleDefault
            else:
                self.ScaleDefault = cmds.createNode("transform" , n = self.NamingFormat.format(count = "" , name = "_ScaleDefault"))
        if self.ScaleDefault:
            self.ScaleDefaultExpDic = {"ScaleDefaultExpFunc" : "float $ScaleDefault = {}.sx;\n" .format(self.ScaleDefault) , "ScaleDefaultVar" : "$ScaleDefault"}

        
        
    def setStretch(self , AttrName = "Stretch" , Min = 0 , Max = 10):
        '''
        [메서드 설명]
        - setStretch : 스트래치 Attr 설정 root 조인트에 attr만들어짐 , setIKBuild 메서드 사용시 스트래치 진행됨
            - AttrName : Attr 네임
            - Min,Max : Attr 최소값 ,최대값
        
        
        '''
        if AttrName and self.Root:
            self.IsStretch = True
            self.StretchAttrName =  AttrName
            if cmds.attributeQuery(self.StretchAttrName , node = self.Root ,exists=True) == False:
                cmds.addAttr(self.Root, ln=self.StretchAttrName, at='float', k=1 , min = Min , max = Max)


            self.StretchAttrExpDic = {"StretchExpFunc" : "float $StretchSwitch = setRangeFunc({root}.{attr} , {oldmin} , {oldmax} , 0 , 1);\n" .format(root = self.Root , attr = self.StretchAttrName , oldmin = Min , oldmax = Max)  , "StretchExpVar" : "$StretchSwitch"}
        else:
            print ("AttrName is None")

    def setVolume(self , AttrName = "Volume"  , Min = 0 , Max = 10 , Offset_suffixName = "_Offset"):
        '''
        [메서드 설명]
        - setVolume : 볼륨메 Attr 설정 root 조인트에 attr만들어짐 , setIKBuild 메서드 사용시 볼륨메 진행됨
            - AttrName : Attr 네임
            - Min,Max : Attr 최소값 ,최대값
            - Offset_suffixName : 볼륨메 옵셋 Attr 네임 설정 (AttrName + Offset_suffixName )
        
        
        '''
        if AttrName and self.Root:
            self.IsVolume = True
            self.VolumeAttrName = AttrName
            self.VolumeOffsetName = AttrName + Offset_suffixName
            if cmds.attributeQuery(self.VolumeAttrName , node = self.Root ,exists=True) == False:
                cmds.addAttr(self.Root, ln=self.VolumeAttrName, at='float', k=1 , min = Min , max = Max)
            if cmds.attributeQuery(self.VolumeOffsetName , node = self.Root ,exists=True) == False:
                cmds.addAttr(self.Root, ln=self.VolumeOffsetName, at='float', k=1 )

            self.VolumeAttrExpDic = {"VolumeExpFunc" : "float $VolumeSwitch = setRangeFunc({root}.{attr} , {oldmin} , {oldmax} , 0 , 1);\n" .format(root = self.Root , attr = self.VolumeAttrName , oldmin = Min , oldmax = Max)  , "VolumeExpVar" : "$VolumeSwitch"}
            self.VolumeOffsetAttrExpDic = {"VolumeOffsetExpFunc" : "float $VolumeOffset = {}.{} +1;\n" .format(self.Root ,self.VolumeOffsetName ) ,"VolumeOffsetExpVar" : "$VolumeOffset" }
        else:
            print ("AttrName is None")

    def setFold(self , AttrName = "Fold" ,  Min = 0 , Max = 10 , Offset_suffixName = "_Offset"):
        if AttrName and self.Root:
            self.IsFold = True
            self.FoldAttrName = AttrName
            self.FoldOffsetName = AttrName + Offset_suffixName
            if cmds.attributeQuery(self.FoldAttrName , node = self.Root , exists=1) == False:
                cmds.addAttr(self.Root , ln = self.FoldAttrName , at = "float" , k =1 , min = Min , max = Max)
            if cmds.attributeQuery(self.FoldOffsetName , node = self.Root , exists=1) == False:
                cmds.addAttr(self.Root, ln=self.FoldOffsetName , at='float', k=1 )

            self.FoldAttrExpDic = {"FoldExpFunc" : "float $FoldSwitch = setRangeFunc({root}.{attr} , {oldmin} , {oldmax} , 0 , 1);\n" .format(root = self.Root , attr = self.FoldAttrName , oldmin = Min , oldmax = Max)  , "FoldExpVar" : "$FoldSwitch"}
            self.FoldOffsetAttrExpDic =  {"FoldOffsetExpFunc" : "float $FoldOffset = {}.{} +1;\n" .format(self.Root ,self.FoldOffsetName ) ,"FoldOffsetExpVar" : "$FoldOffset" }

    def createCrv(self , CrvList = None):
        '''
        [메서드 설명]
        - createCrv : Ikspline에 필요한 커브 생성 degree는 3이 고정
            - CrvList : 만일 이미 만들어진 커브가 있다면 쓸것 <반드시 [커브 transform , 커브 shape ] >형태로 입력되어야함
            - 예시  CrvList = ["curve_IK_Crv" ,"curve_IK_Crvshape" ]

        '''
        Poslist = []
        if CrvList is None:
            if all(cmds.objectType(x) == "joint" for x in self.Jntlst ) and len(self.Jntlst) > 2 and self.NamingFormat:
                for x in self.Jntlst:
                    Pos = tuple(cmds.xform(x , q =1 , t =1 ,ws =1))
                    Poslist.append(Pos)
                Crv = cmds.curve(n = self.NamingFormat.format(count = "",name = "_Crv") , p = Poslist ,d =3 )
                Crv = cmds.rebuildCurve( Crv , ch =1 , rpo =1 , rt =0 , end =1 , kr = 0 , kep =1 , kt =0 ,s = len(self.Jntlst)-1, d =3 , tol = 100 )
                CrvShp = cmds.rename(cmds.listRelatives(Crv[0] , s =1 )[0] , self.NamingFormat.format(count = "" , name = "_CrvShape"))

                self.Crv = [Crv[0] , CrvShp]
        else: 
            self.Crv = CrvList




    def setIKBuild(self ):
        '''
        [메서드 설명]
        - setIKBuild : 최종 빌드 메서드 , 대부분의 리깅은 expression으로 세팅됨


        '''


        if self.Jntlst and self.Crv and self.IsNamingFormat:
            #print (self.Jntlst)

            IKSet = cmds.ikHandle( n = self.NamingFormat.format(count = "" , name = "_IK") , c = self.Crv[0] , ee =self.Jntlst[-1] , sj = self.Jntlst[0] , sol = "ikSplineSolver",ccv = 0)
            self.IK = IKSet
            DisTanceNodes = []
            if self.IsStretch or self.IsVolume:
                if self.ScaleDefault is None:
                    self.setScaleDefault()
                self.StretchFuncExpDic = {"DistanceExpFunc" : [] , "DisTanceExpVar" : [] , "StaticExpFunc" : [] , "StaticExpVar" : [] , "StretchExpFunc" : []}
                self.VolumeFuncExpDic = {"DivPowerExpVar" : [] ,"DivPowerExpFunc" : [] , "VolumeExpFunc" : []}
                if self.ScaleDefault is None:
                    self.setScaleDefault()
                OldPOCIF = None
                Parameter = 0

                for i , Jnt in enumerate(self.Jntlst):
                    DM = cmds.createNode("decomposeMatrix" , n = self.NamingFormat.format(count = "_" + str(i+1).zfill(2) , name = "_DM"))
                    NPOC = cmds.createNode("nearestPointOnCurve" , n = self.NamingFormat.format(count = "_" + str(i+1).zfill(2) , name = "_NPOC"))
                    cmds.connectAttr(self.Crv[1] + ".worldSpace[0]" , NPOC + ".inputCurve" ,f =1)
                    cmds.connectAttr(Jnt + ".worldMatrix[0]" , DM + ".inputMatrix")

                    for Axis in "XYZ":
                        cmds.connectAttr(DM + ".outputTranslate{}" .format(Axis) , NPOC + ".inPosition{}".format(Axis) , f=1)
                    Parameter = cmds.getAttr(NPOC + ".result.parameter")
                    try:
                        cmds.delete(NPOC)
                        cmds.delete(DM)
                    except:
                        pass

                    POCIF = cmds.createNode("pointOnCurveInfo" , n = self.NamingFormat.format(count = "_" + str(i+1).zfill(2) , name = "_POCIF"))
                    cmds.connectAttr(self.Crv[1] + ".worldSpace[0]" , POCIF + ".inputCurve")
                    cmds.setAttr(POCIF + ".turnOnPercentage" , 1)
                    cmds.setAttr(POCIF + ".parameter" , Parameter)

                    if OldPOCIF:
                        Distance = cmds.createNode("distanceBetween" , n = self.NamingFormat.format(name = "_DTB" , count = "_" + str(i+1).zfill(2)))
                        for Axis in "XYZ":
                            cmds.connectAttr(OldPOCIF + ".position{}" .format(Axis) , Distance + ".point1{}" .format(Axis) ,f =1)
                            cmds.connectAttr(POCIF + ".position{}" .format(Axis) , Distance + ".point2{}" .format(Axis) ,f =1)
                        DisTanceNodes.append(Distance)
                    OldPOCIF = POCIF
                
                
                
                for  i , Distance in enumerate(DisTanceNodes):
                    GetDistance = cmds.getAttr(Distance + ".distance")
                    self.StretchFuncExpDic["StaticExpFunc"].append("float $Static_{}_DT = {};\n" .format(str(i+1) , GetDistance))
                    ##self.StretchFuncExpDic["StaticExpVar"].append( "$Static_{}_DT" .format(str(i+1)))

                    self.StretchFuncExpDic["DistanceExpFunc"].append("float $DTB{} = {}.distance;\n".format(str(i+1), Distance ) )
                    ##self.StretchFuncExpDic["DisTanceExpVar"].append("$DTB{}" .format(str(i+1)))



                self.ExpTotal += self.ScaleDefaultExpDic["ScaleDefaultExpFunc"]
                self.ExpTotal += self.StretchAttrExpDic["StretchExpFunc"]
            OldJnt= self.Jntlst[1]
            PlusMiuns = 1
            if self.IsStretch and self.AxisDic:
                for  i , Distance in enumerate(DisTanceNodes):
                    if OldJnt:
                        roundTz = round(cmds.getAttr(OldJnt + ".translate{}" .format(self.AxisDic["Axis"]) ) , 2)
                        PlusMiuns = roundTz/abs(roundTz)


                    StretchExp = "{}.translate{} = " .format(self.Jntlst[i+1] , self.AxisDic["Axis"])
                    StretchExp += "{} * $Static_{}_DT" .format(PlusMiuns , str(i+1))
                    StretchExp += "* BlendFunc({attr} , 1 , {distance}/({static}* {scale}) );" .format(attr = self.StretchAttrExpDic["StretchExpVar"] , distance = "$DTB{}" .format(str(i+1)) ,static = "$Static_{}_DT".format(str(i+1)) , scale = self.ScaleDefaultExpDic["ScaleDefaultVar"] )
                    StretchExp += "\n"

                    self.StretchFuncExpDic["StretchExpFunc"].append(StretchExp)
                for String in [ "DistanceExpFunc" ,"StaticExpFunc" , "StretchExpFunc"  ]:
                    for x in self.StretchFuncExpDic[String]:
                        self.ExpTotal +=x

    
            if self.IsVolume and self.AxisOtherDic:
                self.ExpTotal += self.VolumeAttrExpDic["VolumeExpFunc"]
                self.ExpTotal += self.VolumeOffsetAttrExpDic["VolumeOffsetExpFunc"]

                for  i , Distance in enumerate(DisTanceNodes[:-1]):
                    FuncStringExp = "float $VolumeFunc_{num} =  pow((1 / ({dt} / ({static} * {scale}))) , 0.5);\n" .format(num = str(i+1) , dt = "$DTB{}" .format(str(i+1)) ,  static = "$Static_{}_DT".format(str(i+1)) ,  scale = self.ScaleDefaultExpDic["ScaleDefaultVar"] )
                    self.VolumeFuncExpDic["DivPowerExpVar"].append(FuncStringExp)
                for  i , Func in enumerate(DisTanceNodes[:-1]):
                    FuncStringExp = "{jt}.scale{ax} = ".format(jt = self.Jntlst[i+1] ,ax =  self.AxisOtherDic["Axis"][0])
                    FuncStringExp += "BlendFunc({attr} , {offset} , $VolumeFunc_{num} *{offset} );\n" .format(attr = self.VolumeAttrExpDic["VolumeExpVar"] , num = str(i+1), offset = self.VolumeOffsetAttrExpDic["VolumeOffsetExpVar"])
                    FuncStringExp += "{jt}.scale{ax} = ".format(jt = self.Jntlst[i+1] ,ax =  self.AxisOtherDic["Axis"][1])
                    FuncStringExp += "BlendFunc({attr} , {offset} , $VolumeFunc_{num} *{offset});\n" .format(attr = self.VolumeAttrExpDic["VolumeExpVar"] , num = str(i+1), offset = self.VolumeOffsetAttrExpDic["VolumeOffsetExpVar"])
                    self.VolumeFuncExpDic["VolumeExpFunc"].append(FuncStringExp)

                for String in [ "DivPowerExpVar" , "VolumeExpFunc" ]:
                    for x in self.VolumeFuncExpDic[String]:
                        self.ExpTotal +=x


            if self.IsStretch or self.IsVolume:
                print (self.ExpTotal )
                ExpName = "Exp_" + self.NamingFormat.format(count = "" , name = "") + "_Func"
                if cmds.objExists(ExpName):
                    cmds.delete(ExpName)
                cmds.expression(string= self.ExpTotal,  n = ExpName)

            












            









'''


sel = cmds.ls(sl =1)

for AlpInt , root in enumerate(sel):
    cmds.select(root , hi =1)
    rootHi = cmds.ls(sl =1)
    IK = c_IKspline(rootHi , "Hair_IK" )
    IK.setAxis("Y")
    #IK.createCrv()
    IK.setStretch("Stretch")
    IK.setVolume("Volume")
    IK.setIKBuild()


IK = c_IKspline(sel , "Tail")
IK.setAxis("Z")
IK.createCrv()
IK.setStretch("Stretch")
IK.setVolume("Volume")
IK.setIKBuild()"
'''