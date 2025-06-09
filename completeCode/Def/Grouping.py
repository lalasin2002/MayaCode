import maya.cmds as cmds
from collections import OrderedDict


def Set_CntParent(Object_list , Name = ["_loc" , "_locParent"] , Grplist = ["_Grp" , "_Offset"]):
    Work_Dic = OrderedDict()
    All = cmds.createNode('transform' , n = Object_list[0] + '_CntParent_All')
    lst_loc = [ cmds.spaceLocator(n = y +   Name[0])[0]   for y in Object_list]
    lst_locParent = [cmds.spaceLocator(n =  y + Name[1])[0] for y in Object_list]

    Work_Dic["Constraints"] = lst_loc
    Work_Dic["Connects"] = lst_locParent
    for key , list_values in Work_Dic.items():
        Oldloc = None
        for i , loc in enumerate(list_values):
            OldGrp  =None
            FirstGrp = None
            Grp = None
            for GrpCount , GrpName in enumerate(Grplist):
                Grp = cmds.createNode('transform' , n = loc + GrpName)
                if GrpCount  == 0:
                    cmds.parent(loc , Grp)
                cmds.delete(cmds.parentConstraint(Object_list[i]  , Grp)[0])
                if OldGrp:
                    cmds.parent( OldGrp , Grp)
                if GrpCount == len(Grplist)-1:
                    cmds.parent(Grp , All)

                OldGrp  = Grp
            if key == "Connects" and Oldloc:
                cmds.parent(Grp , Oldloc)
            Oldloc = loc
    for i, x in enumerate(Object_list):
        ObjParent = None
        if cmds.listRelatives(x , p = 1):
            ObjParent = cmds.listRelatives(x , p = 1)[0]
            for Attr in [".translate" , ".rotate" , ".scale"]:
                for Axis in "XYZ":
                    cmds.connectAttr(Work_Dic["Connects"][i] + "{}{}" .format(Attr , Axis) , ObjParent  + "{}{}" .format(Attr , Axis) , f =1 )
            cmds.parentConstraint(Work_Dic["Constraints"][i]  , Work_Dic["Connects"][i])
    Work_Dic["Main"] = All
    return Work_Dic



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