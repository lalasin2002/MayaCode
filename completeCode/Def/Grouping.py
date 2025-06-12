import maya.cmds as cmds
from collections import OrderedDict


def Set_CntParent(Object_list , Name = ["_loc" , "_locParent"] , Grplist = ["_Grp" , "_Offset"]):
    """
    주어진 오브젝트 목록에 대해 컨트롤러 부모 계층을 설정합니다.
    각 오브젝트에 대해 두 개의 로케이터와 지정된 그룹 계층을 생성하여 연결합니다.
    마지막으로, 원본 오브젝트의 부모를 새로 생성된 "Connects" 로케이터에 연결합니다.

    Args:
        Object_list (list): 컨트롤러 부모 계층을 설정할 오브젝트 이름의 리스트.
        Name (list, optional): 로케이터의 이름 접미사.
                               첫 번째 요소는 제약 로케이터에, 두 번째 요소는 연결 로케이터에 사용됩니다.
                               기본값은 ["_loc", "_locParent"].
        Grplist (list, optional): 각 로케이터 아래에 생성할 그룹의 이름 접미사 리스트.
                                   기본값은 ["_Grp", "_Offset"].

    Returns:
        OrderedDict: 생성된 Maya 노드들을 포함하는 OrderedDict.
                     "Constraints": 제약 로케이터 리스트.
                     "Connects": 연결 로케이터 리스트.
                     "Main": 전체 계층의 최상위 그룹 ("_CntParent_All").
    """
    Work_Dic = OrderedDict()
    # 전체 계층의 최상위 그룹 생성
    All = cmds.createNode('transform' , n = Object_list[0] + '_CntParent_All')
    # 제약 로케이터와 연결 로케이터 리스트 생성
    lst_loc = [ cmds.spaceLocator(n = y +   Name[0])[0]   for y in Object_list]
    lst_locParent = [cmds.spaceLocator(n =  y + Name[1])[0] for y in Object_list]

    Work_Dic["Constraints"] = lst_loc
    Work_Dic["Connects"] = lst_locParent

    # 각 로케이터 타입(Constraints, Connects)에 대해 반복
    for key , list_values in Work_Dic.items():
        Oldloc = None # 이전 로케이터를 저장 (Connects 로케이터를 부모로 설정하기 위해)
        for i , loc in enumerate(list_values):
            OldGrp  = None # 이전 그룹을 저장 (그룹 계층을 구축하기 위해)
            FirstGrp = None # 사용되지 않음
            Grp = None
            # 각 로케이터에 대해 그룹 계층 생성
            for GrpCount , GrpName in enumerate(Grplist):
                Grp = cmds.createNode('transform' , n = loc + GrpName)
                if GrpCount  == 0:
                    # 첫 번째 그룹에 로케이터를 부모로 설정
                    cmds.parent(loc , Grp)
                # 원본 오브젝트의 위치에 그룹을 스냅 (제약 후 삭제)
                cmds.delete(cmds.parentConstraint(Object_list[i]  , Grp)[0])
                if OldGrp:
                    # 이전 그룹을 현재 그룹의 자식으로 설정하여 계층 구축
                    cmds.parent( OldGrp , Grp)
                if GrpCount == len(Grplist)-1:
                    # 마지막 그룹을 최상위 "All" 그룹의 자식으로 설정
                    cmds.parent(Grp , All)

                OldGrp  = Grp # 현재 그룹을 OldGrp로 업데이트
            # "Connects" 로케이터인 경우, 이전 "Constraints" 로케이터의 자식으로 설정
            if key == "Connects" and Oldloc:
                cmds.parent(Grp , Oldloc)
            Oldloc = loc # 현재 로케이터를 Oldloc로 업데이트

    # 원본 오브젝트의 부모를 "Connects" 로케이터에 연결하고, 제약 조건 설정
    for i, x in enumerate(Object_list):
        ObjParent = None
        if cmds.listRelatives(x , p = 1):
            ObjParent = cmds.listRelatives(x , p = 1)[0]
            # 원본 오브젝트의 부모와 "Connects" 로케이터의 translate, rotate, scale 연결
            for Attr in [".translate" , ".rotate" , ".scale"]:
                for Axis in "XYZ":
                    cmds.connectAttr(Work_Dic["Connects"][i] + "{}{}" .format(Attr , Axis) , ObjParent  + "{}{}" .format(Attr , Axis) , f =1 )
            # "Constraints" 로케이터와 "Connects" 로케이터 간의 부모 제약 조건 설정
            cmds.parentConstraint(Work_Dic["Constraints"][i]  , Work_Dic["Connects"][i])
    # 최종 결과에 최상위 "All" 그룹 추가
    Work_Dic["Main"] = All
    return Work_Dic



def Grping(Target , Count , Grp_Suffix = ["_Grp" , "_Offset" , "_Prime" , '_GrpPrime']):
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