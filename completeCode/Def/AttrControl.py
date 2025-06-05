import maya.cmds as cmds
import maya.api.OpenMaya as om # Maya API 2.0 사용
import math


def SetAttr_HideLockVectorAttr(item, lock=True, TurnOnKeyable= False):
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

def SetAttr_ObjectsVis(Type, Turn_Bool=False):
    All = cmds.ls(type=Type)
    for x in All:
        cmds.setAttr(x + '.visibility', Turn_Bool)


def Get_JntRotateOrder(Jnt):
    """
    조인트의 'rotateOrder' 속성 값(정수)을 maya.api.OpenMaya.MEulerRotation.RotationOrder 열거형으로 변환.
    """
    ro_attr_val = cmds.getAttr(Jnt + ".rotateOrder")
    # Maya 'rotateOrder' 속성 값과 MEulerRotation.RotationOrder 매핑:
    # 0: kXYZ, 1: kYZX, 2: kZXY, 3: kXZY, 4: kYXZ, 5: kZYX
    mapping = [
        om.MEulerRotation.kXYZ, om.MEulerRotation.kYZX, om.MEulerRotation.kZXY,
        om.MEulerRotation.kXZY, om.MEulerRotation.kYXZ, om.MEulerRotation.kZYX
    ]
    if 0 <= ro_attr_val < len(mapping):
        return mapping[ro_attr_val]
    




def SetAttr_CleanJntOrient_Matrix(Joint):
    """
    매트릭스 연산을 사용하여 조인트의 rotate 값을 jointOrient로 옮기고 rotate를 0으로 설정합니다.
    조인트의 최종 월드 공간 방향을 유지합니다.
    """
    JntRotateOrder = None

    # jointOrient 값을 가져와서 매트릭스로 변환
    # jointOrient 값 (Deg 단위)
    JntOrient_Deg = cmds.getAttr("{}.jointOrient".format(Joint))[0]  # (jointOrientX, jointOrientY, jointOrientZ)
    
    # MEulerRotation 객체 생성 (jointOrient, XYZ 회전 순서 사용)
    JntOrientEuler = om.MEulerRotation(
        math.radians(JntOrient_Deg[0]),
        math.radians(JntOrient_Deg[1]),
        math.radians(JntOrient_Deg[2]),
        om.MEulerRotation.kXYZ  # jointOrient는 고정적으로 XYZ 순서로 간주
    )
    JntOrientMatrix = JntOrientEuler.asMatrix() # jointOrient 매트릭스

    
    # rotate 값 (Deg 단위)
    

    GetJntOrder =  cmds.getAttr(Joint + ".rotateOrder") # JntOrder : XYZ , YZX, ... 어떤건지 추출
    Mapping = [
        om.MEulerRotation.kXYZ, om.MEulerRotation.kYZX, om.MEulerRotation.kZXY,
        om.MEulerRotation.kXZY, om.MEulerRotation.kYXZ, om.MEulerRotation.kZYX
    ]
    # Mapping에 따라 JntOrder의 Enem 추출 
    # 0: XYZ, 1: YZX, 2: ZXY, 3: XZY, 4: YXZ, 5: ZYX
    JntRotateOrder = Mapping(GetJntOrder)



    # rotate 값을 가져와서 rotateOrder를 고려하여 매트릭스로 변환
    # MEulerRotation 객체 생성 (해당 조인트의 rotateOrder 사용)
    RotateValue_Deg= cmds.getAttr("{}.rotate".format(Joint))[0] 
    JntOrderEular = om.MEulerRotation(
        math.radians(RotateValue_Deg[0]),
        math.radians(RotateValue_Deg[1]),
        math.radians(RotateValue_Deg[2]),
        JntRotateOrder
    )
    JntRotateMatrix = JntOrderEular.asMatrix() # Rotate 매트릭스

    # 두 매트릭스 결합: JntOrientMatrix * JntRotateMatrix
    # Maya에서 조인트의 로컬 변환은 jointOrient가 적용된 후 rotate가 적용
    # 따라서, 이 두 효과를 합친 새로운 jointOrient 매트릭스는 기존 JntOrientMatrix * JntRotateMatrix을 곱한 결과
    CombineMatrix = JntOrientMatrix * JntRotateMatrix
    
    #결합된 매트릭스를 다시 jointOrient를 위한 Euler 각도로 변환
    # jointOrient는 XYZ 회전 순서를 사용하므로, XYZ로 추출
    NewJntOrientEular = om.MEulerRotation.decompose(CombineMatrix, om.MEulerRotation.kXYZ)
    
    # 라디안을 다시 도로 변환
    NewJntOrient_Deg = [math.degrees(NewJntOrientEular.x) , math.degrees(NewJntOrientEular.y) , math.degrees(NewJntOrientEular.z)]
    for i ,x in enumerate("XYZ"):
        cmds.setAttr("{}.jointOrient{}".format(Joint , x), NewJntOrient_Deg[i])
        cmds.setAttr("{}.rotate{}".format(Joint , x), 0)



SetAttr_CleanJntOrient_Matrix("joint2")