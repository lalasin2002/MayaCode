import maya.cmds as cmds
import pprint
import re



class CntBlsh():
    def __init__(self):
        Brow = 'BrowBlsh_Ctrl'
        Eye = 'EyeBlsh_Ctrl'
        Mouth = 'MouthBlsh_Ctrl'


        Blsh = cmds.ls(type = 'blendShape')

        Pattern = r'^(Eye|Face|Mouth)(?:_L|_R)?$'
        Com = re.compile(Pattern)
        Blshlst = []

        #print ("_____________")
        print (Blsh)
        for x in Blsh:

            match = Com.match(x)
            if match:
                Blshlst.append(x)

        Blsh_Target_lst = []

        for x in Blshlst:
            Attr = cmds.listAttr('{}.w' .format(x) ,m =1)
            for y in Attr:
                Target = x + '.' + y
                Blsh_Target_lst.append(Target)

        Dic = {}

        Molst =[]
        Brlst =[]
        Eylst = []
        for x in Blsh_Target_lst:
            SplitTarget = x.split(".")[-1]

            if 'Mo' in SplitTarget:
                Molst.append(x)
            elif 'Br' in SplitTarget:
                Brlst.append(x)
            elif 'Ey' in SplitTarget:
                Eylst.append(x)

        Dic[Mouth] = Molst
        Dic[Brow] = Brlst
        Dic[Eye] = Eylst

        pprint.pprint(Dic)

        for x ,lstT in Dic.items():
            for y in lstT:
                split_st = y.split('.')[-1].split("_")
                split_st.pop(0)
                Attr = "_".join(split_st)

                if not any( Attr == at for at in  cmds.listAttr(x , k =1 , iu =1)):
                    cmds.addAttr(x , at ='double', longName = Attr ,  defaultValue=0, minValue=0, maxValue=10,k=1 )


        for x ,lstT in Dic.items():
            for y in lstT:
                BlshT = y.split('.')
                CtrlAttr = '.' + "_".join(BlshT[-1].split('_')[1:])
                print (BlshT , CtrlAttr)

                try:
                    cmds.setDrivenKeyframe(BlshT[0], at=BlshT[-1], cd=x + CtrlAttr, itt='linear', ott='linear')
                    cmds.setAttr(x + CtrlAttr , 10)
                    cmds.setAttr(y , 1)
                    cmds.setDrivenKeyframe(BlshT[0], at=BlshT[-1], cd=x + CtrlAttr, itt='linear', ott='linear')
                    cmds.setAttr(x + CtrlAttr , 0)
                    cmds.setAttr(y , 0)
                except:
                    pass





CntBlsh()