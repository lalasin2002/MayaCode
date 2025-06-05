import maya.cmds as cmds

def Add_MatrixAttr(Target, LongName, CntTarget=None):
    """매트릭스 타입 속성을 추가하고 선택적으로 월드 매트릭스를 연결."""
    if not cmds.attributeQuery(LongName, node=Target, exists=True):
        cmds.addAttr(Target, ln=LongName, at="matrix", k=True)
        if CntTarget:
            cmds.connectAttr('{}.worldMatrix'.format(CntTarget), '{}.{}'.format(Target, LongName), force=True)
    return LongName


def Add_StringAttr(Target, LongName, String):
    """문자열 타입 속성을 추가하고 초기값을 설정."""
    if not cmds.attributeQuery(LongName, node=Target, exists=True):
        cmds.addAttr(Target, ln=LongName, dt="string")
        cmds.setAttr('{}.{}'.format(Target, LongName), String, type="string")
    return LongName


def Add_FloatAttr(Target, LongName, Min, Max):
    """최소/최대값이 있는 float 타입 속성을 추가."""
    if not cmds.attributeQuery(LongName, node=Target, exists=True):
        cmds.addAttr(Target, ln=LongName, at='double', min=Min, max=Max, k=True)
    return LongName


def Add_FloatOffsetAttr(Target, LongName):
    """제한 없는 float 속성을 추가."""
    if not cmds.attributeQuery(LongName, node=Target, exists=True):
        cmds.addAttr(Target, ln=LongName, at='double', k=True)
    return LongName


def Add_IntAttr(Target, LongName, Min, Max):
    """최소/최대값이 있는 int 속성을 추가."""
    if not cmds.attributeQuery(LongName, node=Target, exists=True):
        cmds.addAttr(Target, ln=LongName, at='long', min=Min, max=Max, k=True)
    return LongName


def Add_IntOffsetAttr(Target, LongName):
    """제한 없는 int 속성을 추가."""
    if not cmds.attributeQuery(LongName, node=Target, exists=True):
        cmds.addAttr(Target, ln=LongName, at='long', k=True)
    return LongName


def Add_BoolAttr(Target, LongName):
    """Boolean 속성을 추가."""
    if not cmds.attributeQuery(LongName, node=Target, exists=True):
        cmds.addAttr(Target, ln=LongName, at='bool', k=True)
    return LongName


def Add_EnumAttr(Target, LongName, Enum_List):
    """Enum 속성을 추가."""
    if not cmds.attributeQuery(LongName, node=Target, exists=True):
        EnumString = ":".join(Enum_List)
        cmds.addAttr(Target, ln=LongName, en=EnumString, at='enum', k=True)
    return LongName


def Add_SeparatorAttr(Target, LongName, EnumString="__"):
    """UI 구분선용 Enum 속성을 추가."""
    if not cmds.attributeQuery(LongName, node=Target, exists=True):
        cmds.addAttr(Target, ln=LongName, nn="_______________", en=EnumString, at='enum', k=True)
        cmds.setAttr('{}.{}'.format(Target, LongName), e=True, keyable=False, channelBox=True)
    return LongName

def Add_JntLebal(Target, Lebal, Side='M'):
    if Side == 'M':
        JntSide = 0
    elif Side == 'L':
        JntSide = 1
    elif Side == 'R':
        JntSide = 2
    else:
        JntSide = 3

    if cmds.objectType(Target) == 'joint':
        cmds.setAttr(Target + '.side', JntSide)
        cmds.setAttr(Target + '.type', 18)
        cmds.setAttr(Target + '.drawLabel', 1)
        cmds.setAttr(Target + '.otherType', Lebal, type="string")

    if JntSide == 0:
        ReturnSide = 'Center'
    elif JntSide == 1:
        ReturnSide = 'Left'
    elif JntSide == 2:
        ReturnSide = 'Right'
    else:
        ReturnSide = 'None'

    ReTurnString = cmds.getAttr(Target + '.otherType')
    return [ReturnSide, ReTurnString]


def Get_EnumAttrItem(Target, LongName):
    """Enum 속성의 항목 리스트 반환."""
    if cmds.attributeQuery(LongName, node=Target, exists=True):
        Enum = cmds.attributeQuery(LongName, node=Target, listEnum=True)
        return Enum[0].split(":")
    return []


def Get_AttrValue(Target, LongName):
    """속성의 최소, 최대, 현재 값을 딕셔너리로 반환."""
    if cmds.attributeQuery(LongName, node=Target, exists=True):
        Dic = {}
        Dic["Min"] = cmds.attributeQuery(LongName, node=Target, minimum=True)[0]
        Dic["Max"] = cmds.attributeQuery(LongName, node=Target, maximum=True)[0]
        Dic["Current"] = cmds.getAttr("{}.{}".format(Target, LongName))
        return Dic
    return {}


def Delete_Attr(Target, LongName):
    """속성 삭제."""
    if cmds.attributeQuery(LongName, node=Target, exists=True):
        cmds.deleteAttr("{}.{}".format(Target, LongName))
