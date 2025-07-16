from typing import Callable
from enum import Enum


NullValue = -128


class Vector2D:
    """点坐标"""
    __slots__ = ('X', 'Y', 'value')
    def __init__(self, value:int = NullValue):
        self.X = 0
        self.Y = 0
        self.value = value

    def __init__(self, x, y, value:int = NullValue):
        self.X = x
        self.Y = y
        self.value = value

    def __init__(self, pt:tuple[int, int], value:int = NullValue):
        self.X = pt[0]
        self.Y = pt[1]
        self.value = value

    def __init__(self, other: Vector2D):
        self.X = other.X
        self.Y = other.Y
        self.value = other.value
    
    @property
    def x(self) -> int:
        ...
    
    @property
    def y(self) -> int:
        ...
    
    @property
    def data(self) -> tuple[int, int]:
        ...
    
    @property
    def point(self) -> tuple[int, int]:
        ...
    
    @property
    def val(self) -> int:
        ...

    @property
    def length(self) -> float:
        ...

    @property
    def length_sqr(self) -> int:
        ...

    @property
    def size(self) -> int:
        return 2

    def set_value(self, val, check = True):
        """设置值"""
        ...

    def clone(self) -> Vector2D:
        """获取深层拷贝副本"""
        ...

    def to_json(self) -> dict:
        ...

    @staticmethod
    def from_json(json: dict):
        ...

    def __getitem__(self, i) -> int:
        ...

    def __setitem__(self, i, val):
        ...

    def __eq__(self, other):
        """=="""
        ...

    def __ne__(self, other):
        """!="""
        ...

    def __len__(self):
        """ 数据长度 """
        return 2

    def __reversed__(self):
        """ 翻转 """
        ...

    def reversed(self):
        """ 翻转 """
        ...

    def __add__(self, other):
        """ 加法 """
        ...

    __radd__ = __add__

    def __iadd__(self, other):
        """ 加法 """
        ...

    def __sub__(self, other):
        """ 差值 """
        ...

    def __rsub__(self, other):
        """ 差值 """
        ...

    def __isub__(self, other):
        """ 差值 """
        ...

    def __mul__(self, other):
        """ 乘法 """
        ...

    __rmul__ = __mul__

    def __imul__(self, other):
        ...

    def __floordiv__(self, other):
        """ 整除 """
        ...

    def __rfloordiv__(self, other):
        """ 整除 """
        ...

    def __ifloordiv__(self, other):
        ...

    def __neg__(self):
        """负号 向量求反"""
        ...

    def __invert__(self):
        """归一化"""
        ...

    def __hash__(self):
        ...

    def __abs__(self):
        """x,y的绝对值"""
        ...

    def __repr__(self):
        ...

    __str__ = __repr__

    def to_null(self):
        """清除数据
           """
        ...

    def to_0(self):
        ...

    def is_0(self):
        ...

    def is_null(self):
        ...

    def is_valid(self):
        ...

    def is_lattice(self, other):
        """连线是否水平或垂直"""
        ...

    def is_diagonal(self, other):
        """连线是否斜45°"""
        ...
    
    def is_parallel(self, other, structure = 8):
        """连线是否平行"""
        ...

    @classmethod
    def ascending_vector(cls, data):
        ...
    
    def in_size(self, size):
        ...
    
    def in_box(self, pt1, pt2):
        ...




class PointMirrorEnum(Enum):
    """对称类型：无对称，中心对称，x轴对称，y轴对称，x=y轴对称，-x=y轴对称"""
    P = 0
    X = 1
    Y = 2
    XPY = 3
    XSY = 4
    O = 5



class AxisEnum(Enum):
    Null = 0
    X = 1
    Y = 2
    XY = 3


class NeighborTypeEnum(Enum):
    """NeighborTable数据模式"""
    Structure = 0
    Direction = 1
    Mathvector = 2
    Link = 3




def contain_int(val, left = 0, right = 0):
    """测试int是否在范围内"""
    ...
def map_int(val, left = 0, right = 0, circle = 0):
    """调整int到范围内"""
    ...

def as_point(pt):
    """尝试转换为point"""
    ...

