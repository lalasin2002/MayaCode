
import maya.cmds as cmds

def d_Grping(Target , Count , Grp_Suffix = ["_Grp" , "_Offset" , "_Prime" , '_GrpPrime']):
    
    Count = int(Count)
    Groups =[]
    Parent_Group = None
    for i , x in enumerate(Grp_Suffix[:Count]):
        Group = cmds.createNode("transform" , n = "{}{}" .format(Target ,x))

        if Parent_Group:
            cmds.parent( Parent_Group ,Group )
        Parent_Group = Group
        Groups.append(Group)
    cmds.delete(cmds.parentConstraint(Target, Groups[-1]))
    cmds.parent(Target ,  Groups[0])

    return  Groups