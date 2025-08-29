# -*- coding: utf-8 -*-
import pprint

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.mel as mel
import getpass, sys, re, os, json

from PySide2.QtWidgets import QApplication, QFileDialog  ,QListWidgetItem , QWidget
from PySide2 import QtCore, QtWidgets, QtUiTools, QtGui 
from shiboken2 import wrapInstance
from collections import OrderedDict
from functools import partial
PythonV = sys.version
Version = cmds.about(version=True)
User = getpass.getuser()
Folder = 'AniSimTag'


def d_PathDir():
    import inspect , os
    currentPath = inspect.getfile(inspect.currentframe())
    
    
    DirPath = os.path.dirname(currentPath)
    return DirPath


def d_PathBasic(User , Version , Folder):
    Path = "C:/Users/{}/Documents/maya/{}/scripts/{}".format(User, Version, Folder)
    return Path

def d_PathSysModule(Path):
    Module_Path = Path
    Dir_Path =os.path.dirname(Path)
    sys.path.append(Module_Path)
    sys.path.append(Dir_Path)

#Path = d_PathDir()

#if Path == '':
Path =d_PathBasic(User , Version , Folder)


Folder_Dir = [x for x in os.listdir(Path) if os.path.isdir(os.path.join(Path, x)) ]
PathSys = [d_PathSysModule('{}/{}' .format(Path , x)) for x in Folder_Dir ]


# ------------------------------------------------------------------------------------
def d_Add_StringAttr(Target, LongName, String):
    Attr = cmds.attributeQuery(LongName, node=Target, exists=True)
    if not Attr == True:
        cmds.addAttr(Target, ln=LongName, dt="string")
        cmds.setAttr('{}.{}'.format(Target, LongName), String, type="string")
        GetAttr = LongName
        return GetAttr
    
    
    
def d_Delete_Attr(Target, LongName):
    Attr = cmds.attributeQuery(LongName, node=Target, exists=True)
    if Attr == True:
        AttrName = '{}.{}'.format(Target, LongName)
        cmds.deleteAttr(AttrName)
        
        
        

def d_Return_lst_LWItem(QList):
    lst = []
    lst = [QList.item(i).text() for i in range(QList.count())]
    return lst


def d_Add_lst_LWItem(QList , ItemLst , Clear = True , Align = "" ):
    Worklst = []
    QAlign = None
    item =None
    if Align == "Left" or Align ==  "":
        QAlign = QtCore.Qt.AlignLeft
    if Align == "Center":
        QAlign = QtCore.Qt.AlignHCenter
    if Align == "Right":
        QAlign = QtCore.Qt.AlignRight
    
    if type(ItemLst) == list and len(ItemLst) > 0:
        Worklst =  [x for i ,x in enumerate(ItemLst ) if x not in ItemLst[:i]]
    if Clear:
        QList.clear()
    
    
    
    
    for x in Worklst:
        item = QListWidgetItem(str(x))
        item.setTextAlignment(QAlign)

        QList.addItem(item)
        
def d_Delete_Item_LWItem(QList):
    TargetItem = None
    lst = [QList.item(i).text() for i in range(QList.count())]
    SelectItem = QList.selectedItems()
    
    if len(SelectItem) > 0:
        TargetItem = [x.text() for x in SelectItem]
    if TargetItem:
        Newlst = []
        Prelst = lst[:]
        for x in TargetItem:
            TargetIndex = Prelst.index(x)
            Prelst.pop(TargetIndex)

        Newlst = Prelst
        QList.clear()
        for x in Newlst:
            QList.addItem(x)
    
def d_Sort_Item_LWItem(QList):
    lst = [QList.item(i).text() for i in range(QList.count())]
    lst.sort()
    lst = [x for i ,x in enumerate(lst ) if x not in lst[:i]]
    QList.clear()
    for x in lst:
        QList.addItem(x)
    
    
        
def d_Selected_lst(Type = "transform" , ShpType = "mesh"):
    Returnlst = []
    lst = cmds.ls(sl =1 , type = Type)
    if len(lst) >0:
        for x in lst:
            Shp = cmds.listRelatives(x , s=1, type = ShpType)
            if not  Shp is None:
                Returnlst.append(x)
        
    return Returnlst 
        
