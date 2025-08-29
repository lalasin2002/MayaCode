# -*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
from collections import OrderedDict
import re

def uniqueName(Name , maxLoop = 100 ):
    """
    Maya 씬 내에서 고유한 이름을 생성합니다.

    주어진 이름을 기반으로, 이미 존재하는 경우 숫자 접미사를 붙여
    중복되지 않는 새 이름을 찾아 반환합니다.

    Args:
        Name (str): 기본으로 사용할 이름 문자열.
        maxLoop (int, optional): 고유 이름을 찾기 위해 시도할 최대 반복 횟수. 기본값은 100.

    Returns:
        str: Maya 씬 내에서 고유성이 보장된 이름.
    """
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


def Create_Node(name, nodeTyp='transform'):
    """
    지정된 이름과 타입으로 Maya 노드를 생성합니다.

    Args:
        name (str): 생성할 노드의 이름.
        nodeTyp (str, optional): 생성할 노드의 타입. 기본값은 'transform'.

    Returns:
        str: 생성된 노드의 이름.
    """
    node = cmds.createNode(nodeTyp, n=name)
    return node


def Create_BlendcolorNode(Name):
    """
    'blendColors' 노드를 생성하고, 초기 color1 및 color2 속성의 R, G, B 값을 0으로 설정합니다.

    Args:
        Name (str): 생성할 'blendColors' 노드의 이름.

    Returns:
        str: 생성된 'blendColors' 노드의 이름.
    """
    node = cmds.createNode('blendColors', n=Name)
    for x in "RGB":
        cmds.setAttr("{}.color1{}".format(node, x), 0)
        cmds.setAttr("{}.color2{}".format(node, x), 0)
    return node


def Create_SetrangeNode(Name):
    """
    'setRange' 노드를 생성합니다.

    Args:
        Name (str): 생성할 'setRange' 노드의 이름.

    Returns:
        str: 생성된 'setRange' 노드의 이름.
    """
    node = cmds.createNode('setRange', n=Name)
    return node


def Create_MdNode(Name, operation=1):
    """
    'multiplyDivide' 노드를 생성하고, 지정된 연산으로 설정합니다.

    Args:
        Name (str): 생성할 'multiplyDivide' 노드의 이름.
        operation (int, optional): 노드의 연산 타입 (1: 곱하기, 2: 나누기, 3: 거듭제곱). 기본값은 1 (곱하기).

    Returns:
        str: 생성된 'multiplyDivide' 노드의 이름.
    """
    node = cmds.createNode('multiplyDivide', n=Name)
    cmds.setAttr("{}.operation".format(node), operation)
    return node


def Create_MdlNode(Name, Input_Value=0):
    """
    'multDoubleLinear' 노드를 생성하고, input2 속성에 초기 값을 설정합니다.

    Args:
        Name (str): 생성할 'multDoubleLinear' 노드의 이름.
        Input_Value (float, optional): 'input2' 속성에 설정할 초기 값. 기본값은 0.

    Returns:
        str: 생성된 'multDoubleLinear' 노드의 이름.
    """
    node = cmds.createNode('multDoubleLinear', n=Name)
    cmds.setAttr("{}.input2".format(node), Input_Value)
    return node


def Create_AdlNode(Name, Input_Value=0):
    """
    'addDoubleLinear' 노드를 생성하고, input2 속성에 초기 값을 설정합니다.

    Args:
        Name (str): 생성할 'addDoubleLinear' 노드의 이름.
        Input_Value (float, optional): 'input2' 속성에 설정할 초기 값. 기본값은 0.

    Returns:
        str: 생성된 'addDoubleLinear' 노드의 이름.
    """
    node = cmds.createNode('addDoubleLinear', n=Name)
    cmds.setAttr("{}.input2".format(node), Input_Value)
    return node


