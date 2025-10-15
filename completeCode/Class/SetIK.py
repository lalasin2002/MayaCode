# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import re , pprint


class Ikrig:
    def __init__(self , Jntlist ):
        
        self.Jntlist = None
        self.IKs = []
        self.Distances = []
        self.Root = None
        self.ScaleDefault = None
        self.ScalingMD = None
        self.CurrentDistanceNode = None
        self.CurrentIK = None
        self.resultNodes = {}
        self.poleVectorStretchNodes = {}
        self.stretchBC = None
        self.volumeBC = None
        self.stretchDistance = None
        

        self.AxisDic = {"Axis" : "X" , "axis" : "x"}
        self.AxisOtherDic = {"Axis" : ["Y" ,"Z"] , "axis" : ["y" , "z"]}

        self.IsIKstretch = False
        self.IsIKVolume = False
        self.IsPoleVector = False
        self.IsSlide = False
        self.DistanceDic = None

        self.startDT_loc = None
        self.endDT_loc = None
        self.AttrsDicList =[]

        self.stretchNodeDic = {
            "scaleDefault" : None,
            "distance" : None,
            "distanceLentgh" : None,
            "jointList" : None,
            "jointLength": None,
            "scalingMD" : None,
            "normalMD" : None,
            "lengthCon" : None,
            "attrSR" : None,
            "stretchBC" : None 
        }

        self.volumeNodeDic = {

            "jointList" : None,
            "divMD" : None,
            "powerMD" : None,
            "offsetADL" : None,
            "attrSR" : None , 
            "volumeBC" : None,
            "stretchBC" : None ,
        }

        self.poleVectorDic = {
            "obj" : None,
            "shape" : None,
            "ik" : None,
            "annotation" : None,
            "annotationShape" : None
        }

        self.stretchAttrDic = {
            "attr" : None,
            "min" : None,
            "max" : None,
            "obj" : None 
        }
        self.volumeAttrDic = {
            "attr" : None,
            "offsetAttr" : None,
            "min"  : None,
            "max"  : None,
            "obj"  : None
        }
        self.poleVectorStretchAttrDic={
            "attr" : None,
            "min"  : None,
            "max"  : None,
            "obj"  : None
        }

        self.log_messages = []
        self.defineJntlist(Jntlist , True)
        

    def defineJntlist(self , Jntlist , reset = False ):
        if not isinstance(Jntlist, list) or not all(cmds.objectType(x) == "joint" for x in Jntlist):
            raise TypeError("Invalid input. Expected a Existed Joint list")

        if reset:
            self.Jntlist = []
            self.resultNodes = {}
            self.log("--- Joint list has been reset. ---", True)

        for jnt in Jntlist:
            # 기존 리스트에 없는 조인트만 추가합니다.
            if jnt not in self.Jntlist:
                self.Jntlist.append(jnt)
                #IsDicNode = any(y.get("Jnt") == jnt for y in self.resultNodes)
                self.resultNodes[jnt] = {
                    "MDL": None,
                    "ADL": None,
                    "Jnt": jnt,
                    "SlideAttr": None,
                    "VolumeADL": None,
                }
                #self.resultNodes.append(resultDic)
                self.log("> Joint '{}' added to the list." .format(jnt), True)
        else:
            self.log("> Joint '{}' already exists, skipping." .format(jnt), True)

    def log(self, msg, print_now=False):

        self.log_messages.append(msg)
        if print_now:
            print(msg)

    def Grping(self,Target , Count , Grp_Suffix = ["_Grp" , "_Offset" , "_Prime" , '_GrpPrime']):
        """
        주어진 대상 오브젝트에 대해 여러 개의 그룹을 생성하고 계층화합니다.
        생성된 그룹은 대상 오브젝트의 위치에 스냅된 후, 대상 오브젝트는 가장 안쪽 그룹의 자식이 됩니다.

        Args:
            Target (str): 그룹 계층을 생성할 대상 오브젝트의 이름.
            Count (int): 생성할 그룹의 개수 (Grp_Suffix 리스트의 처음부터 Count 만큼 사용).
            Grp_Suffix (list, optional): 생성할 그룹의 이름에 사용될 접미사 리스트.
                                        기본값은 ["_Grp", "_Offset", "_Prime", "_GrpPrime"].

        Returns:
            list: 생성된 그룹의 리스트 (바깥쪽 그룹부터 안쪽 그룹 순서).
        """

        Count = int(Count) # Count를 정수로 변환
        Groups =[] # 생성된 그룹들을 저장할 리스트
        Parent_Group = None # 이전 그룹을 저장하여 계층을 구축

        # 지정된 Count 만큼 그룹 생성 및 계층화
        for i , x in enumerate(Grp_Suffix[:Count]):
            Group = cmds.createNode("transform" , n = "{}{}" .format(Target ,x)) # 그룹 노드 생성

            if Parent_Group:
                cmds.parent( Parent_Group ,Group ) # 이전 그룹을 현재 그룹의 자식으로 설정 (바깥쪽에서 안쪽으로)
            Parent_Group = Group # 현재 그룹을 이전 그룹으로 업데이트
            Groups.append(Group) # 생성된 그룹을 리스트에 추가

        # 가장 바깥쪽 그룹을 대상 오브젝트의 위치에 스냅하고 제약 조건 삭제
        cmds.delete(cmds.parentConstraint(Target, Groups[-1]))
        # 대상 오브젝트를 가장 안쪽 그룹의 자식으로 설정
        cmds.parent(Target ,  Groups[0])

        return  Groups

    def CreateOrGet_Loc(self,obj_or_pos , Name  = "locator" , MaxWhileCount =100): #2025-06-13 추가
        """
        주어진 오브젝트나 위치값을 기반으로 로케이터를 생성하거나,
        이미 로케이터일 경우 해당 로케이터 정보를 가져옵니다.

        Args:
            obj_or_pos (str or list or tuple): 오브젝트의 이름 또는 월드 좌표값.
            Name (str): 생성될 로케이터의 기본 이름.
            MaxWhileCount (int): 고유 이름을 찾기 위해 시도할 최대 횟수.

        Returns:
            list: [로케이터 트랜스폼 노드, 로케이터 쉐잎 노드]
        """
        string_type = None
        try:
            string_type = basestring
        except NameError:
            string_type = str
        loc = None
        shape = None
        if isinstance(obj_or_pos , string_type) and cmds.objExists(obj_or_pos):
            objType = cmds.objectType(obj_or_pos)
            if objType == "locator":
                loc = cmds.listRelatives(loc, p=1, type="transform")[0]
                shape = obj_or_pos
            if objType == "transform":
                loc = obj_or_pos
                shape = cmds.listRelatives(loc, s=1, type="locator")[0]

        if Name == "" and isinstance(obj_or_pos , string_type):
            Name = loc
        count =0
        loc_name = ""
        for i in range(MaxWhileCount):
            count = str(i) if i> 0 else ""
            temp_name = "{}{}" .format(Name , count )
            if not cmds.objExists(temp_name):
                loc_name = temp_name
                break
        if not loc_name :
            raise RuntimeError("Could not generate a unique locator name for: {}{}." .format(Name , count )) #2025-06-13 추가
        
        
        if isinstance(obj_or_pos , (list , tuple) ) and not loc and not shape:
            if isinstance(obj_or_pos , tuple):
                obj_or_pos = list(obj_or_pos)

            loc = cmds.spaceLocator(n = loc_name)[0]
            shape = cmds.listRelatives(loc , s =1)[0]
            cmds.xform(loc , ws =1 , t = obj_or_pos)
        elif isinstance(obj_or_pos ,  string_type) and not loc and not shape:
            loc = cmds.spaceLocator(n = loc_name)[0]
            shape = cmds.listRelatives(loc , s =1)[0]
            cmds.delete(cmds.parentConstraint(obj_or_pos , loc , mo = 0))

        return [loc ,shape]
    def Create_Distance(self ,startObj_or_pos , endObj_or_pos , Names = ["startlocator" , "endlocator"  , "Distance"] ):
        """
        CreateOrGet_Loc 함수 사용
        두 지점 사이에 동적인 거리 측정 노드를 생성합니다.

        이 함수는 시작점과 끝점에 로케이터를 생성하거나 찾고,
        이 두 로케이터 사이의 거리를 실시간으로 측정하는 `distanceDimension` 노드를
        생성하여 연결합니다. 이 모든 과정은 이전에 정의한 `CreateOrGet_Loc` 함수를
        활용하여 수행됩니다.

        Args:
            startObj_or_pos (str or list or tuple): 시작점으로 사용할 오브젝트의 이름 또는 월드 좌표값.
            endObj_or_pos (str or list or tuple): 끝점으로 사용할 오브젝트의 이름 또는 월드 좌표값.
            Names (list): 생성될 노드들의 기본 이름 리스트.
                        [0]: 시작 로케이터, [1]: 끝 로케이터, [2]: 거리 측정 노드 순서입니다.

        Returns:
            -dict or None: 
                딕셔너리 키
                {
                "startLoc" : startLoc ,
                "endLoc" : endLoc ,
                "startLoc_shape" : startLocShape ,
                "endLoc_shape" : endLocShape ,
                "distance_node" : DistanceShape ,
                "distance_transform" : Distance
                }
                성공 시, 생성되거나 사용된 모든 노드(로케이터, 쉐잎, 거리 노드 등)의 
                이름을 담은 딕셔너리를 반환합니다.
                로케이터 생성에 실패하면 None을 반환합니다.
        """
        
        string_typ = None
        try:
            string_type = basestring
        except NameError:
            string_type = str

        startLoc = None
        startLocShape = None
        endLoc = None
        endLocShape = None
        
        Distance = None
        DistanceShape = None
        DistanceName  = None
        DistanceShapeSuffix = "Shape"
        DistanceCount = 0
        returnDic = None

        

        startLocs = self.CreateOrGet_Loc(startObj_or_pos , Names[0])
        endLocs = self.CreateOrGet_Loc(endObj_or_pos , Names[1])
        

        if startLocs and endLocs:
            startLoc = startLocs[0]
            startLocShape = startLocs[1]
            endLoc = endLocs[0]
            endLocShape = endLocs[1]

            while True:
                DistanceName = "{}{}{}" .format(Names[2] , DistanceShapeSuffix , "" if DistanceCount == 0 else DistanceCount)
                if not cmds.objExists(DistanceName ):
                    break
                DistanceCount += 1
            DistanceShape = cmds.createNode("distanceDimShape" , n = DistanceName )
            Distance = cmds.listRelatives(DistanceShape, p =1 , type= "transform")
            Distance = cmds.rename(Distance[0] , '{}{}' .format(Names[2]  , "" if DistanceCount == 0 else DistanceCount))

            cmds.connectAttr(startLocShape + ".worldPosition[0]" , DistanceShape + ".startPoint" ,f =1)
            cmds.connectAttr(endLocShape + ".worldPosition[0]" , DistanceShape + ".endPoint" ,f =1)

            returnDic = {
                "startLoc" : startLoc ,
                "endLoc" : endLoc ,
                "startLoc_shape" : startLocShape ,
                "endLoc_shape" : endLocShape ,
                "distance_node" : DistanceShape ,
                "distance_transform" : Distance
            }
            
        return returnDic
    
    def Get_Distance(self , StartObj, EndObj , Round =3 ):
        """두 오브젝트의 거리값 가져오기"""
        S_Pos = cmds.xform(StartObj , q =1, t =1 ,ws =1)
        E_Pos = cmds.xform(EndObj, q=1, t=1, ws=1)
        DT = round(((S_Pos[0] - E_Pos[0])**2 + (S_Pos[1] - E_Pos[1])**2 + (S_Pos[2] - E_Pos[2])**2)**0.5 , Round)
        return DT

    def uniqueName(self , Name , maxLoop = 100 ):
        string_type = None
        try:
            string_type = basestring
        except NameError:
            string_type = str
        returnName = None
        formatName = None
        count = 0
        if isinstance(Name , string_type ):

            hasFormatPattern = r"\{.*?\}"
            hasFormat = re.search(hasFormatPattern , Name)
            
            isIntPattern = r"(.*?)([0-9]+)(.*?)"
            isInt = re.search(isIntPattern , Name)
            if isInt:
                matchs = isInt.groups()
                count = int(isInt.group(2))
                joinName = []
                for x in matchs:
                    if x == isInt.group(2):
                        x = "{}"
                        joinName.append(x)
                        continue
                    joinName.append(x)
                formatName = "".join(joinName)
            else:
                formatName = Name + "{}"
            
            for x in range(count , maxLoop + count):
                count = x if x > 0 else ""

                returnName = formatName.format("" if count == 0 else count )
                if not cmds.objExists(returnName):
                    break

        return returnName

    def setAxis(self , Axis = "X", printLog = False):

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
        self.log("> Primary Axis : {pa}\n> Other Axis : {oa}" .format(pa =self.AxisDic["Axis"] , oa = self.AxisOtherDic["Axis"]), printLog)

    def getPoleVectorPosData(self ,first , second , third , scalar = 1):
        poleVecorPos = None
        #if all(cmds.objectType(x) == "transform" in x for x in [first , second , third]):

        firstPos = cmds.xform(first , q= 1, ws =1 , t =1)
        secondPos = cmds.xform(second , q= 1, ws =1 , t =1)
        thirdPos =  cmds.xform(third , q= 1, ws =1 , t =1)

        firstVector = om.MVector(firstPos[0] , firstPos[1] ,firstPos[2])
        secondVector = om.MVector(secondPos[0], secondPos[1] , secondPos[2])
        thirdVector = om.MVector(thirdPos[0] , thirdPos[1] , thirdPos[2])

        firstThirdVector = (thirdVector - firstVector)
        firstSecondVector = (secondVector - firstVector)

        dotProduct = firstThirdVector * firstSecondVector
        proJectLength = float(dotProduct)/(firstThirdVector.length())

        normalizeFirstThird = firstThirdVector.normal()
        proJectVector = normalizeFirstThird * proJectLength
        arrowVector = (firstSecondVector - proJectVector) * scalar 
        poleVector = arrowVector + secondVector

        poleVecorPos = [poleVector.x , poleVector.y , poleVector.z]
        
        return poleVecorPos



    def setScaleDefault(self , ScaleDefault = None , printLog = False):

        if ScaleDefault:
            if cmds.objExists(ScaleDefault):
                self.ScaleDefault = ScaleDefault
                self.log("> Using existing node for ScaleDefault : {}" .format(self.ScaleDefault) , printLog)
            else:
                self.ScaleDefault = cmds.createNode("transform" , n = self.uniqueName("ScaleDefault"))
                self.log("> Created new node for ScaleDefault: {}".format(self.ScaleDefault) , printLog)
        elif not self.ScaleDefault:
            self.ScaleDefault = cmds.createNode("transform" , n =  self.uniqueName("ScaleDefault"))
            self.log("> Created new node for ScaleDefault: {}".format(self.ScaleDefault) , printLog)


        if ScaleDefault:
            self.ScalingMD = cmds.createNode("multiplyDivide" , n = self.ScaleDefault + "_Scaling_MD" )
            cmds.connectAttr(self.ScaleDefault + ".scaleX"  , self.ScalingMD + ".input2X" , f=1)

        else:
            self.log("> ScaleDefault is already set to: {}" .format(self.ScaleDefault) , printLog)

    def setIKHandle(self ,  Name = None ,RootJnt = None,TargetJnt = None  , GrpCount = 0 , solver =  "ikRPsolver" , printLog = False):
        if RootJnt is None and TargetJnt is None:
            if len(self.Jntlist) >1 :
                RootJnt = self.Jntlist[0]
                TargetJnt= self.Jntlist[-1]

        if cmds.objExists(RootJnt) and cmds.objExists(TargetJnt):
            if Name is None:
                Name = self.uniqueName(TargetJnt +"_IK")
            else:
                Name = self.uniqueName(Name)

            ikResult= cmds.ikHandle( sj = RootJnt , ee = TargetJnt ,n = Name  ,sol = solver  )
            IK = ikResult[0]
            print (">>>>", IK)
            #self.IKs.append(IK[0])
            Grp = None
            if GrpCount>0:
                Grp = self.Grping(IK , GrpCount)
            IK_Dic = {
                "IKhandle" : IK,
                "Group" : Grp ,
                "TargetJnt" : TargetJnt
            }
            self.IKs.append(IK_Dic)
            self.CurrentIK = IK
            
            self.log("> Create IK handle : {}\n> Create IK handleGrp : {}" .format(IK_Dic["IKhandle"], IK_Dic["Group"])  ,printLog  )
        else:
            self.log("> Not Exist objs to set Ikhandle: {} , {}" .format(RootJnt , TargetJnt) , printLog )

    def addAttrStretch( self, Target , AttrName = "Stretch" , Min = 0 , Max = 10 ,printLog = False):
        
        if cmds.objExists(Target):
            IsAttr = cmds.attributeQuery(AttrName , node = Target , exists= 1)
            if not IsAttr:
                cmds.addAttr(Target , ln = AttrName ,  at='double', min=Min, max=Max, k=True)

            
            MinV = None
            MaxV = None
            if IsAttr:

                IsMin = cmds.attributeQuery(AttrName , node = Target , minimum=1 )
                IsMax = cmds.attributeQuery(AttrName , node= Target  , maximum=1 )
                if IsMin and IsMax:
                    self.stretchAttrDic["attr"] = AttrName
                    self.stretchAttrDic["obj"] = Target

                    
                    if IsMin:
                        MinV = cmds.attributeQuery(AttrName , node = Target  , minimum=1)
                        self.stretchAttrDic["min"] = MinV[0]
                    if IsMax:
                        MaxV = cmds.attributeQuery(AttrName , node = Target , maximum=1)
                        self.stretchAttrDic["max"] = MaxV[0]
                    self.log("> Add {tg}.{attr} stretch Attribute\n> Min : {min}\n> Max : {max}" .format(tg = Target , attr = AttrName , min = MinV , max = MaxV) ,printLog)

    def addSlide(self , Target , AttrName ,printLog = False):
        if cmds.objExists(Target):
            IsAttr = cmds.attributeQuery(AttrName , node = Target , exists= 1)
            if not IsAttr:
                cmds.addAttr(Target , ln = AttrName ,  at='double', k=True)
        
        if IsAttr:
            self.log("> Add {tg}.{attr} Slide Attribute" .format(tg = Target , attr = AttrName ) ,printLog)



    def addAttrVolume(self , Target , AttrName = "Volume" , Min = 0 , Max = 10 , printLog = False):
        OffsetAttrName = AttrName + "_Offset"
        if cmds.objExists(Target):
            IsAttr = cmds.attributeQuery(AttrName , node = Target , exists= 1)
            OffsetAttr = cmds.attributeQuery(OffsetAttrName  , node = Target , exists= 1)
            if not IsAttr:
                cmds.addAttr(Target , ln = AttrName ,  at='double', min=Min, max=Max, k=True)
            if not OffsetAttr:
                cmds.addAttr(Target , ln = OffsetAttrName ,  at='double', k=True)           

            MinV = None
            MaxV = None
            if IsAttr:
                IsMin = cmds.attributeQuery(AttrName , node = Target , minimum=1 )
                IsMax = cmds.attributeQuery(AttrName , node= Target  , maximum=1)
                if IsMin and IsMax:
                    self.volumeAttrDic["attr"] = AttrName
                    self.volumeAttrDic["obj"] = Target

                    if IsMin:
                        MinV = cmds.attributeQuery(AttrName , node = Target  , minimum=1)
                        self.volumeAttrDic["min"] = MinV[0]
                    if IsMax:
                        MaxV = cmds.attributeQuery(AttrName , node = Target , maximum=1)
                        self.volumeAttrDic["max"] = MaxV[0]
            
            if OffsetAttr:
                self.volumeAttrDic["offsetAttr"] = OffsetAttrName


            self.log("> Add {tg}.{attr} volume Attribute\n> Min : {min}\n> Max : {max}" .format(tg = Target , attr = AttrName , min = MinV , max = MaxV) ,printLog)
    def addAttrPoleVectorStretch(self , Target , AttrName = "PoleVectorStretch" , Min = 0 , Max = 10 , printLog = False):
        if cmds.objExists(Target):
            IsAttr = cmds.attributeQuery(AttrName , node = Target , exists= 1)
            if not IsAttr:
                cmds.addAttr(Target , ln = AttrName ,  at='double', min=Min, max=Max, k=True)
            MinV = None
            MaxV = None
            if IsAttr:
                IsMin = cmds.attributeQuery(AttrName , node = Target , minimum=1 )
                IsMax = cmds.attributeQuery(AttrName , node= Target  , maximum=1 )
                if IsMin and IsMax:
                    self.poleVectorStretchAttrDic["attr"] = AttrName
                    self.poleVectorStretchAttrDic["obj"] = Target

                    if IsMin:
                        MinV = cmds.attributeQuery(AttrName , node = Target  , minimum=1)
                        self.poleVectorStretchAttrDic["min"] = MinV[0]
                    if IsMax:
                        MaxV = cmds.attributeQuery(AttrName , node = Target , maximum=1)
                        self.poleVectorStretchAttrDic["max"] = MaxV[0]
            self.log("> Add {tg}.{attr} poleVectorStretch Attribute\n> Min : {min}\n> Max : {max}" .format(tg = Target , attr = AttrName , min = MinV , max = MaxV) ,printLog)
    def setDistance(self,Start , End , NameList = None):
        if NameList is None:
            NameList = [Start , End , End + "End"]

        if all(cmds.objExists(x) == True for x in [Start , End]):
            StartLoc = "{}_loc" .format(NameList[0])
            EndLoc = "{}_loc" .format(NameList[1])
            DT = "{}_Distance" .format(NameList[2])
            DictanceDic = self.Create_Distance(Start , End , [StartLoc , EndLoc , DT])

            self.DistanceDic = DictanceDic
            self.CurrentDistanceNode =  DictanceDic["distance_node"]
            self.startDT_loc = DictanceDic["startLoc"]
            self.endDT_loc = DictanceDic["endLoc"]

            self.Distances = set(self.Distances )
            self.Distances.add(self.CurrentDistanceNode)
            self.Distances = list(self.Distances)
        else:
            raise TypeError(">> Invalid input. Expected a Existed obj")
        
    def defineDistance(self , Start , End , Distance):
        if all(cmds.objExists(x) == True for x in [Start , End , Distance] ) and any(cmds.objectType(Distance) == y for y in ["distanceBetween" ,"distanceDimShape" ]):
            self.CurrentDistanceNode=  Distance
            self.startDT_loc = Start
            self.endDT_loc = End
        else:
            raise TypeError(">> Invalid input. Expected a Existed obj")
        



    def setSlide(self , Jnt , AttrTarget , AttrName ):
        if cmds.objExists(Jnt):
            IsAttr = cmds.attributeQuery(AttrName , node = AttrTarget , exists= 1)
            

            if not IsAttr:
                self.addSlide(AttrTarget , AttrName)
            
            #IsAttr:
            #pprint.pprint (self.resultNodes)

            IsDicNode = Jnt in self.resultNodes
            #print ()

            if IsDicNode:
                MDL = self.resultNodes[Jnt]["MDL"]
                ADL = cmds.createNode("addDoubleLinear" , n = Jnt + "_Slide" )

                IsCntAttr = cmds.listConnections( Jnt + ".translate{}" .format(self.AxisDic["Axis"]),s =1  , plugs=True )[-1]
                
                
                if IsCntAttr:
                    cmds.disconnectAttr(IsCntAttr , Jnt + ".translate{}" .format(self.AxisDic["Axis"]) )


                
                cmds.connectAttr("{}.{}" .format(AttrTarget , AttrName) , ADL + ".input2" , f=1)
                cmds.connectAttr("{}.{}" .format(MDL, "output")  ,ADL + ".input1" , f=1)
                cmds.connectAttr(ADL + ".output" , Jnt + ".translate{}" .format(self.AxisDic["Axis"]) , f=1)


                self.resultNodes[Jnt]["ADL"] = ADL
                self.resultNodes[Jnt]["SlideAttr"] = "{}.{}" .format(AttrTarget , AttrName)

    
    def createPoleVectorStretchNode(self , TargetJnt , inputNode = None , inputAttr = None ):
        try:
            string_type = basestring
        except NameError:
            string_type = str

        noralizeNode = None 
        noralizeNodeAttr = None

        if not cmds.objectType(TargetJnt) == "joint":
            raise TypeError(">  Invalid <TargetJnt> input. Expected a Existed Joint list")
        if not TargetJnt in self.resultNodes:
            raise TypeError(">  Invalid <TargetJnt > input. Could not Found <TargetJnt> in <self.resultNodes.>")

        if not inputNode:
            if self.stretchNodeDic["stretchBC"]:
                noralizeNode = self.stretchNodeDic["stretchBC"]
                noralizeNodeAttr = "outputR"
            else:
                raise ValueError(">  The required node 'stretchBC' is not defined or does not exist in the scene.")
        elif inputNode and cmds.objExists("{}" .format(inputNode)):
            if inputAttr and  isinstance(inputAttr, string_type ) and cmds.objExists("{}.{}" .format(inputNode , inputAttr)):

                noralizeNode = inputNode
                noralizeNodeAttr = inputAttr
            else :
                raise TypeError(">  Invalid <inputAttr> input. Expect a Existed <{}.{}> Attr" .format(inputNode , inputAttr))
            
    
        if not self.poleVectorStretchAttrDic["obj"] and not self.poleVectorStretchAttrDic["attr"]:
            if all(cmds.objectType(x) == "joint" for x in self.Jntlist):
                self.addAttrPoleVectorStretch(self.Jntlist[0])
            else:
                raise ValueError("> Could not find the required attribute: 'poleVectorStretchAttr'")
        

        DivMD = cmds.createNode("multiplyDivide" , n = TargetJnt + "_poleVectorStretch_Div_MD")
        ScalingMD = cmds.createNode("multiplyDivide" , n  = TargetJnt + "_poleVectorStretch_ScalingMD" )
        PoleStretchBC = cmds.createNode("blendColors", n  = TargetJnt + "_poleVectorStretch_BC" )
        AttrSR = cmds.createNode("setRange" ,  n =TargetJnt + "_poleVectorStretch_SR")

        cmds.setAttr(DivMD + ".input1X" , 1)
        cmds.setAttr(DivMD + ".operation" , 2)

        cmds.setAttr(PoleStretchBC + ".color1R" , 1)
        cmds.setAttr(PoleStretchBC + ".color2R" , 1)
            
        cmds.setAttr(AttrSR + ".minX" , 0)
        cmds.setAttr(AttrSR + ".maxX" , 1)
        cmds.setAttr(AttrSR + ".oldMinX" , self.poleVectorStretchAttrDic["min"])
        cmds.setAttr(AttrSR + ".oldMaxX" , self.poleVectorStretchAttrDic["max"])
        
        cmds.connectAttr("{}.{}" .format(noralizeNode , noralizeNodeAttr) , PoleStretchBC + ".color2R" , f=1)
        cmds.connectAttr(ScalingMD + ".outputX" ,DivMD + ".input2X" , f=1)
        cmds.connectAttr(DivMD + ".outputX" , PoleStretchBC + ".color1R" , f=1)
        cmds.connectAttr(AttrSR + ".outValueX" ,PoleStretchBC +  ".blender" ,f =1)
        cmds.connectAttr("{}.{}" .format(self.poleVectorStretchAttrDic["obj"] , self.poleVectorStretchAttrDic["attr"]) , AttrSR + ".valueX" ,f=1 )


        self.poleVectorStretchNodes[TargetJnt] = {
            "divMD": DivMD,
            "scalingMD": ScalingMD,
            "poleStretchBC": PoleStretchBC,
            "stretchBC" : noralizeNode,
            "stretchBC_Attr" : noralizeNodeAttr,
            "MDL" : self.resultNodes[TargetJnt]["MDL"],
            "MDL_Attr" : "input1",
            "attrSR": AttrSR
        }

    def createStretchNode(self ,Name , Jntlist , DistanceNode , ScaleDefaultDate= None ):

        uniqueName = self.uniqueName(Name)
        self.setScaleDefault(ScaleDefaultDate)
        self.stretchNodeDic["scaleDefault"] = self.ScaleDefault

        #pprint.pprint(self.stretchNodeDic)
        if self.stretchNodeDic["distance"] is None:
            if cmds.objectType(DistanceNode) == "distanceDimShape" or cmds.objectType(DistanceNode) == "distanceBetween":
                self.stretchNodeDic["distance"] = DistanceNode
                GetDistance = round(cmds.getAttr(self.stretchNodeDic["distance"]  + ".distance") ,3)
                self.stretchNodeDic["distanceLentgh"] = GetDistance
            else:
                raise TypeError("> Invalid <DistanceNode> input. Expected a DistanceNode  Shape")


        if self.stretchNodeDic["scaleDefault"] and self.stretchNodeDic["distance"]:
            if all(cmds.objectType(x) == "joint" for x in Jntlist) and isinstance(Jntlist , list):

                OldJnt = None
                TotalLength = 0
                self.stretchNodeDic["jointList"] = []
                for Jnt in Jntlist:
                    if OldJnt:
                        self.stretchNodeDic["jointList"].append(OldJnt)
                        JntLength = self.Get_Distance(OldJnt , Jnt )


                        
                        TotalLength += JntLength
                    OldJnt = Jnt
                
                self.stretchNodeDic["jointLength"] = TotalLength
                self.defineJntlist(self.stretchNodeDic["jointList"])

                ScalingMD = cmds.createNode("multiplyDivide" , n = self.stretchNodeDic["scaleDefault"] + "_Scaling_MD")
                NormalMD = cmds.createNode("multiplyDivide" , n =uniqueName + "_Nor_MD")
                LengthCon = cmds.createNode("condition" , n = uniqueName + "_Length_CON")
                
                StretchBC = cmds.createNode("blendColors" , n  = uniqueName + "_BC" )
                AttrSR = cmds.createNode("setRange" ,  n = uniqueName + "_SR")


                cmds.setAttr(AttrSR + ".minX" , 0)
                cmds.setAttr(AttrSR + ".maxX" , 1)

                cmds.setAttr(ScalingMD + ".input1X" , self.stretchNodeDic["jointLength"])
                cmds.setAttr(NormalMD + ".operation" , 2)
                cmds.setAttr(LengthCon + ".operation" , 2)
                cmds.setAttr(LengthCon + ".colorIfFalseR" , 1)
                cmds.setAttr(LengthCon + ".secondTerm" , TotalLength)

                cmds.setAttr(StretchBC + ".color1R" , 1)
                cmds.setAttr(StretchBC + ".color2R" , 1)
                cmds.setAttr(StretchBC + ".blender" , 0)

                #ScalingMD
                cmds.connectAttr(self.stretchNodeDic["scaleDefault"] + ".scaleX" , ScalingMD + ".input2X" , f=1)
                #NormalMD
                cmds.connectAttr(self.stretchNodeDic["distance"]  + ".distance" , NormalMD + ".input1X" , f=1)
                cmds.connectAttr(ScalingMD + ".outputX" , NormalMD + ".input2X" , f=1)
                #LengthCon
                cmds.connectAttr(DistanceNode  + ".distance" , LengthCon + ".firstTerm" , f=1)
                cmds.connectAttr(NormalMD + ".outputX" , LengthCon + ".colorIfTrueR" , f=1)
                #StretchBC
                cmds.connectAttr(LengthCon + ".outColorR" , StretchBC + ".color1R" , f=1)

                if any(value is None for value in self.stretchAttrDic.values()):
                    self.addAttrStretch(Jntlist[0] )

                if all(value is not None for value in self.stretchAttrDic.values()):
                    cmds.setAttr(AttrSR + ".oldMinX" , self.stretchAttrDic["min"])
                    cmds.setAttr(AttrSR + ".oldMaxX" , self.stretchAttrDic["max"])
                    cmds.connectAttr(AttrSR + ".outValueX" , StretchBC + ".blender" ,f =1)
                    cmds.connectAttr("{}.{}".format(self.stretchAttrDic["obj"] , self.stretchAttrDic["attr"])  , AttrSR + ".valueX" , f=1)

                self.stretchNodeDic["scalingMD"] = ScalingMD 
                self.stretchNodeDic["normalMD"] = NormalMD
                self.stretchNodeDic["lengthCon"] = LengthCon
                self.stretchNodeDic["attrSR"] = AttrSR
                self.stretchNodeDic["stretchBC"] = StretchBC
            else:
                raise TypeError(">  Invalid <Jntlist> input. Expected a Existed Joint list")

    def createVolumeNode(self , Name  , inputNode = None , inputAttr = None ):
        '''
        self.volumeNodeDic = {

            "jointList" : None,
            "divMD" : None,
            "powerMD" : None,
            "offsetADL" : None,
            "attrSR" : None , 
            "volumeBC" : None,
            "stretchBC" : None ,
        }
        '''
        string_type = None
        noralizeNode = None 
        noralizeNodeAttr = None
        uniqueName = self.uniqueName(Name)
        try:
            string_type = basestring
        except NameError:
            string_type = str

        
        

        if inputNode is None:
            if self.stretchNodeDic["stretchBC"]  and  cmds.objExists(self.stretchNodeDic["stretchBC"]):
                noralizeNode = self.stretchNodeDic["stretchBC"]
                noralizeNodeAttr ="outputR" 
            else:
                raise ValueError(">  The required node 'stretchBC' is not defined or does not exist in the scene.")
        elif inputNode and cmds.objExists("{}" .format(inputNode)):
            if inputAttr and  isinstance(inputAttr, string_type ) and cmds.objExists("{}.{}" .format(inputNode , inputAttr)):

                noralizeNode = inputNode
                noralizeNodeAttr = inputAttr
            else :
                raise TypeError(">  Invalid <inputAttr> input. Expect a Existed <{}.{}> Attr" .format(inputNode , inputAttr))

        else:
            print (inputNode , inputAttr) 
            raise ValueError(">  The required node 'stretchBC' is not defined or does not exist in the scene.")


        volumeBC = cmds.createNode("blendColors" , n  = Name + "_BC" )
        AttrSR = cmds.createNode("setRange" ,  n = Name + "_SR")
        DivMD = cmds.createNode("multiplyDivide" , n = Name + "_Div_MD")
        PowerMD = cmds.createNode("multiplyDivide" , n = Name + "_Power_MD")
        OffsetADL = cmds.createNode("addDoubleLinear" , n = Name + "_offset_ADL")

        cmds.setAttr(volumeBC + ".color1R" , 1)
        cmds.setAttr(volumeBC+ ".color2R" , 1)

        cmds.setAttr(DivMD + ".operation" , 2)
        cmds.setAttr(PowerMD + ".operation" , 3) #Power

        cmds.setAttr(DivMD + ".input1X" , 1)
        cmds.setAttr(PowerMD + ".input2X" , 0.5)

        cmds.setAttr(AttrSR + ".minX" , 0)
        cmds.setAttr(AttrSR + ".maxX" , 1)

        cmds.connectAttr("{}.{}".format(noralizeNode ,noralizeNodeAttr ) , volumeBC + ".color1R" , f=1)
        cmds.connectAttr(AttrSR + ".outValueX" , volumeBC + ".blender" ,f =1)

        cmds.connectAttr(volumeBC + ".outputR" , DivMD + ".input2X" , f= 1)
        cmds.connectAttr(DivMD + ".outputX" ,PowerMD + ".input1X" , f=1 )
        cmds.connectAttr(PowerMD + ".outputX" , OffsetADL + ".input1" , f=1)

        if any(value is None for value in self.volumeAttrDic.values()):
            self.addAttrVolume(self.Jntlist[0])
        if all(value is not None for value in self.volumeAttrDic.values()):
            cmds.setAttr(AttrSR + ".oldMinX" , self.volumeAttrDic["min"])
            cmds.setAttr(AttrSR + ".oldMaxX" , self.volumeAttrDic["max"])
            cmds.connectAttr("{}.{}" .format(self.volumeAttrDic["obj"]  ,self.volumeAttrDic["attr"] ) ,AttrSR + ".valueX" , f =1 )
            cmds.connectAttr("{}.{}" .format(self.volumeAttrDic["obj"]  ,self.volumeAttrDic["offsetAttr"] ) , OffsetADL + ".input2" ,f =1 )

        self.volumeNodeDic["divMD" ] = DivMD
        self.volumeNodeDic["powerMD"] = PowerMD
        self.volumeNodeDic["offsetADL"] = OffsetADL
        self.volumeNodeDic["attrSR"] = AttrSR
        self.volumeNodeDic["volumeBC"] = volumeBC
        self.volumeNodeDic["stretchBC" ] = noralizeNode


    def connectStrerchToJoint(self , TargetJoint , Axis = None , Length = None ):
        getPlusMinus = 1
        if Axis is None:
            Axis = self.AxisDic["Axis"]
        if not any(Axis == ax for ax in ["X" , "Y" , "Z"]):
            raise TypeError(">  Invalid <Axis> input. Please use one of the valid axes: X, Y, or Z.")
        

        if self.stretchNodeDic["stretchBC"]:
            if cmds.objectType(TargetJoint) == "joint":
                #FindIndex = None
                IsDicNode = TargetJoint in self.resultNodes
                #if IsDicNode:
                #    #FindIndex = next((Num for Num , i in enumerate(self.resultNodes)if i.get("Jnt") == TargetJoint), None ) 
                #    FindIndex = 

                if Length is None or not isinstance(Length , float):
                    ParentJnt = cmds.listRelatives(TargetJoint , p =1 , type = "joint")
                    IsParentDic = None
                    if ParentJnt:
                        IsParentDic =ParentJnt[0] in self.resultNodes
                        if IsParentDic:
                            Length = self.Get_Distance(ParentJnt[0] ,TargetJoint )
                            getTrans = cmds.getAttr(TargetJoint + ".translate{}" .format(self.AxisDic["Axis"]))
                            getPlusMinus = int(getTrans)/int(abs( getTrans))

                        else:
                            raise ValueError("> <TargetJoint> is not in JointChain")
                    else:
                        raise ValueError("> <TargetJoint> is not in JointChain")
                
                if Length and IsDicNode:

                    resultMDL = cmds.createNode("multDoubleLinear" , n =  "{}_result_MDL".format(TargetJoint ))
                    self.resultNodes[TargetJoint]["MDL"] = resultMDL

                    #pprint.pprint(self.resultNodes)
                    cmds.setAttr(self.resultNodes[TargetJoint]["MDL"] + ".input2" , Length * getPlusMinus)

                    cmds.connectAttr(self.stretchNodeDic["stretchBC"] + ".outputR" , self.resultNodes[TargetJoint]["MDL"] + ".input1" ,f =1 )
                    cmds.connectAttr(self.resultNodes[TargetJoint]["MDL"] + ".output" , TargetJoint + ".translate{}" .format( Axis) , f=1 )

            else:
                raise TypeError("> Invalid <TargetJoint > input. Expected a Existed Joint")
        else:
            raise ValueError("> Not existed a 'stretchBlend Node'." )

    def connectVolumeToJoint(self , TargetJoint , AxisList = None ):
        try:
            string_type = basestring
        except NameError:
            string_type = str

        if AxisList is None:
            AxisList = self.AxisOtherDic["Axis"]
        if not isinstance(AxisList ,  (list, tuple) ): 
            raise TypeError(">  Invalid <AxisList> input. Expected a List or Tuple ")
        
        MatchCount = sum( 1 for item in AxisList if item in ["X" , "Y" , "Z"])
        if not MatchCount ==2:
            raise ValueError(">   Invalid <AxisList> input. Expected exactly 2 elements from ['X', 'Y', 'Z']")
        
        if not cmds.objectType(TargetJoint) == "joint":
            raise TypeError("> Invalid <TargetJoint > input. Expected a Existed Joint")
        
        if self.volumeNodeDic["offsetADL"] and self.volumeAttrDic["attr"] and self.volumeAttrDic["offsetAttr"]:

            IsDicNode = TargetJoint in self.resultNodes
            if IsDicNode:

                for ax in AxisList:
                    cmds.connectAttr(self.volumeNodeDic["offsetADL"] + ".output" , TargetJoint + ".scale{}" .format(ax) , f=1)
                self.resultNodes[TargetJoint]["ADL"] = self.volumeNodeDic["offsetADL"]
        else:
            raise ValueError("> Not existed a 'volumeBlend Node'." )

    def connectPoleVectorStretchToNode(self, TargetJnt , DistanceNode  , Length = None ):
        try:
            string_type = basestring
        except NameError:
            string_type = str

        #JntLength = None

        if not cmds.objectType(TargetJnt) == "joint":
            raise TypeError(">  Invalid <TargetJnt> input. Expected a Existed Joint list")
        if not TargetJnt in self.resultNodes or not self.poleVectorStretchNodes[TargetJnt]:
            raise TypeError(">  Invalid <TargetJnt > input. Could not Found <TargetJnt> in <self.resultNodes.>")
        
        if not cmds.objectType(DistanceNode) == "distanceDimShape" or cmds.objectType(DistanceNode) == "distanceBetween":
            raise TypeError("> Invalid <DistanceNode> input. Expected a DistanceNode  Shape")
        
        if not self.ScaleDefault:
            raise ValueError("> The required node <self.ScaleDefault>")
        

        
        if Length is None or not isinstance(Length , float):
            ParentJnt = cmds.listRelatives(TargetJnt , p =1 , type = "joint")
            IsParentDic = None
            if ParentJnt:
                IsParentDic =ParentJnt[0] in self.resultNodes
                if IsParentDic:
                    Length = self.Get_Distance(ParentJnt[0] ,TargetJnt )
                else:
                    raise ValueError("> <TargetJoint> is not in JointChain")
            else:
                raise ValueError("> <TargetJoint> is not in JointChain")
            
            
        
        cmds.setAttr(self.poleVectorStretchNodes[TargetJnt]["scalingMD"] + ".input1X" , Length)
        cmds.connectAttr(self.ScaleDefault + ".scaleX" , self.poleVectorStretchNodes[TargetJnt]["scalingMD"] + ".input2X" ,f=1)
        cmds.connectAttr(DistanceNode  + ".distance" , self.poleVectorStretchNodes[TargetJnt]["divMD"]+ ".input1X" ,f=1)

        
        #if self.poleVectorStretchNodes[TargetJnt]["MDL"]:
        sourceAttr = "{}.{}" .format(self.poleVectorStretchNodes[TargetJnt]["stretchBC"] ,self.poleVectorStretchNodes[TargetJnt]["stretchBC_Attr"] )
        destinationAttr = "{}.{}" .format(self.poleVectorStretchNodes[TargetJnt]["MDL"] , self.poleVectorStretchNodes[TargetJnt]["MDL_Attr" ])
        poleVectorBlend = self.poleVectorStretchNodes[TargetJnt]["poleStretchBC"]
        jointMDL = self.poleVectorStretchNodes[TargetJnt]["MDL"]

        IsCntAttr = cmds.listConnections(destinationAttr ,s =1 , plugs=1 )


        cmds.disconnectAttr(sourceAttr , destinationAttr)
        cmds.connectAttr(poleVectorBlend + ".outputR" ,  self.poleVectorStretchNodes[TargetJnt]["MDL"] + ".input1" ,f=1)


        


    def createPoleVector(self , Name , posData , IkHandle  , annotationRoot = None ):
        pos = None
        poleLoc = None
        poleLocShape = None
        annotation = None
        annotationShape = None

        try:
            string_type = basestring
        except NameError:
            string_type = str

        uniqueName = self.uniqueName(Name)


        if isinstance(posData  , list) or isinstance(posData  , tuple):
            if len(posData ) > 2:
                pos = posData
            else:
                raise IndexError("> Invalid <posData> input. Expected <posData> to have at least 3 items ")
        elif isinstance(posData ,  string_type) and cmds.objExists(posData ):
            pos = cmds.xform(posData , q =1 , ws =1 , t =1)[:3]

        else:
            raise TypeError("> Invalid <posData> input. Expected a valid list, tuple, or an existing obj ")
            
        if pos:
            preLoc = self.CreateOrGet_Loc(pos  , uniqueName )
            poleLoc = preLoc[0]
            poleLocShape = preLoc[-1]

            self.poleVectorDic["obj"] = poleLoc
            self.poleVectorDic["shape"] = poleLocShape

        if cmds.objExists(annotationRoot):
            annotationShape = cmds.createNode("annotationShape" , n = uniqueName + "_ANTShape")
            parentAnnotation = cmds.listRelatives( annotationShape , p =1 , type = "transform")[0]
            annotation = cmds.rename(parentAnnotation , uniqueName + "_ANT")

            cmds.pointConstraint(annotationRoot , annotation , mo= 0)

            self.poleVectorDic["annotation"] = annotation
            self.poleVectorDic["annotationShape"] = annotationShape

        if poleLocShape and annotationShape:
            cmds.connectAttr("{}.worldMatrix[0]" .format(poleLocShape) , "{}.dagObjectMatrix[0]".format(annotationShape) ,f=1)

        if isinstance(IkHandle , string_type) and cmds.objectType(IkHandle) == "ikHandle" and poleLoc  :
            cmds.poleVectorConstraint(poleLoc  ,IkHandle )
            self.poleVectorDic["ik" ] = IkHandle

        else:
            raise TypeError("> Invalid <IkHandle> input. Expected a 'ikHandle'")






        








                            






            
            







                



        





                
            
                
                




            




