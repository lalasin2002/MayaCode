# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om


def Get_SelectFaces(list):
    Faces = [x for x in list if ".f" in x]
    return Faces

def Get_SelectEdges(list):
    Edges = [x for x in list if ".e" in x]
    return Edges

def Get_SelectVtxs(list):
    Vtxs = [x for x in list if ".vtx" in x]
    return Vtxs



def GetMeshVtx_SequencePos(FirstVtxs , ConversionTuple = True):
    """메쉬 버텍스 시작점 부터 시퀀스 대로 중심점 Pos 가져오기"""
    Mesh = None
    MeshTF = None
    AllVtx = None
    TatalRange = 0
    RenturnList = []
    if any("vtx" in x for x in FirstVtxs): 
        MeshTF = FirstVtxs[0].split(".")[0]
        if cmds.objExists(MeshTF):
            Mesh = cmds.listRelatives(MeshTF , s =1 , type = "mesh")[0]
            
        if cmds.objExists(Mesh):
            AllVtx = cmds.ls("{}.vtx[*]" .format(MeshTF) , fl =1 )

            SearcheList = []
            Add = FirstVtxs
            Current = FirstVtxs
            while  len(SearcheList) < len(AllVtx) :

                cmds.select(Add )
                mel.eval('PolySelectTraverse 1')
                Add = cmds.ls(sl =1 ,fl =1)
                SearcheList += Add 
                SearcheList = list(set(SearcheList))
                TatalRange +=1

                if len(SearcheList) == len(AllVtx):
                    break
            TatalRange = TatalRange+ 1
            SearcheList = []
            Add = FirstVtxs
            Current = FirstVtxs

            for x in range(TatalRange):

                Cls = cmds.cluster(Current)
                PointTf = cmds.createNode("transform" ,  n = "PreSet_{}{}_Tf" .format(MeshTF[0] , TatalRange))
                CP = cmds.parentConstraint(Cls[-1] , PointTf , mo = 0)
                Pos = cmds.xform(PointTf ,q =1,  ws =1, t =1)

                if ConversionTuple:
                    Pos = tuple(Pos)
                RenturnList.append(Pos)
                cmds.delete(CP)
                cmds.delete(Cls)
                cmds.delete(PointTf)


                
                cmds.select(Add )
                mel.eval('PolySelectTraverse 1')
                Add = cmds.ls(sl =1 ,fl =1)
                Current = list(set(Add) -  set(SearcheList))
                SearcheList += Add 
                SearcheList = list(set(SearcheList))
                
        return RenturnList


def Get_PoleVectorPos(Root , Middle , End , Scalar = 1):
    """IK PoleVector 정확한 위치 가져오기"""
    RootPos = cmds.xform(Root , q= 1, ws =1 , t =1)
    MiddlePos = cmds.xform(Middle , q= 1, ws =1 , t =1)
    EndPos =  cmds.xform(End , q= 1, ws =1 , t =1)
    
    RootVector = om.MVector(RootPos[0] , RootPos[1] , RootPos[2])
    MiddleVector = om.MVector(MiddlePos[0] , MiddlePos[1] , MiddlePos[2])
    EndVector = om.MVector(EndPos[0] , EndPos[1] , EndPos[2])
    
    
    RootEnd_Vector = (EndVector - RootVector)
    RootMiddle_Vector = (MiddleVector- RootVector)
    
    DotP = RootEnd_Vector * RootMiddle_Vector
    
    ProJect_Length= float(DotP)/float(RootEnd_Vector.length())
    
    Normalize_RootEnd = RootEnd_Vector.normal()
    
    ProJ_Vector = Normalize_RootEnd * ProJect_Length
    
    Arrow_Vector = (RootMiddle_Vector  - ProJ_Vector) *  Scalar
    
    Pole_Vector = Arrow_Vector + MiddleVector
    

    Pole_Vecotor_Pos = [Pole_Vector.x , Pole_Vector.y , Pole_Vector.z]
    return Pole_Vecotor_Pos