def as_vector(pt):
    """尝试转换为Vector"""
    ...

def as_vectorset(pts):
    """尝试转换为Vector"""
    ...

def gcd(vec):
    """x,y的最大公因数"""
    ...

def vector_unit(vec):
    """向量的单位因子"""
    ...

def points_step(vec):
    """向量的单位因子"""
    ...

def vectors_trans(vec1, vec2):
    """转置"""
    ...

def point_mirror_point(pt, origin = (0, 0)):
    """求pt关于点origin的对称 """
    ...

def point_mirror_axis(pt, axis:PointMirrorEnum = PointMirrorEnum.O):
    """求pt关于轴线的对称 """
    ...

def point_mirror_box(pt, corner1, corner2, axis:PointMirrorEnum = PointMirrorEnum.O):
    """求pt在box内的对称 """
    ...

def point_rotate(pt, origin = (0, 0), rotate = 1j):
    """求pt关于点origin的旋转放缩"""
    ...

def point_rotate_box(pt, corner1, corner2, rotate = 1j):
    """求pt关于点origin的旋转放缩"""
    ...





# 轴方向对应的基本向量。
StandardAxisMathvectorMap = {
        0:  Vector2D(0, 0),
        1:  Vector2D(0, 1),
        2:  Vector2D(1, 0),
        3:  Vector2D(1, 1),
        4:  Vector2D(-1, 1),
        -4: Vector2D(1, -1),
        -3: Vector2D(-1, -1),
        -2: Vector2D(-1, 0),
        -1: Vector2D(0, -1)
    }


def structure_mathvector(structure: int):
    """列出常见方向向量
        structure 方向
    """
    ...

def standard_at_axis(axis):
    ...

def region_structure_mathvector(structure: int, region, pt):
    ...

def standard_to_axis(vec):
    """判断方向向量所属的轴线
    """
    ...

def standard_structure_nbrs(pt, structure):
    ...

def standard_filter_structure_set(structure_set: set[int]):
    """删除重复数据"""
    ...


def flatten_as_point(pts):
    """Point数据拍平
    """
    ...

def flatten_as_vector(pts):
    """Point数据拍平
    """
    ...

def points_box(array):
    ...

def box_merge(boxes):
    ...

def points_rank(pt1: Vector2D, pt2: Vector2D) -> list[Vector2D]:
    """获取pt1到pt2所在的直线队列"""
    ...

def points_line(region: 'RegionRect', pt1: Vector2D, pt2: Vector2D) -> tuple[list[Vector2D], bool]:
    """获取pt1到pt2之间的区域"""
    ...


def array_size(array2d):
    """获取2d点阵的尺寸"""
    ...

def array2d_size(array2d):
    """获取2d点阵的尺寸"""
    ...

def rect_slice_trans(start1, stop1, step1, start2, stop2, step2, func: Callable[[int, int], Vector2D]):
    """获取array2d切片"""
    ...

def rect_slice(start1, stop1, start2, stop2):
    """获取array2d切片"""
    ...

def array2d_slice(array2d, slice1:tuple[int, int, int], slice2:tuple[int, int, int], func: Callable[[int, int], Vector2D]):
    """获取array2d切片"""
    ...




class Direction:
    __slots__ = ('axis_mathvector_map',)
    def __init__(self, axis_mathvector_map: dict[int, Vector2D]):
        self.axis_mathvector_map: dict[int, Vector2D] = axis_mathvector_map

    def clone(self):
        ...
    
    def mathvectors(self):
        ...
    
    def region_mathvectors(self, region, pt):
        ...

    def __eq__(self, other):
        ...

    def __ne__(self, other):
        ...

    def __getitem__(self, axis):
        ...

    def add_axis(self, axis, vector):
        ...

    def add_axises(self, listpair):
        ...

    def union_other(self, other):
        ...

    def union_map(self, other):
        ...
    
    def at_axis(self, axis):
        ...
    
    def to_axis(self, vec):
        ...

    @classmethod
    def create_from_axises(cls, axises):
        ...

    @classmethod
    def create_from_mathvectors(cls, mathvectors):
        ...

    @classmethod
    def create_from_structure_set(cls, structure_set):
        ...

    def to_json(self) -> dict:
        ...

    @staticmethod
    def from_json(json: dict):
        ...




