import maya.cmds as cmds


class Main(object):
    def __init__(self):
        self.list = []
        self.listA = []
        self.listB = []
        self.listC = []
        self.listD = []
        self.All = []


class Hide_Lock_Att():
    def __init__(self, TGT, Att, Lock, Hide):
        self.TGT = TGT
        self.Att = Att
        self.Lock = Lock
        self.Hide = Hide

        for x in Att:
            cmds.setAttr(self.TGT + '.' + x, k=Hide, l=Lock)


class Jnt_DrawType():
    def __init__(self, TGT, type):
        self.TGT = TGT
        self.type = type
        cmds.setAttr(self.TGT + '.drawStyle', self.type)


class Grp_Set_item(Main):
    def __init__(self, TGT, val):
        grp_name = ['set_', 'grp_', 'prime_', 'grp_prime_']
        Main.__init__(self)

        self.TGT = TGT
        self.val = val
        lst = []
        for x in range(0, self.val):
            grp = cmds.createNode('transform', n=grp_name[x] + self.TGT)
            self.list.append(grp)
        for x in range(0, len(self.list)):
            try:
                cmds.parent(self.list[x], self.list[x + 1])
            except:
                pass
        cmds.parentConstraint(self.TGT, self.list[-1], mo=0)
        Find = cmds.listRelatives(self.list[-1], type='parentConstraint')
        cmds.delete(Find[0])

        cmds.parent(TGT, self.list[0])
        self.list.insert(0, self.TGT)


class Grp_Set_list(Main):
    def __init__(self, TGT, val):
        grp_name = ['set_', 'grp_', 'prime_', 'grp_prime_']
        Main.__init__(self)
        self.TGT = TGT
        self.val = val
        for t in range(0, len(self.TGT)):
            item_list = []

            for x in range(0, self.val):
                grp = cmds.createNode('transform', n=grp_name[x] + self.TGT[t])

                cmds.parentConstraint(self.TGT[t], grp, mo=0)
                Find = cmds.listRelatives(grp, type='parentConstraint')
                cmds.delete(Find[0])

                if x == 0:
                    item_list.append(self.TGT[t])
                    item_list.append(grp)
                    cmds.parent(self.TGT[t], grp)
                else:
                    try:
                        item_list.append(grp)
                        cmds.parent(item_list[x], item_list[x + 1])
                    except:
                        pass

            self.list.append(item_list)


