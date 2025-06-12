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