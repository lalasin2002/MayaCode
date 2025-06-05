import maya.cmds as cmds

def d_Match_CP(Staric, Target, Bool_Point=True, Bool_Orient=True, Bool_Scale=False):
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