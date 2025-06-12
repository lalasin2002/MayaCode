import maya.cmds as cmds


def Constraint_WithCntScale(Static , Target , MainTain = True):
    """
    Static 오브젝트와 Target 오브젝트 사이에 parentConstraint를 생성하고,
    Static 오브젝트의 스케일을 Target 오브젝트의 스케일에 직접 연결합니다.

    Args:
        Static (str): 제약 조건을 제공하는 소스 오브젝트 (부모).
        Target (str): 제약 조건을 받는 대상 오브젝트 (자식).
        MainTain (bool, optional): 제약 조건 생성 시 대상 오브젝트의 현재 오프셋을 유지할지 여부. 기본값은 True.

    Returns:
        str: 생성된 parentConstraint 노드의 이름.
    """
    Constraint = None
    Constraint = cmds.parentConstraint(Static , Target , mo = MainTain)
    # Static 오브젝트의 스케일 속성을 Target 오브젝트의 스케일 속성에 직접 연결
    for x in "XYZ":
        cmds.connectAttr('{}.scale{}' .format(Static, x) ,'{}.scale{}' .format(Target ,x),f =1)
    return Constraint[0]

def Constraint_WithScale(Static , Target , MainTain = True):
    """
    Static 오브젝트와 Target 오브젝트 사이에 parentConstraint와 scaleConstraint를 생성합니다.

    Args:
        Static (str): 제약 조건을 제공하는 소스 오브젝트 (부모).
        Target (str): 제약 조건을 받는 대상 오브젝트 (자식).
        MainTain (bool, optional): 제약 조건 생성 시 대상 오브젝트의 현재 오프셋을 유지할지 여부. 기본값은 True.

    Returns:
        list: [parentConstraint 노드 이름, scaleConstraint 노드 이름]을 포함하는 리스트.
    """
    Constraint = cmds.parentConstraint(Static , Target , mo = MainTain)
    ScaleConstraint = cmds.scaleConstraint(Static , Target , mo = MainTain) # 'm'이 아닌 'mo'로 변경했습니다.

    return [Constraint[0] , ScaleConstraint[0]]

def Constraint_PointAndOrient(Static , Target , MainTain = True , Scaling = False):
    """
    Static 오브젝트와 Target 오브젝트 사이에 pointConstraint와 orientConstraint를 생성합니다.
    선택적으로 scaleConstraint도 생성할 수 있습니다.

    Args:
        Static (str): 제약 조건을 제공하는 소스 오브젝트 (부모).
        Target (str): 제약 조건을 받는 대상 오브젝트 (자식).
        MainTain (bool, optional): 제약 조건 생성 시 대상 오브젝트의 현재 오프셋을 유지할지 여부. 기본값은 True.
        Scaling (bool, optional): scaleConstraint를 생성할지 여부. 기본값은 False.

    Returns:
        list: 생성된 제약 조건 노드들의 이름을 포함하는 리스트.
              Scaling이 False이면 [pointConstraint, orientConstraint]를 반환하고,
              Scaling이 True이면 [pointConstraint, orientConstraint, scaleConstraint]를 반환합니다.
    """
    Point = cmds.pointConstraint(Static , Target , mo = MainTain)
    Orient = cmds.orientConstraint(Static , Target , mo = MainTain)
    Scale = None
    if Scaling:
        Scale = cmds.scaleConstraint(Static , Target , mo = MainTain)[0] # 'm'이 아닌 'mo'로 변경했습니다.

    return [Point[0] , Orient[0]] if Scaling == False else [Point[0] , Orient[0] , Scale]