def Create_DmNode(Name, Target, input='inputMatrix'):
    """
    'decomposeMatrix' 노드를 생성하고, 대상 오브젝트의 worldMatrix를 연결합니다.

    Args:
        Name (str): 생성할 'decomposeMatrix' 노드의 이름.
        Target (str): worldMatrix를 연결할 대상 오브젝트의 이름.
        input (str, optional): 'decomposeMatrix' 노드의 입력 매트릭스 속성 이름. 기본값은 'inputMatrix'.

    Returns:
        str: 생성된 'decomposeMatrix' 노드의 이름.
    """
    node = cmds.createNode('decomposeMatrix', n=Name)
    cmds.connectAttr("{}.worldMatrix".format(Target), "{}.{}".format(node, input))
    return node


def Create_ConditionNode(Name, operation=0):
    """
    'condition' 노드를 생성하고, 지정된 연산으로 설정합니다.

    Args:
        Name (str): 생성할 'condition' 노드의 이름.
        operation (int, optional): 노드의 연산 타입. 기본값은 0 (사용자 정의에 따라 달라짐).

    Returns:
        str: 생성된 'condition' 노드의 이름.
    """
    node = cmds.createNode('condition', n=Name)
    cmds.setAttr("{}.operation".format(node), operation)
    return node


def Create_CrvinfoNode(Name, Crv=None):
    """
    'curveInfo' 노드를 생성하고, 선택적으로 주어진 커브에 연결합니다.

    Args:
        Name (str): 생성할 'curveInfo' 노드의 이름.
        Crv (str, optional): 연결할 커브의 이름. None이면 연결하지 않습니다.

    Returns:
        str: 생성된 'curveInfo' 노드의 이름.
    """
    node = cmds.createNode('curveInfo', n=Name)
    if Crv:
        Shp = Crv
        if not cmds.objectType(Crv) == "nurbsCurve":
            Shp = cmds.listRelatives(Crv, s=1)[0]
        cmds.connectAttr("{}.worldSpace[0]".format(Shp), "{}.inputCurve".format(node), f=1)
    return node


def Create_PocifNode(Name, CrvName="", Parameter=0, TurnOnPercentage=True):
    """
    'pointOnCurveInfo' 노드를 생성하고, 매개변수 및 백분율 모드를 설정합니다.
    선택적으로 주어진 커브에 연결합니다.

    Args:
        Name (str): 생성할 'pointOnCurveInfo' 노드의 이름.
        CrvName (str, optional): 연결할 커브의 이름. 비어 있으면 연결하지 않습니다.
        Parameter (float, optional): 'parameter' 속성에 설정할 값. 기본값은 0.
        TurnOnPercentage (bool, optional): 'turnOnPercentage' 속성을 활성화할지 여부. 기본값은 True.

    Returns:
        str: 생성된 'pointOnCurveInfo' 노드의 이름.
    """
    POCIF = cmds.createNode('pointOnCurveInfo', n=Name)
    cmds.setAttr("{}.turnOnPercentage".format(POCIF), TurnOnPercentage)
    cmds.setAttr("{}.parameter".format(POCIF), Parameter)

    if cmds.objExists(CrvName):
        cmds.connectAttr("{}.worldSpace[0]".format(CrvName), "{}.inputCurve".format(POCIF), f=1)

    return POCIF