class jnt_Ctrl_Setting():
    def __init__(self, TGT, Shp, Trans, Axis, ScaleX, ScaleY, ScaleZ):

        self.TGT = TGT
        self.Shp = Shp
        self.ScaleX = ScaleX
        self.ScaleY = ScaleY
        self.ScaleZ = ScaleZ
        self.Axis = Axis
        self.Trans = Trans

        if self.Shp == 'circle':
            Ctrl_Shp = cmds.circle(nr=(0, 1, 0))

        elif self.Shp == 'triangle':
            Ctrl_Shp = cmds.curve(d=1, p=[(-1, 0, -1), (0, 0, 1), (1, 0, -1), (-1, 0, -1)], k=[0, 1, 2, 3])

        elif self.Shp == 'square':
            Ctrl_Shp = cmds.curve(d=1, p=[(-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1), (-1, 0, -1)])

        elif self.Shp == 'round_square':
            Ctrl_Shp = cmds.curve(d=3,
                                  p=[(-1, 0, 0), (-1, 0, 0.333), (-1, 0, 0.444), (-1, 0, 0.500), (-0.951, 0, 0.684),
                                     (-0.835, 0, 0.835), (-0.684, 0, 0.951), (-0.500, 0, 1), (-0.444, 0, 1),
                                     (-0.333, 0, 1), (0, 0, 1), (0.333, 0, 1), (0.444, 0, 1), (0.500, 0, 1),
                                     (0.684, 0, 0.951), (0.835, 0, 0.835), (0.951, 0, 0.684), (1, 0, 0.500),
                                     (1, 0, 0.444), (1, 0, 0.333), (1, 0, 0), (1, 0, -0.333), (1, 0, -0.444),
                                     (1, 0, -0.500), (0.951, 0, -0.684), (0.835, 0, -0.835), (0.684, 0, -0.951),
                                     (0.500, 0, -1), (0.444, 0, -1), (0.333, 0, -1), (0, 0, -1), (-0.333, 0, -1),
                                     (-0.444, 0, -1), (-0.500, 0, -1), (-0.684, 0, -0.951), (-0.835, 0, -0.835),
                                     (-0.951, 0, -0.684), (-1, 0, -0.500), (-1, 0, -0.444), (-1, 0, -0.333),
                                     (-1, 0, 0)])

        elif self.Shp == 'cube':
            Ctrl_Shp = cmds.curve(d=1,
                                  p=[(1, 1, 1), (1, 1, -1), (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, -1, 1), (1, -1, -1),
                                     (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (-1, -1, -1), (-1, -1, 1),
                                     (-1, 1, 1), (-1, -1, 1), (1, -1, 1)],
                                  k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

        elif self.Shp == 'orbs':
            Ctrl_Shp = cmds.createNode('transform', n='prefix_Ctrl')

            for x in range(0, 3):
                Ctrl_Orb = cmds.circle(nr=(0, 1, 0), r=0.25)
                if x == 0:
                    cmds.setAttr(Ctrl_Orb[0] + '.rotateX', 90)
                elif x == 1:
                    cmds.setAttr(Ctrl_Orb[0] + '.rotateX', 90)
                    cmds.setAttr(Ctrl_Orb[0] + '.rotateY', 90)
                else:
                    pass

                cmds.makeIdentity(Ctrl_Orb[0], apply=True, r=1)

                Find = cmds.listRelatives(Ctrl_Orb[0], s=1, type='shape')
                cmds.parent(Find[0], Ctrl_Shp, r=1, s=1)
                cmds.delete(Ctrl_Orb[0])

        elif self.Shp == 'arrow':
            Ctrl_Shp = cmds.curve(d=1,
                                  p=[(-1, 0, -2), (-1, 0, 0), (-2, 0, 0), (0, 0, 2), (2, 0, 0), (1, 0, 0), (1, 0, -2),
                                     (-1, 0, -2)], k=[0, 1, 2, 3, 4, 5, 6, 7])

        if self.Axis == 'X':
            Vector = '.translateX'
            Dir_val = 1
            Trans_setX = Dir_val * self.Trans
            Trans_setY = 0
            Trans_setZ = 0

            cmds.setAttr(Ctrl_Shp + '.rotateZ', 90)
        elif self.Axis == '-X':
            Vector = '.translateX'
            Dir_val = -1
            Trans_setX = Dir_val * self.Trans
            Trans_setY = 0
            Trans_setZ = 0

            cmds.setAttr(Ctrl_Shp + '.rotateZ', -90)
        elif self.Axis == 'Y':
            Vector = '.translateY'
            Dir_val = 1
            Trans_setX = 0
            Trans_setY = Dir_val * self.Trans
            Trans_setZ = 0

            cmds.setAttr(Ctrl_Shp + '.rotateX', 0)
        elif self.Axis == '-Y':
            Vector = '.translateY'
            Dir_val = -1
            Trans_setX = 0
            Trans_setY = Dir_val * self.Trans
            Trans_setZ = 0

            cmds.setAttr(Ctrl_Shp + '.rotateX', 0)
        elif self.Axis == 'Z':
            Vector = '.translateZ'
            Dir_val = 1
            Trans_setX = 0
            Trans_setY = 0
            Trans_setZ = Dir_val * self.Trans

            cmds.setAttr(Ctrl_Shp + '.rotateX', 90)

        elif self.Axis == '-Z':
            Vector = '.translateZ'
            Dir_val = -1
            Trans_setX = 0
            Trans_setY = 0
            Trans_setZ = Dir_val * self.Trans

            cmds.setAttr(Ctrl_Shp + '.rotateX', 90)
        cmds.makeIdentity(Ctrl_Shp, apply=True, r=1, s=1)

        Find = cmds.listRelatives(Ctrl_Shp, s=1, type='shape')
        CV_list = []
        for x in range(0, len(Find)):
            CV = cmds.ls(Find[x] + '.cv[:]', fl=1)
            for y in CV:
                CV_list.append(y)
        cmds.select(CV_list)
        cmds.scale(self.ScaleX, self.ScaleY, self.ScaleZ, r=1, cp=1)
        cmds.move(Trans_setX, Trans_setY, Trans_setZ, r=1, os=1, wd=1)

        cmds.makeIdentity(Ctrl_Shp, apply=True, r=1, s=1)

        Find = cmds.listRelatives(Ctrl_Shp, type='shape')
        for x in range(0, len(Find)):
            cmds.parent(Find[x], self.TGT, r=1, s=1)
            cmds.rename(Find[x], self.TGT + str(x + 1) + 'shape')
        cmds.delete(Ctrl_Shp)

        if cmds.objectType(self.TGT) == "joint":
            cmds.setAttr(self.TGT + ".drawStyle", 2)


class Match_Mrt():
    def __init__(self, TGT01, TGT02, Trans, Rot, Par):
        self.Par = Par
        self.Trans = Trans
        self.Rot = Rot

        self.TGT01 = TGT01
        self.TGT02 = TGT02

        P = cmds.listRelatives(self.TGT01, p=1)

        Grp = cmds.createNode('transform', n='PreFix_' + self.TGT01)
        CP = cmds.parentConstraint(self.TGT01, Grp, mo=0)

        cmds.delete(CP[0])
        cmds.parent(self.TGT01, Grp)

        if self.Trans == 1:
            PO = cmds.pointConstraint(self.TGT02, Grp)
            cmds.delete(PO[0])
        else:
            pass
        if self.Rot == 1:
            OR = cmds.orientConstraint(self.TGT02, Grp)
            cmds.delete(OR[0])
        else:
            pass

        cmds.parent(self.TGT01, w=1)
        cmds.delete(Grp)
        if self.Par == 1:
            try:
                cmds.parent(self.TGT01, P[0])
            except:
                pass
        else:
            pass


class Eyelid_UI():
    def __init__(self):
        self.Axis = ['X', 'Y', 'Z']
        self.sAxis = ['x', 'y', 'z']
        self.DirectBase = ['L', 'M', 'R']
        self.Vertical = ['Up', 'Dw']
        self.width = 300
        if cmds.window("Eyelid_rig_window", exists=True):
            cmds.deleteUI("Eyelid_rig_window")
        my_window = cmds.window("Eyelid_rig_window", title="Eyelid_rig_window", s=1, w=self.width);
        LY_Main = cmds.columnLayout(columnAlign="center")

        cmds.text(al='center', w=self.width, l='1.Eyelid rig', bgc=(0.13, 0.13, 0.13), h=self.width / 20,
                  fn='boldLabelFont')

        LYrow01 = cmds.rowColumnLayout(nc=2, cw=[(1, self.width / 2.5), (2, self.width / 1.6666)])
        cmds.text(l="Side Guide Count : ", al='right')
        self.IF_SideCount = cmds.intField(v=2, min=1, max=5)
        cmds.text(l="Vertical Guide Count : ", al='right')
        self.IF_VerticalCount = cmds.intField(v=2, min=1, max=5)

        cmds.setParent('..')
        self.Btn_CreateGuide = cmds.button(l='Create Guide', w=self.width, c=lambda x: self.set_Create_Guide())
        cmds.separator(h=2, style='double')
        self.Btn_Build = cmds.button(l='Build Guide', w=self.width, bgc=(1, 0, 0), c=lambda x: self.set_Build())

        cmds.showWindow()

    def set_Create_Guide(self):
        self.pre_Create_Guide("L")

    def pre_Create_Guide(self, Side):
        self.Side = Side
        self.Input_SideCount = cmds.intField(self.IF_SideCount, q=1, v=1)
        self.Input_VerticalCount = cmds.intField(self.IF_VerticalCount, q=1, v=1)

        self.Guide_Up_list = []
        self.Guide_Dw_list = []

        self.Guide_Subs_Up_list = []
        self.Guide_Subs_Dw_list = []

        self.Guide_Side_list = []
        self.Guide_Main_list = []

        self.Guide_Aim_list = []
        self.Guide_Aim_Detail_list = []
        self.Guide_Aim_Cir_val_list = []

        self.Guide_Aim_DTroot_list = []

        cmds.select(cl=1)
        Main = cmds.joint(n='Guide_Eyelid_' + self.Side + '_Main', rad=5)

        self.Guide_Main_list.append(Main)
        self.MidValue = self.Input_SideCount * 2 // 2
        for x in range(0, 2):
            All_pre_list = []

            All_Aim_list = []
            if x == 0:
                Ver = self.Vertical[0]
                Ver_val = 0.33
            else:
                Ver = self.Vertical[1]
                Ver_val = -0.33

            cmds.select(cl=1)

            All = cmds.joint(n='Guide_Eyelid_' + self.Side + '_All_' + Ver, rad=3.5)
            nodeDT = cmds.createNode('distanceBetween', n='DT_Guide_' + self.Side + '_' + Ver)
            Cir = cmds.circle(n='Guide_Cir_' + self.Side + '_' + Ver, nr=(1, 0, 0))

            cmds.move(0, Ver_val, 0, All)

            cmds.parentConstraint(All, Cir[0])
            cmds.parent(Cir[0], All)

            cmds.setAttr(Cir[0] + '.overrideEnabled', 1)
            cmds.setAttr(Cir[0] + '.overrideDisplayType', 1)
            cmds.setAttr(All + '.drawLabel', 1)
            cmds.setAttr(All + '.type', 18)
            if x == 0:
                cmds.setAttr(All + '.otherType', 'Up_All', type='string')
            else:
                cmds.setAttr(All + '.otherType', 'Dw_All', type='string')

            cmds.connectAttr(All + '.worldMatrix[0]', nodeDT + '.inMatrix1')
            cmds.connectAttr(nodeDT + '.distance', Cir[1] + '.radius')

            self.Guide_Main_list.append(All)

            for y in range(0, self.Input_SideCount * 2 + 1):
                Aim_list = []

                cmds.select(cl=1)
                loc = cmds.joint(n='Guide_Eyelid_' + self.Side + '_' + Ver + '_' + chr(65 + y), rad=1.5)

                cmds.move((-(self.Input_SideCount * 0.66) - 0.66) + ((y * 0.66) + 0.66), Ver_val, 2.5, loc)
                if x == 0:
                    if y == 0:
                        cmds.select(cl=1)
                        loc01 = cmds.joint(n='Guide_Eyelid_In_' + self.Side, rad=1.5)

                        cmds.move((-(self.Input_SideCount * 0.66) - (0.66 * 2)) + ((y * 0.66) + 0.66), 0, 2.5, loc01)
                        cmds.parent(loc01, Main)

                        self.Guide_Side_list.append(loc01)

                    elif y == self.Input_SideCount * 2:
                        cmds.select(cl=1)
                        loc01 = cmds.joint(n='Guide_Eyelid_' + self.Side + '_Out', rad=1.5)
                        cmds.move((-(self.Input_SideCount * 0.66) - (0.66)) + ((y * 0.66) + (0.66 * 2)), 0, 2.5, loc01)
                        cmds.parent(loc01, Main)

                        self.Guide_Side_list.append(loc01)

                    self.Guide_Up_list.append(loc)
                else:
                    self.Guide_Dw_list.append(loc)

                All_loc = cmds.createNode('transform', n='All_Guide_Aim_' + self.Side + '_' + Ver + '_' + chr(65 + y))

                Aim01 = cmds.spaceLocator(n='Guide_Aim_locStart_' + self.Side + '_' + Ver + '_' + chr(65 + y))
                Aim02 = cmds.spaceLocator(n='Guide_Aim_locEnd_' + self.Side + '_' + Ver + '_' + chr(65 + y))
                AimVector = cmds.spaceLocator(n='Guide_Vector_' + self.Side + '_' + Ver + '_' + chr(65 + y))
                AimTGT = cmds.spaceLocator(n='Guide_Aim_TGT_' + self.Side + '_' + Ver + '_' + chr(65 + y))

                cmds.move((-(self.Input_SideCount * 0.66) - 0.66) + ((y * 0.66) + 0.66), Ver_val, 0, All_loc)
                cmds.move( Ver_val, 0, Aim01[0])
                cmds.move( Ver_val, 0, Aim02[0])
                cmds.move( Ver_val, 0, AimVector[0])
                cmds.move((-(self.Input_SideCount * 0.66) - 0.66) + ((y * 0.66) + 0.66), Ver_val, 0, AimTGT[0])

                cmds.setAttr(Aim01[0] + '.visibility', 0)
                cmds.setAttr(Aim02[0] + '.visibility', 0)
                cmds.setAttr(AimVector[0] + '.visibility', 0)
                cmds.setAttr(AimTGT[0] + '.visibility', 0)

                cmds.parent(Aim01[0], AimVector[0], Aim02[0], AimTGT[0], All_loc)
                cmds.parent(Aim02[0], Aim01[0])
                cmds.parent(loc, All_loc, All)

                cmds.parentConstraint(Aim02[0], AimTGT[0], mo=1)
                cmds.aimConstraint(loc, Aim01[0], mo=0, aim=[0, 0, 1], upVector=[0, 1, 0], worldUpVector=[0, 1, 0],
                                   worldUpType="objectrotation", worldUpObject=AimVector[0])

                Aim_list.append(Aim01[0])
                Aim_list.append(Aim02[0])
                Aim_list.append(AimVector[0])
                Aim_list.append(AimTGT[0])
                if y == self.MidValue:
                    cmds.addAttr(loc, ln='End_Rotate', at="float", k=1)
                    # cmds.connectAttr(loc + '.End_Rotate', Aim02[0] + '.rotateX')
                    cmds.connectAttr(loc + '.worldMatrix[0]', nodeDT + '.inMatrix2')
                    GetValue = Cir[1] + '.radius'
                    self.Guide_Aim_Cir_val_list.append(GetValue)
                else:
                    pass

                total = 1.0
                value = self.Input_VerticalCount + 1
                Dv = total / value

                pre_list = []

                for z in range(0, self.Input_VerticalCount + 2):
                    cmds.select(cl=1)
                    Subs_root = cmds.joint(
                        n='Guide_Eyelid_root_' + self.Side + '_' + Ver + '_' + chr(65 + y) + str(z + 1) + '_Detail',
                        rad=0.25)
                    cmds.select(cl=1)
                    Subs = cmds.joint(
                        n='Guide_Eyelid_' + self.Side + '_' + Ver + '_' + chr(65 + y) + str(z + 1) + '_Detail',
                        rad=0.25)

                    cmds.setAttr(Subs_root + '.overrideEnabled', 1)
                    cmds.setAttr(Subs_root + '.overrideDisplayType', 1)

                    Match_Mrt(Subs_root, All, 1, 1, 0)
                    Match_Mrt(Subs, loc, 1, 1, 0)

                    cmds.setAttr(Subs_root + '.overrideEnabled', 1)
                    cmds.setAttr(Subs_root + '.overrideDisplayType', 1)

                    cmds.pointConstraint(Aim01[0] , Aim02[0] , Subs_root , mo =1 )
                    CP = cmds.orientConstraint(Aim01[0], Aim02[0], Subs_root, mo=0)

                    Match_Mrt(Subs, loc, 1, 1, 0)
                    cmds.parent(Subs, Subs_root)
                    cmds.parent(Subs_root, All)


                    cmds.connectAttr(nodeDT + '.distance', Subs + '.translateZ')

                    CP_Val = Dv * z
                    r_CP_Val = 1.0 - CP_Val

                    cmds.setAttr(CP[0] + '.' + Aim01[0] + 'W0', r_CP_Val)
                    cmds.setAttr(CP[0] + '.' + Aim02[0] + 'W1', CP_Val)
                    if z == 0:
                        pre_list.append(Subs_root)

                    elif z == self.Input_VerticalCount + 1:
                        pre_list.append(Subs_root)
                    else:
                        pass
                All_pre_list.append(pre_list)

                All_Aim_list.append(Aim_list)
            self.Guide_Aim_DTroot_list.append(All_pre_list)
            self.Guide_Aim_list.append(All_Aim_list)

        for x in range(0, 2):
            if x == 0:
                list = self.Guide_Up_list
            else:
                list = self.Guide_Dw_list
            for y in range(0, len(list)):
                cmds.connectAttr(list[self.MidValue] + '.End_Rotate', self.Guide_Aim_list[x][y][1] + '.rotateX')

        cmds.parent(self.Guide_Main_list[1], self.Guide_Main_list[0])
        cmds.parent(self.Guide_Main_list[2], self.Guide_Main_list[0])

    def set_Build(self):
        print('>>>root>>>', self.Guide_Aim_DTroot_list)
        self.pre_Build("L")

    def pre_Build(self, Side):
        print(self.Guide_Up_list)
        print(self.Guide_Dw_list)

        # print (self.Guide_Subs_Up_list )
        # print (self.Guide_Subs_Dw_list )

        print(self.Guide_Side_list)
        print(self.Guide_Main_list)
        print(self.Guide_Aim_Detail_list)

        self.Side = Side

        Up_AimTGT_list = []
        Dw_AimTGT_list = []
        Up_AimTGT_Start_list = []
        Dw_AimTGT_Start_list = []
        Up_AimTGT_End_list = []
        Dw_AimTGT_End_list = []

        Side_AimTGT_list = []

        Side_Detail_list = []
        Up_Detail_list = []
        Dw_Detail_list = []

        Side_locAim_list = []

        Main_list = []

        cmds.select(cl=1)

        Main_Ctrl = cmds.joint(n='Eyelid_Main_' + self.Side + '_Ctrl')
        Match_Mrt(Main_Ctrl, self.Guide_Main_list[0], 1, 1, 0)
        All_Side_Aim = cmds.createNode('transform', n='All_Side_Aim_Eyelid_' + self.Side)

        Main_list.append(Main_Ctrl)

        for x in range(0, 2):
            if x == 0:
                Ver = self.Vertical[0]
                Guidelist = self.Guide_Up_list
            else:
                Ver = self.Vertical[1]
                Guidelist = self.Guide_Dw_list

            All = cmds.createNode('transform', n='All_Eyelid_' + self.Side + '_' + Ver)
            All_Detail = cmds.createNode('transform', n='All_Eyelid_' + self.Side + '_' + Ver + '_Detail')
            All_Aim_main = cmds.createNode('transform', n='All_Aim_Eyelid_' + self.Side + '_' + Ver)

            locVector = cmds.spaceLocator(n='loc_Vector_' + self.Side + '_' + Ver)
            cmds.setAttr(locVector[0] + '.visibility', 0)

            Match_Mrt(All_Aim_main, self.Guide_Main_list[x + 1], 1, 1, 0)
            Match_Mrt(All_Side_Aim, self.Guide_Main_list[x], 1, 1, 0)
            Match_Mrt(locVector[0], self.Guide_Main_list[x], 1, 1, 0)

            Eyelid_Vector = Grp_Set_item(locVector[0], 1)

            cmds.parent(Eyelid_Vector.list[-1], All)
            cmds.parent(All_Aim_main, All)

            cmds.parent(All, Main_Ctrl)
            cmds.parent(All_Detail, Main_Ctrl)
            cmds.parent(All_Side_Aim, Main_Ctrl)

            for y in range(0, len(Guidelist)):
                list01 = []
                list02 = []
                cmds.select(cl=1)
                All_TR = cmds.joint(n="Eyelid_All_" + self.Side + '_' + Ver + '_' + chr(65 + y) + '_Ctrl')
                cmds.select(cl=1)
                Start = cmds.joint(n="Eyelid_Start_" + self.Side + '_' + Ver + '_' + chr(65 + y) + '_Ctrl')
                cmds.select(cl=1)
                End = cmds.joint(n="Eyelid_End_" + self.Side + '_' + Ver + '_' + chr(65 + y) + '_Ctrl')

                Ctrl_S_Bind_Detail = jnt_Ctrl_Setting(All_TR, 'round_square', 0, 'Z', 0.333, 0.333, 0.333)
                Ctrl_S_Start = jnt_Ctrl_Setting(Start, 'cube', 0, 'Z', 0.25, 0.25, 0.25)
                Ctrl_S_End = jnt_Ctrl_Setting(End, 'cube', 0, 'Z', 0.25, 0.25, 0.25)

                Match_Mrt(All_TR, Guidelist[y], 1, 1, 0)
                Match_Mrt(Start, Guidelist[y], 1, 1, 0)
                Match_Mrt(End, Guidelist[y], 1, 1, 0)

                Eyelid_All = Grp_Set_item(All_TR, 3)
                Eyelid_Start = Grp_Set_item(Start, 3)
                Eyelid_End = Grp_Set_item(End, 3)

                cmds.select(cl=1)
                JntStartRoot = cmds.joint(n='Jnt_root_Eyelid_Start_' + self.Side + '_' + Ver + '_' + chr(65 + y))
                cmds.select(cl=1)
                JntEndRoot = cmds.joint(n='Jnt_root_Eyelid_End_' + self.Side + '_' + Ver + '_' + chr(65 + y))
                cmds.select(cl=1)
                JntStart = cmds.joint(n='Jnt_Eyelid_Start_' + self.Side + '_' + Ver + '_' + chr(65 + y))
                cmds.select(cl=1)
                JntEnd = cmds.joint(n='Jnt_Eyelid_End_' + self.Side + '_' + Ver + '_' + chr(65 + y))

                Jnt_DrawType(JntStartRoot, 2)
                Jnt_DrawType(JntStart, 2)
                Jnt_DrawType(JntEndRoot, 2)
                Jnt_DrawType(JntEnd, 2)

                Jnt_DrawType(JntStartRoot, 2)
                Jnt_DrawType(JntStart, 2)
                Jnt_DrawType(JntEndRoot, 2)
                Jnt_DrawType(JntEnd, 2)

                Match_Mrt(JntStart, Guidelist[y], 1, 1, 0)
                Match_Mrt(JntEnd, Guidelist[y], 1, 1, 0)

                GetVal_X = cmds.getAttr(Guidelist[y] + '.translateX')
                GetVal_Z = cmds.getAttr(Guidelist[y] + '.translateZ')

                Match_Mrt(JntStartRoot, self.Guide_Main_list[x + 1], 1, 1, 0)
                Match_Mrt(JntEndRoot, self.Guide_Main_list[x + 1], 1, 1, 0)

                # cmds.setAttr(JntStart + '.translateX', GetVal_X)
                # cmds.setAttr(JntStart + '.translateZ', GetVal_Z)
                # cmds.setAttr(JntEnd + '.translateX', GetVal_X)
                # cmds.setAttr(JntEnd + '.translateZ', GetVal_Z)

                cmds.parent(JntStart, JntStartRoot)
                cmds.parent(JntEnd, JntEndRoot)
                cmds.parent(Eyelid_Start.list[-1], JntStart)
                cmds.parent(Eyelid_End.list[-1], JntEnd)

                Eyelid_JntEndRoot = Grp_Set_item(JntEndRoot, 3)
                Eyelid_JntStartRoot = Grp_Set_item(JntStartRoot, 3)

                cmds.orientConstraint(Main_list, Eyelid_Start.list[-1], mo=0)
                cmds.orientConstraint(Main_list, Eyelid_End.list[-1], mo=0)

                # --------------------------------------------------------------------------------------------------Start_End_Aim
                All_Aim = cmds.createNode('transform', n='All_Eyelid_Aim_' + self.Side + '_' + Ver + '_' + chr(65 + y))
                locS_Aim = cmds.spaceLocator(n='loc_Aim_Eyelid_Start_' + self.Side + '_' + Ver + '_' + chr(65 + y))
                locE_Aim = cmds.spaceLocator(n='loc_Aim_Eyelid_End_' + self.Side + '_' + Ver + '_' + chr(65 + y))

                cmds.setAttr(locS_Aim[0] + '.visibility', 0)
                cmds.setAttr(locE_Aim[0] + '.visibility', 0)

                Match_Mrt(All_Aim, self.Guide_Main_list[x + 1], 1, 1, 0)
                Match_Mrt(locS_Aim[0], self.Guide_Main_list[x + 1], 1, 1, 0)
                Match_Mrt(locE_Aim[0], self.Guide_Main_list[x + 1], 1, 1, 0)

                Eyelid_S_locAim = Grp_Set_item(locS_Aim[0], 1)
                Eyelid_E_locAim = Grp_Set_item(locE_Aim[0], 1)

                AimS = cmds.aimConstraint(Eyelid_Start.list[0], Eyelid_S_locAim.list[0], mo=1, aim=[0, 0, 1],
                                          upVector=[0, 1, 0], worldUpVector=[0, 1, 0], worldUpType="objectrotation",
                                          worldUpObject=Eyelid_Vector.list[0])
                AimE = cmds.aimConstraint(Eyelid_End.list[0], Eyelid_E_locAim.list[0], mo=1, aim=[0, 0, 1],
                                          upVector=[0, 1, 0], worldUpVector=[0, 1, 0], worldUpType="objectrotation",
                                          worldUpObject=Eyelid_Vector.list[0])

                cmds.parent(Eyelid_S_locAim.list[-1], Eyelid_E_locAim.list[-1], All_Aim)
                cmds.parent(All_Aim, All_Aim_main)

                list01.append(Eyelid_Start.list)
                list01.append(Eyelid_JntStartRoot.list)
                list02.append(Eyelid_End.list)
                list02.append(Eyelid_JntEndRoot.list)
                # --------------------------------------------------------------------------------Detail

                Detail_list = []

                All_Detail_Alpha = cmds.createNode('transform', n='All_Eyelid_' + self.Side + '_' + Ver + '_' + chr(
                    65 + y) + '_Detail')
                Match_Mrt(All_Detail_Alpha, self.Guide_Main_list[x + 1], 1, 1, 0)

                total = 1.0
                value = self.Input_VerticalCount + 1
                Dv = total / value

                s_value = total / (self.Input_VerticalCount + 1)

                for z in range(0, self.Input_VerticalCount + 2):
                    cmds.select(cl=1)
                    Detail = cmds.joint(
                        n='Eyelid_' + self.Side + '_' + Ver + '_' + chr(65 + y) + str(z + 1) + '_Detail_Ctrl')
                    cmds.select(cl=1)
                    JntRootDetail = cmds.joint(
                        n='Jnt_root_Eyelid_' + self.Side + '_' + Ver + chr(65 + y) + str(z + 1) + '_Detail')
                    cmds.select(cl=1)
                    JntDetail = cmds.joint(
                        n='Jnt_Eyelid_' + self.Side + '_' + Ver + chr(65 + y) + str(z + 1) + '_Detail')

                    Ctrl_Detail_S = jnt_Ctrl_Setting(Detail, 'triangle', 0, 'Y', 0.15, 0.15, 0.15)

                    Jnt_DrawType(JntRootDetail, 2)
                    Jnt_DrawType(JntDetail, 2)

                    Eyelid_Detail = Grp_Set_item(Detail, 3)

                    cmds.parent(JntDetail, JntRootDetail)
                    cmds.parent(Eyelid_Detail.list[-1], JntDetail)

                    Eyelid_JntDetailRoot = Grp_Set_item(JntRootDetail, 3)

                    Match_Mrt(Eyelid_JntDetailRoot.list[-1], Eyelid_JntStartRoot.list[0], 1, 1, 0)
                    Match_Mrt(JntDetail, JntStart, 1, 1, 1)

                    Detail_list.append(Eyelid_Detail.list)
                    Detail_list.append(Eyelid_JntDetailRoot.list)

                    cmds.parent(Eyelid_JntDetailRoot.list[-1], All_Detail_Alpha)

                    CP = cmds.parentConstraint(Eyelid_S_locAim.list[0], Eyelid_E_locAim.list[0],
                                               Eyelid_JntDetailRoot.list[-2])

                    cmds.orientConstraint(Main_Ctrl, Eyelid_Detail.list[-1], mo=0)
                    O = cmds.orientConstraint(Eyelid_Start.list[0], Eyelid_End.list[0], Eyelid_Detail.list[2], mo=1)

                    O_Val = Dv * z
                    r_O_Val = 1.0 - O_Val

                    cmds.setAttr(O[0] + '.' + Eyelid_Start.list[0] + 'W0', O_Val)
                    cmds.setAttr(O[0] + '.' + Eyelid_End.list[0] + 'W1', r_O_Val)
                    cmds.setAttr(CP[0] + '.' + Eyelid_S_locAim.list[0] + 'W0', O_Val)
                    cmds.setAttr(CP[0] + '.' + Eyelid_E_locAim.list[0] + 'W1', r_O_Val)

                    Sc_Val = s_value * z
                    r_Sc_Val = 1.0 - Sc_Val
                    if z == 0:
                        cmds.connectAttr(Eyelid_End.list[0] + '.scale', Eyelid_Detail.list[1] + '.scale', f=1)
                    elif z == self.Input_VerticalCount + 1:
                        cmds.connectAttr(Eyelid_Start.list[0] + '.scale', Eyelid_Detail.list[1] + '.scale', f=1)
                    else:

                        MD01 = cmds.createNode('multiplyDivide', n='MD_scaleS_' + Eyelid_Detail.list[0])
                        MD02 = cmds.createNode('multiplyDivide', n='MD_scaleE_' + Eyelid_Detail.list[0])

                        PM = cmds.createNode('plusMinusAverage', n='PM_SumValue_' + Eyelid_Detail.list[0])

                        cmds.connectAttr(Eyelid_End.list[0] + '.scale', MD01 + '.input1', f=1)
                        cmds.connectAttr(Eyelid_Start.list[0] + '.scale', MD02 + '.input1', f=1)

                        cmds.setAttr(MD01 + '.input2X', r_Sc_Val)
                        cmds.setAttr(MD01 + '.input2Y', r_Sc_Val)
                        cmds.setAttr(MD01 + '.input2Z', r_Sc_Val)

                        cmds.setAttr(MD02 + '.input2X', Sc_Val)
                        cmds.setAttr(MD02 + '.input2Y', Sc_Val)
                        cmds.setAttr(MD02 + '.input2Z', Sc_Val)

                        cmds.connectAttr(MD01 + '.output', PM + '.input3D[0]', f=1)
                        cmds.connectAttr(MD02 + '.output', PM + '.input3D[1]', f=1)
                        cmds.connectAttr(PM + '.output3D', Eyelid_Detail.list[1] + '.scale', f=1)

                # --------------------------------------------------------Start End Rot
                # self.Guide_Aim_DTroot_list
                F_abs = abs(cmds.getAttr(self.Guide_Aim_DTroot_list[x][y][0] + '.rotateX'))
                B_abs = abs(cmds.getAttr(self.Guide_Aim_DTroot_list[x][y][1] + '.rotateX'))
                if x == 0:
                    Fix = (F_abs - B_abs)
                else:
                    Fix = -(F_abs - B_abs)

                cmds.setAttr(Eyelid_JntEndRoot.list[-1] + '.rotateX', Fix)

                cmds.parent(Eyelid_JntStartRoot.list[-1], All)
                cmds.parent(Eyelid_JntEndRoot.list[-1], All)
                cmds.parent(All_Detail_Alpha, All_Detail)
                cmds.parent(Eyelid_All.list[-1], All)
                # -----------------------------------------------------------------
                All_locSet = cmds.createNode('transform',
                                             n='All_loc_Eyelid_All_' + self.Side + '_' + Ver + '_' + chr(65 + y))
                locSetS = cmds.spaceLocator(n='loc_All_Eyelid_Start_' + self.Side + '_' + Ver + '_' + chr(65 + y))
                locSetE = cmds.spaceLocator(n='loc_All_Eyelid_End_' + self.Side + '_' + Ver + '_' + chr(65 + y))

                Match_Mrt(All_locSet, Eyelid_Start.list[0], 1, 1, 0)
                Match_Mrt(locSetS[0], Eyelid_Start.list[0], 1, 1, 0)
                Match_Mrt(locSetE[0], Eyelid_End.list[0], 1, 1, 0)

                Grping_locSetS = Grp_Set_item(locSetS[0], 1)
                Grping_locSetE = Grp_Set_item(locSetE[0], 1)

                cmds.parent(Grping_locSetS.list[-1], All_locSet)
                cmds.parent(Grping_locSetE.list[-1], All_locSet)

                cmds.parentConstraint(Eyelid_All.list[0], Grping_locSetS.list[0], mo=1)
                cmds.parentConstraint(Eyelid_All.list[0], Grping_locSetE.list[0], mo=1)

                cmds.setAttr(All_locSet + '.visibility', 0)

                for i in range(0, 3):
                    cmds.connectAttr(Grping_locSetS.list[0] + '.translate' + self.Axis[i],
                                     Eyelid_Start.list[1] + '.translate' + self.Axis[i])
                    cmds.connectAttr(Grping_locSetE.list[0] + '.translate' + self.Axis[i],
                                     Eyelid_End.list[1] + '.translate' + self.Axis[i])
                cmds.parent(All_locSet, All)

                if x == 0:
                    Up_Detail_list.append(Detail_list)
                    Up_AimTGT_Start_list.append(list01)
                    Up_AimTGT_End_list.append(list02)
                else:
                    Dw_Detail_list.append(Detail_list)
                    Dw_AimTGT_Start_list.append(list01)
                    Dw_AimTGT_End_list.append(list02)
            #
            Up_AimTGT_list.append(Up_AimTGT_Start_list)
            Up_AimTGT_list.append(Up_AimTGT_End_list)
            Dw_AimTGT_list.append(Dw_AimTGT_Start_list)
            Dw_AimTGT_list.append(Dw_AimTGT_End_list)

        for x in range(0, len(self.Guide_Side_list)):
            list_All = []
            list = []
            list_D = []
            if x == 0:
                Hor = 'In'
            else:
                Hor = 'Out'

            All_Side = cmds.createNode("transform", n='All_Eyelid_' + self.Side + '_' + Hor)

            cmds.select(cl=1)
            Side = cmds.joint(n="Eyelid_" + self.Side + '_' + Hor + '_Ctrl')
            cmds.select(cl=1)
            JntSide_root = cmds.joint(n="Jnt_Eyelid_root_" + self.Side + '_' + Hor)
            cmds.select(cl=1)
            JntSide = cmds.joint(n="Jnt_Eyelid_" + self.Side + '_' + Hor)

            cmds.select(cl=1)
            Side_Detail = cmds.joint(n="Eyelid_" + self.Side + '_' + Hor + '_Detail_Ctrl')
            cmds.select(cl=1)
            JntSide_Detail_root = cmds.joint(n="Jnt_Eyelid_root_" + self.Side + '_' + Hor + '_Detial')
            cmds.select(cl=1)
            JntSide_Detail = cmds.joint(n="Jnt_Eyelid_" + self.Side + '_' + Hor + '_Detial')
            cmds.select(cl=1)

            jnt_Ctrl_Setting(Side_Detail, 'triangle', 0, 'Y', 0.15, 0.15, 0.15)
            jnt_Ctrl_Setting(Side, 'cube', 0, 'Z', 0.25, 0.25, 0.25)

            Match_Mrt(Side, self.Guide_Side_list[x], 1, 1, 0)
            Match_Mrt(JntSide, self.Guide_Side_list[x], 1, 1, 0)
            Match_Mrt(JntSide_root, self.Guide_Main_list[-1], 1, 1, 0)

            Match_Mrt(Side_Detail, self.Guide_Side_list[x], 1, 1, 0)
            Match_Mrt(JntSide_Detail, self.Guide_Side_list[x], 1, 1, 0)

            Match_Mrt(JntSide_Detail_root, self.Guide_Main_list[-1], 1, 1, 0)

            Jnt_DrawType(JntSide_Detail_root, 2)
            Jnt_DrawType(JntSide_Detail, 2)
            Jnt_DrawType(JntSide_root, 2)
            Jnt_DrawType(JntSide, 2)

            Eyelid_Ctrl_Side = Grp_Set_item(Side, 3)
            Eyelid_JntSide_root = Grp_Set_item(JntSide_root, 3)
            Eyelid_Ctrl_Side_Detail = Grp_Set_item(Side_Detail, 3)
            Eyelid_JntSide_Detail_root = Grp_Set_item(JntSide_Detail_root, 3)

            cmds.parent(JntSide, Eyelid_JntSide_root.list[0])
            cmds.parent(Eyelid_Ctrl_Side.list[-1], JntSide)

            cmds.parent(JntSide_Detail, Eyelid_JntSide_Detail_root.list[0])
            cmds.parent(Eyelid_Ctrl_Side_Detail.list[-1], JntSide_Detail)

            locSideAim = cmds.spaceLocator(n='loc_Aim_Eyelid_' + self.Side + '_' + Hor)
            VectorSide = cmds.spaceLocator(n='loc_Vector_Eyelid_' + self.Side + '_' + Hor)
            Match_Mrt(VectorSide[0], self.Guide_Main_list[0], 1, 1, 0)
            Match_Mrt(locSideAim[0], self.Guide_Main_list[0], 1, 1, 0)
            Eyelid_locSideAim = Grp_Set_item(locSideAim[0], 1)
            Eyelid_VectorSide = Grp_Set_item(VectorSide[0], 1)

            cmds.setAttr(Eyelid_locSideAim.list[0] + '.visibility', 0)
            cmds.setAttr(Eyelid_VectorSide.list[0] + '.visibility', 0)

            cmds.parent(Eyelid_locSideAim.list[-1], Eyelid_VectorSide.list[-1], Main_Ctrl)
            cmds.aimConstraint(Eyelid_Ctrl_Side.list[0], Eyelid_locSideAim.list[0], mo=1, aim=[0, 0, 1],
                               upVector=[0, 1, 0], worldUpVector=[0, 1, 0], worldUpType="objectrotation",
                               worldUpObject=Eyelid_VectorSide.list[0])
            cmds.parentConstraint(Eyelid_locSideAim.list[0], Eyelid_JntSide_Detail_root.list[-1], mo=1)
            cmds.orientConstraint(Main_Ctrl, Eyelid_Ctrl_Side_Detail.list[-1], mo=0)
            cmds.orientConstraint(Eyelid_Ctrl_Side.list[0], Eyelid_Ctrl_Side_Detail.list[2], mo=1)

            cmds.parent(Eyelid_JntSide_root.list[-1], Eyelid_JntSide_Detail_root.list[-1], All_Side)
            cmds.parent(All_Side, Main_Ctrl)

            cmds.connectAttr(Eyelid_Ctrl_Side.list[0] + '.scale', Eyelid_Ctrl_Side_Detail.list[1] + '.scale')

            cmds.parent(Eyelid_locSideAim.list[1], Eyelid_VectorSide.list[1], All_Side_Aim)

            Side_locAim_list.append(Eyelid_locSideAim.list)

            list.append(Eyelid_Ctrl_Side.list)
            list.append(Eyelid_JntSide_root.list)

            list_D.append(Eyelid_Ctrl_Side_Detail.list)
            list_D.append(Eyelid_JntSide_Detail_root.list)

            Side_AimTGT_list.append(list)
            Side_Detail_list.append(list_D)

        Eyelid_Ctrl_All_list = []
        All_Ctrl_All_Close = cmds.createNode('transform', n='All_Eyelid_Blink_' + self.Side)

        cmds.parent(All_Ctrl_All_Close, Main_list[0])
        for x in range(0, 2):
            pre_list = []
            if x == 0:
                Ver = self.Vertical[0]
                list = Up_AimTGT_list[0]
                Ctrl_S_Aixs = 'Z'
            else:
                Ver = self.Vertical[1]
                list = Dw_AimTGT_list[0]
                Ctrl_S_Aixs = '-Z'

            print
            '>>>', len(list), list

            Mid = len(list) // 2

            Main_Follow = cmds.createNode('transform', n='All_Follow_' + "Jnt_Eyelid_root_" + self.Side + '_' + Ver)

            cmds.select(cl=1)
            Ctrl_All_Close = cmds.joint(n='Eyelid_' + self.Side + '_' + Ver + '_Blink_Ctrl')
            Ctrl_S = jnt_Ctrl_Setting(Ctrl_All_Close, 'square', 0, Ctrl_S_Aixs, 0.333, 0.333, 0.333)

            Match_Mrt(Ctrl_All_Close, list[Mid][0][0], 1, 1, 0)
            Eyelid_Ctrl = Grp_Set_item(Ctrl_All_Close, 3)

            cmds.select(cl=1)
            IK_root = cmds.joint(n='Jnt_Eyelid_root_' + self.Side + '_' + Ver + '_Blink')
            cmds.select(cl=1)
            IK_End = cmds.joint(n='Jnt_Eyelid_' + self.Side + '_' + Ver + '_Blink')

            Jnt_DrawType(IK_root, 2)
            Jnt_DrawType(IK_End, 2)

            Match_Mrt(IK_End, list[Mid][0][0], 1, 1, 0)
            Match_Mrt(IK_root, self.Guide_Main_list[x + 1], 1, 1, 0)

            cmds.parent(IK_End, IK_root)

            Eyelid_IK_root = Grp_Set_item(IK_root, 3)
            IK_Solver = cmds.ikHandle(n='IK_Eyelid_' + self.Side + '_' + Ver, sj=IK_root, ee=IK_End)
            cmds.setAttr(IK_Solver[0] + '.visibility', 0)

            cmds.parent(IK_Solver[0], Eyelid_Ctrl.list[0])

            pre_list.append(Eyelid_Ctrl.list)
            pre_list.append(Eyelid_IK_root.list)
            Eyelid_Ctrl_All_list.append(pre_list)
            cmds.parent(Eyelid_IK_root.list[-1], Main_Follow, Eyelid_Ctrl.list[-1], All_Ctrl_All_Close)

            total = 1.0
            value = Mid + 1
            Dv = total / value

            for y in range(0, len(list)):
                All_Follow = cmds.createNode('transform',
                                             n='All_Follow_' + "Jnt_Eyelid_root_" + self.Side + '_' + Ver + '_' + chr(
                                                 65 + y))

                StaricLoc = cmds.spaceLocator(
                    n='loc_Staric_' + "Jnt_Eyelid_root_" + self.Side + '_' + Ver + chr(65 + y))
                FollowLoc = cmds.spaceLocator(
                    n='loc_Follow_' + "Jnt_Eyelid_root_" + self.Side + '_' + Ver + chr(65 + y))

                cmds.parent(StaricLoc[0], FollowLoc[0], All_Follow)
                cmds.parent(All_Follow, Main_Follow)

                cmds.setAttr(StaricLoc[0] + '.visibility', 0)
                cmds.setAttr(FollowLoc[0] + '.visibility', 0)

                Match_Mrt(All_Follow, self.Guide_Main_list[x + 1], 1, 1, 0)

                cmds.parentConstraint(Eyelid_IK_root.list[0], FollowLoc[0], mo=1)

                CP = cmds.parentConstraint(StaricLoc[0], FollowLoc[0], list[y][-1][-2], mo=1)
                cmds.addAttr(Eyelid_Ctrl.list[0], ln=list[y][0][0], at="float", k=1, min=0, max=1)

                cmds.parent(All_Follow, Main_Follow)

                result = Dv * y
                r_result = -1 * (1.0 - (Dv * y))

                Rv = cmds.createNode('reverse', n='RV_value_' + list[y][0][0])
                if y < Mid:
                    cmds.connectAttr(Eyelid_Ctrl.list[0] + '.' + list[y][0][0], CP[0] + '.' + FollowLoc[0] + 'W1')
                    cmds.connectAttr(Eyelid_Ctrl.list[0] + '.' + list[y][0][0], Rv + '.input.inputX')
                    cmds.connectAttr(Rv + '.outputX', CP[0] + '.' + StaricLoc[0] + 'W0')
                    # cmds.setAttr(Eyelid_Ctrl.list[0]  +'.'+ list[y][0][0] , result )
                    cmds.parentConstraint(Side_locAim_list[0][0], StaricLoc[0], mo=1)
                elif y == Mid:
                    cmds.connectAttr(Eyelid_Ctrl.list[0] + '.' + list[y][0][0], Rv + '.input.inputX')
                    cmds.connectAttr(Rv + '.outputX', CP[0] + '.' + StaricLoc[0] + 'W0')
                    cmds.setAttr(Eyelid_Ctrl.list[0] + '.' + list[y][0][0], 1)
                    cmds.parentConstraint(self.Guide_Main_list[x + 1], StaricLoc[0], mo=1)
                else:
                    cmds.connectAttr(Eyelid_Ctrl.list[0] + '.' + list[y][0][0], CP[0] + '.' + FollowLoc[0] + 'W1')
                    cmds.connectAttr(Eyelid_Ctrl.list[0] + '.' + list[y][0][0], Rv + '.input.inputX')
                    cmds.connectAttr(Rv + '.outputX', CP[0] + '.' + StaricLoc[0] + 'W0')
                    # cmds.setAttr(Eyelid_Ctrl.list[0]  +'.'+ list[y][0][0] , r_result )
                    cmds.parentConstraint(Side_locAim_list[1][0], StaricLoc[0], mo=1)

        All_Side_Follow = cmds.createNode('transform', n='All_Side_Follow_' + self.Side)
        Side_Staric = cmds.spaceLocator(n='Eyelid_Staric_Side_' + self.Side)
        Side_Up_Follow = cmds.spaceLocator(n='Eyelid_Follow_Side_Up_' + self.Side)
        Side_Dw_Follow = cmds.spaceLocator(n='Eyelid_Follow_Side_Dw_' + self.Side)

        cmds.parent(Side_Staric[0], Side_Dw_Follow[0], Side_Up_Follow[0], All_Side_Follow)

        Match_Mrt(All_Side_Follow, Main_list[0], 1, 1, 0)

        cmds.parent(All_Side_Follow, Main_list[0])

        cmds.setAttr(All_Side_Follow + '.visibility', 0)
        cmds.parentConstraint(Eyelid_Ctrl_All_list[0][-1][0], Side_Up_Follow[0], mo=1)
        cmds.parentConstraint(Main_list[0], Side_Staric[0], mo=1)
        cmds.parentConstraint(Eyelid_Ctrl_All_list[-1][-1][0], Side_Dw_Follow[0], mo=1)

        for x in range(0, 2):
            cmds.addAttr(Side_AimTGT_list[x][0][0], ln=Side_Up_Follow[0], at="float", k=1, min=0, max=1)
            cmds.addAttr(Side_AimTGT_list[x][0][0], ln=Side_Staric[0], at="float", k=1, min=0, max=1)
            cmds.addAttr(Side_AimTGT_list[x][0][0], ln=Side_Dw_Follow[0], at="float", k=1, min=0, max=1)
            CP = cmds.orientConstraint(Side_Up_Follow[0], Side_Staric[0], Side_Dw_Follow[0],
                                       Side_AimTGT_list[x][-1][-1], mo=1)

            Attr = cmds.listAttr(Side_AimTGT_list[x][0][0], ud=1)
            CP_Attr = cmds.listAttr(CP[0], ud=1)

            for z in range(0, 3):
                if z == 0:
                    set = 0.07
                elif z == 1:
                    set = 1
                else:
                    set = 0.07
                cmds.connectAttr(Side_AimTGT_list[x][0][0] + '.' + Attr[z], CP[0] + '.' + CP_Attr[z])
                cmds.setAttr(Side_AimTGT_list[x][0][0] + '.' + Attr[z], set)


A = Eyelid_UI()