def Constraint_SeceneAim(Static, Target , aimV = (1,0,0) , upV = (0,1,0) , worldV = (0,1,0)  , MainTain = True):
    """
    Static 오브젝트와 Target 오브젝트 사이에 'scene' worldUpType을 사용하는 aimConstraint를 생성합니다.
    Target 오브젝트가 Static 오브젝트를 바라보도록 합니다.

    Args:
        Static (str): 목표(바라볼) 오브젝트의 이름.
        Target (str): 바라볼 대상이 되는 오브젝트의 이름.
        aimV (tuple, optional): Target 오브젝트의 어떤 축이 Static 오브젝트를 향할지 정의하는 벡터. 기본값은 (1,0,0) (X축).
        upV (tuple, optional): Target 오브젝트의 어떤 축이 worldUpVector와 일치할지 정의하는 벡터. 기본값은 (0,1,0) (Y축).
        worldV (tuple, optional): 'scene' worldUpType에 사용될 세계 상향 벡터. 기본값은 (0,1,0).
        MainTain (bool, optional): 제약 조건 생성 시 대상 오브젝트의 현재 오프셋을 유지할지 여부. 기본값은 True.

    Returns:
        str: 생성된 aimConstraint 노드의 이름.
    """
    worldUpType = "scene"
    Aim = cmds.aimConstraint(Static , Target  , mo = MainTain , aim = aimV  , u = upV , wu = worldV , wut = worldUpType)
    return Aim[0]

def Constraint_VectorAim(Static, Target , aimV = (1,0,0) , upV = (0,1,0) , worldV = (0,1,0)  , MainTain = True):
    """
    Static 오브젝트와 Target 오브젝트 사이에 'vector' worldUpType을 사용하는 aimConstraint를 생성합니다.
    Target 오브젝트가 Static 오브젝트를 바라보도록 합니다.

    Args:
        Static (str): 목표(바라볼) 오브젝트의 이름.
        Target (str): 바라볼 대상이 되는 오브젝트의 이름.
        aimV (tuple, optional): Target 오브젝트의 어떤 축이 Static 오브젝트를 향할지 정의하는 벡터. 기본값은 (1,0,0) (X축).
        upV (tuple, optional): Target 오브젝트의 어떤 축이 worldUpVector와 일치할지 정의하는 벡터. 기본값은 (0,1,0) (Y축).
        worldV (tuple, optional): 'vector' worldUpType에 사용될 세계 상향 벡터. 기본값은 (0,1,0).
        MainTain (bool, optional): 제약 조건 생성 시 대상 오브젝트의 현재 오프셋을 유지할지 여부. 기본값은 True.

    Returns:
        str: 생성된 aimConstraint 노드의 이름.
    """
    worldUpType = "vector"
    Aim = cmds.aimConstraint(Static , Target  , mo = MainTain , aim = aimV  , u = upV , wu = worldV , wut = worldUpType)
    return Aim[0]

def Constraint_ObjRotateAim(Static, Target, Obj , aimV = (1,0,0) , upV = (0,1,0) , worldV = (0,1,0)  , MainTain = True):
    """
    Static 오브젝트와 Target 오브젝트 사이에 'objectrotation' worldUpType을 사용하는 aimConstraint를 생성합니다.
    Target 오브젝트가 Static 오브젝트를 바라보도록 하며, Obj 오브젝트의 회전을 세계 상향 벡터로 사용합니다.

    Args:
        Static (str): 목표(바라볼) 오브젝트의 이름.
        Target (str): 바라볼 대상이 되는 오브젝트의 이름.
        Obj (str): 'objectrotation' worldUpType에 사용될 오브젝트의 이름. 이 오브젝트의 회전이 세계 상향 벡터를 결정합니다.
        aimV (tuple, optional): Target 오브젝트의 어떤 축이 Static 오브젝트를 향할지 정의하는 벡터. 기본값은 (1,0,0) (X축).
        upV (tuple, optional): Target 오브젝트의 어떤 축이 worldUpVector와 일치할지 정의하는 벡터. 기본값은 (0,1,0) (Y축).
        worldV (tuple, optional): 'objectrotation' worldUpType에 사용될 세계 상향 벡터. 이 벡터는 Obj의 로컬 공간에서 해석됩니다. 기본값은 (0,1,0).
        MainTain (bool, optional): 제약 조건 생성 시 대상 오브젝트의 현재 오프셋을 유지할지 여부. 기본값은 True.

    Returns:
        str: 생성된 aimConstraint 노드의 이름.
    """
    worldUpType = "objectrotation"
    Aim = cmds.aimConstraint(Static , Target  , mo = MainTain , aim = aimV  , u = upV , wu = worldV , wut = worldUpType , wuo = Obj )
    return Aim[0]