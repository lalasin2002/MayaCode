import maya.cmds as cmds


def Match_ConstraintJnt(Staric, Target, Bool_Point=True, Bool_Orient=True, Bool_Scale=False):
    '''
    조인트를 매치 기능 \n
    기능 자체는 d_Match_CP와 동일하나  Orient정보를 JointOrient에 입력되도록 설계함 \n
    원리는 해당  Target의 조인트에 그룹 만들엇 이동후 해체 \n
    __________________________________________________________________________\n
    Target :: 조인트 오브젝트만 적용됨
    각 Bool_(Trans , Orient , Scale) ::  가져올 타입을 의미함 
    '''
    
    if cmds.objectType(Target) == 'joint':
        Axis = ["X" , "Y" , "Z"]
        Grp = cmds.createNode('transform', n='{}_PreFix'.format(Target))
        CP = cmds.parentConstraint(Target , Grp, mo=0)
        cmds.delete(CP)

        cmds.parent(Target, Grp)

        if Bool_Point == True:
            Point = cmds.pointConstraint(Staric, Grp)
            cmds.delete(Point)
        if Bool_Orient == True:
            Orient = cmds.orientConstraint(Staric, Grp)
            cmds.delete(Orient)
        if Bool_Scale == True:
            Scale = cmds.scaleConstraint(Staric, Grp)
            cmds.delete(Scale)

        for x in Axis:
            cmds.setAttr(Target + '.rotate{}' .format(x) , 0)

        cmds.parent(Target, w=1)
        cmds.delete(Grp)