select = cmds.ls(sl =1)

a = Ikrig(select) 
a.setIKHandle("Test", a.Jntlist[0] , a.Jntlist[2] , 1)
a.setScaleDefault()
a.setAxis("Z")
pprint.pprint(a.Jntlist)

Pos = a.getPoleVectorPosData(select[0],select[1] ,select[2])

a.createPoleVector("poleVector" , Pos , a.CurrentIK , a.Jntlist[1])
a.addAttrStretch(a.Jntlist[0] , "Stretch")
a.addAttrVolume(a.Jntlist[0] , "Volume")
a.addAttrPoleVectorStretch(a.Jntlist[0] , "PoleVectorStretch")
a.setDistance( a.Jntlist[0] , a.Jntlist[2])

a.createStretchNode("Stretch" , a.Jntlist[:3], a.CurrentDistanceNode)
a.createVolumeNode("Volume" , a.stretchNodeDic["stretchBC"] ,  "outputR"  )

a.connectStrerchToJoint(a.Jntlist[1])
a.connectStrerchToJoint(a.Jntlist[2])
a.setSlide(a.Jntlist[1] , a.Jntlist[0]  , "Slide_1")
a.setSlide(a.Jntlist[2] , a.Jntlist[0]  , "Slide_2")
a.connectVolumeToJoint(a.Jntlist[1])
a.createPoleVectorStretchNode(a.Jntlist[1] )
a.createPoleVectorStretchNode(a.Jntlist[2] )
a.setDistance(a.Jntlist[0] , a.poleVectorDic["obj"] , [a.Jntlist[0] + "Pole" ,a.poleVectorDic["obj"]+"Pole" , a.poleVectorDic["obj"]+ a.Jntlist[0]])
PoleStartDT = a.CurrentDistanceNode
a.setDistance(a.Jntlist[2] , a.poleVectorDic["obj"], [a.Jntlist[2] + "Pole" ,a.poleVectorDic["obj"]+"Pole" , a.poleVectorDic["obj"]+ a.Jntlist[2] ])
PoleEndDT = a.CurrentDistanceNode
a.connectPoleVectorStretchToNode(a.Jntlist[1] , PoleStartDT)
a.connectPoleVectorStretchToNode(a.Jntlist[2] , PoleEndDT)



#a.setVolume("Volume" , a.Jntlist[:3]) 