def Create_NpocNode(Name, CrvName="", inPositionTGT="", inPositionAttrName="translate"):
    """
    'nearestPointOnCurve' 노드를 생성하고, 선택적으로 커브와 입력 위치 타겟에 연결합니다.

    Args:
        Name (str): 생성할 'nearestPointOnCurve' 노드의 이름.
        CrvName (str, optional): 연결할 커브의 이름. 비어 있으면 연결하지 않습니다.
        inPositionTGT (str, optional): 'inPosition'에 연결할 타겟 오브젝트의 이름. 비어 있으면 연결하지 않습니다.
        inPositionAttrName (str, optional): 'inPosition'에 연결할 타겟 오브젝트의 속성 이름. 기본값은 'translate'.

    Returns:
        str: 생성된 'nearestPointOnCurve' 노드의 이름.
    """
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
    """
    Maya 로케이터를 생성하고, 스케일을 설정하며, 반환 타입을 제어합니다.

    Args:
        Name (str): 생성할 로케이터의 이름.
        ShpScale (float, optional): 로케이터 셰이프의 로컬 스케일. 기본값은 1.
        NolistBool (bool, optional): True이면 로케이터 트랜스폼 노드만 반환하고, False이면 트랜스폼 노드와 셰이프 노드를 리스트로 반환합니다. 기본값은 True.

    Returns:
        str or list: NolistBool 값에 따라 로케이터 트랜스폼 노드 이름 또는 [트랜스폼 노드 이름, 셰이프 노드 이름] 리스트.
    """
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
    """
    Maya 조인트를 생성하고, 선택적으로 대상 오브젝트의 위치에 맞춥니다.

    Args:
        Name (str): 생성할 조인트의 이름.
        CP_Target (str, optional): 조인트를 위치시킬 대상 오브젝트의 이름. None이면 위치 맞춤을 수행하지 않습니다.

    Returns:
        str: 생성된 조인트의 이름.
    """
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
    """
    NURBS 커브를 생성하고, 주어진 위치 목록과 차수를 사용하여 재구축합니다.

    Args:
        Name (str): 생성할 커브의 이름.
        Poslist (list): 커브를 정의할 [x, y, z] 좌표 리스트.
        degree (int, optional): 커브의 차수. 기본값은 1 (선형).

    Returns:
        str: 재구축된 커브의 이름.
    """
    Crv = cmds.curve(n = Name , p = Poslist , d= 1)
    reCrv = cmds.rebuildCurve(Crv , ch =1  , rpo =1 , rt = 0 , end = 1 , kr = 0, kcp = 0 , kep =1 , kt =0 , s= len(Poslist) ,d =degree )
    Shp = cmds.listRelatives(Crv , s= 1)
    ReName = cmds.rename("{}Shape" .format(Name) , Shp[0] )
    return reCrv


def Create_ANT(Name , CP_Target = None , Cnt_Target  = None , NonSelect = True ):
    """
    Maya 주석 노드를 생성하고, 선택적으로 위치 제약 조건 및 매트릭스 연결을 설정합니다.
    주석의 선택 가능 여부를 제어합니다.

    Args:
        Name (str): 생성할 주석 노드의 이름.
        CP_Target (str, optional): 주석 노드를 제약할 대상 오브젝트의 이름 (pointConstraint). None이면 제약하지 않습니다.
        Cnt_Target (str, optional): 주석 노드의 dagObjectMatrix에 연결할 대상 오브젝트의 이름. None이면 연결하지 않습니다.
        NonSelect (bool, optional): 주석을 선택할 수 없게 할지 여부. True이면 선택 불가, False이면 선택 가능. 기본값은 True.

    Returns:
        list: [주석 트랜스폼 노드 이름, 주석 셰이프 노드 이름] 리스트.
    """
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
    """
    주어진 텍스트 문자열을 기반으로 Maya 텍스트 커브를 생성합니다.
    선택적으로 피벗을 중앙으로 이동하고, 글꼴 크기 및 글꼴을 설정합니다.

    Args:
        Name (str): 생성할 텍스트 커브의 이름.
        TextString (str): 커브로 변환할 텍스트 문자열.
        CenterPivotBool (bool, optional): 생성된 텍스트 커브의 피벗을 중앙으로 이동할지 여부. 기본값은 True.
        FontSizePt (float, optional): 텍스트의 글꼴 크기 (포인트). 기본값은 27.8.
        Font (str, optional): 사용할 글꼴 이름. 기본값은 "Lucida Sans Unicode".

    Returns:
        str: 생성된 텍스트 커브의 이름.
    """
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


def CreateOrGet_Loc(obj_or_pos , Name  = "locator" , MaxWhileCount =100): #2025-06-13 추가
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




