import maya.cmds as cmds

class SetLimit:
    """
    Maya 오브젝트의 트랜스폼(이동, 회전, 스케일) 및 커스텀 속성에 한계를 설정하는 클래스입니다.
    """
    def __init__(self , Item):
        """
        SetLimit 클래스의 인스턴스를 초기화합니다.

        Args:
            Item (str): 한계를 설정할 Maya 오브젝트의 이름입니다.
        """
        self.Item = Item

    def SetTransform(self , axis , min = -10 , max = 10 , Enable = (1,1)):
        """
        오브젝트의 특정 이동(translate) 축에 대한 한계를 설정합니다.

        Args:
            axis (str): 한계를 설정할 축 ('x', 'y', 'z' 중 하나). 대소문자 구분 없음.
            min (float, optional): 해당 축의 최소 이동 값. 기본값은 **-10**.
            max (float, optional): 해당 축의 최대 이동 값. 기본값은 **10**.
            Enable (tuple, optional): (최소 한계 활성화 여부, 최대 한계 활성화 여부)를 나타내는 튜플.
                                      각 요소는 0(비활성화) 또는 1(활성화)입니다. 기본값은 **(1, 1)** (양쪽 활성화).

        Returns:
            None
        """
        if axis.isupper:
            axis = axis.lower()
        if axis not in {'x', 'y', 'z' , "X" , "Y" , "Z"}:
            raise ValueError("Axis must be 'x', 'y', or 'z'")
        key_limit = "t{}" .format(axis)
        key_enable = "et{}" .format(axis)
        cmds.transformLimits(self.Item,**{key_limit: (min, max),key_enable: Enable })

    def SetRotate(self , axis , min = -90 , max = 90 , Enable = (1,1)):
        """
        오브젝트의 특정 회전(rotate) 축에 대한 한계를 설정합니다.

        Args:
            axis (str): 한계를 설정할 축 ('x', 'y', 'z' 중 하나). 대소문자 구분 없음.
            min (float, optional): 해당 축의 최소 회전 값. 기본값은 **-90**.
            max (float, optional): 해당 축의 최대 회전 값. 기본값은 **90**.
            Enable (tuple, optional): (최소 한계 활성화 여부, 최대 한계 활성화 여부)를 나타내는 튜플.
                                      각 요소는 0(비활성화) 또는 1(활성화)입니다. 기본값은 **(1, 1)** (양쪽 활성화).

        Returns:
            None
        """
        if axis.isupper:
            axis = axis.lower()
        if axis not in {'x', 'y', 'z' , "X" , "Y" , "Z"}:
            raise ValueError("Axis must be 'x', 'y', or 'z'")
        key_limit = "r{}" .format(axis)
        key_enable = "er{}" .format(axis)
        cmds.transformLimits(self.Item,**{key_limit: (min, max),key_enable: Enable })

    def SetScale(self , axis , min = -10 , max = 10 , Enable = (1,1)):
        """
        오브젝트의 특정 스케일(scale) 축에 대한 한계를 설정합니다.

        Args:
            axis (str): 한계를 설정할 축 ('x', 'y', 'z' 중 하나). 대소문자 구분 없음.
            min (float, optional): 해당 축의 최소 스케일 값. 기본값은 **-10**.
            max (float, optional): 해당 축의 최대 스케일 값. 기본값은 **10**.
            Enable (tuple, optional): (최소 한계 활성화 여부, 최대 한계 활성화 여부)를 나타내는 튜플.
                                      각 요소는 0(비활성화) 또는 1(활성화)입니다. 기본값은 **(1, 1)** (양쪽 활성화).

        Returns:
            None
        """
        if axis.isupper:
            axis = axis.lower()
        if axis not in {'x', 'y', 'z' , "X" , "Y" , "Z"}:
            raise ValueError("Axis must be 'x', 'y', or 'z'")
        key_limit = "s{}" .format(axis)
        key_enable = "es{}" .format(axis)
        cmds.transformLimits(self.Item,**{key_limit: (min, max),key_enable: Enable })

    def SetAttr(self ,Attr ,minV = 0 , maxV = 10 , Enable = (1,1)):
        """
        오브젝트의 지정된 커스텀 속성에 대한 최소/최대 값을 설정하고 활성화합니다.

        Args:
            Attr (str): 한계를 설정할 커스텀 속성의 이름입니다. (예: "myCustomAttr").
            minV (float, optional): 속성의 최소 값. 기본값은 **0**.
            maxV (float, optional): 속성의 최대 값. 기본값은 **10**.
            Enable (tuple, optional): (최소 값 활성화 여부, 최대 값 활성화 여부)를 나타내는 튜플.
                                      각 요소는 0(비활성화) 또는 1(활성화)입니다. 기본값은 **(1, 1)** (양쪽 활성화).

        Returns:
            None

        Raises:
            ValueError: 지정된 속성이 오브젝트에 존재하지 않을 경우 발생합니다.
        """
        ItemAttr = "{}.{}" .format(self.Item , Attr)
        if cmds.objExists(ItemAttr):
            cmds.addAttr(ItemAttr , e = 1 , hasMinValue = Enable[0])
            cmds.addAttr(ItemAttr , e = 1 , hasMaxValue = Enable[1])
            if  Enable[0] > 0 :
               cmds.addAttr(ItemAttr , e = 1 , min = minV)

            if  Enable[1] > 0 :
                cmds.addAttr(ItemAttr , e =1 , max = maxV)
        else :
            raise ValueError("Dont Exist Attr {} " .format(ItemAttr ))