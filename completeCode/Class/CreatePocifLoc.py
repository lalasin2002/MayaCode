# -*- coding: utf-8 -*-
import maya.cmds as cmds
from collections import OrderedDict

class CreatePocifLoc:
    def __init__(self, main_name="Pocif_Crv", suffix_name="_Pocif", loc_suffix="_loc"):
        '''
        NURBS 커브를 생성하고, pointOnCurveInfo 노드를 이용해 커브 위의 특정 지점들에
        로케이터(Locator)를 자동으로 생성 및 연결하기 위한 클래스입니다.\n

        =======================메서드 설명========================\n
        =
        __init__: 클래스 초기화 및 기본 이름/접미사 설정.\n
        log: 작업 내역을 내부 리스트에 기록.\n
        clear_position: 추가된 모든 위치 정보를 초기화.\n
        add_object_positions: 오브젝트의 월드 좌표를 커브 생성 포인트로 추가.\n
        add_positions: XYZ 좌표값을 커브 생성 포인트로 직접 추가.\n
        define_crv: 씬에 이미 존재하는 커브를 사용하도록 지정.\n
        create_crv: 추가된 위치 정보로 새로운 커브를 생성.\n
        create_pocif: 커브 위의 특정 위치에 pointOnCurveInfo 노드를 1개 생성.\n
        create_loc: pointOnCurveInfo 노드에 연결될 로케이터를 1개 생성.\n
        create_pocifs: 지정된 개수만큼 pointOnCurveInfo 노드들을 균일한 간격으로 생성.\n
        create_locs: pocif 노드 리스트에 각각 로케이터를 생성하여 연결.\n
        create_pocif_locs: pocif 노드와 로케이터를 한 번의 명령으로 모두 생성.\n
        
        
        Args:
            main_name (str): 생성될 커브의 기본 이름.\n
            suffix_name (str): 생성될 pointOnCurveInfo 노드의 기본 접미사.\n
            loc_suffix (str): 생성될 로케이터의 기본 접미사.\n
        '''
        self.crv = None
        self.crv_shp = None
        self.pocif_node = None

        self.locs = []
        self.pocif_nodes = []
        self.points_for_make_crv = []
        self.count_add_point = 0
        self.main_name = main_name
        self.suffix_name = suffix_name
        self.loc_suffix = loc_suffix
        self.pocif_dic = OrderedDict()
        self.log_messages = []

    def log(self, msg, print_now=False):
        """
        작업 내역을 로그 리스트에 추가하고, 필요시 콘솔에 출력합니다.\n

        Args:
            msg (str): 기록할 메시지.
            print_now (bool): True이면 콘솔에 즉시 출력합니다.
        """
        self.log_messages.append(msg)
        if print_now:
            print(msg)

    def clear_position(self):
        """커브 생성을 위해 추가된 모든 위치 정보(points_for_make_crv)를 초기화합니다."""
        self.points_for_make_crv = []
        self.count_add_point = 0
        self.log("Cleared all stored positions.", print_now=True)

    def add_object_positions(self, obj, print_log=False):
        """
        오브젝트의 월드 공간(world space) 위치를 커브 생성을 위한 포인트로 추가합니다.

        Args:
            obj (str or list/tuple): 위치를 가져올 오브젝트의 이름 또는 이름의 리스트.
            print_log (bool): 로그 메시지를 콘솔에 즉시 출력할지 여부.
        """
        if isinstance(obj, str) and cmds.objExists(obj):
            pos = tuple(cmds.xform(obj, q=True, t=True, ws=True))
            self.points_for_make_crv.append(pos)
            self.count_add_point += 1
            self.log("> AddCount {}, obj: {}, Pos: {}".format(self.count_add_point, obj, pos), print_now=print_log)
        elif isinstance(obj, (list, tuple)):
            for x in obj:
                if cmds.objExists(x):
                    pos = tuple(cmds.xform(x, q=True, t=True, ws=True))
                    self.points_for_make_crv.append(pos)
                    self.count_add_point += 1
                    self.log("> AddCount {}, obj: {}, Pos: {}".format(self.count_add_point, x, pos), print_now=print_log)
                else:
                    self.log(">> Object does not exist: {}".format(x), print_now=print_log)
        else:
            raise TypeError(">> Invalid object type. Expected a string or a list/tuple of strings.")

    def add_positions(self, pos_list, print_log=False):
        """
        좌표값(tuple) 또는 좌표값의 리스트를 커브 생성을 위한 포인트로 직접 추가합니다.

        Args:
            pos_list (tuple or list): (x,y,z) 형식의 튜플 또는 이런 튜플들의 리스트.
            print_log (bool): 로그 메시지를 콘솔에 즉시 출력할지 여부.
        """
        if (isinstance(pos_list, tuple) and len(pos_list) == 3 and all(isinstance(x, (int, float)) for x in pos_list)):
            self.points_for_make_crv.append(pos_list)
            self.count_add_point += 1
            self.log("> AddCount {}, Pos: {}".format(self.count_add_point, pos_list), print_now=print_log)
        elif isinstance(pos_list, (list, tuple)):
            for element in pos_list:
                if (isinstance(element, tuple) and len(element) == 3 and all(isinstance(x, (int, float)) for x in element)):
                    if isinstance(element , list):  #2025-06-12 list이면 튜플화
                        element = tuple(element)  # 
                    self.points_for_make_crv.append(element)
                    self.count_add_point += 1
                    self.log("> AddCount {}, Pos: {}".format(self.count_add_point, element), print_now=print_log)
                else:
                    raise TypeError(">> Invalid element in list. Expected a tuple like (0, 0, 0), got: {}".format(element))
        else:
            raise TypeError(">> Invalid input. Expected a tuple like (0, 0, 0) or a list/tuple of such tuples.")

    def define_crv(self, curve, normalization=True):
        """
        씬에 이미 존재하는 커브를 이 클래스에서 사용하도록 지정합니다.

        Args:
            curve (str): 사용할 커브의 transform 또는 shape 노드 이름.
            normalization (bool): True이면 커브의 파라미터를 0-1 범위로 정규화(rebuild)합니다.
        """
        crv = None
        crv_shp = None
        if isinstance(curve, str):
            obj_type = cmds.objectType(curve)
            if obj_type == "transform":
                shapes = cmds.listRelatives(curve, s=True, type="nurbsCurve")
                if shapes:
                    crv = curve
                    crv_shp = shapes[0]
                else:
                    raise ValueError(">> No nurbsCurve shape found under transform {}".format(curve))
            elif obj_type == "nurbsCurve":
                parents = cmds.listRelatives(curve, p=True, type="transform")
                if parents:
                    crv_shp = curve
                    crv = parents[0]
                else:
                    raise ValueError(">> No transform parent found for nurbsCurve {}".format(curve))
            else:
                raise TypeError(">> Invalid input. Expected a transform or nurbsCurve node name (string).")
        else:
            raise TypeError(">> Invalid input. Expected a string for curve name.")

        if normalization:
            result = cmds.rebuildCurve(crv, rebuildType=0, keepRange=0, endKnots=1,
                                     keepControlPoints=1, replaceOriginal=True)
            crv = result[0]
            self.log("Curve rebuilt and normalized: {}".format(crv))

        self.crv = crv
        self.crv_shp = cmds.listRelatives(crv, s=True, type="nurbsCurve")[0]
        self.pocif_dic["Curve"] = self.crv
        self.pocif_dic["CurveShape"] = self.crv_shp
        self.pocif_dic["Connections"] = OrderedDict()

    def create_crv(self, name="", degree=1):
        """
        add_positions나 add_object_positions로 추가된 위치들을 기반으로 새로운 커브를 생성합니다.

        Args:
            name (str): 생성할 커브의 이름. 지정하지 않으면 __init__의 main_name을 따릅니다.
            degree (int): 커브의 디그리(degree). 1은 직선, 3은 부드러운 곡선입니다.
        """
        if len(self.points_for_make_crv) < 2:
            raise ValueError(">> Not enough points to create curve. At least 2 points are required.")
        
        base_name = name if name else self.main_name
        count = 1
        candidate_name = base_name

        while cmds.objExists(candidate_name):
            candidate_name = "{}{}".format(base_name, count)
            count += 1

        self.crv = cmds.curve(n=candidate_name, d=degree, p=self.points_for_make_crv)
        shapes = cmds.listRelatives(self.crv, s=True) or []
        if not shapes:
            raise RuntimeError(">> Failed to create curve shape for {}".format(self.crv))
        self.crv_shp = cmds.rename(shapes[0], self.crv + "Shape")
        self.pocif_dic["Curve"] = self.crv
        self.pocif_dic["CurveShape"] = self.crv_shp
        self.pocif_dic["Connections"] = OrderedDict()
        self.log("Created curve '{}' with shape '{}'".format(self.crv, self.crv_shp))

    def create_pocif(self, parameter=0, name="", suffix=None):
        """
        정의된 커브 위의 특정 파라미터 위치에 pointOnCurveInfo 노드를 1개 생성합니다.

        Args:
            parameter (float): pocif 노드가 위치할 커브 파라미터 (0.0 ~ 1.0).
            name (str): 생성될 노드의 기본 이름. 지정하지 않으면 커브 이름을 따릅니다.
            suffix (str): 생성될 노드의 접미사. 지정하지 않으면 __init__의 suffix_name을 따릅니다.
        """
        if not self.crv or not self.crv_shp:
            raise RuntimeError(">> Curve and curve shape must be defined before creating pocif nodes.")
        
        base_name = name if name else self.crv
        suffix_to_use = suffix if suffix is not None else self.suffix_name
        
        count = 0
        while True:
            node_name = "{}{}{}".format(base_name, "" if count == 0 else count, suffix_to_use)
            if not cmds.objExists(node_name):
                break
            count += 1
            
        node = cmds.createNode('pointOnCurveInfo', n=node_name)
        cmds.connectAttr("{}.worldSpace[0]".format(self.crv_shp), "{}.inputCurve".format(node), f=True)
        cmds.setAttr("{}.turnOnPercentage".format(node), 1)
        cmds.setAttr("{}.parameter".format(node), parameter)
        self.pocif_nodes.append(node)
        self.pocif_node = node
        self.log("Create '{}' pointOnCurveInfo node".format(self.pocif_node))

    def create_loc(self, pocif=None, name="", suffix=None):
        """
        지정된 pointOnCurveInfo 노드에 연결될 로케이터를 1개 생성합니다.

        Args:
            pocif (str, optional): 연결할 pointOnCurveInfo 노드. 지정하지 않으면 마지막으로 생성된 pocif 노드를 사용합니다.
            name (str, optional): 생성될 로케이터의 기본 이름. 지정하지 않으면 pocif 노드 이름을 따릅니다.
            suffix (str, optional): 생성될 로케이터의 접미사. 지정하지 않으면 __init__의 loc_suffix를 따릅니다.
        """
        if pocif is None:
            pocif = self.pocif_node
        
        base_name = name if name else pocif
        suffix_to_use = suffix if suffix is not None else self.loc_suffix

        count = 0
        while True:
            loc_name = "{}{}{}".format(base_name, "" if count == 0 else count, suffix_to_use)
            if not cmds.objExists(loc_name):
                break
            count += 1
            
        loc = cmds.spaceLocator(n=loc_name)[0]
        cmds.connectAttr("{}.position".format(pocif), "{}.translate".format(loc), f=True)
        self.locs.append(loc)
        
        if "Connections" in self.pocif_dic:
            self.pocif_dic["Connections"][loc] = pocif 

        self.pocif_node = None
        self.log("Create '{}' locator connected to '{}' pointOnCurveInfo".format(loc, pocif))

    def create_pocifs(self, count_or_objs, name="", suffix=None):
        """
        정수 또는 리스트를 입력받아, 그 개수만큼 pocif 노드를 커브 위에 균일한 간격으로 생성합니다.

        Args:
            count_or_objs (int or list/tuple): 생성할 노드의 개수(int) 또는 길이를 셀 리스트.
            name (str, optional): 생성될 노드의 기본 이름.
            suffix (str, optional): 생성될 노드의 접미사.
        """
        num_to_create = 0
        if isinstance(count_or_objs, int):
            if count_or_objs < 1:
                raise ValueError(">> Input integer must be 1 or greater.")
            num_to_create = count_or_objs
        
        elif isinstance(count_or_objs, (list, tuple)):
            if not count_or_objs:
                raise ValueError(">> Input list/tuple cannot be empty.")
            num_to_create = len(count_or_objs)
            
        else:
            raise TypeError(">> Input must be an integer or a list/tuple.")

        if not self.crv or not self.crv_shp:
            raise RuntimeError(">> A curve must be defined before creating pocif nodes.")
            
        for i in range(num_to_create):
            parameter = (1.0 / (num_to_create - 1)) * i if num_to_create > 1 else 0.0
            self.create_pocif(parameter, name, suffix)

    def create_locs(self, pocifs=None, name="", suffix=None):
        """
        주어진 pocif 노드 리스트에 대해 각각 로케이터를 생성하고 연결합니다.

        Args:
            pocifs (list, optional): 로케이터를 생성할 pocif 노드들의 리스트. 지정하지 않으면 클래스 내부에 저장된 모든 pocif 노드를 사용합니다.
            name (str, optional): 생성될 로케이터의 기본 이름.
            suffix (str, optional): 생성될 로케이터의 접미사.
        """
        if pocifs is None:
            if not self.pocif_nodes:
                self.log(">> No pocif nodes to create locators for.", print_now=True)
                return
            pocifs = self.pocif_nodes

        if not isinstance(pocifs, (list, tuple)):
             raise ValueError(">> Invalid input: 'pocifs' must be a list or tuple.")

        if not self.crv or not self.crv_shp:
            raise RuntimeError(">> A curve must be defined before creating pocif nodes.")
        
        for i, x in enumerate(pocifs):
            if not cmds.objExists(x) or cmds.objectType(x) != 'pointOnCurveInfo':
                self.log(">> Skipping invalid item: '{}' is not a valid pointOnCurveInfo node.".format(x))
                continue
            self.create_loc(x, name, suffix)

    def create_pocif_locs(self, count_or_objs, name="", pocif_suffix=None, loc_suffix=None):
        """
        pocif 노드들과 로케이터들을 한 번의 명령으로 모두 생성하고 연결합니다.

        Args:
            count_or_objs (int or list/tuple): 생성할 노드의 개수(int) 또는 길이를 셀 리스트.
            name (str, optional): 생성될 노드들의 기본 이름.
            pocif_suffix (str, optional): pocif 노드에만 적용할 접미사.
            loc_suffix (str, optional): 로케이터에만 적용할 접미사.
        """
        self.create_pocifs(count_or_objs, name, pocif_suffix)
        self.create_locs(self.pocif_nodes, name, loc_suffix)