def Create_Distance(startObj_or_pos , endObj_or_pos , Names = ["startlocator" , "endlocator"  , "Distance"] ):
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

    startLocs = CreateOrGet_Loc(startObj_or_pos , Names[0])
    endLocs = CreateOrGet_Loc(endObj_or_pos , Names[1])

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
        DistanceShp = cmds.createNode("distanceDimShape" , n = DistanceName )
        Distance = cmds.listRelatives(DistanceShp , p =1 , type= "transform")
        Distance = cmds.rename(Distance[0] , '{}{}' .format(Names[2]  , "" if DistanceCount == 0 else DistanceCount))

        cmds.connectAttr(startLocShape + ".worldPosition[0]" , DistanceShp + ".startPoint" ,f =1)
        cmds.connectAttr(endLocShape + ".worldPosition[0]" , DistanceShp + ".endPoint" ,f =1)

        returnDic = {
            "startLoc" : startLoc ,
            "endLoc" : endLoc ,
            "startLoc_shape" : startLocShape ,
            "endLoc_shape" : endLocShape ,
            "distance_node" : DistanceShape ,
            "distance_transform" : Distance
        }

    return returnDic

def Create_CurveFromMeshEdge(Edge , Name = "" ): #2025-06-13 추가
    """
    선택한 메쉬의 특정 엣지(Edge)로부터 커브를 생성하는 유틸리티 노드를 만듭니다.

    Args:
        Edge (str): 'pCube1.e[100]'과 같은 엣지 컴포넌트 이름.
        Name (str, optional): 생성될 'curveFromMeshEdge' 노드의 이름. 지정하지 않으면
                              오브젝트 이름을 기반으로 자동 생성됩니다.

    Returns:
        str: 성공적으로 생성된 'curveFromMeshEdge' 노드의 이름.
    """

    string_type = None
    try:
        string_type = basestring
    except NameError:
        string_type = str

    IntPattern = r"\[(\d+)\]"
    Geo = None
    EdgeIndex = None
    NodeName = None
    IsEdge = cmds.filterExpand(Edge , selectionMask= 32 , expand= 1) 
    if not isinstance(Edge ,string_type) and IsEdge:
        raise TypeError(">> Invalid input: 'Edge' must be a meshEdge.")
    Geo = cmds.ls(Edge , objectsOnly=1)[0]
    Search = re.search(IntPattern , IsEdge[0])
    if Search:
        Match = Search.group(1)
        EdgeIndex = int(Match)
    
    if Name == "":
        Name = "{}_CFME" .format(Geo)  #Geo + "_CFME"
    Count = 0 
    while True:
        NodeName = "{}{}" .format(Name , "" if Count== 0 else Count)
        if not cmds.objExists(NodeName):
            break
        Count += 1
    
    Node = cmds.createNode("curveFromMeshEdge" , n = NodeName)
    cmds.setAttr(Node + ".edgeIndex[0]" , EdgeIndex)
    cmds.connectAttr(Geo + ".worldMesh[0]" , Node + ".inputMesh" ,f=1)

    return Node


