import maya.cmds as cmds

def Add_MatrixAttr(target, attr_name, connect_target=None):
    """매트릭스 타입 속성을 추가하고 선택적으로 월드 매트릭스를 연결."""
    if not cmds.attributeQuery(attr_name, node=target, exists=True):
        cmds.addAttr(target, ln=attr_name, at="matrix", k=True)
        if connect_target:
            cmds.connectAttr(f"{connect_target}.worldMatrix", f"{target}.{attr_name}", force=True)
    return attr_name


def Add_StringAttr(target, attr_name, value):
    """문자열 타입 속성을 추가하고 초기값을 설정."""
    if not cmds.attributeQuery(attr_name, node=target, exists=True):
        cmds.addAttr(target, ln=attr_name, dt="string")
        cmds.setAttr(f"{target}.{attr_name}", value, type="string")
    return attr_name


def Add_FloatAttr(target, attr_name, min_val, max_val):
    """최소/최대값이 있는 float 타입 속성을 추가."""
    if not cmds.attributeQuery(attr_name, node=target, exists=True):
        cmds.addAttr(target, ln=attr_name, at='double', min=min_val, max=max_val, k=True)
    return attr_name


def Add_FloatOffsetAttr(target, attr_name):
    """제한 없는 float 속성을 추가."""
    if not cmds.attributeQuery(attr_name, node=target, exists=True):
        cmds.addAttr(target, ln=attr_name, at='double', k=True)
    return attr_name


def Add_IntAttr(target, attr_name, min_val, max_val):
    """최소/최대값이 있는 int 속성을 추가."""
    if not cmds.attributeQuery(attr_name, node=target, exists=True):
        cmds.addAttr(target, ln=attr_name, at='long', min=min_val, max=max_val, k=True)
    return attr_name


def Add_IntOffsetAttr(target, attr_name):
    """제한 없는 int 속성을 추가."""
    if not cmds.attributeQuery(attr_name, node=target, exists=True):
        cmds.addAttr(target, ln=attr_name, at='long', k=True)
    return attr_name


def Add_BoolAttr(target, attr_name):
    """Boolean 속성을 추가."""
    if not cmds.attributeQuery(attr_name, node=target, exists=True):
        cmds.addAttr(target, ln=attr_name, at='bool', k=True)
    return attr_name


def Add_EnumAttr(target, attr_name, enum_list):
    """Enum 속성을 추가."""
    if not cmds.attributeQuery(attr_name, node=target, exists=True):
        enum_str = ":".join(enum_list)
        cmds.addAttr(target, ln=attr_name, en=enum_str, at='enum', k=True)
    return attr_name


def Add_SeparatorAttr(target, attr_name, label="_____"):
    """UI에서 구분선용 enum 속성 추가."""
    if not cmds.attributeQuery(attr_name, node=target, exists=True):
        cmds.addAttr(target, ln=attr_name, nn=label, en="__", at='enum', k=True)
        cmds.setAttr(f"{target}.{attr_name}", e=True, keyable=False, channelBox=True)
    return attr_name


def Get_EnumAttrItem(target, attr_name):
    """Enum 속성의 항목 리스트 반환."""
    if cmds.attributeQuery(attr_name, node=target, exists=True):
        enum_str = cmds.attributeQuery(attr_name, node=target, listEnum=True)[0]
        return enum_str.split(":")
    return []


def Get_AttrValue(target, attr_name):
    """속성의 최소값, 최대값, 현재값을 딕셔너리로 반환."""
    if cmds.attributeQuery(attr_name, node=target, exists=True):
        return {
            "Min": cmds.attributeQuery(attr_name, node=target, minimum=True)[0],
            "Max": cmds.attributeQuery(attr_name, node=target, maximum=True)[0],
            "Current": cmds.getAttr(f"{target}.{attr_name}")
        }
    return {}


def Delete_Attr(target, attr_name):
    """지정한 속성을 제거."""
    if cmds.attributeQuery(attr_name, node=target, exists=True):
        cmds.deleteAttr(f"{target}.{attr_name}")
