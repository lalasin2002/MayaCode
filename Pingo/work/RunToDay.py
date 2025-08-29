import maya.cmds as cmds
import re
# -*- coding: utf-8 -*-
import maya.cmds as cmds

class SetDrivenKey:
    def __init__(self):
        self.relationships = []
    
    def addDriven(self, driver_attr, driver_value, driven_attr, driven_value):
        '''
        -driver_attr : 드라이버 + Attr\n
        -driver_value : 드라이버 값\n
        -driven_attr : 드라이븐 + Attr\n
        driven_value : 드라이븐 값\n
        '''
        self.relationships.append({
            'driver': driver_attr,
            'driver_value': driver_value,
            'driven': driven_attr,
            'driven_value': driven_value
        })
        
    def setKey(self):
        '''
        -셋드라이버 키 세팅
        '''
        if not self.relationships:
            cmds.warning("No relationships added!")
            return
            
        for rel in self.relationships:
            # Set 0
            cmds.setDrivenKeyframe(rel['driven'], 
                                 cd=rel['driver'], 
                                 dv=0, 
                                 v=0)
            
            # Set valuqes
            cmds.setDrivenKeyframe(rel['driven'], 
                                 cd=rel['driver'], 
                                 dv=rel['driver_value'], 
                                 v=rel['driven_value'])
            
            # animation curve
            anim_curve = cmds.listConnections(rel['driven'], type='animCurve')
            if anim_curve:
                cmds.keyTangent(anim_curve, itt='linear', ott='linear')


#예시
'''
SD = SetDrivenKeyManager()#클래스 정의
SD.addDriven("SetDriverA.translateX" , 10 , "SetDrivenA.translateX" , 1)
SD.addDriven("SetDriverB.translateX" , 10 , "SetDrivenB.translateX" , 1)
SD.addDriven("SetDriverC.translateX" , 10 , "SetDrivenC.translateX" , 1)
SD.setKey()'
'''


SD = SetDrivenKey()
FaceSam = "face_SamBS"
MouthSam = "mouth_BS"
SD.addDriven("B_L_inUp_boxControl.ty" , 1 , "{}.B01_L_inup" .format(FaceSam) , 1)
SD.addDriven("B_L_sad_box.ty" , 1  ,"{}.B06_L_sad".format(FaceSam)  , 1)
SD.addDriven("B02_L_surprise_boxControl.ty" , 1 , "{}.B02_L_surprise".format(FaceSam)  , 1)
SD.addDriven("B_L_angry_boxControl.ty " , 1, "{}.B04_L_angry".format(FaceSam) , 1)
SD.addDriven("B_L_down_boxControl.ty", 1,"{}.B05_L_down" .format(FaceSam) , 1)

SD.addDriven("B_R_inUp_boxControl.ty" , 1 , "{}.B01_R_inup" .format(FaceSam) , 1)
SD.addDriven("B_R_sad_box.ty" , 1  ,"{}.B06_R_sad".format(FaceSam)  , 1)
SD.addDriven("B02_R_surprise_boxControl.ty" , 1 , "{}.B02_R_surprise".format(FaceSam)  , 1)
SD.addDriven("B_R_angry_boxControl.ty " , 1, "{}.B04_R_angry".format(FaceSam) , 1)
SD.addDriven( "B_R_down_boxControl.ty", 1,"{}.B05_R_down" .format(FaceSam) , 1)

#---------------------------------------------------------------------------------------------------
SD.addDriven("E_L_upperLid_boxControl.ty" , 1 , "{}.E02_L_surprise_up" .format(FaceSam) , 1)
SD.addDriven("E_L_upperLid_boxControl.ty" , -1 , "{}.E01_L_blink_down" .format(FaceSam) , 1)

SD.addDriven("E_L_lowerLid_boxControl.ty" , 1 , "{}.E01_L_blink_up".format(FaceSam) , 1)
SD.addDriven("E_L_lowerLid_boxControl.ty" , -1 , "{}.E02_L_surprise_down".format(FaceSam) , 1)

SD.addDriven("E_L_outdown_boxControl.ty" , 1 , "{}.E05_L_closecry" .format(FaceSam), 1)


SD.addDriven("E_R_upperLid_boxControl.ty" , 1 , "{}.E02_R_surprise_up" .format(FaceSam) , 1)
SD.addDriven("E_R_upperLid_boxControl.ty" , -1 , "{}.E01_R_blink_down" .format(FaceSam) , 1)

SD.addDriven("E_R_lowerLid_boxControl.ty" , 1 , "{}.E01_R_blink_up".format(FaceSam) , 1)
SD.addDriven("E_R_lowerLid_boxControl.ty" , -1 , "{}.E02_R_surprise_down".format(FaceSam) , 1)