class NeighborTable:
    __slots__ = ('structure_map', 'direction_map', 'mathvector_map',
                 'link_map')
    def __init__(self):
        self.structure_map: dict[RegionBase, int] = {}
        self.direction_map: dict[RegionBase, Direction] = {}
        self.mathvector_map: dict[RegionBase, set[Vector2D]] = {}
        self.link_map: dict[Vector2D, set[Vector2D]] = {}

    def set_flag(type:NeighborTypeEnum, state:bool):
        ...

    def get_flag(type:NeighborTypeEnum):
        ...
    
    def clear_nbrs(self):
        ...
    
    @classmethod
    def structure_only(cls, structure_map):
        ...

    @classmethod
    def direction_only(cls, direction_map):
        ...
    
    @classmethod
    def mathvector_only(cls, mathvector_map):
        ...
    
    @classmethod
    def link_only(cls, link_map):
        ...

    def add_structure_map(self, structure_map):
        ...

    def add_direction_map(self, direction_map):
        ...
    
    def add_mathvector_map(self, mathvector_map):
        ...
    
    def add_link_map(self, link_map):
        ...

    def get_structure(self, pt):
        ...

    def get_direction(self, pt):
        ...
    
    def get_structure_direction(self, pt):
        ...

    def get_structure_mathvector(self, pt, baseregion = None):
        ...

    def get_direction_mathvector(self, pt, baseregion = None):
        ...

    def get_mathvector(self, pt):
        ...

    def get_link(self, pt):
        ...

    def point_all_mathvectors(self, pt):
        ...

    def get_nbrs(self, pt, baseregion):
        ...

    def get_nbrs_vects(self, pt, baseregion):
        ...

    def get_axises(self, pt, baseregion):
        ...

    def get_axises_and_vects(self, pt, baseregion):
        ...
    
    def point_axis_nbr(self, pt, axis = 0):
        ...

    def point_nbr_axis(self, pt, nbr):
        """邻居对应的轴向"""
        ...
    
    def structures_mathvector_map(self, baseregion = None):
        """ structures对应的邻居向量"""
        ...

    def directions_mathvector_map(self, baseregion = None):
        """directions对应的邻居向量"""
        ...
    
    def pts_mathvector_map(self):
        """mathvector对应的邻居向量"""
        ...

    def all_mathvectors(self, baseregion = None):
        ...

    def all_nbrs(self, baseregion = None):
        ...

    def clone(self):
        """获取深层拷贝副本"""
        ...

    def to_json(self) -> dict:
        ...

    @staticmethod
    def from_json(json: dict):
        ...



class RegionBase:
    """区域。 表示二维坐标的范围"""
    __slots__ = ('data', 'circle')

    def box(self):
        """bounding box"""
        ...

    def size(self) -> tuple[int, int]:
        """size"""
        ...

    def points(self):
        ...
    
    def contains(self, pt: Vector2D) -> bool:
        """判断点是否在区域内"""
        ...

    def map(self, pt: Vector2D) -> Vector2D|None:
        """调整点到范围内"""
        ...

    def clone(self):
        """获取深层拷贝副本"""
        ...
    
    def delete_point(self, pt) -> 'RegionBase':
        ...

    def __eq__(self, other):
        ...

    def __hash__(self):
        ...

    def to_json(self) -> dict:
        ...

    @staticmethod
    def from_json(json: dict):
        ...




class RegionPoints(RegionBase):
    """区域。 表示离散点坐标的范围"""
    __slots__ = ('data', 'circle')
    def __init__(self, points = None):
        self.data = points or []
        self.circle = 0

    @classmethod
    def new_rank(cls, pt1: Vector2D, pt2: Vector2D) -> 'RegionPoints':
        """获取pt1到pt2所在的直线队列"""
        ...



class RegionLine(RegionBase):
    """区域。 表示一维坐标的范围"""
    __slots__ = ('data', 'circle')
    def __init__(self, n: int, circle = 0):
        ...

    def __init__(self, point, circle = 0):
        ...


