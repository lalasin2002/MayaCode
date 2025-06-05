import maya.cmds as cmds
import maya.mel as mel
import pprint


def SkinWeightToCls(Name , Jnt , Geo  ):
    xformJnt = cmds.xform(Jnt , q =1 , ws = 1, t =1)
    skin_cluster_nodes = mel.eval('findRelatedSkinCluster("{}")'.format(Geo))
    num_vertices = cmds.polyEvaluate(Geo, vertex=True)
    all_vtxs = ["{}.vtx[{}]" .format(Geo , i ) for i in range(num_vertices)]
    joint_weights  = []
    for x in all_vtxs:
        joint_weight = cmds.skinPercent(skin_cluster_nodes, x, transform=Jnt, query=True, value=True)
        joint_weights.append(joint_weight)
        
    cmds.select(all_vtxs)
    ClsInfo = cmds.cluster( n = "{}".format(Name))
    ClsNode = ClsInfo[0]
    ClsHandle = ClsInfo[1]
    ClsShape = cmds.listRelatives(ClsHandle , s =1 )[0]

    for  i , x in enumerate ("XYZ"):
        cmds.setAttr(ClsShape + ".origin{}" .format(x) , xformJnt[i])
        cmds.setAttr(ClsHandle + ".rotatePivot{}" .format(x) , xformJnt[i])

    for  i , x in enumerate(joint_weights):
        FixWeight = round(x ,3)
        if  0.0 == x:
            FixWeight = 0   
        cmds.percent(ClsNode , all_vtxs[i] ,v = FixWeight )

    return [ClsHandle , ClsNode ]