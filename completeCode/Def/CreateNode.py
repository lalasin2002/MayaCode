# -*- coding: utf-8 -*-
import maya.cmds as cmds


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