def d_Arrange_lst_LWItem(QList, Drt = True):
    TargetItem = None
    Newlst = []
    
    Itemlst  = [QList.item(i).text() for i in range(QList.count())]
    SelectItem = QList.selectedItems()
    
    
    if len(SelectItem) > 0:
        TargetItem = SelectItem[0].text()
        
    if TargetItem:
        PreItemlst =Itemlst[:]

        TargetIndex = Itemlst.index(TargetItem)
        MoveIndex = TargetIndex + (-1 if Drt else 1)
        
        PreItemlst.pop(TargetIndex)
        PreItemlst.insert(MoveIndex , TargetItem)

        Newlst = PreItemlst
        QList.clear()
        for x in Newlst:
            QList.addItem(x)
            
        QList.setCurrentRow(MoveIndex)

def d_Find_Match_Attr_Obj(Obj, AttrName, String):
    if cmds.objExists(Obj) == True:
        Attr = cmds.attributeQuery(AttrName, node=Obj, exists=True)
        if Attr == True:
            GetAttr = cmds.getAttr('{}.{}'.format(Obj, AttrName))
            if GetAttr == String:
                return Obj
    return None  


#-------------------------------------------------------------------------------------------

def maya_main_window():
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)


class DesignerUI(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(DesignerUI, self).__init__(parent)
        #------------------------------------
        
        self.__Define_Instance_Bool = False
        self.__SceneFileName = ""
        self.__JsonFolderName = "SD_JsonData"
        
        self.__TagArrayDataPath  = "{}/{}".format (Path,"Data")
        self.__NameSpaceFindString = r"(.+):(\w+)"
        
        
        self.setWindowTitle("AniSimTag UI")
        self.init_ui()
        self.Define_Widget()
        if self.__Define_Instance_Bool:
            self.PreSetting_Widget()
        self.Connect_Function_To_Widget()
        
        

    def Define_Widget(self):
        
        #--------------------------Btn
        self.Btn_AddItem = self.ui.Btn_AddItem
        self.Btn_AddTagItem = self.ui.Btn_AddTagItem
        #self.Btn_SortItem = self.ui.Btn_SortItem
        self.Btn_DeleteItem = self.ui.Btn_DeleteItem
        self.Btn_ClearItem = self.ui.Btn_Clear
        
        #self.Btn_SelectAll_Item = self.ui.Btn_SelectAll_Item
        #self.Btn_DeSelectAll_Item = self.ui.Btn_DeSelectAll_Item
        
        self.Btn_FindScenePath = self.ui.Btn_FindScenePath
        self.Btn_OpenScene = self.ui.Btn_OpenScene
        self.Btn_FindJsonDataPath = self.ui.Btn_FindJsonDataPath
        self.Btn_JsonFolderOpen = self.ui.Btn_JsonFolderOpen
        self.Btn_reLoadJsonFolderPath = self.ui.Btn_reLoadJsonFolderPath
        self.Btn_reLoadScenePath =self.ui.Btn_reLoadScenePath
        
        self.Btn_AddTag = self.ui.Btn_AddTag
        self.Btn_DeleteTag = self.ui.Btn_DeleteTag
        
        self.Btn_SearchTagItem = self.ui.Btn_SearchTagItem
        self.Btn_DeleteSearchTagItem = self.ui.Btn_DeleteSearchTagItem
        self.Btn_SearchClear = self.ui.Btn_SearchClear
        self.Btn_ExportJson = self.ui.Btn_ExportJson
        
        self.Btn_ReloadTagArray =self.ui.Btn_ReloadTagArray
        
        #--------------------------LineEdit
        self.LE_ScenePath = self.ui.LE_ScenePath
        self.LE_JsonFolderPath = self.ui.LE_JsonFolderPath
        
        self.LE_AddString = self.ui.LE_AddString
        
        
        self.LE_TagCh = self.ui.LE_TagCh
        self.LE_TagPr = self.ui.LE_TagPr
        self.LE_TagBg = self.ui.LE_TagBg
        self.LE_TagBp = self.ui.LE_TagBp
        
        #--------------------------TestEdit
        
        self.TE_ResultString = self.ui.TE_ResultString
        
        #--------------------------ListWidget
        self.LW_ItemList = self.ui.LW_ItemList
        self.LW_SearchTagList = self.ui.LW_SearchTagList

        #--------------------------CheckBox
        self.CHB_DeleteAllTag = self.ui.CHB_DeleteAllTag
        
        #--------------------------ComboBox
        
        self.CBB_TagArrayStyle = self.ui.CBB_TagArrayStyle
        
        
        
        
        #----------------DefineBool
        self.__Define_Instance_Bool = True
    
    def init_ui(self):
        UI_File = 'AniSimTag.ui'
        f = QtCore.QFile(Path + "/{}".format(UI_File))
        f.open(QtCore.QFile.ReadOnly)

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(f, parentWidget=self)
        f.close()        
        self.setFixedSize(self.ui.size())
        
    def PreSetting_Widget(self):
        CurrentScenePath = None
        CurrentSceneFoldePath = None
        CurrentJsonFolderPath = None
        

        self.String = "[NameSpace]:[ObjectName]"
        self.Function_Change_LineEditText(self.TE_ResultString , self.String , "")
        self.Function_Insert_Combo_TagArray()
        self.Function_Select_TagArray()
        if self.LE_ScenePath.text() == "":
            self.Function_Load_Path(self.LE_ScenePath , "")
            CurrentScenePath = self.LE_ScenePath.text()
            
            Split_CurrentScenePath = CurrentScenePath.split("/")
            if Split_CurrentScenePath[-1]:
                self.__SceneFileName = Split_CurrentScenePath [-1].split(".")[0]
                
        if CurrentScenePath and self.LE_JsonFolderPath.text() == "":
            self.Function_Load_Path(self.LE_JsonFolderPath ,self.__JsonFolderName)

        
    def Connect_Function_To_Widget(self):
        #---------------------------------------------------------------------Path_Function
        self.Btn_FindScenePath.clicked.connect(self.Functon_FindScenePath)
        self.Btn_FindJsonDataPath.clicked.connect(lambda : self.Function_FindJsonFolderPath(self.LE_JsonFolderPath))
        self.Btn_OpenScene.clicked.connect(lambda : self.Function_OpenScene(self.LE_ScenePath.text()))
        self.Btn_JsonFolderOpen.clicked.connect(lambda : self.Function_OpenFolder(self.LE_JsonFolderPath.text()))
        
        self.Btn_reLoadScenePath.clicked.connect(lambda :self.Function_Load_Path(self.LE_ScenePath))
        self.Btn_reLoadJsonFolderPath.clicked.connect(lambda :self.Function_Load_Path(self.LE_JsonFolderPath , self.__JsonFolderName))
        
        #----------------------------------------------------------------------Work List
        
        self.Btn_AddItem.clicked.connect(self.Function_Add_ItemWorkList)
        self.Btn_AddItem.clicked.connect(lambda : d_Sort_Item_LWItem(self.LW_ItemList))
        
        #self.Btn_SortItem.clicked.connect(lambda : d_Sort_Item_LWItem(self.LW_ItemList))
        self.Btn_AddTagItem.clicked.connect(lambda : self.Function_Add_FindTagItem(self.LW_ItemList))
        self.Btn_AddTagItem.clicked.connect(lambda : d_Sort_Item_LWItem(self.LW_ItemList))
        
        self.Btn_DeleteItem.clicked.connect(lambda : d_Delete_Item_LWItem(self.LW_ItemList))
        self.Btn_ClearItem.clicked.connect(lambda : self.LW_ItemList.clear())
        
        
        self.LW_ItemList.itemClicked.connect(lambda : self.Function_Select_ListWidget_Item(self.LW_ItemList ))
        #self.Btn_SelectAll_Item.clicked.connect(lambda : self.Function_Select_ListWidget_Item(self.LW_ItemList ,True))
        #self.Btn_DeSelectAll_Item.clicked.connect(lambda :self.Function_DeSelect_ListWidget_Item(self.LW_ItemList))
        
        #----------------------------------------------------------------------Add Tag
        
        self.LE_AddString.textChanged.connect(lambda : self.Function_Change_LineEditText(self.TE_ResultString , self.String , self.LE_AddString.text() ))
        self.Btn_AddTag.clicked.connect(self.Function_Create_Tag)
        self.Btn_DeleteTag.clicked.connect(lambda : self.Function_Delete_Tag(self.CHB_DeleteAllTag.isChecked()))
        
        #----------------------------------------------------------------------FindTagItem
        
        self.Btn_SearchTagItem.clicked.connect(lambda : self.Function_Add_FindTagItem(self.LW_SearchTagList))
        self.Btn_SearchTagItem.clicked.connect(lambda : d_Sort_Item_LWItem(self.LW_SearchTagList))
        self.Btn_DeleteSearchTagItem.clicked.connect(lambda : d_Delete_Item_LWItem(self.LW_SearchTagList))
        self.Btn_SearchClear.clicked.connect(lambda : self.LW_SearchTagList.clear())
        
        self.LW_SearchTagList.clicked.connect(lambda : self.Function_Select_ListWidget_Item(self.LW_SearchTagList))
        self.Btn_ExportJson.clicked.connect(self.Function_Export_JsonData)
        
        
        #-----------------------------------------------------------------------TagArray
        self.Btn_ReloadTagArray.clicked.connect(self.Function_Insert_Combo_TagArray)
        self.CBB_TagArrayStyle.activated[str].connect(self.Function_Select_TagArray)
        
        
        
        
    def Function_Export_JsonData(self):
        Work_lst = []
        Export_DicValue_lst = []
        Export_DicBgValue_lst = []
        Export_DicPrValue_lst = []
        
        Export_Dic = {}
        
        JsonFolderPath = self.LE_JsonFolderPath.text()
        Pre_Work_lst = d_Return_lst_LWItem(self.LW_SearchTagList)
        
        for x in Pre_Work_lst:
            FindTag = cmds.attributeQuery("SimTag", node=x, exists=True)
            FindBgTag = cmds.attributeQuery("BgTag", node=x, exists=True)
            FinPrTag = cmds.attributeQuery("PrTag", node=x, exists=True)
            if FindTag:
                Export_DicValue_lst.append(x)
            if FindBgTag:
                Export_DicBgValue_lst.append(x)
            if FinPrTag:
                Export_DicPrValue_lst.append(x)

        Export_Dic["SimTag"] = Export_DicValue_lst
        Export_Dic["PrTag"] = Export_DicPrValue_lst
        Export_Dic["BgTag"] = Export_DicBgValue_lst
        

                
        
        
        JsonExportFileName = "{}.json" .format(self.__SceneFileName)
        JsonExportPath = "{}/{}" .format(JsonFolderPath , JsonExportFileName)
        
        if not os.path.exists(JsonFolderPath):
            os.mkdir(JsonFolderPath)
        
        with open(JsonExportPath , "w" ) as JsonFile:
            json.dump(Export_Dic , JsonFile)
        
        print ("Data saved to :: \n{}" .format(JsonExportPath))
        
        os.startfile(self.LE_JsonFolderPath.text())
        

    def Function_Add_FindTagItem(self , QList):
        All_lst = []
        FindTag_Objlst = []
        Pre_All_lst = cmds.ls(type = "transform")
        for x in Pre_All_lst:
            Shp = cmds.listRelatives(x , s =1 , type = "mesh")
            if not Shp is None:
                All_lst.append(x)
                
        for x in All_lst:
            FindTag = cmds.attributeQuery("SimTag", node=x, exists=True)
            FindBgTag = cmds.attributeQuery("BgTag", node=x, exists=True)
            FinPrTag = cmds.attributeQuery("PrTag", node=x, exists=True)
            if FindTag or FindBgTag or FinPrTag:
                FindTag_Objlst.append(x)   
                    
        d_Add_lst_LWItem(QList , FindTag_Objlst)
        
    
    def Function_Select_ListWidget_Item(self , QList , All_Select_Bool = False):
        
        if All_Select_Bool:
            LenQList = QList.count()
            for x in range(LenQList):
                Item = QList.item(x)
                Item.setSelected(True)
                
        SeletedWidgetItems = QList.selectedItems()  
        SeletedWidgetItems = [x.text() for x in SeletedWidgetItems if cmds.objExists(x.text())]
        
        
        cmds.select(SeletedWidgetItems )
        
        
    def Function_DeSelect_ListWidget_Item(self , QList ):
        LenQList = QList.count()
        for x in range(LenQList):
            Item = QList.item(x)
            Item.setSelected(False)
            
    def Function_Select_TagArray(self):
        
        TagArrayDataPathDir = os.listdir(self.__TagArrayDataPath)
        TagArrayDataPathFindDir = [x for x in TagArrayDataPathDir if x.endswith(".json")]
        
        SelectComboItem = self.CBB_TagArrayStyle.currentText()
        JsonTagArrayPath = "{}/{}.json" .format(self.__TagArrayDataPath,SelectComboItem)  
        
        TagArrayData = None
        
        with open (JsonTagArrayPath , "r" ) as JsonFile:
            TagArrayData = json.load(JsonFile)
            
        self.LE_TagCh.setText(TagArrayData["Ch"])
        self.LE_TagPr.setText(TagArrayData["Pr"])
        self.LE_TagBg.setText(TagArrayData["Bg"])
        self.LE_TagBp.setText(TagArrayData["Bp"])
        #self.__NameSpaceFindString = TagArrayData["reString"]
        
    
    
    def Function_Insert_Combo_TagArray(self):
        TagArrayDataPathDir = os.listdir(self.__TagArrayDataPath)
        TagArrayDataPathFindDir = [x for x in TagArrayDataPathDir if x.endswith(".json")]
        TagArrayDataPathFindDir = [x.split(".")[0] for x in TagArrayDataPathFindDir ]
        
  
        self.CBB_TagArrayStyle.clear()
        
        for x in TagArrayDataPathFindDir:
            self.CBB_TagArrayStyle.addItem(x)
        
        
    
    
    
    def Function_Create_Tag(self):
        WorkList = d_Return_lst_LWItem(self.LW_ItemList)
        NameSpacePattern = "{}" .format(self.__NameSpaceFindString)
        
        NameSpaceComPile = re.compile(NameSpacePattern)
        
        ChFind = self.LE_TagCh.text()
        PrFind = self.LE_TagPr.text()
        BgFind = self.LE_TagBg.text()
        BpFind = self.LE_TagBp.text()
        
        
        #, "reString":"([a-zA-Z]+)_(\d+)_(\w+):(\w+)"
        #,"reString":"([a-zA-Z]+)_([a-zA-Z])(\\d+).:"
        #Result_list = []
        
        for x in WorkList:
            Join_list =  []
            #SceneName = None
            NameSpace = None
            ObjectName = None
            AddString = None
            
            FullMatchName = NameSpaceComPile.match(x)
            
            if FullMatchName:
                SplitAssetName = x.split(":")
                
                NameSpace = SplitAssetName[0]
                ObjectName = SplitAssetName[1]
                
                #Fucking Duplicate Name!!
                if len(SplitAssetName) > 1:
                    ObjectName = ":".join(SplitAssetName[1:])
                    
            else:
                ObjectName = x  
                 
            #SceneName = self.__SceneFileName
            AddString = None if self.LE_AddString.text() == "" else self.LE_AddString.text()
            
            Join_list = [ NameSpace , ObjectName , AddString]
            Join_list = [ item for item in Join_list if not item is None]
            
            TagString = ":".join(Join_list)
            print ("NameSpace>>>",NameSpace)
            d_Delete_Attr(x , "SimTag")
            d_Delete_Attr(x , "BgTag")
            d_Delete_Attr(x , "PrTag")
            if ChFind in  NameSpace:
                d_Add_StringAttr(x , "SimTag" , str(TagString))
            if BgFind in  NameSpace or BpFind in NameSpace:
                d_Add_StringAttr(x , "BgTag" , str(TagString))
            if PrFind in NameSpace:
                d_Add_StringAttr(x , "PrTag" , str(TagString))
                
    def Function_Load_Path(self,QLine  ,  AddPath = ""):
        CurrentScenePath = cmds.file(query=True, sceneName=True)
        CurrentSceneFoldePath = os.path.dirname(CurrentScenePath)
        
        if AddPath == "":
            QLine.setText(CurrentScenePath)
        else:
            QLine.setText(CurrentSceneFoldePath + "/{}" .format(AddPath))
        
        
        
     
    def Function_Delete_Tag(self , Delete_All_Bool = False):

        work_lst = d_Return_lst_LWItem(self.LW_ItemList)
        
        if Delete_All_Bool == True:
            
            All_lst = []
            FindTag_Objlst = []
            Pre_All_lst = cmds.ls(type = "transform")
            for x in Pre_All_lst:
                Shp = cmds.listRelatives(x , s =1 , type = "mesh")
                if not Shp is None:
                    All_lst.append(x)

            for x in All_lst:
                FindTag = cmds.attributeQuery("SimTag", node=x, exists=True)
                FindBgTag = cmds.attributeQuery("BgTag", node=x, exists=True)
                if FindTag or FindBgTag:
                    FindTag_Objlst.append(x)
            
            if len(FindTag_Objlst )>0:
                work_lst = FindTag_Objlst
                
        if len(work_lst )> 0 :
            for x in work_lst:
                d_Delete_Attr(x , "SimTag")
                d_Delete_Attr(x , "BgTag")
                d_Delete_Attr(x , "PrTag")
        else:
            print (r"Don't Find Tag Item")
            

        
    def Function_Change_LineEditText(self , QLineEidt , Text , AddString):
        
        InsertString = ""
        
        if AddString.isspace():
            AddString = AddString.replace(" " , "_")
        if not AddString == "":
            InsertString = ":{}".format(AddString)
        
        
        QLineEidt.setText(Text+InsertString)
        
    def Function_Add_ItemWorkList(self):
        SelectedItem = d_Selected_lst()
        if not len(SelectedItem) == 0:
            d_Add_lst_LWItem(self.LW_ItemList , SelectedItem, False )

    def Function_OpenScene(self , Path):
        try:
            cmds.file(Path, f=1, o=True, iv=1, typ='mayaBinary')
            #os.startfile(Path)
            self.PreSetting_Widget()
        except:
            print ("No Path")
            
    def Function_OpenFolder(self , Path ):
        try:
            if not os.path.exists(Path):
                os.makedirs(Path)
            os.startfile(Path)
        except:
            print  ("No Path")
    
        
    def Function_FindJsonFolderPath(self,QLineTarget,  FileSelet = False):
        if not QApplication.instance():
            App = QApplication(sys.argv)
        Options = QFileDialog.Options()
        
        DirSelect = "Folder"
        if FileSelet == True:
            DirSelect = "File"
            Options |= QFileDialog.ReadOnly
            
        DirPath = None
        Path = None
        if FileSelet == True:
            DirPath = QFileDialog.getOpenFileName(None , "Select {}" .format(DirSelect) , options=Options)
            Path = DirPath[0]
        else:
            DirPath = QFileDialog.getExistingDirectory(None , "Select {}" .format(DirSelect) , options=Options)
            Path = DirPath + "/{}" .format(self.__JsonFolderName)
        if DirPath:
            QLineTarget.setText( Path) 
    
    
    
    
    def Functon_FindScenePath(self):
        if not QApplication.instance():
            App = QApplication(sys.argv)
        Options = QFileDialog.Options()
        Options |= QFileDialog.ReadOnly
        
        DirPath = QFileDialog.getOpenFileName(None , "Select {}" .format("File") , options=Options)
        if DirPath:
            #cmds.file(DirPath[0] , f=1, o=True, iv=1)
            self.LE_ScenePath.setText(DirPath[0])




'''
if __name__ == "__main__":
    try:
        desinger_ui.close()
        desinger_ui.deleteLater(
    except:
        pass
    desinger_ui = DesignerUI()
    desinger_ui.show()
'''
