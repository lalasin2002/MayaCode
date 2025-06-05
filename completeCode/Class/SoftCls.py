import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma


class softCluster():
    def __init__(self):
        self.Geo_name = None
        Axis = ["X" , "Y" , "Z"]
        Count = 1

        sel_soft = om.MGlobal.getRichSelection()
        sel_rich = om.MRichSelection(sel_soft)
        lst_sel_rich = sel_rich.getSelection()
        lst_sel_vtx = om.MSelectionList(lst_sel_rich)

        self.Geo_name = lst_sel_vtx.getSelectionStrings()[0].split('.')[0]
        FindOldCluster = cmds.ls("{}_{}_softCluter" .format(self.Geo_name  , "*"))
        if len(FindOldCluster )> 0 :
            Count = int(len(FindOldCluster))
            
        self.ClusterName = "{}_{}_softCluter" .format(self.Geo_name ,Count  )

        sel = cmds.ls(sl=1, fl=1)
        Pre_Cls = cmds.cluster(n="__preset__" + self.ClusterName)
        pos = cmds.xform(Pre_Cls[-1], q=1, rp=1, ws=1)
        cmds.delete(Pre_Cls)

        component = lst_sel_rich.getComponent(0)

        componentIndex = om.MFnSingleIndexedComponent(component[1])
        lst_vertex = componentIndex.getElements()

        componentIndex = om.MFnSingleIndexedComponent(component[1])

        lst_vertex = componentIndex.getElements()

        lst_weight = {}
        for x in range(len(lst_vertex)):
            weight = componentIndex.weight(x)
            influence = weight.influence

            lst_weight.setdefault(lst_vertex[x], influence)

        rangeVertexs = lst_sel_rich.getSelectionStrings()
        self.Cls = cmds.cluster(rangeVertexs, n=self.ClusterName)
        cmds.xform(self.Cls[-1], ws=1, rp=pos)
        shp = cmds.listRelatives(self.Cls[-1], s=1)[0]
        for x in range(0,len(Axis)):
            cmds.setAttr(shp + '.origin' + Axis[x] , pos[x])


        for x in lst_weight:
            element_Vex = x
            element_Weight = lst_weight[x]

            cmds.setAttr('{}.weightList[0].w[{}]'.format(self.Cls[0], x), float(lst_weight[x]))

def show():
    softCluster()