def Create_Pocif_FromMeshEdge(Edge, Parameter =0.5, Names = ["curveFromMeshEdge" , "pointOnCurveInfo" , ""] ):
    """
    메쉬의 특정 엣지(Edge) 위 한 지점의 정보를 읽는 노드 네트워크를 생성합니다.

    이 함수는 먼저 'Create_CurveFromMeshEdge'를 호출하여 엣지로부터 동적인 커브를
    생성합니다. 그 다음, 'pointOnCurveInfo' 노드를 만들어 해당 커브 위의 특정 지점
    (Parameter)에 대한 위치 정보를 실시간으로 읽어옵니다.
    선택적으로, 이 위치에 로케이터를 생성하고 연결하여 시각적으로 표시할 수 있습니다.

    Args:
        Edge (str): 
            정보를 읽어올 기준이 되는 엣지 컴포넌트 이름. (예: 'pCube1.e[100]')
        
        Parameter (float, optional): 
            엣지 위의 위치를 나타내는 값. 0.0은 엣지의 시작점, 1.0은 끝점을 의미합니다.
            기본값은 0.5 (중간 지점)입니다.
            
        Names (list, optional): 
            생성될 유틸리티 노드들의 기본 이름 리스트.
            [0]: 'curveFromMeshEdge' 노드 이름
            [1]: 'pointOnCurveInfo' 노드 이름 순서입니다.
            [2]: 생성될 로케이터 이름 ""경우 생성되지않음
            

    Returns:
        dict: 
            생성된 모든 주요 노드들의 이름을 담은 딕셔너리.
            
            {
                "pocif": (str) 생성된 pointOnCurveInfo 노드,\n
                "cfme": (str) 생성된 curveFromMeshEdge 노드,\n
                "locator": (str or None) 생성된 로케이터의 트랜스폼 노드,\n
                "locator_shape": (str or None) 생성된 로케이터의 쉐잎 노드\n
            }
    """
    returnDic = {}
    Loc = None
    LocShape = None
    CFME = Create_CurveFromMeshEdge(Edge , Names[0])
    PocifName = uniqueName(Names[1])
    Pocif = cmds.createNode("pointOnCurveInfo" , n = PocifName)
    cmds.setAttr(Pocif + ".turnOnPercentage" ,1)
    cmds.setAttr(Pocif + ".parameter", Parameter)
    cmds.connectAttr(CFME + ".outputCurve" , Pocif + ".inputCurve" , f=1)

    if not Names[2] == "":
        LocName = uniqueName(Names[2])
        Loc = cmds.spaceLocator( n = LocName)[0]
        LocShape = cmds.listRelatives(Loc , s =1)[0]

        for x in "XYZ":
            cmds.connectAttr(Pocif + ".position{}" .format(x) , Loc + ".translate{}" .format(x) , f =1)

    returnDic = {
        "pocif" : Pocif,
        "cfme" : CFME,
        "locator" : Loc,
        "locator_shape" : LocShape
    }

    return returnDic

def Create_PointOnSurface_FromMeshEdge(startEdge , endEdge  , Names = ["start_curveFromMeshEdge" , "end_curveFromMeshEdge" , "startEnd_loft" , "startEnd_surFace"] ):
    """
    두 메쉬 엣지(startEdge, endEdge)를 기반으로 Loft(로프트)된 서피스를 생성하고,
    해당 서피스 위의 특정 지점 정보를 읽는 노드 네트워크를 구성합니다.

    이 함수는 두 엣지로부터 각각 동적인 커브를 생성한 뒤, 이 커브들을 로프트하여
    하나의 서피스를 만듭니다. 그 다음, 'pointOnSurfaceInfo' 노드를 생성하여
    서피스 위의 특정 파라미터(기본값: U=0.5, V=0.5)에 대한 정보를 실시간으로
    읽어올 수 있도록 설정합니다.

    Args:
        startEdge (str): 로프트의 시작 커브가 될 엣지 컴포넌트 이름.
                         (예: 'pCube1.e[100]')
        endEdge (str): 로프트의 끝 커브가 될 엣지 컴포넌트 이름.
                       (예: 'pCube1.e[102]')
        Names (list, optional):
            생성될 유틸리티 노드들의 기본 이름 리스트.
            [0]: 시작 엣지용 'curveFromMeshEdge' 노드 이름
            [1]: 끝 엣지용 'curveFromMeshEdge' 노드 이름
            [2]: 'loft' 노드 이름
            [3]: 'pointOnSurfaceInfo' 노드 이름

    Returns:
        dict:
            생성된 모든 주요 노드들의 이름을 담은 딕셔너리.
            {
                "start_cfme": (str) 시작 엣지로부터 생성된 curveFromMeshEdge 노드,
                "end_cfme": (str) 끝 엣지로부터 생성된 curveFromMeshEdge 노드,
                "loft": (str) 생성된 loft 노드,
                "posif": (str) 생성된 pointOnSurfaceInfo 노드
            }
    """
    startCFME = Create_CurveFromMeshEdge(startEdge,  Names[0] )
    endCFME = Create_CurveFromMeshEdge(endEdge, Names[1] )
    LoftName = uniqueName(Names[2])
    SurFaceName = None
    SurFaceInfo = None
    returnDic = {}

    Loft = cmds.createNode("loft", n = LoftName)
    cmds.connectAttr( "{}.outputCurve" .format(startCFME ) , "{}.inputCurve[0]" .format(Loft), f=1)
    cmds.connectAttr( "{}.outputCurve" .format(endCFME ) , "{}.inputCurve[1]" .format(Loft),f=1)
    if not Names == "":
        SurFaceName = uniqueName(Names[3])
        SurFaceInfo = cmds.createNode("pointOnSurfaceInfo" , n = SurFaceName)
        cmds.setAttr("{}.turnOnPercentage" .format(SurFaceInfo), 1)
        for x in "UV":
            cmds.setAttr(SurFaceInfo + ".parameter{}" .format(x) , 0.5)
        cmds.connectAttr("{}.outputSurface" .format(Loft), "{}.inputSurface" .format(SurFaceInfo) ,f =1 )


    returnDic = {
        "start_cfme" : startCFME,
        "end_cfme" : endCFME,
        "loft" : Loft,
        "posif" : SurFaceInfo
    }
    return returnDic


