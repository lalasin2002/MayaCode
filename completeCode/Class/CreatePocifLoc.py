import maya.cmds as cmds


class CreatePocifLoc:
    def __init__(self  ):
        self.Crv = None
        self.CrvShp = None
        self.Locs = []
        self.PocifNodes = []
        self.Points_for_makeCrv = []
        self.__CountAddPoint = 0
        self.MainName = ""
        self.SuffixName = ""
    
    def Add_ObjForMakeCrvPos(self , Obj , Printing = False):
        PrintString = ""
        if isinstance(Obj , str) and cmds.objExists(Obj):
            Pos = tuple(cmds.xform(Obj , q =1 , t = 1 , ws =1))
            self.Points_for_makeCrv.append(Pos)
            self.__CountAddPoint +=1
            PrintString += "> AddCount{num}, obj : {var} , Pos : {pos} \n" .format(num = self.__CountAddPoint , var = Obj , pos = Pos )   
        elif isinstance(Obj , list):
            for x in Obj:
                if cmds.objExists(x):
                    Pos = tuple(cmds.xform(x , q =1 , t = 1 , ws =1))
                    self.Points_for_makeCrv.append(Pos)
                    self.__CountAddPoint +=1
                    PrintString += "> AddCount{num}, obj : {var} , Pos : {pos} \n" .format(num = self.__CountAddPoint , var = x , pos = Pos )
        else:
            raise TypeError( ">>  Invalid object type. Expected a string or a list.")
        if Printing:
            print (PrintString)

    def Add_PosForMakeCrvPos(self ,Pos ,Printing = False):
        PrintString = ""
        if (isinstance(Pos , tuple) and len(Pos) ==3 and all(isinstance(x ,(int, float)) for x in Pos) ):
            self.Points_for_makeCrv.append(Pos)
            self.__CountAddPoint +=1
            PrintString += "> AddCount{num}, Pos : {pos} \n" .format(num = self.__CountAddPoint , pos = Pos )
        elif isinstance (Pos , list):
            for element in Pos:
                if (isinstance(element , tuple) and len(element) ==3 and all(isinstance(x ,(int, float)) for x in element) ):
                    self.Points_for_makeCrv.append(element)
                    self.__CountAddPoint +=1
                    PrintString += "> AddCount{num}, Pos : {pos} \n" .format(num = self.__CountAddPoint , pos = element )
                else:
                    raise TypeError(">> Invalid element in list. Expected a tuple like (0, 0, 0), got: {} " .format(element))
                    
        else:
            raise TypeError(">> Invalid input. Expected a tuple like (0, 0, 0) or a list of such tuples.")
        if Printing:
            print (PrintString)

    def MakeCrv(self , Name = "", Degree = 1):
        self.MainName = "Pocif_Crv"
        if len(self.Points_for_makeCrv)>1:
            if Name == "":
                Name = self.MainNamee
                Count = 1
                while cmds.objExists(Name):
                    Name = "{}{}".format(self.MainName , Count)
                    Count += 1

            self.Crv = cmds.curve(n = Name , d =Degree  , p = self.Points_for_makeCrv)
            self.CrvShp = cmds.listRelatives(self.Crv , s =1)[0]
        else:
            raise TypeError(">> Not enough points to create curve. At least 2 points are required.")
        

    def MakePocifs(self , Name = "" , Suffix = "_Pocif"):
        BaseName = ""
        NodeName = None
        if self.Crv and self.CrvShp:
            if Name == "":
                BaseName = self.Crv
            else:
                BaseName = Name

            Count = 1
            while True:
                NodeName = "{}_{}{}" .format(BaseName , Count , Suffix)
                if not cmds.objExists(NodeName):
                    break
                Count +=1
                

                
                
                



Test = CreatePocifLoc()
sel = cmds.ls(sl =1)

Test.Add_ObjForMakeCrvPos(sel , 1)
Test.MakeCrv()
