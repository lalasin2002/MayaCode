import maya.cmds as cmds
import maya.mel as mel

import re
def SetAttr_HideLockVectorAttr(item, lock=True, TurnOnKeyable= False):
    """오브젝트의 translate , rotate , scale  하이드 앤 락"""
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

def Add_BoolAttr(Target, LongName):
    """Boolean 속성을 추가."""
    if not cmds.attributeQuery(LongName, node=Target, exists=True):
        cmds.addAttr(Target, ln=LongName, at='bool', k=True)
    return LongName

sel = cmds.ls(sl =1)

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


Selects = cmds.ls(sl =1)

AttrName = "GeoVis"

Pattern = r"(.+)(_Grp)"


for x in sel:
    
    search = re.search(Pattern ,x)
    print (x)
    if search:
        match = search.group(1)
        GeoGrp = cmds.createNode("transform" , n = x + "_Grp")
        Ctrl = cmds.curve( n = match + "_Ctrl" ,d=1, p=[(1, 1, 1), (1, 1, -1), (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, -1, 1),
                                          (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1),
                                          (-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1)],
                                  k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        VisCtrl = Create_TextCrv(match + "_Vis_Ctrl" , "Vis")
        Attr = Add_BoolAttr(VisCtrl , "GeoVis")
        cmds.connectAttr(VisCtrl + ".{}" .format(Attr) , GeoGrp + ".visibility" , f =1)


        Match_ConstraintObject(x ,GeoGrp )
        Match_ConstraintObject(x , Ctrl)
        Match_ConstraintObject(x , VisCtrl)

        CtrlGrp = Grping(Ctrl , 2)
        VisCtrlGrp = Grping(VisCtrl , 2)

        cmds.parent(VisCtrlGrp[-1] , Ctrl)
        Constraint_WithScale(Ctrl , GeoGrp)

        
        p = cmds.listRelatives(x , p =1 )
        cmds.parent(x , GeoGrp)

        cmds.parent(x)
        if p:
            cmds.parent(GeoGrp , p[0]) 
        


    
    
    
    
    
    
    
    
    
    
    
    
    