class RegionRect(RegionBase):
    """区域。 表示二维矩形坐标的范围"""
    __slots__ = ('data', 'circle')
    def __init__(self, n: int, circle = 0):
        ...

    def __init__(self, point, circle = 0):
        ...

    def __init__(self, pt1, pt2, circle = 0):
        ...

    def __init__(self, data: tuple[int, int, int, int], circle = 0):
        ...

    def point0(self):
        ...

    def point1(self):
        ...

    def get_line(self, pt1: Vector2D, pt2: Vector2D) -> tuple[RegionPoints, bool]:
        """获取pt1到pt2之间的区域"""
        ...



class MoveDest:
    """移动目的地"""
    __slots__ = ('region', 'structure', 'direction', 'mathvector', 'link')
    def __init__(self, region: RegionBase = None,
                        structure: int = 0,
                        direction: Direction = None,
                        mathvector: RegionBase = None,
                        link: RegionBase = None):
        ...

    def to_json(self) -> dict:
        ...

    @staticmethod
    def from_json(json: dict):
        ...
    
    def all_mathvectors(self):
        ...

    def get_structure_direction(self):
        ...

    def get_dest(self, pt):
        '''获取pt的目的地点'''
        ...

    def get_dest_vects(self, pt):
        ...

    def get_axises(self, pt):
        ...

    def clone(self):
        """获取深层拷贝副本"""
        ...

    def in_moved(self, pt0, pt):
        """判断pt是否在pt0移动目标内"""
        ...




