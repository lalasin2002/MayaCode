# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os , json ,pprint ,re






def Hierarchy(Root , patternString= None):

    cmds.select(Root , hi =1)
    hierarchySelects = cmds.ls(sl =1 , type = "transform" )
    List = []
    Pattern = ""
    if isinstance(patternString ,str ):
        Pattern = patternString
    for x in hierarchySelects:
        if patternString:
            search = re.search( Pattern ,x )
            
            if search:
                cmds.select(x)
                fullpath = cmds.ls(sl =1 , long=1)
                List.append(fullpath[0])


    return List
def DictPos(List , flagDict = {"t" : True , "os" : True }):

    Dict = {}
    for x in List:
        Pos = cmds.xform(x , q =1 , **flagDict)
        Dict[x] = Pos

    return Dict



def setPosDict(PosDict , flag = ["os", "t"] , printLog = True):
    ErrorString = ""
    WorkLogString = "\n\n"
    if printLog:
        ErrorString += "_____________________________________________\n"
    if isinstance(PosDict , dict):
        Count = 1
        for obj , value in PosDict.items():
            if cmds.objExists(obj):
                cmds.xform(obj , **{ flag[0] : True , flag[1] :value })
                if printLog:
                    WorkLogString += ">>작업경과 {n} : 딕셔너리의 데이터 {o} \n    > {v} \n     > 적용되었습니다\n" .format( n = Count , o = obj , v =value )
            else:
                if printLog:
                    ErrorString += ">>작업경과 {n} : 현재 씬에서 딕셔너리의 데이터 {o} \n > 존재하지않습니다.\n" .format(n = Count , o = obj)
            Count +=1 
    if printLog:
        print (WorkLogString)
        print (ErrorString)

def ctrlPosData(PathVar  , WorkType = "export" , fileName = "ctrlPosData.json" , Pattern = r".+_Aim_Ctrl$"):
    printLog = "\n\n"
    if not any(WorkType == t for t in ["export" , "import"]):
        raise TypeError(">> 적절한 WorkType 지정되지않았습니다. export , import 둘중 하나만 정확히 입력해야 합니다.)")
    

    select = cmds.ls(sl =1 )
    absPath = os.path.abspath(PathVar)
    JsonPath = os.path.join( absPath , fileName)
    lsExistPath = os.path.isdir(absPath)
    IsExistJsonPath = os.path.isfile(JsonPath)

    if WorkType == "export" and len(select) == 0 :
        raise IndexError(">> 에러! : 상위 그룹을 셀렉트 했는지 확인하세요")
    if lsExistPath == False:
        raise TypeError(">> 에러! : 입력한 폴더경로의 탐색하지 못했습니다. PathVar의 경로를 확인하세요")
    if WorkType == "import":
        if IsExistJsonPath == False:
            raise TypeError (">> 에러! : 입력된 제이슨 경로 파일을 탐색하지 못했습니다. PathVar , fileName를 확인하세요")

    if WorkType == "export" and len(select) >0 and lsExistPath:
        HierarchyData = Hierarchy(select[0] ,Pattern )
        CtrlPosDict = DictPos(HierarchyData)
        if len(CtrlPosDict)>0:
            with open(JsonPath, "w" ) as file:
                json.dump(CtrlPosDict , file ,indent=4)
            for k, v in CtrlPosDict.items():
                print ("> {} : {} 데이터" .format(k , v))
            print ("\n\n >> {path} \n   > 에 데이터가 저장되었습니다.")

        else:
            raise RuntimeError(">> 에러! : 조건에 맞는 데이터를 찾지 못했습니다. Pattern를 다시 정의 하거나 ,적절한 상위 그룹을 셀렉트 했는지 확인하세요")
    
    if WorkType == "import" and IsExistJsonPath == True:
        Data = None
        with open(JsonPath , "r") as file:
            Data = json.load(file)
        if Data and isinstance(Data , dict):
            setPosDict(Data)

Path = r""

#"export" #"import"
#TypeString = "import" 
TypeString = "export"

fileNameString = "ctrlPosData.json"
PatternString =  r".+_Aim_Ctrl$"
ctrlPosData(Path  , TypeString , fileNameString , PatternString)