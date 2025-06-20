
from typing import Callable, TypeVar
from .until import (RegionModeEnum, NeighborTypeEnum, PointMirrorEnum)



PointTransformation = Callable[[tuple[int, int]|TypeVar('Vector2D')], TypeVar('Vector2D')|None]


NullValue = -128





def contain_int(n, left = 0, right = 0):
    """测试int是否在范围内"""
    return left <= n < right

def map_int(n, left = 0, right = 0, circle = 0):
    """调整int到范围内"""
    if contain_int(n, left, right):
        return n
    if circle != 0:
        if (n := (n - left)%(right - left) + left) < left:
            n += (right - left)
    else:
        n = None
    return n


def as_point(pt):
    """尝试转换为point"""
    match pt:
        case Vector2D():
            return pt.data
        case (int(x), int(y)):
            return (x, y)
        case (x,):
            return as_point(x)
    return None

def as_vector(pt):
    """尝试转换为Vector"""
    match pt:
        case Vector2D():
            return pt
        case (int(),int()):
            return Vector2D(*pt)
        case (x,):
            return as_vector(x)
    return None

def gcd(vec):
    """x,y的最大公因数"""
    if vec[0] == 0 or vec[1] == 0:
        return 0
    def _gcd(p, q):
        if p < q: p,q = q,p
        return p if q == 0 else _gcd(p, p%q)
    return _gcd(abs(vec[0]), abs(vec[1]))