#----------------------------------------------------------------------------------Attr
def Get_EnumAttrItem(Target, LongName):
    """Enum 속성의 항목 리스트 반환."""
    if cmds.attributeQuery(LongName, node=Target, exists=True):
        Enum = cmds.attributeQuery(LongName, node=Target, listEnum=True)
        return Enum[0].split(":")
    return []


def Get_AttrValue(Target, LongName):
    """속성의 최소, 최대, 현재 값을 딕셔너리로 반환."""
    if cmds.attributeQuery(LongName, node=Target, exists=True):
        Dic = {}
        Dic["Min"] = cmds.attributeQuery(LongName, node=Target, minimum=True)[0]
        Dic["Max"] = cmds.attributeQuery(LongName, node=Target, maximum=True)[0]
        Dic["Current"] = cmds.getAttr("{}.{}".format(Target, LongName))
        return Dic
    return {}

def Get_JntRotateOrder(Jnt):
    """
    조인트의 'rotateOrder' 속성 값(정수)을 maya.api.OpenMaya.MEulerRotation.RotationOrder 열거형으로 변환.
    """
    ro_attr_val = cmds.getAttr(Jnt + ".rotateOrder")
    # Maya 'rotateOrder' 속성 값과 MEulerRotation.RotationOrder 매핑:
    # 0: kXYZ, 1: kYZX, 2: kZXY, 3: kXZY, 4: kYXZ, 5: kZYX
    mapping = [
        om.MEulerRotation.kXYZ, om.MEulerRotation.kYZX, om.MEulerRotation.kZXY,
        om.MEulerRotation.kXZY, om.MEulerRotation.kYXZ, om.MEulerRotation.kZYX
    ]
    if 0 <= ro_attr_val < len(mapping):
        return mapping[ro_attr_val]

#---------------------------------------------------------------------------Obj
def Get_HierarchyObj_List(Target , Type = None):
    cmds.select(Target, hi=1)
    lst = cmds.ls(sl=1 )
    if not Type == None:
        lst = [x for x in lst if cmds.objectType(x) == Type]
    cmds.select(cl =1)
    return lst

#---------------------------------------------------------------------------Skin


def Get_SkinCluster(obj):
    skin_cluster_nodes = mel.eval('findRelatedSkinCluster("{}")'.format(obj))
    return skin_cluster_nodes

def Get_SkinPercent(obj):
    Dic = {}
    Shp = cmds.listRelatives(obj, s=1)[0]
    skinCluter = cmds.listConnections(Shp, type='skinCluster')[0]
    vtxs = cmds.ls(obj + '.vtx[*]', fl=1)

    for x in vtxs:
        weight = cmds.skinPercent(skinCluter, x, q=1, value=1, ignoreBelow=0.001)
        Jnt = cmds.skinPercent(skinCluter, x, q=1, transform=None)
        for y in range(len(Jnt) - 1):
            if len(weight) == 1:
                weight.append(0)
        list = []

        for y in range(len(Jnt)):
            Tu = []
            Tu.append(Jnt[y])
            Tu.append(weight[y])
            Tu = tuple(Tu)
            list.append(Tu)

        Dic[x] = list
    return Dic


#---------------------------------------------------------------------------Render
def Get_Shader(Obj , Type = "lambert"):
    """타입별 오브젝트 쉐이더 가져오기"""
    WorkItme = Obj
    ShadingEngine = None
    Shader = None
    if cmds.objectType(WorkItme) == "transform":
        if cmds.listRelatives(WorkItme , c =1):
            WorkItme = cmds.listRelatives(WorkItme , c =1)[0]

    if cmds.objectType(WorkItme) in ["mesh", "nurbsCurve"]:
        ShadingEngine = cmds.listConnections(WorkItme , type="shadingEngine")
        if ShadingEngine and len(ShadingEngine)>0:
            ShadingEngine = ShadingEngine[0]

    if ShadingEngine:
        Shader = cmds.listConnections(ShadingEngine , s= 1 , d =0  ,  t = Type)
    
    return Shader

