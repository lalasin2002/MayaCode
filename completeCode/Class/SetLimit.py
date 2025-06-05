import maya.cmds as cmds

class SetLimit:
    def __init__(self , Item):
        self.Item = Item

    def SetTransform(self , axis  ,min = -10 , max = 10 , Enable = (1,1)):
        if axis.isupper:
            axis = axis.lower()
        if axis not in {'x', 'y', 'z' , "X" , "Y" , "Z"}:
            raise ValueError("Axis must be 'x', 'y', or 'z'")
        key_limit = "t{}" .format(axis)
        key_enable = "et{}" .format(axis)
        cmds.transformLimits(self.Item,**{key_limit: (min, max),key_enable: Enable })

    def SetRotate(self , axis  ,min = -90 , max = 90 , Enable = (1,1)):
        if axis.isupper:
            axis = axis.lower()
        if axis not in {'x', 'y', 'z' , "X" , "Y" , "Z"}:
            raise ValueError("Axis must be 'x', 'y', or 'z'")
        key_limit = "r{}" .format(axis)
        key_enable = "er{}" .format(axis)
        cmds.transformLimits(self.Item,**{key_limit: (min, max),key_enable: Enable })

    def SetScale(self , axis  ,min = -10 , max = 10 , Enable = (1,1)):
        if axis.isupper:
            axis = axis.lower()
        if axis not in {'x', 'y', 'z' , "X" , "Y" , "Z"}:
            raise ValueError("Axis must be 'x', 'y', or 'z'")
        key_limit = "s{}" .format(axis)
        key_enable = "es{}" .format(axis)
        cmds.transformLimits(self.Item,**{key_limit: (min, max),key_enable: Enable })

    def SetAttr(self ,Attr ,minV = 0 , maxV = 10 , Enable = (1,1)):
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