def d_MeshHardEdge_Ctrl(MeshItem , Name , size =1 , Position = False):
    """
    주어진 메쉬(MeshItem)의 하드 엣지(Hard Edge)를 감지하여,
    해당 엣지들의 형태를 따라 커브 컨트롤러를 생성합니다.

    이 함수는 먼저 메쉬에서 모든 하드 엣지를 찾습니다. 그 다음, 각 하드 엣지를
    별도의 커브로 변환하고, 이 커브들을 하나의 그룹(컨트롤러)으로 묶습니다.
    생성된 컨트롤러의 크기와 위치를 조절할 수 있습니다.

    Args:
        MeshItem (str): 컨트롤러를 생성할 대상 메쉬의 이름.
        Name (str): 생성될 컨트롤러(그룹)의 이름.
        size (float, optional): 컨트롤러의 전체적인 크기. 기본값은 1.
        Position (bool, optional):
            True이면 컨트롤러의 위치와 회전값을 대상 메쉬와 일치시킵니다.
            False이면 월드 원점(0,0,0)에 생성됩니다. 기본값은 False.

    Returns:
        str: 생성된 컨트롤러(그룹)의 이름.
    """
    ReturnItem = None
    
    if cmds.objectType(MeshItem) == "transform" or cmds.objectType(MeshItem)  == "mesh":
        cmds.select(MeshItem)
        cmds.polySelectConstraint( m =3 ,t = 0x8000  ,sm =1)
        HardEdges = cmds.ls(sl =1,fl =1)
        
        Ctrl = cmds.createNode("transform" , n = Name)
        PosT = [0,0,0]
        PosR = [0,0,0]
        if Position:
            CP = cmds.parentConstraint(MeshItem , Ctrl, mo =0)
            PosT = cmds.xform(Ctrl , q =1, ws =1 , t =1)
            PosR = cmds.xform(Ctrl , q =1, ws =1 , ro =1)
            PosT = [-1 * x for x in PosT]
            cmds.delete(CP)
        
        for i, x in enumerate(HardEdges):
            cmds.select(x)
            Crv = cmds.polyToCurve(degree =1, form=2)
            cmds.xform(Crv , ws =1, t = PosT)
            cmds.xform(Crv , ws =1, ro = PosR)
            #cmds.makeIdentity(Crv , a =1,t =1)
            
            
            Shp = cmds.listRelatives(Crv , s =1 )[0]
            if Position:
                Cv = cmds.ls(Shp + ".cv[*]" ,fl =1)
                print (Cv)
                cmds.select(Cv ,r =1)
                
                cmds.move( PosT[0],PosT[1] , PosT[2] , r =1)
            ReNameShp = cmds.rename(Shp ,"{}{}Shape" .format(Name , i+1))
            cmds.parent(ReNameShp , Ctrl ,r =1, s=1)
            cmds.delete( Crv  )

        cmds.scale(size , size , size , Ctrl)
        cmds.makeIdentity(Ctrl , a =1 , s =1, pn =1)
        ReturnItem = Ctrl
    
    return Ctrl