def Get_RenderSet(Obj):
    lstAttr = ['castsShadows', 'receiveShadows', 'holdOut', 'motionBlur', 'primaryVisibility', 'smoothShading',
               'visibleInReflections', 'visibleInRefractions', 'doubleSided']

    Dic = {}
    for x in range(len(lstAttr)):
        GetValue = cmds.getAttr('{}.{}'.format(Obj, lstAttr[x]))
        Dic[lstAttr[x]] = GetValue
    return Dic

def Get_Node_From_MeshShaderEngine(Object , Types = ["blendColors" , "RedshiftMaterialBlender"],returnToDic = True ):
    """
    오브젝트(transform 또는 mesh)에서 셰이딩 엔진을 찾아, 연결된 모든 상위 노드 중 
    지정한 타입의 노드들을 반환합니다.

    Args:
        -obj (str): 오브젝트의 이름 (transform 또는 mesh)
        -types (list, optional): 찾고 싶은 노드 타입 리스트.
        -return_to_dic (bool, optional): 결과를 딕셔너리로 반환할지 리스트로 반환할지 결정.

    Returns:
        -dict or list: 찾은 노드들. return_to_dic 값에 따라 형식이 달라짐.
    """
    
    def Find_all_CntUpstream(Start , FoundNodes = None):
        '''재귀함수'''
        if FoundNodes is None:
            FoundNodes = set()
        connects = cmds.listConnections(Start , s =1 , d =0) or []
        for node in connects:
            if node not in FoundNodes:
                FoundNodes.add(node)
                Find_all_CntUpstream(node , FoundNodes)
        return FoundNodes


    TransForm = None
    MeshShp = None
    ShadingEngine = None
    returnDic = {}
    returnList = []
    ObjectType= cmds.objectType(Object)
    if ObjectType == "transform":
        shps = cmds.listRelatives(Object , s = 1 , type = "mesh" , fullPath=1)
        if shps:
            TransForm = Object
            MeshShp = shps[0]
    if ObjectType == "mesh":
        parents = cmds.listRelatives(Object , p= 1 , type = "transform" , fullPath=1)
        if parents :
            TransForm = parents[0]
            MeshShp = Object
    if TransForm is None or MeshShp is None:
        raise TypeError(">> Invalid input. Expected a transform or mesh node name (string).")
    try:
        ShadingEngine = cmds.listConnections(MeshShp  , type="shadingEngine")[0]
    except (TypeError, IndexError):
        print(">> Warning: No shadingEngine found for  '{}'." .format(MeshShp))
        return returnDic if returnToDic else returnList
    for type in Types:
        returnDic[type] = []
    
    Conects = Find_all_CntUpstream(ShadingEngine)
    TypesSet = set(Types)
    for node in Conects:
        node_type = cmds.objectType(node)
        if node_type in TypesSet:
            returnDic[node_type].append(node)

    if returnToDic:
        returnDic["shadingEngine"] = ShadingEngine
        return returnDic
    else:
        for k , v in returnDic.items():
            returnList += v
        return returnList
    



#-------------------------------------------------------------------Cal
def Get_Distance(StartObj, EndObj ):
    """두 오브젝트의 거리값 가져오기"""
    S_Pos = cmds.xform(StartObj , q =1, t =1 ,ws =1)
    E_Pos = cmds.xform(EndObj, q=1, t=1, ws=1)
    DT = ((S_Pos[0] - E_Pos[0])**2 + (S_Pos[1] - E_Pos[1])**2 + (S_Pos[2] - E_Pos[2])**2)**0.5
    return DT

def Get_ParameterValue(Total , Parameter):
    """정규화된 파라미터 기반 값 구하기"""
    Value = Total * Parameter
    return Value

def Get_Parmeter(Total, Value):
    """정규화"""
    Parameter = Value / Total
    return Parameter