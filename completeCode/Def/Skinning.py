import maya.cmds as cmds


def Set_CopySkin(Staric, Target, skinType='closestPoint'):
    """
    소스 오브젝트에서 대상 오브젝트로 스킨 가중치를 복사합니다.

    Args:
        Staric (str): 스킨 가중치를 복사해 올 **소스 오브젝트** (스킨 클러스터가 적용된 오브젝트).
        Target (str): 스킨 가중치를 복사할 **대상 오브젝트** (스킨 클러스터가 적용되지 않은 오브젝트).
        skinType (str, optional): 가중치를 복사하는 데 사용할 방법.
                                  'closestPoint', 'closestJoint', 'surface' 등이 있으며, 기본값은 **'closestPoint'**입니다.

    Returns:
        None
    """
    if skinType == '':
        skinType = 'closestPoint'

    BindJnt = cmds.skinCluster(Staric, q=1, wi=1)
    cmds.select(BindJnt)
    cmds.skinCluster(BindJnt, Target, tsb=1)
    cmds.copySkinWeights(Staric, Target, nm=1, sa=skinType, ia=('closestJoint', 'oneToOne'))


def Set_ComponentSkin(Target , SkinTarget , RenderReSet = True):
    """
    대상 오브젝트에 'component' 스키닝을 설정하여 SkinTarget의 컴포넌트 레벨 가중치를 기반으로 스킨 가중치를 설정하고,
    선택적으로 렌더링 속성을 원래대로 복원합니다.

    Args:
        Target (str): 스킨 클러스터가 적용될 **대상 오브젝트**의 트랜스폼 노드 이름.
        SkinTarget (str): 스킨 가중치 정보를 가져올 **소스 오브젝트**의 트랜스폼 노드 이름.
        RenderReSet (bool, optional): 함수 실행 전 대상 및 SkinTarget의 렌더링 관련 속성 값을 저장하고,
                                     함수 완료 후 해당 속성을 원래 값으로 되돌릴지 여부를 결정합니다. 기본값은 **True**입니다.

    Returns:
        str: 생성된 스킨 클러스터 노드의 basePoints[1]에 연결된 노드 (일반적으로 대상 셰이프 노드)의 이름입니다.
             오류 발생 시 **None**을 반환합니다.
    """
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
                try:
                    for Key , Value in Dic.items():
                        cmds.setAttr("{}" .format( Key) , Value)
                except:
                    pass
    return Query