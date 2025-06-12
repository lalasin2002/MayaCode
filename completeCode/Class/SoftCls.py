import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma


class softCluster():
    """
    Maya에서 소프트 셀렉션(soft selection)을 기반으로 클러스터 디포머를 생성하는 클래스입니다.
    선택된 지오메트리 컴포넌트(주로 버텍스)의 소프트 셀렉션 가중치를 클러스터 디포머의 가중치로 변환하여 적용합니다.
    """
    def __init__(self):
        """
        softCluster 클래스의 인스턴스를 초기화하고, 선택된 소프트 셀렉션 데이터를 기반으로 클러스터를 생성합니다.

        이 생성자는 다음 작업을 수행합니다:
        1. 현재 활성화된 소프트 셀렉션에서 지오메트리 이름과 버텍스 가중치 정보를 추출합니다.
        2. 기존에 생성된 유사한 클러스터가 있는지 확인하여 새로운 클러스터의 고유한 이름을 생성합니다.
        3. 임시 클러스터를 생성하여 중심 위치를 얻고 삭제합니다.
        4. 추출된 소프트 셀렉션 가중치를 사용하여 실제 클러스터를 생성하고 해당 가중치를 적용합니다.

        Args:
            None: 이 생성자는 명시적인 인자를 받지 않습니다. 모든 정보는 현재 Maya의 소프트 셀렉션에서 가져옵니다.

        Returns:
            None: 이 생성자는 명시적인 값을 반환하지 않습니다. 대신 Maya 씬에 클러스터 디포머를 생성합니다.
        """
        self.Geo_name = None
        Axis = ["X" , "Y" , "Z"]
        Count = 1

        sel_soft = om.MGlobal.getRichSelection()
        sel_rich = om.MRichSelection(sel_soft)
        lst_sel_rich = sel_rich.getSelection()
        lst_sel_vtx = om.MSelectionList(lst_sel_rich)

        self.Geo_name = lst_sel_vtx.getSelectionStrings()[0].split('.')[0]
        FindOldCluster = cmds.ls("{}_{}_softCluter" .format(self.Geo_name , "*"))
        if len(FindOldCluster )> 0 :
            Count = int(len(FindOldCluster))
            
        self.ClusterName = "{}_{}_softCluter" .format(self.Geo_name ,Count )

        sel = cmds.ls(sl=1, fl=1)
        Pre_Cls = cmds.cluster(n="__preset__" + self.ClusterName)
        pos = cmds.xform(Pre_Cls[-1], q=1, rp=1, ws=1)
        cmds.delete(Pre_Cls)

        component = lst_sel_rich.getComponent(0)

        componentIndex = om.MFnSingleIndexedComponent(component[1])
        lst_vertex = componentIndex.getElements()

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

