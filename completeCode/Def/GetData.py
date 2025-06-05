import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om



def GetMeshVtx_SequencePos(FirstVtxs , ConversionTuple = True):
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