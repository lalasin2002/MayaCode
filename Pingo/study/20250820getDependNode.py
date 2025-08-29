import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma

class Get_omSkinDate:
    def __init__(self , skinNode , skinGeo):
        selects = om.MSelectionList() #set선언과 같음
        selects.add(skinNode)
        selects.add(skinGeo)

        string_list = selects.getSelectionStrings() #실질 리스트화 , 이래야 for 돌려서 출력이 가능


        # getDependNode :
        #    -Dependency Node( ex ) skinCluster , blendShape , ...) 같은 계층 구조 없이 데이터 계산/처리를 담당하는 노드를 추출하는 메서드
        #    - 숫자는 해당 set의 인덱스 숫자를 가르킴
        #    - 프린트시 , 메모리주소를 가져옴
        #    - 네임을 따오려면 
        #    -- 1. dep_node_fn =   om.MFnDependencyNode(Mobj) 로 상세정로 개념의 Function Set를 따온다
        #    -- 2. node_name = dep_node_fn.name() 로 네임을 가져온다 


        # 
        Mobj = selects.getDependNode(0)
        dep_node_fn = om.MFnDependencyNode(Mobj)
        node_name = dep_node_fn.name()
        #print ( "Mobj node_name : " ,node_name )

        #oma.MFnSkinCluster: 
        #    - OpenMayaAnim 에서 오브젝트 메모리주소기준(MObject)으로 가져와 대한 정보를 읽고, 수정하고, 분석하는 데에 고도로 특화된 '전문가' 클래스
        #    - influenceObjects 메서드 :  모든 조인트 가져오기 
        #    - getWeights 메서드 : 특정 정점(vertex)들에 대한 모든 조인트의 가중치(weight) 값 가져오기
        #    - setWeights 메서드 :  읽어온 가중치 값을 수정해서 다시 덮어쓰기
        #    - getPointsAffectedByInfluence 메서드 : 특정 조인트에 의해 영향받는 모든 정점들을 찾아내기.


        Mfn_skin = oma.MFnSkinCluster(Mobj) 
        Mgeo = selects.getDagPath(1)
        infs = Mfn_skin.influenceObjects()
        influence_objs = [inf.fullPathName() for inf in infs]

        select_compos = om.MGlobal.getSelectionListByName("{}.vtx[*]".format(Mgeo.fullPathName()))
        compos = select_compos.getComponent(0)[1]

        weights , etc = Mfn_skin.getWeights(Mgeo , compos)
        weights = list(weights)

        #print ("weights : " , weights)
        #print ("etc : " , etc)


        #print ("Mfn_skin : ", Mfn_skin)
        #print ("Mgeo : " , Mgeo)
        #print ("infs : " , infs)
        #print ("influence_objs : " , influence_objs)
        #print ("compos : " , compos)

        self.influece_objs = influence_objs
        self.weights = weights 