class MatrixData:
    """矩阵模板"""
    def __init__(self, size: tuple[int,int], region:RegionBase,
                 neighbortable: NeighborTable, array2d: list[list[int]],
                 movedests: MoveDest = None, value_func = lambda x, y: NullValue):
        ...

    def __init__(self, size:tuple[int,int], region:RegionBase = None, neighbortable: NeighborTable = None):
        ...

    def __init__(self, size:tuple[int,int], structure: int = None,
                 region:RegionBase = None,
                 neighbortable: NeighborTable = None, array2d: list[list[int]]= None,
                 movedests: MoveDest = None, value_func = lambda x, y: 0):
        ...

    def clone(self):
        """获取深层拷贝副本"""
        ...

    def to_json(self) -> dict:
        ...

    @staticmethod
    def from_json(json: dict):
        ...

    def data_clone(self):
        """获取深层拷贝副本"""
        ...

    def set_array2d(self, array2d = None):
        """设置 self._array2d"""
        ...

    @property
    def region(self) -> RegionBase:
        return self._region

    @property
    def circle(self):
        return self._region.circle

    @property
    def array2d(self):
        return self._array2d

    @property
    def neighbortable(self):
        return self._neighbortable

    @property
    def movedests(self):
        return self._movedests

    @property
    def size(self):
        return self._region.size

    def add_dest(self, value, dest):
        ...

    def set_dests(self, dests):
        ...

    def mapping_point(self, pt) -> Vector2D:
        ...

    def mapping_points(self, pts) -> list[Vector2D]:
        ...
    
    def all_points(self):
        """获取多个点"""
        ...
    
    def collection(self, block = None):
        """获取多个点"""
        ...

    def __getitem__(self, index):
        ...

    def __setitem__(self, index, value):
        """默认给None点赋值"""
        ...

    def slice_get(self, slice1:tuple[int, int, int], slice2:tuple[int, int, int]):
        """获取切片"""
        ...

    def slice_set(self, slice1:tuple[int, int, int], slice2:tuple[int, int, int], array2d):
        """给切片范围赋值"""
        ...

    def get_valid_value(self, pt):
        """获取数据，pt超出范围报错"""
        ...

    def get_value(self, pt):
        """获取数据，pt超出范围不报错"""
        ...

    def is_valid(self, pt):
        """判断是否为None"""
        ...

    def delete_point(self, pt):
        """删除点"""
        ...

    def delete_points(self, pts):
        """点pt归空"""
        ...

    def set_value(self, pt, val, check = True):
        """点pt设值"""
        ...

    def set_values(self, pts, vals, check = True):
        """点pt设值"""
        ...
    
    def all_edges(self) -> set[tuple[Vector2D]]:
        """获取边缘点"""
        ...
    
    def get_edges(self, pt) -> set[tuple[Vector2D]]:
        """获取边缘点"""
        ...
    
    def get_edges(self, pts) -> set[tuple[Vector2D]]:
        """获取边缘点"""
        ...

    def to_null(self, pts):
        """点pt归空"""
        ...

    def to_0(self, pts, check = False):
        """点pt归零"""
        ...

    def to_point_value(self, pt1, pt2, check = False):
        """点pt设值为矩阵内值"""
        ...

    def get_value_dest(self, value):
        """获取邻居"""
        ...

    def pt_in_value_dest(self, value, origin, aim):
        """获取邻居"""
        ...

    def get_point_nbrs(self, pt):
        """获取邻居"""
        ...

    def get_point_value_nbrs(self, pt, value = 0):
        """获取邻居"""
        ...
    
    def get_point_nbrs_vects(self, pt):
        """获取邻居"""
        ...
    
    def get_point_axises_and_vects(self, pt):
        """获取邻居"""
        ...

    def point_move_vector(self, pt, vector):
        """点pt移动vector后的坐标 """
        ...

    def point_axis_vector(self, pt, axis = 0):
        """点pt移动axis后的vector """
        ...

    def point_axis_pairs(self, pt, axises = tuple()):
        """过某点的直线方向对，默认相反数为pair"""
        ...

    def point_vector_pairs(self, pt):
        """过某点的直线方向对，默认相反数为pair"""
        ...

    def search_value_vector(self, pt, vector, value = NullValue):
        """扫描直线上的点, 不包括pt
            vector：方向
        """
        ...

    def search_endvalue_vector(self, pt, vector, end_value = NullValue):
        """扫描直线上的点, 不包括pt, 直到end_value
            vector：方向
        """
        ...

    def search_value_vector_pairs(self, pt, pair:tuple, value = NullValue):
        """双向扫描直线上的点, 包括pt
            vector：方向
        """
        ...

    def search_endvalue_vector_pairs(self, pt, pair:tuple, end_value = NullValue):
        """双向扫描直线上的点, 包括pt, 直到end_value
            vector：方向
        """
        ...

    def search_value_axis_pairs(self, pt, axis = 1, value = NullValue, sides = False):
        """双向扫描直线上的点, 包括pt
            axis：方向
            sides: 是否同时扫描两侧
        """
        ...

    def search_endvalue_axis_pairs(self, pt, axis = 1, end_value = NullValue, sides = False):
        """扫描直线上的点, 包括pt, 直到val
            axis：方向
            sides: 是否同时扫描两侧
        """
        ...

    def search_line(self, pt1, pt2, val = NullValue, structure = 8):
        """扫描直线上的两点，并判断共线、求向量
           val: 如果val不是None则判断之间值是否全部为val
        """
        ...

    def collection_line(self, pt1, pt2):
        """获取多个点，不包括起止点"""
        ...
    def move_links(links):
        ...

    def group_move_pairs(pairs):
        ...
    
    def move_pairs(pairs):
        ...

    def search_block(self, pt):
        """查找连通的棋块"""
        ...

    def block_nbrs(self, block):
        """查找连通的棋块所有的行走的出路（气的位置）"""
        ...

    def block_liberties(self, block):
        """Liberties 计算出路数量，气的个数"""
        ...

    def liberties_test(self, pt, val, robbery = tuple()):
        """模拟并测试该点落子后的情况"""
        ...

    def dead_nbrs(self, pt):
        """无气的异值邻居"""
        ...

    def dead_value_nbrs(self, pt, val):
        """无气的值为val的邻居"""
        ...

    def dead_all(self, val):
        """值为val的所有点均无气"""
        ...

    def val_count(self, val):
        """计数"""
        ...

    def all_filled(self):
        """棋盘是否满了"""
        ...

    def skip_test(self, pt1, pt2, value = NullValue):
        """隔一子跳"""
        ...

    def search_skip(self, pt, value = NullValue):
        """隔一子跳"""
        ...

    def search_value(self, value):
        ...

    def search_in_row(self, pt, n):
        """判断数子连珠 连珠个数不到n则返回[]"""
        ...

    def search_pincer(self, pt, value, end_value):
        """查找pt和某个同值点夹击异值val点"""
        ...

    def search_to_face(self, pt, other, structure = 0):
        """判断棋子共线、照面， 即直线连接并且中间值为0
        """
        ...
    
    def search_shortest_path(self, pt1, pt2, skip = True, test_func = None):
        ...



