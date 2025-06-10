import maya.cmds as cmds


def Constraint_WithCntScale(Static , Target , MainTain = True):
    Constraint = None
    Constraint = cmds.parentConstraint(Static , Target , mo = MainTain)
    for x in "XYZ":
        cmds.connectAttr('{}.scale{}' .format(Static, x) ,'{}.scale{}' .format(Target ,x),f =1)
    return Constraint[0]

def Constraint_WithScale(Static , Target , MainTain = True):
    Constraint = cmds.parentConstraint(Static , Target , m = MainTain)
    ScaleConstraint = cmds.scaleConstraint(Static , Target , m = MainTain)

    return [Constraint[0] , ScaleConstraint[0]]

def Constraint_PointAndOrient(Static , Target , MainTain = True , Scaling = False):
    Point = cmds.pointConstraint(Static , Target , m = MainTain)
    Orient = cmds.orientConstraint(Static , Target , m = MainTain)
    Scale = None
    if Scaling:
        Scale = cmds.scaleConstraint(Static , Target , m = MainTain)[0]

    return [Point[0] , Orient[0]] if Scaling == False else [Point[0] , Orient[0] , Scale]
        


