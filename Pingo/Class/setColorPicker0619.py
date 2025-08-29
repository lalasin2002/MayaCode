# coding: utf-8
from __future__ import unicode_literals
import maya.cmds as cmds
import maya.mel as mel

from PySide2.QtWidgets import (QApplication, QWidget, QFrame, QVBoxLayout, QCheckBox,
                               QHBoxLayout, QLabel, QDoubleSpinBox, QPushButton)
from PySide2.QtGui import QColor, QImage, QPixmap, QPainter
from PySide2.QtCore import Qt, Signal, QPoint
from collections import OrderedDict
# Maya의 메인 윈도우를 가져오는 헬퍼 함수
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

def get_maya_main_window():
    main_win_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win_ptr), QWidget)

def colorHueSliderImage(width, height):
    image = QImage(width, height, QImage.Format_RGB32)
    painter = QPainter(image)
    
    for y in range(height):
        hue = float(y) / (height - 1)
        color = QColor.fromHsvF(hue, 1.0, 1.0)
        painter.setPen(color)
        painter.drawLine(0, y, width, y)
        
    painter.end()
    return QPixmap.fromImage(image)

class setColorPicker(QWidget):
    colorSelected = Signal(QColor)

    def __init__(self, parent=None):
        super(setColorPicker, self).__init__(parent)
        self.current_hue = 0.0

        self.svLabel = QLabel()
        self.svLabel.setMinimumSize(256, 256)
        self.hueLabel = QLabel()
        self.hueLabel.setMinimumSize(20, 256)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addWidget(self.svLabel)
        layout.addWidget(self.hueLabel)

        self.huePixmap = colorHueSliderImage(20, 256)
        self.hueLabel.setPixmap(self.huePixmap)

        self._update_sv_pixmap()
        self.svLabel.installEventFilter(self)
        self.hueLabel.installEventFilter(self)

    def _update_sv_pixmap(self):
        image = QImage(256, 256, QImage.Format_RGB32)
        for y in range(256):
            for x in range(256):
                saturation = float(x) / 255.0
                value = 1.0 - (float(y) / 255.0)
                color = QColor.fromHsvF(self.current_hue, saturation, value)
                image.setPixel(x, y, color.rgb())
        self.svLabel.setPixmap(QPixmap.fromImage(image))

    def eventFilter(self, source, event):
        if event.type() in [event.MouseButtonPress, event.MouseMove] and event.buttons() == Qt.LeftButton:
            pos = event.pos()
            if source is self.hueLabel:
                y = max(0, min(pos.y(), self.huePixmap.height() - 1))
                self.current_hue = float(y) / (self.huePixmap.height() - 1)
                self._update_sv_pixmap()
                self._pickColor(self.svLabel, QPoint(0,0))
                return True
            elif source is self.svLabel:
                self._pickColor(source, pos)
                return True
        return super(setColorPicker, self).eventFilter(source, event)

    def _pickColor(self, label, pos):
        pixmap = label.pixmap()
        if not pixmap: return
        x = max(0, min(pos.x(), pixmap.width() - 1))
        y = max(0, min(pos.y(), pixmap.height() - 1))
        image = pixmap.toImage()
        color = image.pixelColor(x, y)
        if color.isValid():
            self.colorSelected.emit(color)