def Create_Foli(Name , Geo = None , ParameterUV = (0.5 , 0.5)): #2025
    """
    지오메트리(메쉬 또는 NURBS 서피스)에 부착되는 폴리클(Follicle) 노드를 생성합니다.

    이 함수는 지정된 UV 좌표에 폴리클을 생성하고, 이를 대상 지오메트리에 연결하여
    지오메트리가 변형될 때 폴리클이 표면을 따라 움직이도록 합니다.
    폴리클은 주로 헤어, 리깅, 오브젝트 부착 등에 사용됩니다.

    Args:
        Name (str): 생성될 폴리클의 기본 이름.
        Geo (str, optional): 폴리클을 부착할 대상 지오메트리(메쉬 또는 NURBS 서피스)의 이름.
                             None이면 연결 없이 폴리클만 생성됩니다. 기본값은 None.
        ParameterUV (tuple or list, optional):
            폴리클이 위치할 서피스의 UV 좌표. (U, V) 형식으로 제공합니다.
            값의 범위는 일반적으로 0.0에서 1.0 사이입니다. 기본값은 (0.5, 0.5) (중앙).

    Returns:
        list: [폴리클 트랜스폼 노드 이름, 폴리클 쉐잎 노드 이름] 리스트.
    """
    FoliShp = cmds.createNode( "follicle", n = Name + "Shape" )
    FoliTransForm = cmds.listRelatives(FoliShp , p = 1 , type= "transform")[0]
    FoliTransForm = cmds.rename(FoliTransForm, Name)
    returnList = [FoliTransForm ,  FoliShp]

    cmds.connectAttr("{}.outTranslate" .format(FoliShp) , "{}.translate".format(FoliTransForm) , f=1)
    cmds.connectAttr("{}.outRotate" .format(FoliShp) , "{}.rotate".format(FoliTransForm) , f=1)
    Shp = None
    OutputAttr = ".outMesh"
    InputAttr = ".inputMesh"

    # 지오메트리가 제공되었는지 확인
    if Geo and cmds.objExists(Geo):
        # 입력된 지오메트리의 쉐잎 노드를 찾음
        if cmds.objectType(Geo) == "transform":
            Shp = cmds.listRelatives(Geo , s =1 )[0]
        else:
            Shp = Geo # 이미 쉐잎 노드일 경우
        
        # 지오메트리 타입에 따라 연결할 속성을 결정 (NURBS 또는 메쉬)
        if cmds.objectType(Shp) == "nurbsSurface":
            OutputAttr = ".local"
            InputAttr = ".inputSurface"
        
        # 지오메트리의 아웃풋과 월드 매트릭스를 폴리클에 연결
        cmds.connectAttr("{}{}" .format(Geo , OutputAttr) , "{}{}" .format(FoliShp , InputAttr) ,f =1)
        cmds.connectAttr("{}.worldMatrix[0]" .format(Geo ) , "{}.inputWorldMatrix" .format(FoliShp ) ,f =1)
        
    # 파라미터 UV 값 설정
    for  i, Axis in enumerate("UV"):
        cmds.setAttr("{}.parameter{}" .format(FoliShp , Axis) , ParameterUV[i])
        
    return returnList