def unit(vec):
    """向量的单位因子"""
    x, y = vec
    match x,y:
        case 0, 0:
            return Vector2D(0, 0)
        case 0, _:
            return Vector2D(0, 1 if y > 0 else -1)
        case _, 0:
            return Vector2D(1 if x > 0 else -1, 0)
        case (_, 1)|(1, _)|(_, -1)|(-1, _):
            return Vector2D(x, y)
        case _, _:
            p = gcd(vec)
            return Vector2D(x//p, y//p)

def points_step(vec):
    """向量的单位因子"""
    x, y = vec
    match x,y:
        case 0, 0:
            return Vector2D(0, 0), 0
        case 0, _:
            return Vector2D(0, 1 if y > 0 else -1), abs(y)
        case _, 0:
            return Vector2D(1 if x > 0 else -1, 0), abs(x)
        case (_, 1)|(1, _)|(_, -1)|(-1, _):
            return Vector2D(x, y), 1
        case _, _:
            p = gcd(vec)
            return Vector2D(x//p, y//p), p





class Vector2D:
    """点坐标"""
    __slots__ = ('X', 'Y', 'value')
    
    def __init__(self, *args, value: int = NullValue):
        if len(args) == 0:  # 无参数情况
            self.X, self.Y = 0, 0
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, tuple):  # 元组 (x,y)
                self.X, self.Y = arg
            elif isinstance(arg, Vector2D):  # 另一个 Vector2D 对象
                self.X, self.Y = arg.X, arg.Y
                value = arg.value  # 继承原值
            else:  # 单个整数 (视为 value)
                self.X, self.Y = 0, 0
                value = arg
        elif len(args) == 2:  # (x, y)
            self.X, self.Y = args
        elif len(args) == 3:  # (x, y)
            self.X, self.Y, value = args
        else:
            raise TypeError("Invalid arguments for Vector2D")
        self.value = value

    @property
    def x(self):
        return self.X

    @property
    def y(self):
        return self.Y

    @property
    def data(self):
        return (self.X, self.Y)

    @property
    def point(self):
        return (self.X, self.Y)

    @property
    def length(self):
        return self.length_sqr**0.5

    @property
    def length_sqr(self):
        return self.X**2 + self.Y**2

    @property
    def val(self):
        return self.value

    def __getitem__(self, i):
        return self.data[i]

    def set_value(self, val, check = True):
        """设置值"""
        if check and self.value is None:
            return
        self.value = val

    def __eq__(self, other):
        """=="""
        return self.data == as_point(other)

    def __ne__(self, other):
        """!="""
        return not self.__eq__(other)

    def __len__(self):
        """ 数据长度 """
        return 2

    def __iter__(self):
        yield self.X
        yield self.Y

    def to_json(self) -> dict:
        return {"Vector2D": [self.X, self.Y, self.value]}

    @staticmethod
    def from_json(json: dict):
        return Vector2D(*json["Vector2D"])

    def __reversed__(self):
        """ 翻转 """
        return self.__class__(self.y, self.x, value = self.value)

    def reversed(self):
        """ 翻转 """
        return reversed(self)

    def __add__(self, other):
        """ 加法 """
        other = self.__class__(*other)
        return self.__class__(self.x+other.x, self.y+other.y, value = self.value)

    __radd__ = __add__

    def __iadd__(self, other):
        """ 加法 """
        other = self.__class__(*other)
        return self.__class__(self.x+other.x, self.y+other.y, value = self.value)

    def __sub__(self, other):
        """ 差值 """
        other = self.__class__(*other)
        return self.__class__(self.x-other.x, self.y-other.y, value = self.value)

    def __rsub__(self, other):
        """ 差值 """
        other = self.__class__(*other)
        return other - self

    def __isub__(self, other):
        """ 差值 """
        other = self.__class__(*other)
        return self.__class__(self.x-other.x, self.y-other.y, value = self.value)

    def __mul__(self, other):
        """ 乘法 """
        if isinstance(other, (float, int)):
            return self.__class__(int(self.x*other), int(self.y*other), value = self.value)
        if isinstance(other, complex):
            c = self.complex*other
            return self.__class__(round(c.real), round(c.imag), value = self.value)
        other = self.__class__(*other)
        return self.__class__(self.x*other.x, self.y*other.y, value = self.value)

    __rmul__ = __mul__

    def __imul__(self, other):
        if isinstance(other, (float, int)):
            return self.__class__(int(self.x*other), int(self.y*other), value = self.value)
        other = self.__class__(*other)
        return self.__class__(self.x*other.x, self.y*other.y, value = self.value)

    def __floordiv__(self, other):
        """ 整除 """
        if isinstance(other, (float, int)):
            return self.__class__(int(self.x//other), int(self.y//other), value = self.value)
        other = self.__class__(*other)
        return self.__class__(self.x//other.x, self.y//other.y, value = self.value)

    def __rfloordiv__(self, other):
        """ 整除 """
        other = self.__class__(*other)
        return other//self

    def __ifloordiv__(self, other):
        if isinstance(other, (float, int)):
            return self.__class__(int(self.x//other), int(self.y//other), value = self.value)
        other = self.__class__(*other)
        return self.__class__(self.x//other.x, self.y//other.y, value = self.value)

    def __neg__(self):
        """负号 向量求反"""
        return self.__class__(-self.x, -self.y, value = self.value)

    def __invert__(self):
        """归一化"""
        # 符号函数
        f = lambda p: 1 if p>0 else (-1 if p<0 else 0)
        return self.__class__(f(self.x), f(self.y), value = self.value)

    def __hash__(self):
        return self.data.__hash__()

    def __abs__(self):
        """x,y的绝对值"""
        return self.__class__(abs(self.x), abs(self.y), value = self.value)

    def __repr__(self):
        return f'{self.__class__.__name__}{self.data}({self.value})'

    __str__ = __repr__

    def to_nil(self):
        """清除数据
           """
        self.value = None

    def to_0(self):
        self.value = 0

    def to_1(self):
        self.value = 1

    def to_2(self):
        self.value = 2

    def is_lattice(self, other):
        """连线是否水平或垂直"""
        x,y = self - other
        return x == 0 or y == 0

    def is_diagonal(self, other):
        """连线是否斜45°"""
        x,y = self - other
        return x == y or x == -y
    
    def is_parallel(self, other, structure = 8):
        """连线是否平行"""
        if structure == 4 and self.is_lattice(other):
            return True
        elif structure == -4 and self.is_diagonal(other):
            return True
        elif structure == 8 and (self.is_diagonal(other) or self.is_lattice(other)):
            return True
        elif structure == 0:
            return True
        else:
            if unit(self) - unit(other) == 0:
                return True
            if unit(self) + unit(other) == 0:
                return True
        return False

    @classmethod
    def ascending_vector(cls, data):
        vect = cls(*data)
        if vect.x > vect.y:
            return reversed(vect)
        return vect
    
    def in_size(self, size):
        x, y = size
        return contain_int(self.x, 0, x) and contain_int(self.y, 0, y)
    
    def in_box(self, pt1, pt2):
        x1,y1 = pt1
        x2,y2 = pt2
        return contain_int(self.x, x1, x2) and contain_int(self.y, y1, y2)


# 轴方向对应的基本向量。
axis_mathvector_map = {
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
    match structure:
        case 0:
            return (axis_mathvector_map[0],)
        case 1:
            return (axis_mathvector_map[2],)
        case -1:
            return (axis_mathvector_map[-2],)
        case 2:
            return (axis_mathvector_map[2],
                    axis_mathvector_map[-2])
        case -2:
            return (axis_mathvector_map[1],
                    axis_mathvector_map[-1])
        case 3:
            return (axis_mathvector_map[2],
                    axis_mathvector_map[1],
                    axis_mathvector_map[-1])
        case -3:
            return (axis_mathvector_map[-2],
                    axis_mathvector_map[1],
                    axis_mathvector_map[-1])
        case 4:
            return (axis_mathvector_map[2],
                    axis_mathvector_map[-2],
                    axis_mathvector_map[1],
                    axis_mathvector_map[-1])
        case -4:
            return (axis_mathvector_map[3],
                    axis_mathvector_map[-3],
                    axis_mathvector_map[4],
                    axis_mathvector_map[-4])
        case 8:
            return (axis_mathvector_map[2],
                    axis_mathvector_map[-2],
                    axis_mathvector_map[1],
                    axis_mathvector_map[-1],
                    axis_mathvector_map[3],
                    axis_mathvector_map[-3],
                    axis_mathvector_map[4],
                    axis_mathvector_map[-4])
        case _:
            return (axis_mathvector_map[0])


def region_structure_mathvector(structure: int, region, pt):
    mathvector = structure_mathvector(structure)
    return [v for v in mathvector if pt+v in region]


def at_axis(axis):
    return axis_mathvector_map.get(axis)


def to_axis(vec):
    """判断方向向量所属的轴线
    """
    x,y = vec
    if x > 0 and y == 0:
        return 2
    elif x < 0 and y == 0:
        return -2
    elif x == 0 and y > 0:
        return 1
    elif x == 0 and y < 0:
        return -2
    elif x == y and x > 0:
        return 3
    elif x == y and x < 0:
        return -3
    elif x == -y and y > 0:
        return 4
    elif x == -y and y < 0:
        return -4
    return 0



def filter_structure_set(structure_set: set[int]):
    """删除重复数据"""
    # 特殊情况
    if 8 in structure_set:
        return set([8])
    if 4 in structure_set and -4 in structure_set:
        return set([8])
    # 清除数字
    if 0 in structure_set:
        structure_set.remove(0)
        return filter_structure_set(structure_set)
    def find_4(_structure_set):
        if 4 in _structure_set:
            for i in [1, -2, -1, 2, 3, -3]:
                if i in _structure_set:
                    _structure_set.remove(i)
    find_4(structure_set)
    # 组合情况
    def find_com(_structure_set, x, y, a):
        if x in _structure_set and y in _structure_set:
            _structure_set.remove(x)
            _structure_set.remove(x)
            _structure_set.add(a)
            return True
        return False
    # 找2
    find_com(structure_set, 1, -1, 2)
    if find_com(structure_set, 2, -2, 4): find_4()
    # 找3、-3
    find_com(structure_set, 1, -2, 3)
    find_com(structure_set, -1, -2, -3)
    if find_com(structure_set, 3, -3, 4): find_4()
    if find_com(structure_set, 1, -3, 4): find_4()
    if find_com(structure_set, -1, 3, 4): find_4()
    return structure_set





class Direction:
    __slots__ = ('axis_mathvector_map',)
    def __init__(self, axis_mathvector_map = None):
        self.axis_mathvector_map = axis_mathvector_map or {} #  所有轴向对应的向量

    @property
    def mathvectors(self):
        return self.axis_mathvector_map.values()
    
    def region_mathvectors(self, region, pt):
        return [p for p in self.mathvectors if p+pt in region]

    def __eq__(self, other):
        return self.axis_mathvector_map == other.axis_mathvector_map

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, axis):
        return self.axis_mathvector_map[axis]

    def __lt__(self, other):
        return len(self.axis_mathvector_map) < len(other.axis_mathvector_map)

    def add_axis(self, axis, vector):
        self.axis_mathvector_map[axis] = vector

    def add_axises(self, listpair):
        for axis, vector in listpair:
            self.axis_mathvector_map[axis] = vector

    def union_other(self, other):
        self.axis_mathvector_map.update(other.axis_mathvector_map)

    def union_map(self, other):
        return {**self.axis_mathvector_map, **other.axis_mathvector_map}
    
    def at_axis(self, axis):
        return self.axis_mathvector_map.get(axis)
    
    def to_axis(self, vec):
        for axis, vector in self.axis_mathvector_map.items():
            if vec == vector:
                return axis

    @classmethod
    def create_from_axises(cls, axises):
        axis_vector_map = {k: axis_mathvector_map[k]
                            for k in axises}
        return cls(axis_vector_map)

    @classmethod
    def create_from_mathvectors(cls, mathvectors):
        axis_vector_map = {}
        mathvector = set(mathvectors)
        for k, v in axis_mathvector_map.items():
            if v in mathvector:
                axis_vector_map[k] = v
        return cls(axis_vector_map)

    @classmethod
    def create_from_structure(cls, structure):
        mathvector = structure_mathvector(structure)
        return cls.create_from_mathvectors(mathvector)

    @classmethod
    def create_from_structure_set(cls, structure_set):
        mathvector = set()
        for structure in structure_set:
            mathvector.update(structure_mathvector(structure))
        return cls.create_from_mathvectors(mathvector)





class NeighborTable:
    __slots__ = ('structure_map', 'direction_map', 'mathvector_map',
                 'link_map', 'nbrtype_map')
    def __init__(self):
        # 下面容器取并集
        self.structure_map  = {}   # 标准方向结构，region--structure
        self.direction_map  = {}   # 轴向结构，region--direction
        self.mathvector_map = {}   # 向量方向集合，region--[pt+]set(vecs)
        self.link_map       = {}   # 邻居集合，pt--set(nbrs)
        self.nbrtype_map = {
            NeighborTypeEnum.Structure: False,
            NeighborTypeEnum.Direction: False,
            NeighborTypeEnum.Mathvector: False,
            NeighborTypeEnum.Link: False
            }
    
    def clear_nbrs(self):
        self.nbrtype_map = {
            NeighborTypeEnum.Structure: False,
            NeighborTypeEnum.Direction: False,
            NeighborTypeEnum.Mathvector: False,
            NeighborTypeEnum.Link: False
            }
    
    @classmethod
    def structure_only(cls, structure_map = None):
        table = cls()
        table.add_structure_map(structure_map)
        return table

    @classmethod
    def direction_only(cls, direction_map = None):
        table = cls()
        table.add_direction_map(direction_map)
        return table
    
    @classmethod
    def mathvector_only(cls, mathvector_map):
        table = cls()
        table.add_mathvector_map(mathvector_map)
        return table
    
    @classmethod
    def link_only(cls, link_map = None):
        table = cls()
        table.add_link_map(link_map)
        return table

    def add_structure_map(self, structure_map = None):
        self.nbrtype_map[NeighborTypeEnum.Structure] = True
        if structure_map:
            self.structure_map.update(structure_map)

    def add_direction_map(self, direction_map = None):
        self.nbrtype_map[NeighborTypeEnum.Direction] = True
        if direction_map:
            self.direction_map.update(direction_map)
    
    def add_mathvector_map(self, mathvector_map):
        self.nbrtype_map[NeighborTypeEnum.Mathvector] = True
        if mathvector_map:
            self.mathvector_map.update(mathvector_map)
    
    def add_link_map(self, link_map = None):
        self.nbrtype_map[NeighborTypeEnum.Link] = True
        if link_map:
            self.link_map.update(link_map)

    def get_structure(self, pt):
        result = set()
        for region, st in self.structure_map.items():
            if pt in region:
                result.add(st)
        return filter_structure_set(result)

    def get_direction(self, pt):
        result = Direction()
        for region, dr in self.direction_map.items():
            if pt in region:
                result.union_other(dr)
        return result
    
    def get_structure_direction(self, pt):
        result = Direction.create_from_structure_set(self.get_structure(pt))
        result.union_other(self.get_direction(pt))
        return result

    def get_structure_mathvector(self, pt, baseregion = None):
        result = []
        for region, st in self.structure_map.items():
            if pt in region:
                result += region_structure_mathvector(st, baseregion or region, pt)
        return set(result)

    def get_direction_mathvector(self, pt, baseregion = None):
        result = []
        for region, dr in self.direction_map.items():
            if pt in region:
                result += dr.region_mathvectors(baseregion or region, pt)
        return set(result)

    def get_mathvector(self, pt):
        result = set()
        for region, vts in self.mathvector_map.items():
            if pt in region:
                result.update(vts)
        return result

    def get_link(self, pt):
        return self.link_map.get(pt, set())

    def point_all_mathvectors(self, pt):
        vects = set()
        if self.nbrtype_map.get(NeighborTypeEnum.Structure, False):
            for region, st in self.structure_map.items():
                if pt in region:
                    vects.update(structure_mathvector(st))
        if self.nbrtype_map.get(NeighborTypeEnum.Direction, False):
            for region, dr in self.direction_map.items():
                if pt in region:
                    vects.update(dr.mathvectors)
        if self.nbrtype_map.get(NeighborTypeEnum.Mathvector, False):
            for region, vts in self.mathvector_map.items():
                if pt in region:
                    vects.update(vts)
        return vects

    def get_nbrs(self, pt, baseregion):
        vects = self.point_all_mathvectors(pt)
        nbrs = set(npt for v in vects if (npt := baseregion.map(pt + v)))
        nbrs.update(self.get_link(pt))
        if pt in nbrs:
            nbrs.remove(pt)
        return nbrs

    def  get_nbrs_vects(self, pt, baseregion):
        nbrs = self.get_nbrs(pt, baseregion)
        return [p-pt for p in nbrs]


    def get_axises_and_vects(self, pt, baseregion):
        d = self.get_structure_direction(pt)
        return {(d.to_axis(vt) or to_axis(vt)): vt
                 for vt in self.get_nbrs_vects(pt, baseregion)}
    
    def point_axis_nbr(self, pt, axis = 0):
        """轴向对应的邻居"""
        if vt := self.get_structure_direction(pt).at_axis(axis) or at_axis(axis):
            return pt + vt

    def point_nbr_axis(self, pt, nbr):
        """邻居对应的轴向"""
        vt = nbr - pt
        return self.get_structure_direction(pt).to_axis(vt) or to_axis(vt)
    
    def structures_mathvector_map(self, baseregion = None):
        """ structures对应的邻居向量"""
        mathvector_map = {}
        for region, st in self.structure_map.items():
            for pt in region:
                if pt not in mathvector_map:
                    mathvector_map[pt] = set()
                mathvector_map[pt].update(region_structure_mathvector(st, baseregion or region, pt))
        return mathvector_map

    def directions_mathvector_map(self, baseregion = None):
        """directions对应的邻居向量"""
        mathvector_map = {}
        for region, dr in self.direction_map.items():
            for pt in region:
                if pt not in mathvector_map:
                    mathvector_map[pt] = set()
                mathvector_map[pt].update(dr.region_mathvectors(baseregion or region, pt))
        return mathvector_map
    
    def pts_mathvector_map(self):
        """mathvector对应的邻居向量"""
        mathvector_map = {}
        for region, vts in self.mathvector_map.items():
            for pt in region:
                if pt not in mathvector_map:
                    mathvector_map[pt] = set()
                mathvector_map[pt].update(vts)
        return mathvector_map

    def all_mathvectors(self, baseregion = None):
        vects = dict()
        if self.nbrtype_map.get(NeighborTypeEnum.Structure, False):
            vects.update(self.structures_mathvector_map(baseregion))
        if self.nbrtype_map.get(NeighborTypeEnum.Direction, False):
            vects.update(self.directions_mathvector_map(baseregion))
        if self.nbrtype_map.get(NeighborTypeEnum.Mathvector, False):
            vects.update(self.pts_mathvector_map())
        return vects

    def all_nbrs(self, baseregion = None):
        vects = self.all_mathvectors(baseregion)
        nbrs = dict()
        for pt, vts in vects.items():
            nbrs[pt] = set()
            for v in vts:
                nbrs[pt].add(pt + v)
        for pt,ns in self.link_map.items():
            nbrs[pt].update(ns)
        return nbrs

    @classmethod
    def create_from_edges(cls, edges) -> 'NeighborTable':
        """从边数据创建"""
        link_map = {pt: set(nbrs) for pt, nbrs in edges.items()}
        return NeighborTable.link_only(link_map)





def flatten(pts, to_vector = False):
    """Point数据拍平
    """
    # 单点断路检查
    if (pt := as_vector(pts) if to_vector else as_point(pts)) is not None:
        return [pt]
    match pts:
        case ():
            return []
        case tuple()|list()|set():
            new = [flatten(pt, to_vector = to_vector) for pt in pts]
            return sum(new, [])
    return []


def box(array):
    xs = [pt[0] for pt in array]
    ys = [pt[1] for pt in array]
    return Vector2D(min(xs), min(ys)), Vector2D(max(xs) +1, max(ys) +1)


def box_merge(boxes):
    points = []
    for box in boxes:
        points.extend(box)
    return box(points)


def points_rank(pt1: Vector2D, pt2: Vector2D) -> list[Vector2D]:
    """获取pt1到pt2所在的直线队列"""
    unit, step = points_step(pt2 - pt1)
    if step == 0:
        return [as_point(pt1)]
    pt1 = as_point(pt1)
    pts = [pt1 + unit*i for i in range(step)]
    pts.append(as_point(pt2))
    return pts

def points_line(region: 'RegionRect', pt1: Vector2D, pt2: Vector2D) -> tuple[list[Vector2D], bool]:
    """获取pt1到pt2之间的区域"""
    unit, step = points_step(pt1, pt2)
    if step == 0:
        return [as_point(pt1)]
    pt1 = as_point(pt1)
    pts = [pt1 + unit*i for i in range(step)]
    pts.append(as_point(pt2))
    ptA = pts[0]-unit; ptB = pts[-1]+unit
    pre = []; nxt = []
    while ptA in region:
        pre.append(ptA)
        ptA -= unit
    while ptB in region:
        nxt.append(ptB)
        ptB += unit
    # 判断是否闭合
    cil = False
    if (nxt and region.map(ptA) == nxt[-1]) or region.map(ptA) == pts[-1]:
        cil = True
    if (pre and region.map(ptB) == pre[-1]) or region.map(ptB) == pts[0]:
        cil = True
    return pre[::-1] + pts + nxt, cil



class RegionBase:
    """区域。 表示二维坐标的范围"""
    __slots__ = ('_mode', '_data', 'circle')
    def __init__(self, mode: RegionModeEnum = 1, 
            data: list[Vector2D] = None, circle: int = 0):
        self._mode = mode
        self._data = data or []
        self.circle = circle # 是否循环

    @property
    def mode(self):
        return self._mode
    
    @property
    def data(self):
        return self._data

    @property
    def box(self):
        """bounding box"""
        raise NotImplementedError()

    @property
    def size(self) -> tuple[int, int]:
        """size"""
        return self.box[1].x - self.box[0].x, self.box[1].y - self.box[0].y

    @property
    def points(self):
        return [pt for pt in self]
    
    def __contains__(self, pt: Vector2D) -> bool:
        """判断点是否在区域内"""
        return False

    def map(self, pt: Vector2D) -> Vector2D|None:
        """调整点到范围内"""
        if pt in self:
            return pt
        return None

    def __iter__(self):
        return iter(self.data)

    def __bool__(self):
        return bool(self.data)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self._mode == other._mode and self.data == other.data

    def __hash__(self):
        return hash((self._mode, tuple(self.data)))



class RegionPoints(RegionBase):
    """区域。 表示离散点坐标的范围"""
    __slots__ = ('_mode', '_data', 'circle')
    def __init__(self, data = None):
        self._mode = RegionModeEnum.Points
        self._data = [as_vector(p) for p in data] if data else []
        self.circle = 0

    def _set_data(self, data):
        self._data = data

    @property
    def box(self):
        return box(self.data)

    def __contains__(self, pt):
        return pt in self.data


    def map(self, pt) -> Vector2D|None:
        """调整data到范围内"""
        if pt not in self.data:
            return None
        return pt

    def __iter__(self):
        return iter(self.data)
    





class RegionRect(RegionBase):
    """区域。 表示二维矩形坐标的范围"""
    __slots__ = ('_mode', '_data', 'circle')
    def __init__(self, data = None, circle = 0):
        self._mode = RegionModeEnum.Rect
        self._data = [Vector2D(), Vector2D()]
        self.circle = circle
        self.set_data(data)

    def set_data(self, data):
        x1,y1,x2,y2 = 0,0,0,0
        match data:
            case int():
                x2 = y2 = data
            case Vector2D():
                x2, y2 = data
            case (int(), int()):
                x2, y2 = data
            case (int(), int(), int(), int()):
                x1,y1,x2,y2 = data
            case (Vector2D(), Vector2D()):
                x1, y1 = data[0]
                x2, y2 = data[1]
            case ((int(), int()), (int(), int())):
                x1, y1 = data[0]
                x2, y2 = data[1]
            case _:
                raise ValueError('data is not a rect region')
        pt1 = Vector2D.ascending_vector((x1, x2))
        pt2 = Vector2D.ascending_vector((y1, y2))
        self._data = [Vector2D(pt1.x, pt2.x), Vector2D(pt1.y, pt2.y)]

    @property
    def box(self):
        return tuple(self.data)

    @property
    def point0(self):
        return self._data[0]

    @property
    def point1(self):
        return self._data[1]

    def __contains__(self, item: Vector2D):
        return as_vector(item).in_box(self.point0, self.point1)


    def map(self, item) -> Vector2D|None:
        """调整data到范围内"""
        x1,y1 = self.point0
        x2,y2 = self.point1
        x = map_int(item[0], x1, x2, circle = self.circle//2)
        y = map_int(item[1], y1, y2, circle = self.circle%2)
        p = isinstance(x, int) and isinstance(y, int)
        return Vector2D(x, y) if p else None

    def __iter__(self):
        for i in range(self.point0[0], self.point1[0]):
            for j in range(self.point0[1], self.point1[1]):
                yield Vector2D(i, j)



class MoveDest:
    """移动目的地"""
    __slots__ = ('region', 'structure', 'direction', 'mathvector', 'link')
    def __init__(self, region: RegionBase = None,
                        structure: int = 0,
                        direction: Direction = None,
                        mathvector: RegionBase = None,
                        link: RegionBase = None):
        self.region     = region or RegionBase()
        # 下面容器取并集
        self.structure  = structure
        self.direction  = direction or Direction()
        self.mathvector = mathvector or RegionBase()
        self.link       = link or RegionBase()
    
    def all_mathvectors(self):
        vects = set(structure_mathvector(self.structure))
        vects.update(self.direction.mathvectors)
        vects.update(self.mathvector.points)
        return vects

    def get_dest(self, pt):
        vects = self.all_mathvectors()
        dest = set(npt for v in vects if (npt := self.region.map(pt + v)))
        dest.update(self.link.points)
        return dest


    def in_moved(self, pt0, pt):
        """判断是否在移动目标内"""
        return pt in self.get_dest(pt0)