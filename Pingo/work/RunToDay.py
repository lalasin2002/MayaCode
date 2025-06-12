import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

import sys , os , pprint



dirPath =os.path.abspath("D:\Code\MayaCode")
if not os.path.isdir(dirPath):
    print ("nn")
    if dirPath not in sys.path:
        os.path.append(dirPath)

import completeCode.Class , completeCode.Def