SD.addDriven("E_R_outdown_boxControl.ty" , 1 , "{}.E05_R_closecry" .format(FaceSam), 1)
#---------------------------------------------------------------------------------------------------
#Ah
SD.addDriven("fAh_boxControl.ty" , 1 , "{}.S02_ah" .format(FaceSam), 1)
SD.addDriven("fAh_boxControl.ty" , 1 , "{}.S02_ah" .format(MouthSam), 1)
#Ae
SD.addDriven("fAe_boxControl.ty" , 1 , "{}.S03_ae" .format(FaceSam) , 1)
SD.addDriven("fAe_boxControl.ty" , 1 , "{}.S03_ae" .format(MouthSam) , 1)
#Ee
SD.addDriven("fEe_boxControl.ty" ,1 , "{}.S04_ee" .format(FaceSam) , 1)
#Oh
SD.addDriven("fOh_boxControl.ty" ,1 , "{}.S05_oh" .format(FaceSam) ,1)
SD.addDriven("fOh_boxControl.ty" ,1 , "{}.S05_oh" .format(MouthSam) ,1)
#U
SD.addDriven("fU_boxControl.ty" , 1 , "{}.S06_u".format(FaceSam) ,1)
#Hm
SD.addDriven("fHm_boxControl.ty" ,1 , "{}.S01_hmm" .format(FaceSam) , 1)
#Uh
SD.addDriven("fUh_boxControl.ty" , 1 , "{}.S08_uh" .format(FaceSam) ,1)
SD.addDriven("fUh_boxControl.ty" , 1 , "{}.S08_uh" .format(MouthSam) ,1)

#smAh
SD.addDriven("smi_big_boxControl.ty" , 1 , "{}.FM03_smbig" .format(FaceSam) ,1)
SD.addDriven("smi_big_boxControl.ty" , 1 , "{}.FM03_smbig" .format(MouthSam) ,1)
#bigAh
SD.addDriven("big_ah_boxControl.ty" , 1 , "{}.FM06_bigAh" .format(FaceSam) ,1)
SD.addDriven("big_ah_boxControl.ty" , 1 , "{}.FM06_bigAh" .format(MouthSam) ,1)

#---------------------------------------------------------------------------------------------------
SD.addDriven("M_L_mouth_Hap_boxControl.ty" , 1 , "{}.M07_L_sneerhmm" .format(FaceSam) ,1)
SD.addDriven("M_L_mouth_Hap_boxControl.ty" , -1 , "{}.M06_L_sidedown" .format(FaceSam) ,1)

SD.addDriven("M_R_mouth_Hap_boxControl.ty" , 1 , "{}.M07_R_sneerhmm" .format(FaceSam) ,1)
SD.addDriven("M_R_mouth_Hap_boxControl.ty" , -1 , "{}.M06_R_sidedown" .format(FaceSam) ,1)


SD.addDriven("M_lipUp_boxControl.ty" ,1 , "{}.M02_middleup".format(FaceSam) ,1)
SD.addDriven("M_lipUp_boxControl.ty" ,-1 , "{}.M02_middleup".format(FaceSam) ,-1)
SD.addDriven("M_lipUp_boxControl.tx" ,1 , "{}.M03_L_lipup".format(FaceSam) ,1)
SD.addDriven("M_lipUp_boxControl.tx" ,-1 , "{}.M03_R_lipup".format(FaceSam) ,1)

#SD.addDriven("M_lipUp_boxControl.ty" ,-1 , "{}".format(FaceSam) ,1)

SD.addDriven("M_mouth_boxControl.ty" , 1 , "{}.M10_mouthup" .format(FaceSam) , 1)
SD.addDriven("M_mouth_boxControl.ty" , -1 , "{}.M11_mouthdown" .format(FaceSam) , 1)
SD.addDriven("M_mouth_boxControl.tx" , 1 , "{}.M12_L_sulk" .format(FaceSam) , 1)
SD.addDriven("M_mouth_boxControl.tx" , -1 , "{}.M12_R_sulk" .format(FaceSam) , 1)


SD.addDriven("M_lipDown_boxControl.ty " , 1 , "{}.M04_lipdown".format(FaceSam) , 1)
SD.addDriven("M_lipDown_boxControl.ty " , -1 , "{}.M04_lipdown".format(FaceSam) , -1)
SD.addDriven("M_lipDown_boxControl.tx " , 1 , "{}.M05_L_lipdown".format(FaceSam) , 1)
SD.addDriven("M_lipDown_boxControl.tx " , -1 , "{}.M05_R_lipdown".format(FaceSam) , 1)





SD.setKey()


