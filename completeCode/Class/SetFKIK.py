import maya.cmds as cmds

class SetFKIK():
    def __init__(self , item  , Attr , Scale_Bool = True):
        self.Scale_Bool = Scale_Bool
        self.Axis = ['X' , 'Y' , 'Z']
        self.RGB = ['R' , 'G' , 'B']
        self.Attr = Attr
        self.item = item

        self.Switch = self.item + '.{}' .format(self.Attr)
        self.Min = cmds.addAttr(self.Switch ,q =1 , min =1)
        self.Max = cmds.addAttr(self.Switch ,q =1 , max =1)


    def Jnt_Array(self , FK_lst , IK_lst , FKIK_lst):
        self.FK_lst = FK_lst
        self.IK_lst = IK_lst
        self.FKIK_lst = FKIK_lst

        if len(self.FKIK_lst) == len(self.FK_lst):
            if len(self.FKIK_lst) == len(self.IK_lst):
                self.Num_Bool = True
            else:
                self.Num_Bool = False
        else:
            self.Num_Bool = False

    def Vis_Array(self, FK_Vis , IK_Vis ):
        self.FK_Vis = FK_Vis
        self.IK_Vis = IK_Vis
        if not self.FK_Vis == '':
            if not self.IK_Vis == '':
                self.Vis_Bool = True
            else:
                self.Vis_Bool = False
        else:
            self.Vis_Bool = False

        if self.Vis_Bool == True:
            self.FK_Vis = self.FK_Vis + '.visibility'
            self.IK_Vis = self.IK_Vis + '.visibility'



    def Build(self):
        if self.Num_Bool == True:
            BC = cmds.createNode('blendColors' , n = '{}_FKIK_BC' .format(self.item))
            Clean1 = [ cmds.setAttr(BC + '.color1{}' .format(x), 0)  for x in  self.RGB ]
            Clean2 = [ cmds.setAttr(BC + '.color2{}'.format(x), 0) for x in self.RGB]

            cmds.setAttr(BC + '.color1G',1)
            cmds.setAttr(BC + '.color2R',1)

            cmds.setAttr(self.Switch, self.Min)
            cmds.setAttr(BC + '.blender' , 0)
            cmds.setDrivenKeyframe(BC + '.blender' , cd = self.Switch, itt = 'linear' , ott ='linear')

            cmds.setAttr(self.Switch, self.Max)
            cmds.setAttr(BC + '.blender' , 1)
            cmds.setDrivenKeyframe(BC + '.blender', cd=self.Switch, itt='linear', ott='linear')

            cmds.setAttr(self.Switch, self.Min) # setAttr Default

            for x in range(len(self.FKIK_lst)):
                CP = cmds.parentConstraint(self.FK_lst[x] , self.IK_lst[x] , self.FKIK_lst[x] ,mo =1)[0]

                cmds.connectAttr(BC + '.outputR' , CP + '.{}W0' .format(self.FK_lst[x]),f=1)
                cmds.connectAttr(BC + '.outputG', CP + '.{}W1'.format(self.IK_lst[x]),f =1)


            if self.Vis_Bool == True:
                cmds.connectAttr(BC + '.outputR' , self.FK_Vis ,f =1)
                cmds.connectAttr(BC + '.outputG', self.IK_Vis, f=1)


            if self.Scale_Bool == True:
                SD = cmds.listConnections(BC , d =0 , s =1 , type='animCurve')[0]

                for x in range(0,len(self.FKIK_lst)):
                    BC_Scale = cmds.createNode('blendColors' , n = '{}_FKIK_BC' .format(self.FKIK_lst[x]))
                    Clean1 = [cmds.setAttr(BC_Scale + '.color1{}'.format(a), 0) for a in self.RGB]
                    Clean2 = [cmds.setAttr(BC_Scale + '.color2{}'.format(a), 0) for a in self.RGB]

                    cmds.connectAttr(SD + '.output', BC_Scale + '.blender',f =1)
                    for y in range(0, len(self.Axis)):

                        cmds.connectAttr( self.IK_lst[x] + '.scale' + self.Axis[y] , BC_Scale + '.color1' + self.RGB[y], f=1)
                        cmds.connectAttr( self.FK_lst[x] + '.scale' + self.Axis[y], BC_Scale + '.color2' + self.RGB[y], f=1)

                        cmds.connectAttr(BC_Scale + '.output' + self.RGB[y] ,self.FKIK_lst[x] + '.scale' + self.Axis[y] ,f =1 )