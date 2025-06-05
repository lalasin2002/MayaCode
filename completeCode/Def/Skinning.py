import maya.cmds as cmds



def Set_CopySkin(Staric, Target, skinType='closestPoint'):
    if skinType == '':
        skinType = 'closestPoint'

    BindJnt = cmds.skinCluster(Staric, q=1, wi=1)
    cmds.select(BindJnt)
    cmds.skinCluster(BindJnt, Target, tsb=1)
    cmds.copySkinWeights(Staric, Target, nm=1, sa=skinType, ia=('closestJoint', 'oneToOne'))


def Set_ComponentSkin(Target , SkinTarget , RenderReSet = True):
    Target = cmds.listRelatives(Target ,s =1)
    SkinTarget = cmds.listRelatives(SkinTarget ,s =1)
    Query = None
    
    if len(Target) >= 1 and len(SkinTarget)  >= 1:
        Target =Target[0]
        SkinTarget =SkinTarget[0]
        Diclst = []
        Skin_Dic = {}   
        Tgt_Dic = {} 
        if RenderReSet:
            lstAttr = ['castsShadows', 'receiveShadows', 'holdOut', 'motionBlur', 'primaryVisibility', 'smoothShading', 'visibleInReflections', 'visibleInRefractions', 'doubleSided']
            try:
                for x in range(len(lstAttr)):
                    SkinTgtGetValue = cmds.getAttr('{}.{}'.format(SkinTarget, lstAttr[x]))
                    TgtGetValue = cmds.getAttr('{}.{}'.format(Target, lstAttr[x]))
                    SkinAttr = "{}.{}" .format(SkinTarget , lstAttr[x])
                    TgtAttr = "{}.{}" .format(Target , lstAttr[x])
                    
                    Skin_Dic[SkinAttr] = SkinTgtGetValue
                    Tgt_Dic[TgtAttr] = TgtGetValue
                Diclst = [Skin_Dic , Tgt_Dic] 
            except:
                pass
            
        cmds.select(cl =1)
        Jnt = cmds.joint(n = "Pre_{}_CONT_Jnt" .format(Target))
        Skin = cmds.skinCluster(Jnt , Target)
        cmds.select(Target)
        cmds.select( SkinTarget , add = True )
        cmds.skinCluster(Skin[0] ,e =1, dr =4 , ps =0 ,tsb =1 , ug =1,  wt =0 ,ns = 10 ,ai = SkinTarget ,  dt  =1 )
        Query = cmds.listConnections("{}.basePoints[1]" .format(Skin[0]) , d =1 )[0]

        cmds.setAttr("{}.weightList[0].weights[0]" .format(Skin[0]) , 0)
        cmds.setAttr("{}.weightList[0].weights[1]" .format(Skin[0]) , 1)
        cmds.skinCluster(Skin[0] , e =1 , ri = Jnt)
        cmds.delete(Jnt )
        cmds.setAttr( "{}.useComponents".format(Skin[0]) , 1)

        if len(Diclst) >=1:
            for Dic in Diclst:
                #pprint.pprint(Dic)
                try:
                    for Key , Value in Dic.items():
                        cmds.setAttr("{}" .format( Key) , Value)    
                except:
                    pass
    return Query

