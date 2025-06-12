import maya.cmds as cmds

class SetFKIK():
    """
    Maya에서 FK/IK 스위치 시스템을 설정하는 클래스입니다.
    FK 조인트, IK 조인트, 최종 FK/IK 조인트 간의 블렌딩을 제어하며,
    선택적으로 컨트롤러나 기타 오브젝트의 가시성 및 스케일 블렌딩을 처리합니다.
    """
    def __init__(self , item , Attr , Scale_Bool = True):
        """
        SetFKIK 클래스를 초기화합니다.

        Args:
            item (str): FK/IK 스위치를 위한 커스텀 속성을 추가할 메인 컨트롤러나 오브젝트의 이름입니다.
            Attr (str): 'item' 오브젝트에 추가될 FK/IK 스위치 속성의 이름입니다.
            Scale_Bool (bool, optional): 스케일 블렌딩을 설정할지 여부를 결정합니다. 기본값은 **True**입니다.
        """
        self.Scale_Bool = Scale_Bool
        self.Axis = ['X' , 'Y' , 'Z']
        self.RGB = ['R' , 'G' , 'B']
        self.Attr = Attr
        self.item = item

        self.Switch = self.item + '.{}' .format(self.Attr)
        # 이미 존재하는 속성에서 min/max 값을 쿼리합니다.
        # 이 부분은 'item'에 'Attr' 속성이 이미 있고 min/max 값이 설정되어 있다고 가정합니다.
        self.Min = cmds.addAttr(self.Switch ,q =1 , min =1)
        self.Max = cmds.addAttr(self.Switch ,q =1 , max =1)


    def Jnt_Array(self , FK_lst , IK_lst , FKIK_lst):
        """
        FK, IK, 그리고 최종 FK/IK 조인트 목록을 클래스에 등록합니다.
        목록들의 길이가 일치하는지 확인하여 유효성을 검사합니다.

        Args:
            FK_lst (list): FK 리그를 구성하는 조인트 이름의 리스트입니다.
            IK_lst (list): IK 리그를 구성하는 조인트 이름의 리스트입니다.
            FKIK_lst (list): 최종적으로 블렌딩된 FK/IK 애니메이션을 받을 조인트 이름의 리스트입니다.
        """
        self.FK_lst = FK_lst
        self.IK_lst = IK_lst
        self.FKIK_lst = FKIK_lst

        # 조인트 목록들의 길이가 모두 같은지 확인합니다.
        if len(self.FKIK_lst) == len(self.FK_lst):
            if len(self.FKIK_lst) == len(self.IK_lst):
                self.Num_Bool = True
            else:
                self.Num_Bool = False
        else:
            self.Num_Bool = False

    def Vis_Array(self, FK_Vis , IK_Vis ):
        """
        FK 및 IK 컨트롤러나 오브젝트의 가시성 제어를 위한 대상을 등록합니다.
        지정된 대상의 가시성 속성에 '.visibility'를 추가합니다.

        Args:
            FK_Vis (str): FK 컨트롤러(또는 관련 오브젝트)의 가시성을 제어할 대상의 이름입니다.
            IK_Vis (str): IK 컨트롤러(또는 관련 오브젝트)의 가시성을 제어할 대상의 이름입니다.
        """
        self.FK_Vis = FK_Vis
        self.IK_Vis = IK_Vis
        self.Vis_Bool = False # 초기값 설정

        # 가시성 대상이 비어있지 않은지 확인합니다.
        if self.FK_Vis != '' and self.IK_Vis != '':
            self.Vis_Bool = True

        if self.Vis_Bool == True:
            # 가시성 속성의 전체 경로를 구성합니다.
            self.FK_Vis = self.FK_Vis + '.visibility'
            self.IK_Vis = self.IK_Vis + '.visibility'


    def Build(self):
        """
        FK/IK 스위치 시스템을 구축합니다.
        'blendColors' 노드를 사용하여 조인트의 부모 제약 가중치와 가시성을 제어하며,
        'Scale_Bool'이 True인 경우 스케일 블렌딩을 추가로 설정합니다.
        """
        if self.Num_Bool == True: # 조인트 목록의 유효성 검사 통과 시
            # 메인 블렌드 컬러 노드를 생성하여 FK/IK 전환을 제어합니다.
            BC = cmds.createNode('blendColors' , n = '{}_FKIK_BC' .format(self.item))
            # color1과 color2의 RGB 값을 0으로 초기화합니다.
            Clean1 = [ cmds.setAttr(BC + '.color1{}' .format(x), 0)   for x in   self.RGB ]
            Clean2 = [ cmds.setAttr(BC + '.color2{}'.format(x), 0) for x in self.RGB]

            # IK (R)와 FK (G) 블렌딩을 위한 컬러 값을 설정합니다.
            cmds.setAttr(BC + '.color1G',1) # IK가 활성화될 때 (blender=0) G 채널 출력
            cmds.setAttr(BC + '.color2R',1) # FK가 활성화될 때 (blender=1) R 채널 출력

            # 드라이븐 키프레임을 설정하여 스위치 속성으로 블렌더를 제어합니다.
            cmds.setAttr(self.Switch, self.Min) # 스위치 최소값일 때
            cmds.setAttr(BC + '.blender' , 0) # 블렌더를 0으로 설정
            cmds.setDrivenKeyframe(BC + '.blender' , cd = self.Switch, itt = 'linear' , ott ='linear') # 키프레임 생성

            cmds.setAttr(self.Switch, self.Max) # 스위치 최대값일 때
            cmds.setAttr(BC + '.blender' , 1) # 블렌더를 1로 설정
            cmds.setDrivenKeyframe(BC + '.blender', cd=self.Switch, itt='linear', ott='linear') # 키프레임 생성

            cmds.setAttr(self.Switch, self.Min) # 스위치 속성 값을 기본값(최소값)으로 다시 설정

            # 각 FK/IK 조인트 쌍에 대해 parentConstraint를 생성하고 블렌딩을 연결합니다.
            for x in range(len(self.FKIK_lst)):
                # FK 조인트와 IK 조인트를 최종 FK/IK 조인트에 부모 제약합니다.
                CP = cmds.parentConstraint(self.FK_lst[x] , self.IK_lst[x] , self.FKIK_lst[x] ,mo =1)[0]

                # blendColors 노드의 출력을 parentConstraint의 가중치에 연결합니다.
                # outputR (FK)을 FK 조인트의 가중치에, outputG (IK)를 IK 조인트의 가중치에 연결합니다.
                cmds.connectAttr(BC + '.outputR' , CP + '.{}W0' .format(self.FK_lst[x]),f=1)
                cmds.connectAttr(BC + '.outputG', CP + '.{}W1'.format(self.IK_lst[x]),f =1)


            # 가시성 제어 대상이 설정된 경우 가시성 블렌딩을 연결합니다.
            if self.Vis_Bool == True:
                cmds.connectAttr(BC + '.outputR' , self.FK_Vis ,f =1) # FK 가시성 연결
                cmds.connectAttr(BC + '.outputG', self.IK_Vis, f=1) # IK 가시성 연결


            # 스케일 블렌딩이 활성화된 경우 스케일 블렌딩을 설정합니다.
            if self.Scale_Bool == True:
                # 메인 blendColors 노드에 연결된 animCurve 노드를 찾습니다.
                SD = cmds.listConnections(BC , d =0 , s =1 , type='animCurve')[0]

                # 각 조인트에 대해 스케일 블렌딩 노드를 생성합니다.
                for x in range(0,len(self.FKIK_lst)):
                    BC_Scale = cmds.createNode('blendColors' , n = '{}_FKIK_BC' .format(self.FKIK_lst[x]))
                    # 스케일 블렌드 컬러 노드의 color1과 color2의 RGB 값을 0으로 초기화합니다.
                    Clean1 = [cmds.setAttr(BC_Scale + '.color1{}'.format(a), 0) for a in self.RGB]
                    Clean2 = [cmds.setAttr(BC_Scale + '.color2{}'.format(a), 0) for a in self.RGB]

                    # 메인 animCurve의 출력을 스케일 블렌드 컬러 노드의 blender에 연결합니다.
                    cmds.connectAttr(SD + '.output', BC_Scale + '.blender',f =1)
                    for y in range(0, len(self.Axis)):
                        # IK 조인트의 스케일 출력을 color1에 연결합니다.
                        cmds.connectAttr( self.IK_lst[x] + '.scale' + self.Axis[y] , BC_Scale + '.color1' + self.RGB[y], f=1)
                        # FK 조인트의 스케일 출력을 color2에 연결합니다.
                        cmds.connectAttr( self.FK_lst[x] + '.scale' + self.Axis[y], BC_Scale + '.color2' + self.RGB[y], f=1)

                        # 스케일 블렌드 컬러 노드의 출력을 최종 FK/IK 조인트의 스케일에 연결합니다.
                        cmds.connectAttr(BC_Scale + '.output' + self.RGB[y] ,self.FKIK_lst[x] + '.scale' + self.Axis[y] ,f =1 )