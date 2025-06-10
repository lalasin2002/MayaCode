import maya.cmds as cmds
from collections import OrderedDict

class CreatePocifLoc:
    def __init__(self, main_name="Pocif_Crv", suffix_name="_Pocif", loc_suffix="_loc"):
        self.crv = None
        self.crv_shp = None
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
        self.log_messages.append(msg)
        if print_now:
            print(msg)

    def add_object_positions(self, obj, print_log=False):
        if isinstance(obj, str) and cmds.objExists(obj):
            pos = tuple(cmds.xform(obj, q=True, t=True, ws=True))
            self.points_for_make_crv.append(pos)
            self.count_add_point += 1
            self.log("> AddCount {}, obj: {}, Pos: {}".format(self.count_add_point, obj, pos), print_now=print_log)
        elif isinstance(obj, (list, tuple)):
            for x in obj:
                if not isinstance(x, str):
                    raise TypeError(">> Invalid list element type: expected string object name, got {}".format(type(x)))
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
        if (isinstance(pos_list, tuple) and len(pos_list) == 3 and all(isinstance(x, (int, float)) for x in pos_list)):
            self.points_for_make_crv.append(pos_list)
            self.count_add_point += 1
            self.log("> AddCount {}, Pos: {}".format(self.count_add_point, pos_list), print_now=print_log)
        elif isinstance(pos_list, (list, tuple)):
            for element in pos_list:
                if (isinstance(element, tuple) and len(element) == 3 and all(isinstance(x, (int, float)) for x in element)):
                    self.points_for_make_crv.append(element)
                    self.count_add_point += 1
                    self.log("> AddCount {}, Pos: {}".format(self.count_add_point, element), print_now=print_log)
                else:
                    raise TypeError(">> Invalid element in list. Expected a tuple like (0, 0, 0), got: {}".format(element))
        else:
            raise TypeError(">> Invalid input. Expected a tuple like (0, 0, 0) or a list/tuple of such tuples.")

    def define_crv(self, curve, normalization=True):
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
            crv = cmds.rebuildCurve(crv, rebuildType=0, keepRange=0, endKnots=1,
                                   keepControlPoints=1, replaceOriginal=True)
            self.log("Curve rebuilt and normalized: {}".format(crv))

        self.crv = crv
        self.crv_shp = crv_shp
        self.pocif_dic["Curve"] = self.crv
        self.pocif_dic["CurveShape"] = self.crv_shp

    def create_crv(self, name="", degree=1):
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
        self.log("Created curve '{}' with shape '{}'".format(self.crv, self.crv_shp))

    def create_pocifs(self, name="", suffix=None):
        if not self.crv or not self.crv_shp:
            raise RuntimeError(">> Curve and curve shape must be defined before creating pocif nodes.")

        base_name = name if name else self.crv
        suffix = suffix if suffix is not None else self.suffix_name
        self.pocif_nodes = []

        num_points = len(self.points_for_make_crv)
        if num_points < 2:
            raise ValueError(">> Need at least 2 points to create pocif nodes.")

        count = 1
        max_tries = 1000

        for i in range(num_points):
            parameter = i / float(num_points - 1)
            tries = 0

            while tries < max_tries:
                node_name = "{}{}{}".format(base_name, count, suffix)
                if not cmds.objExists(node_name):
                    break
                count += 1
                tries += 1
            else:
                raise RuntimeError(">> Could not find a unique node name after {} attempts.".format(max_tries))

            node = cmds.createNode('pointOnCurveInfo', n=node_name)
            cmds.connectAttr("{}.worldSpace[0]".format(self.crv_shp), "{}.inputCurve".format(node), f=True)
            cmds.setAttr("{}.turnOnPercentage".format(node), 1)
            cmds.setAttr("{}.parameter".format(node), parameter)
            self.pocif_nodes.append(node)
            count += 1

        self.log("Created {} pointOnCurveInfo nodes.".format(len(self.pocif_nodes)))

    def create_locs(self, name="", suffix=None):
        if not self.pocif_nodes:
            raise RuntimeError(">> No pocif nodes available to create locators.")

        base_name = name if name else self.crv
        suffix = suffix if suffix is not None else self.loc_suffix

        self.locs = []
        self.pocif_dic["PocifLocs"] = []

        count = 1
        max_tries = 1000

        for pocif_node in self.pocif_nodes:
            tries = 0
            while tries < max_tries:
                loc_name = "{}{}{}".format(base_name, count, suffix)
                if not cmds.objExists(loc_name):
                    break
                count += 1
                tries += 1
            else:
                raise RuntimeError(">> Could not find a unique locator name after {} attempts.".format(max_tries))

            loc = cmds.spaceLocator(n=loc_name)[0]
            cmds.connectAttr("{}.position".format(pocif_node), "{}.translate".format(loc), f=True)
            self.locs.append(loc)
            self.pocif_dic["PocifLocs"].append({"locator": loc, "pocif_node": pocif_node})
            count += 1

        self.log("Created {} locators connected to pocif nodes.".format(len(self.locs)))

# 사용 예
test = CreatePocifLoc()
sel = cmds.ls(sl=True)

test.add_object_positions(sel, print_log=True)
test.create_crv()
test.create_pocifs()
test.create_locs()