class Coordinate:
    """格线坐标系"""
    __slots__ = ('grid_size', 'x_segments', 'y_segments')
    def __init__(self, grid_size, x_vects, y_vects):
        ...

    def to_json(self) -> dict:
        ...

    @staticmethod
    def from_json(json: dict):
        ...

    @classmethod
    def get_segments(self, vects: list[Vector2D], count = 0, axis = AxisEnum.X):
        ...

    def get_dot(self, pt):
        """获取格线坐标"""
        ...

    @classmethod
    def closet_index(cls, segments, count, n, side = 0):
        ...

    def get_pt(self, dot):
        """获取格线坐标"""
        """根据画布位置 查找坐标"""
        ...


class CanvasGrid:
    """画布上的位置坐标系"""
    __slots__ = ('size', 'canvas_size', 'is_net', 'boundless',
                'temp_pts_dots', 'net_size', 'padding',
                'coordinate', 'origin')
    def __init__(self, size = (0, 0), canvas_size = (0, 0),
                    is_net = True, boundless = True,
                    padding = (0, 0), coordinate = None, origin = (0,0), 
                    obliquity = 1j, centered = True):
        """坐标系
            size: 划分的行列大小
            origin：源点的坐标，画布在这个坐标上增加
            canvas_size：画布的像素大小
            padding：边框
            is_net: 是网状还是格子状
            boundless: 是否收边，不收边的位置不能落子
            obliquity：高宽比与倾斜度，用复数表示，nj为垂直，-nj为自动长度
            centered: 居中对齐
            注：根据复数性质，虚部系数为负时，幅角大于2pi。
        """
        ...

    def compute_coordinate(self, obliquity:complex):
        """单个格子的尺寸，并修正padding"""
        ...
    
    def pt_in_size(self, pt):
        """判断pt是否在size范围内"""
        ...

    def dot_in_canvas(self, dot):
        """判断是否在canvas_size范围内"""
        ...

    def to_json(self) -> dict:
        ...

    @staticmethod
    def from_json(json: dict):
        ...
    
    @property
    def x_segs(self):
        ...
    
    @property
    def y_segs(self):
        ...
    
    @property
    def x_cell(self):
        ...
    
    @property
    def y_cell(self):
        ...

    def dot_in_net(self, dot, e = 35):
        """判断是否在格线范围内"""
        ...
    
    def net_origin(self, is_net = None):
        """获取第一个有效的net点"""
        ...

    def get_dot(self, pt, is_net = None):
        """获取位置点"""
        ...

    def close_point(self, dot):
        """根据画布位置 查找坐标"""
        ...

    def edge_origin(self, axis = AxisEnum.X):
        """获取格线的起点"""
        ...

    def get_axis_edge(self, index = 0, axis = AxisEnum.X):
        """获取格线的边缘点"""
        ...

    def get_axis_edges(self, axis = AxisEnum.X):
        """获取格线的边缘点"""
        ...

    def get_coors(self, axis = AxisEnum.XY, distance = 0.5):
        """计算网格坐标系坐标文字"""
        ...

    def get_stars(self):
        """计算网格坐标系星位"""
        ...

    def get_line(self, edge):
        """计算网格坐标系线框"""
        ...

    def get_lines(self, edges):
        """计算网格坐标系线框"""
        ...

    def get_rect(self, pt):
        """获取格子矩形"""
        ...

    def get_cells(self, pts):
        """计算网格坐标系线框"""
        ...

    def get_cltags(self, pts):
        """计算网格坐标系线框"""
        ...

    def get_pieces_box(self, n):
        """获取棋盒列表"""
        ...

