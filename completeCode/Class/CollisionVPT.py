# -*- coding: utf-8 -*-
import maya.cmds as cmds
import pprint



class c_Create_CorrectiveJnt():
    def __init__(self):
        self.__FirstTgt = None
        self.__SecontDaryTgt = None
        self.__ThirdTgt = None

        self.__CtrlBool = True
        
        self.__Corrective_Max = None
        self.__Corrective_Min = None

        self.__PriamryTuple = None
        self.__SeconDaryTuple = (0,1,0)
        self.__PrimaryAxis = None
        self.__ParentTgt = None

        self.Ctrl = None
        self.JntList = []

    def Option(self , ParentTgt = None ):
        self.__ParentTgt = ParentTgt
    
    def Set_TargetObject( self, FirstTgt , SecontDaryTgt , ThirdTgt):
        self.__FirstTgt = FirstTgt
        self.__SecontDaryTgt = SecontDaryTgt 
        self.__ThirdTgt = ThirdTgt

    def Set_Target_Jnt (self , FirstJnt , SecontDaryJnt , ThirdJnt):
        self.JntList = [FirstJnt , SecontDaryJnt , ThirdJnt]


    def Set_Destination_Jnt(self , De_FirstJnt , De_SecontDaryJnt):
        self.De_FirstJnt  = De_FirstJnt 
        self.De_SecontDaryJnt = De_SecontDaryJnt

    def Set_PrimaryAxis(self , PrimaryAxis , SeconDaryAxis = None):
        PrimaryList = []
        SeconDaryList= []


        for x in "XYZ":
            PriamryInt= 0
            SeconDaryInt = 0
            if PrimaryAxis == x:
                PriamryInt = 1
            PrimaryList.append(PriamryInt)

        self.__PriamryTuple = (0,1,0)
        if  SeconDaryAxis:
            for x in "XYZ":
                SeconDaryInt = 0
                if SeconDaryAxis == x:
                    SeconDaryInt = 1
                SeconDaryList.append(SeconDaryInt )

        self.__PriamryTuple = tuple(PrimaryList)
        self.__PrimaryAxis = str(PrimaryAxis)
        self.__SeconDaryTuple = tuple(SeconDaryList)

    def Set_Corrective_limit(self , Min , Max):
        self.__Corrective_Min = float(Min)
        self.__Corrective_Max = float(Max)

    def Build(self):
        
        CtrlList = []
        TgtPosList = []
        De_FirstJntPos = None
        De_SecontDaryPos = None

        CorrectiveOffset = None
        CorrectiveRoot = None
        CorrectiveCP = None

        CtrlRootOffset = None
        CtrlMiddleOffset = None
        PrimaryMinus = 1
        #----------Find Jnt Axis
        if self.__PriamryTuple is None and self.De_FirstJnt and self.De_SecontDaryJnt:
            De_FirstJntPos = cmds.xform(self.De_FirstJnt ,ws =1 , q =1 , t =1)
            De_SecontDaryPos = cmds.xform(self.De_SecontDaryJnt , ws =1, q =1, t =1)

            De_Pos_DistanceValue = ((De_FirstJntPos[0]- De_SecontDaryPos[0])**2 + (De_FirstJntPos[1] - De_SecontDaryPos[1])**2 + (De_FirstJntPos[2] - De_SecontDaryPos[2])**2)**0.5
            De_Pos_Distance = float("{:.{}f}" .format( De_Pos_DistanceValue, 4))

            FindAxisLoc = cmds.spaceLocator(n = "{}__FindAxis" .format(self.De_FirstJnt))[0]
            cmds.xform(FindAxisLoc , ws =1 , t = De_SecontDaryPos)
            cmds.parent(FindAxisLoc , self.De_FirstJnt)

            FindAxisLocPos = cmds.xform(FindAxisLoc , q =1, t =1 , r =1)


            PrimaryList = []
            
            for i, x in enumerate("XYZ"):
                PrimaryInt = 0
                AxisValue = float("{:{}f}" .format(FindAxisLocPos[i] , 4))
                print ("AxisValue ::" , AxisValue )
                AbsAxisValue = round(abs(AxisValue) , 4)
                
                if AbsAxisValue == De_Pos_Distance:
                    
                    Minus = int(AxisValue/(abs(AxisValue)))
                    PrimaryInt =1 * Minus
                    self.__PrimaryAxis = str(x)
                    PrimaryMinus = Minus
                
                PrimaryList.append(PrimaryInt)
                
            self.__PriamryTuple = tuple(PrimaryList)


            AbsPrimaryList = [abs(item) for item in PrimaryList ]
            AbsPrimaryTuple = tuple(AbsPrimaryList)

            
            if AbsPrimaryTuple == self.__SeconDaryTuple:
                
                SeconDaryList = [0, 0, 0]
                SeconDaryIndex = 0 
                for i , x in enumerate(self.__PriamryTuple):
                    if x == self.__PriamryTuple[i]:
                        SeconDaryIndex = i + 1
                        if SeconDaryIndex > 2:
                            SeconDaryIndex = -(i+1) 
                
                SeconDaryList[SeconDaryIndex] = 1
                self.__SeconDaryTuple = tuple(SeconDaryList)


            cmds.delete(FindAxisLoc)
            print ("Find PrimaryAxis :: {}" .format(self.__PriamryTuple))
            print ("Find SeconDaryAxis :: {}" .format(self.__SeconDaryTuple))
        
        #----------CreateJnt
        if self.__FirstTgt and self.__SecontDaryTgt and self.__ThirdTgt and self.De_FirstJnt and self.De_SecontDaryJnt and self.JntList is None:
            PreTgtList = [self.__FirstTgt , self.__SecontDaryTgt , self.__ThirdTgt]
            TgtPosList = [cmds.xform(x , q =1, ws =1, t =1) for x in PreTgtList]
            OldGrp = None
            OldJnt = None
            OldGrpList = []
            for i, x in enumerate(PreTgtList):
                cmds.select(cl =1)
                Jnt = cmds.joint( n = "{}_Jnt" .format(x))
                PreJntGrp = cmds.group(Jnt ,  n = "{}__PreGrp" .format(Jnt))
                cmds.xform(PreJntGrp , ws =1 , t = TgtPosList[i])

                if OldGrp and OldJnt:
                    AimConstraint = cmds.aimConstraint(Jnt , OldGrp ,aim = self.__PriamryTuple , u = self.__SeconDaryTuple , wu = self.__SeconDaryTuple , wut = "objectrotation" , wuo = self.De_SecontDaryJnt , mo =0 )
                    cmds.parent(Jnt , w =1)
                    cmds.delete(AimConstraint)
                    cmds.parent(Jnt , OldJnt)
                    if i == 2:
                        for Axis in "XYZ":
                            cmds.setAttr("{}.jointOrient{}" .format(Jnt , Axis) , 0 )
                OldJnt = Jnt 
                OldGrp = PreJntGrp 
                self.JntList.append(OldJnt)
                OldGrpList.append(OldGrp)
            cmds.delete(OldGrpList)
            print ("Create Jnt :: {}" .format(self.JntList))

        #----------ExistTgt
        if self.__CtrlBool:
            
            PreCtrlList = [cmds.createNode("transform" , n = "{}_Ctrl" .format(x)) for x in self.JntList] 
            OldCtrl = None
            for i , x in enumerate(PreCtrlList):
                Grp = cmds.createNode("transform" , n = "{}_Grp" .format(x))
                Offset = cmds.createNode("transform" , n ="{}_Offset" .format(x))

                cmds.parent(Grp  , Offset)
                cmds.parent(x , Grp)

                CP = cmds.parentConstraint(self.JntList[i] , Offset , mo = 0)
                cmds.delete(CP)

                if OldCtrl:
                    cmds.parent(Offset , OldCtrl)

                if i == 0 :
                    CtrlRootOffset = Offset
                if i == 1:
                    CtrlMiddleOffset  = Offset
                OldCtrl = x

                CtrlList.append(x)

                cmds.parentConstraint(x , self.JntList[i] , mo =1)

                for Axis in "XYZ":
                    cmds.connectAttr(x + ".scale{}" .format(Axis) , self.JntList[i] + ".scale{}" .format(Axis) ,f =1)

            cmds.addAttr(CtrlList[1] , ln = "Corrective_Value" , at='double', k=1 , dv =1 *PrimaryMinus)
            cmds.addAttr(CtrlList[1] , ln = "Corective_Min" , at='double', k=1 )
            cmds.addAttr(CtrlList[1] , ln = "Corective_Max" , at='double', k=1 )

            if self.__Corrective_Min and self.__Corrective_Max and self.__Corrective_Min < self.__Corrective_Max:
                cmds.setAttr(CtrlList[1] + ".Corective_Min" , self.__Corrective_Min)
                cmds.setAttr(CtrlList[1] + ".Corective_Max" , self.__Corrective_Max)
            else:
                GetTransJnt = cmds.getAttr(self.JntList[1] + ".translate{}" .format(self.__PrimaryAxis))
                PreMin = 0 
                PreMax = GetTransJnt * 2.5

                if PreMin > PreMax:
                    self.__Corrective_Min = PreMax
                    self.__Corrective_Max = PreMin
                else:
                    self.__Corrective_Min = PreMin
                    self.__Corrective_Max = PreMax


                cmds.setAttr(CtrlList[1] + ".Corective_Min" , self.__Corrective_Min)
                cmds.setAttr(CtrlList[1] + ".Corective_Max" , self.__Corrective_Max)





        #--------Corrective Grp
        if CorrectiveOffset is None:
            CorrectiveOffset = cmds.createNode("transform" , n = "{}_CorrectiveOffset" . format(self.JntList[0]))
            CorrectiveRoot = cmds.createNode("transform" , n = "{}_CorrectiveRoot" . format(self.JntList[0]))
            CorrectiveCP = cmds.createNode("transform" , n = "{}_CorrectiveCPTarget" . format(self.JntList[0]))
            cmds.parent(CorrectiveOffset  , CorrectiveCP )
            cmds.parent(CorrectiveCP , CorrectiveRoot)

            CP = cmds.parentConstraint(self.JntList[1] , CorrectiveRoot , mo = 0)
            cmds.delete(CP)

            #cmds.parent(self.JntList[0] , CorrectiveOffset)
            if CtrlRootOffset:
                cmds.parent(CtrlRootOffset , CorrectiveOffset )

            print ("Create and Parent CorrectiveGrp :: {},{}"  .format(CorrectiveOffset , CorrectiveRoot))

        #---------Corrective Node Setting
        if len(self.JntList)==3:
            Corrective_Pos_loc = cmds.spaceLocator( n = "{}_CorrectivePos_loc" .format(self.JntList[0]))
            Corrective_Rot_loc = cmds.spaceLocator( n = "{}_CorrectiveRot_loc" .format(self.JntList[0]))

            CP_POS_loc = cmds.parentConstraint(self.JntList[1] , Corrective_Pos_loc[0] , mo = 0)
            CP_Rot_loc = cmds.parentConstraint(self.JntList[2] , Corrective_Rot_loc[0] , mo = 0 )

            cmds.setAttr(Corrective_Pos_loc[0] + ".visibility" , 0 )

            cmds.delete(CP_POS_loc)
            cmds.delete(CP_Rot_loc)

            cmds.parent(Corrective_Rot_loc[0] , Corrective_Pos_loc[0])

            if CorrectiveRoot:
                cmds.parent(Corrective_Pos_loc[0] , CorrectiveRoot)

            pprint.pprint(Corrective_Pos_loc)

            cmds.parentConstraint(self.De_FirstJnt , self.De_SecontDaryJnt , Corrective_Pos_loc[0] , mo =1 , sr = ["x" , "y" , "z"])
            cmds.parentConstraint(self.De_FirstJnt , self.De_SecontDaryJnt , Corrective_Rot_loc[0] , mo =1 , sr = ["x" , "y" , "z"])

            POS_VPT = cmds.createNode("vectorProduct" , n = "{}_VPT" .format(Corrective_Pos_loc[0]))
            Rot_VPT = cmds.createNode("vectorProduct" , n = "{}_VPT" .format(Corrective_Rot_loc[0]))
            Div_MD = cmds.createNode("multiplyDivide" , n = "{}_Div_MD" .format(self.De_SecontDaryJnt))
            Result_MD = cmds.createNode("multiplyDivide" , n = "{}_CorrectiveRs_MD" .format(self.De_SecontDaryJnt))
            Clamp = cmds.createNode("clamp" , n = "{}_CorrectiveRs_CLP" .format(self.De_SecontDaryJnt))

            print (self.__PriamryTuple)

            cmds.setAttr(Div_MD + ".operation", 2)
            for i, x in enumerate("XYZ"):
                cmds.setAttr(Rot_VPT + ".input1{}" .format(x) , self.__PriamryTuple[i])
                cmds.setAttr(Result_MD + ".input1{}" .format(x) , self.__PriamryTuple[i])

            cmds.connectAttr(Corrective_Pos_loc[0] + ".translate" , POS_VPT + ".input1" ,f =1)
            cmds.connectAttr(Corrective_Rot_loc[0] + ".translate" , POS_VPT + ".input2" ,f =1)
            cmds.connectAttr(Corrective_Rot_loc[0] + ".translate" , Rot_VPT + ".input2" ,f =1)

            cmds.connectAttr(POS_VPT + ".output" , Div_MD + ".input1" ,f =1)
            cmds.connectAttr(Rot_VPT + ".output" , Div_MD + ".input2" ,f =1)
            cmds.connectAttr(Div_MD + ".output" , Result_MD + ".input2" ,f =1)

            cmds.connectAttr(CtrlList[1] + ".Corrective_Value" , Result_MD + ".input1{}" .format(self.__PrimaryAxis))

            cmds.connectAttr(Result_MD + ".output{}" .format(self.__PrimaryAxis) , Clamp + ".inputR" ,f =1)
            cmds.connectAttr(Clamp + ".outputR", CorrectiveOffset + ".translate{}" .format(self.__PrimaryAxis) ,f =1)
            cmds.connectAttr(CtrlList[1] + ".Corective_Min"  , Clamp + ".minR" ,f =1)
            cmds.connectAttr(CtrlList[1] + ".Corective_Max"  , Clamp + ".maxR" ,f =1)

            #cmds.connectAttr(Result_MD + ".output{}" .format(self.__PrimaryAxis) , CorrectiveOffset + ".translate{}" .format(self.__PrimaryAxis) ,f =1)
            

            if self.__Corrective_Min and self.__Corrective_Max:
                if self.__Corrective_Min < self.__Corrective_Max: 
                    
                    limitTuple =(self.__Corrective_Min ,self.__Corrective_Max )

                    
                cmds.connectAttr(CtrlList[1] + ".Corective_Min" , "{}.minTransYLimit" .format(CorrectiveOffset) ,f =1)
                cmds.connectAttr(CtrlList[1] + ".Corective_Max" , "{}.maxTransYLimit" .format(CorrectiveOffset) ,f =1)
            if self.__PrimaryAxis:
                LowerPrimaryAxis = self.__PrimaryAxis.lower()
                print (LowerPrimaryAxis)
                AxisList = ["x" , "y" , "z"]
                SkipList = [x for x in AxisList if not LowerPrimaryAxis in x]
                print ("SkipAxis ::" ,SkipList)
                

                #cmds.parentConstraint(self.De_SecontDaryJnt , CorrectiveCP  , sr = AxisList , st = [LowerPrimaryAxis],mo =1)


            cmds.parentConstraint(self.De_FirstJnt , CorrectiveRoot ,mo =1)
            cmds.orientConstraint(self.De_SecontDaryJnt , CtrlMiddleOffset , mo =1)












'''
sel = cmds.ls(sl =1 , type = "joint")
DeJnt= ["Pelvis_Ctrl" , "L_Leg_Jnt"]

Corrective = c_Create_CorrectiveJnt()
Corrective.Set_Target_Jnt(sel[0] , sel[1] , sel[2])
Corrective.Set_PrimaryAxis("Y" ,"Z")
Corrective.Set_Destination_Jnt(DeJnt[0] , DeJnt[1]) 
Corrective.Build()

'''