class setColorPickerUI(QWidget):
    def __init__(self, parent=None):
        super(setColorPickerUI, self).__init__(parent)
        
        self.LightList = []
        self.printString = []
        self.printError = []
        self.colorV = (0,0,0)
        #--------------------------------------------------
        self.setWindowFlags(Qt.Window)
        self.setObjectName('setColorPickerUI')
        self.setWindowTitle("set Color Picker")

        self.color_picker = setColorPicker()
        self.color_swatch = QFrame()
        self.color_swatch.setMinimumSize(20, 20)
        self.color_swatch.setAutoFillBackground(True)
        #self.color_info_label = QLabel("RGB: (0, 0, 0)")

        colorInfoRed_label = QLabel("R ::")
        colorInfoGreen_label = QLabel("G ::")
        colorInfoBlue_label = QLabel("B ::")

        self.colorInfo_red = QDoubleSpinBox()
        self.colorInfo_green = QDoubleSpinBox()
        self.colorInfo_blue = QDoubleSpinBox()
        self.colorInfo_red.setDecimals(3)
        self.colorInfo_green.setDecimals(3)
        self.colorInfo_blue.setDecimals(3)

    
        self.colorButton = QPushButton("set \nColor")
        self.colorButton.setMinimumSize(10 , 60)

        self.intensityButton = QPushButton("set \nIntensity")
        self.intensityButton.setMinimumSize(10 , 60)

        self.setColorKeyButton = QPushButton("KeyFrame \nColor")
        self.setColorKeyButton.setMinimumSize(10 , 60)
        self.setIntensityLKeyButton = QPushButton("KeyFrame \nIntensit Key")
        self.setIntensityLKeyButton.setMinimumSize(10 , 60)

        self.hierarchyCheck = QCheckBox()
        self.hierarchyCheck.setText("hierarchy")
        self.hierarchyCheck.setChecked(True)

        self.intensityLabel = QLabel("intensity") 
        self.intensityDoubleSpinBox = QDoubleSpinBox()
        self.intensityDoubleSpinBox.setDecimals(3)

        main_layout = QVBoxLayout(self)
        bottom_first_row_layout = QHBoxLayout()
        colorInfo_layout = QVBoxLayout()
        intensityFloat_layout = QVBoxLayout()
        intensityInfo_layout = QHBoxLayout()

        colorInfoRed_layout = QHBoxLayout()
        colorInfoGreen_layout = QHBoxLayout()
        colorInfoBlue_layout = QHBoxLayout()

        #-------------------------------------------------LayOut
        colorInfo_layout.addWidget(self.hierarchyCheck)
        
        colorInfoRed_layout.addWidget(colorInfoRed_label)
        colorInfoRed_layout.addWidget(self.colorInfo_red)
        colorInfoGreen_layout.addWidget(colorInfoGreen_label) 
        colorInfoGreen_layout.addWidget(self.colorInfo_green) 
        colorInfoBlue_layout.addWidget(colorInfoBlue_label)
        colorInfoBlue_layout.addWidget(self.colorInfo_blue)


        colorInfo_layout.addWidget(self.color_swatch)
        colorInfo_layout.addLayout(colorInfoRed_layout)
        colorInfo_layout.addLayout(colorInfoGreen_layout)
        colorInfo_layout.addLayout(colorInfoBlue_layout)
        
        #colorInfo_layout.addWidget(self.color_info_label)
        

        intensityFloat_layout.addWidget(self.intensityLabel)
        intensityFloat_layout.addWidget(self.intensityDoubleSpinBox)

        intensityInfo_layout.addLayout(intensityFloat_layout)
        intensityInfo_layout.addWidget(self.intensityButton)
        intensityInfo_layout.addWidget(self.setIntensityLKeyButton)

        main_layout.addWidget(self.color_picker)

        bottom_first_row_layout.addLayout(colorInfo_layout)
        bottom_first_row_layout.addWidget(self.colorButton)
        bottom_first_row_layout.addWidget(self.setColorKeyButton)



        main_layout.addLayout(bottom_first_row_layout)
        main_layout.addLayout(intensityInfo_layout)
        
        self.color_picker.colorSelected.connect(self.update_selected_color)
        self.update_selected_color(QColor(0,0,0))
        self.colorButton.clicked.connect(lambda x : self.setColors())
        self.setColorKeyButton.clicked.connect(lambda x : self.setColors(True))
        self.intensityButton.clicked.connect(lambda x : self.setIntensitys())
        self.setIntensityLKeyButton.clicked.connect(lambda x: self.setIntensitys(True))

    def update_selected_color(self, color):
        self.color_swatch.setStyleSheet("background-color: %s;" % color.name())
        redV = round(float(color.red())/float(255) , 3)
        greenV = round(float(color.green())/float(255) , 3)
        blueV = round(float(color.blue())/float(255) ,3)

        self.colorInfo_red.setValue(redV)
        self.colorInfo_green.setValue(greenV)
        self.colorInfo_blue.setValue(blueV)  
        #info_text = "RGB: ({r}, {g}, {b})" .format(r = redV,g = greenV,b =  blueV,n =  color.name())
        #self.color_info_label.setText(info_text)
        
    def log(self , msg , e = False):
        
        if e:
            self.printError.append(msg)
        else:
            self.printString.append(msg)


    def printlog(self):
        for x in self.printString:
            print (x)

        self.printString = []
    def printErrorlog(self):
        if len(self.printError)>0:
            print ("__________________________________________\n")
            for x in self.printError:
                print (x)
        self.printError =[]
        
    def get_ColorData(self):
        self.colorV = (self.colorInfo_red.value() , self.colorInfo_green.value() ,self.colorInfo_blue.value() )

    def get_LightElements(self ,  hierarchy = False ,objType = "RedshiftPhysicalLight"):
        selects = cmds.ls(sl =1 ,allPaths=1 )
        Lightshapes = []
        setElement = set()
        if hierarchy:
            for x in selects:
                cmds.select(x ,hierarchy=1)
                hierarchySelects = cmds.ls(sl =1 ,allPaths=1 , type= objType)
                if len(hierarchySelects)>0:
                    for shape in hierarchySelects:
                        p = cmds.listRelatives(shape , p =1 , type = "transform")[0]
                        setElement.add(p)
            cmds.select(selects)
        else:
            for x in selects:
                
                Is_shape = cmds.listRelatives(x  , type =objType ,s =1 )
                
                if Is_shape:

                    setElement.add(x)
                    print (setElement)
        #
        Lightshapes = list(setElement)
        Lightshapes.sort()
        self.LightList = Lightshapes
        
    def setColors(self , Key = False):
        self.get_LightElements(self.hierarchyCheck.checkState())
        self.get_ColorData()
        if len(self.LightList) > 0 :
            works = []
            colorEntryCount = 0
            for  i ,x in enumerate(self.LightList):
                DataDic = {"ramp" : None , "colorEntryCount" : None , "obj" : None}
                isRamp = cmds.listConnections(x + ".color" , s =1 ,d =0 ,type = "ramp")
                if isRamp :
                    colorEntryCount = cmds.getAttr("{}.colorEntryList" .format(isRamp [0]) , size = 1)
                    DataDic["colorEntryCount"] = int(colorEntryCount)
                    DataDic["ramp"] = isRamp[0]
                    DataDic["obj"] = x
                    works.append(DataDic)
                else:
                    self.log("", True)
                    self.log(">> 작업카운트 {n} >> 에러! {obj} 에 ramp 노드가 존재하지 않음" .format(n = i+1 , obj = x) , True)


            if len(works) >0:
                for num , dic in enumerate(works):
                    if all( not k == None for k in dic):
                        self.log("")
                        self.log(">> 작업카운트 {n} >> {obj}.color에 연결된 노드 : {ramp}" .format(n = num+1 , obj = dic["obj"] , ramp = dic["ramp" ]  ))
                        for entryCount in range(dic["colorEntryCount"]):
                            #print (self.colorV)
                            for colorCount ,  r in enumerate("RGB"):
                                cmds.setAttr("{}.colorEntryList[{}].color{}" .format(dic["ramp"], entryCount , r) ,self.colorV[colorCount])
                                if Key:
                                    cmds.setKeyframe("{}".format(dic["ramp"]) , attribute= ".colorEntryList[{}].color{}" .format(entryCount , r ), itt = "linear" , ott = "linear")
                                    self.log("  >{}.colorEntryList[{}].color{} >> 현재 {} 프레임에 setKey".format( dic["ramp"] ,entryCount , r  , cmds.currentTime(q =1)) )
                            self.log("  > {ramp}.colorEntryList[{colorC}] 에 적용된 RGB 값 : {colorVector}" .format(ramp = dic["ramp" ] , colorC = entryCount , colorVector = self.colorV)) 


        self.printlog()
        self.printErrorlog()
                            
    def setIntensitys(self , Key = False):
        self.get_LightElements(self.hierarchyCheck.checkState())
        if len(self.LightList) > 0 :
            works = []
            for x in self.LightList:
                
                IsShp = cmds.listRelatives(x  , s =1 , type= "RedshiftPhysicalLight")
                print (IsShp)
                if IsShp:
                    works.append(IsShp[0])



            for  i , x in enumerate(works):
                IsAttr = cmds.attributeQuery("intensity" ,node = x , exists=1)
                if IsAttr:
                    cmds.setAttr(x + ".intensity" , self.intensityDoubleSpinBox.value())

                    self.log("")
                    if Key:
                        cmds.setKeyframe(x , attribute= ".intensity" , itt = "linear" , ott = "linear")
                        self.log("> {}.intensity >> 현재 {} 프레임에 setKey" .format(x , cmds.currentTime(q =1) ))
                    self.log(">> 작업카운트 {n} >> {obj}.intensity 값 설정 : {v}" .format( n = i +1 , obj = x , v = self.intensityDoubleSpinBox.value()))
                else:
                    self.log("", True)
                    self.log(">> 작업카운트 {n} >> 에러! {obj} 에 intensity Attr가 존재하지 않음" .format(n = i+1 , obj = x) , True)

        self.printlog()
        self.printErrorlog()




def main():
    for widget in QApplication.instance().allWidgets():
        if widget.objectName() == 'setColorPickerUI':
            widget.close()
            widget.deleteLater()

    maya_main_win = get_maya_main_window()
    ex = setColorPickerUI(parent=maya_main_win)
    ex.show()

main()

