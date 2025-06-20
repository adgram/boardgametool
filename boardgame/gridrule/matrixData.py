"""
    棋盘坐标点的操作。
    MatrixP： 二维矩阵
    MatrixP：  二维整数矩阵
    Matrix2D： Point网格，二维图
"""

from .pointData import Vector2D, RegionBase, RegionRect, NeighborTable, MoveDest, NeighborTypeEnum, NullValue
from . import pointData
from typing import Callable
from collections import deque


VectorGenerater1 = Callable[[tuple[int, int]|Vector2D, int|None], Vector2D|int|None]
VectorGenerater2 = Callable[[int, int, int|None], Vector2D|int|None]





def is_array2d(array2d):
    return hasattr(array2d, '__iter__') and hasattr(array2d[0], '__iter__')


def get_box(array2d):
    return pointData.box(array2d)


def get_size(arraydata):
    """获取2d点阵的尺寸"""
    box = get_box(arraydata)
    return (box[1][0] - box[0][0], box[1][1] - box[0][1])





class MatrixP:
    """矩阵模板"""
    __slots__ = ('size', '_region', '_neighbortable', '_array2d', 'value_func', '_movedests')
    def __init__(self, size:tuple[int,int], region:RegionBase = None,
                 neighbortable = None, array2d = None,
                 movedests = None, value_func = None):
        self.size = pointData.as_point(size)
        if self.size[0] is None:
            raise ValueError('size')
        self._region:RegionBase = region or RegionRect(self.size)
        if self._region.size != self.size:
            raise ValueError('region')
        self._neighbortable:NeighborTable = neighbortable or NeighborTable()
        self._array2d:list[list[Vector2D]] = None
        self._movedests:dict[int, MoveDest] = movedests or {} # value: MoveDest
        self.value_func = value_func or (lambda i,j: NullValue)
        self.set_array2d(array2d = array2d)

    def new(self, region = None, array2d = None):
        """获取空拷贝"""
        return self.__class__(self.size, region = region or self._region,
                              neighbortable = self._neighbortable,
                             array2d = array2d or self._array2d)

    def copy_array2d(self):
        """获取深层拷贝副本"""
        return [[pt for pt in array] for array in self._array2d]


    def set_array2d(self, array2d = None):
        """设置 self._array2d"""
        if is_array2d(array2d):
            self._array2d = array2d
        else:
            self._array2d = [[self._value_func(i, j) for j in range(self.size[1])]
                             for i in range(self.size[0])]
    
    def _value_func(self, i, j):
        return self.value_func(i, j)

    @property
    def region(self):
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

    def add_dest(self, value, dest):
        self._movedests[value] = dest or MoveDest()

    def set_dests(self, dests):
        self._movedests.update(dests)

    def get_point(self, pt) -> Vector2D:
        if (pt:= self.region.map(pointData.as_vector(pt))) is not None:
            pt.value = self._array2d[pt[0]][pt[1]]
            return pt  
    
    def get_points(self, value = NullValue):
        """获取多个点"""
        if value == NullValue:
            return self._region.points()
        return [pt for pt in self._region if self.get_value(pt) == value]
    
    def collection(self, block = None):
        """获取多个点"""
        result = {}
        if block is None:
            block = self._region
        for pt in block:
            value = self.get_value(pt)
            result.setdefault(value, []).append(pt)
        return result

    def get_valid_value(self, pt):
        """获取数据，pt超出范围报错"""
        if (pt:= self.get_point(pt)) is not None:
            return pt.value
        raise KeyError('超出范围！')

    def get_value(self, pt):
        """获取数据，pt超出范围不报错"""
        if (pt:= self.get_point(pt)) is not None:
            return pt.value
        return NullValue

    def is_valid(self, pt):
        """判断是否为None"""
        return self.get_value(pt) != NullValue


    def set_value(self, pt, val, check = True):
        """点pt设值"""
        if (pt:= self.get_point(pt)) is not None:
            if check and pt.value == NullValue:
                return
            self._array2d[pt[0]][pt[1]] = val

    def set_values(self, pts, vals, check = True):
        """点pt设值"""
        if len(pts) == len(vals):
            for i,pt in enumerate(pts):
                self.set_value(pt, vals[i], check)
        elif len(vals) == 1:
            for pt in pts:
                self.set_value(pt, vals[0], check)
        else:
            raise KeyError()
    
    def get_edges(self):
        """获取边缘点"""
        edges = set()
        for pt in self.region:
            if self.get_point(pt) is None:
                continue
            for nbr in self._neighbortable.get_nbrs(pt, self._region):
                if (pt,nbr) not in edges and (nbr,pt) not in edges:
                    edges.add((pt,nbr))
        return list(edges)

    def to_nil(self, pts):
        """点pt归空"""
        self.set_value(pts, NullValue, False)

    def to_0(self, pts, check = False):
        """点pt归零"""
        self.set_value(pts, 0, check)

    def to_1(self, pts, check = False):
        """点pt归1"""
        self.set_value(pts, 1, check)

    def to_2(self, pts, check = False):
        """点pt归2"""
        self.set_value(pts, 2, check)

    def to_point_value(self, pt1, pt2, check = False):
        """点pt设值为矩阵内值"""
        self.set_value(pt1, self.get_valid_value(pt2), check)

    def __repr__(self):
        s = ''
        for x in self._array2d:
            s += str(x)+'\n'
        return s

    __str__ = __repr__

    def get_value_dest(self, value):
        """获取邻居"""
        return self._movedests.get(value, MoveDest())

    def pt_in_value_dest(self, value, pt0, pt1):
        """获取邻居"""
        return self.get_value_dest(value).in_moved(pt0, pt1)

    def get_point_nbrs(self, pt):
        """获取邻居"""
        return self._neighbortable.get_nbrs(pt, self._region)

    def get_point_value_nbrs(self, pt, value = None):
        """获取邻居"""
        return [p for p in self.get_point_nbrs(pt) if self.get_value(p) == value]
    
    def get_point_nbrs_vects(self, pt):
        """获取邻居"""
        return self._neighbortable.get_nbrs_vects(pt, self._region)
    
    def get_point_axises_and_vects(self, pt):
        """获取邻居"""
        return self._neighbortable.get_axises_and_vects(pt, self._region)

    def point_move_vector(self, pt, vector = (0,1)):
        """点pt移动vector后的坐标 """
        return self.get_point(self.get_point(pt) + vector)

    def point_axis_pairs(self, pt, axises = None):
        """过某点的直线方向对，默认相反数为pair"""
        pairs = []
        axis = list(axises or self.get_point_axises_and_vects(pt).keys())
        curr = set()
        num = len(axis)
        for i in range(num-1):
            t = False
            if i in curr:
                continue
            curr.add(i)
            for j in range(i+1, num):
                if j in curr:
                    continue
                if axis[i] + axis[j] == 0:
                    pairs.append((axis[i], axis[j]))
                    curr.add(j)
                    t = True
                    break
            if not t:
                pairs.append((axis[i],None))
        return pairs

    def point_vector_pairs(self, pt):
        """过某点的直线方向对，默认相反数为pair"""
        vas = self.get_point_axises_and_vects(pt)
        axis_pairs = self.point_axis_pairs(pt, vas.keys())
        result = []
        for p,q in axis_pairs:
            if p and q:
                result.append((vas[p], vas[q]))
            else:
                result.append((vas[p], ))
        return result

    def search_value_vector(self, pt, vector = (0,1), value = NullValue):
        """扫描直线上的点, 不包括pt
            vector：方向
        """
        pts = []
        p = pt
        while (p := self.point_move_vector(p, vector)) and p not in pts and self.get_valid_value(p) == value:
            pts.append(p)
        return pts


    def search_value_vector_pairs(self, pt, pair:tuple, value = NullValue):
        """双向扫描直线上的点, 包括pt
            vector：方向
        """
        if not pair:
            return
        pts = self.search_value_vector(pt, vector = pair[0], value = value)
        if len(pair) == 2 and (pts2 := self.search_value_vector(pt,
                                vector = pair[1], value = value)):
            return pts2[::-1] + [pt] + pts
        return [pt] + pts


    def search_line(self, pt1, pt2, val = NullValue, structure = 8):
        """扫描直线上的两点，并判断共线、求向量
           val: 如果val不是None则判断之间值是否全部为val
        """
        pt1 = self.get_point(pt1)
        if not pt1.is_parallel(pt2, structure):
            return []
        pts = pointData.points_rank(pt1, pt2)
        if val == NullValue:
            pts = [pt for pt in pts if (self.get_value(pt) is not None)]
        else:
            for pt in pts[1:-1]:
                if self.get_valid_value(pt) != val:
                    return []
        return pts

    def collection_line(self, pt1, pt2):
        """获取多个点，不包括起止点"""
        result = {}
        for pt in pointData.points_rank(pt1, pt2)[1:-1]:
            value = self.get_value(pt)
            result.setdefault(value, []).append(pt)
        return result

    def search_block(self, pt):
        """查找连通的棋块"""
        val = self.get_valid_value(pt)
        if val == NullValue:
            raise TypeError('该点不存在！')
        visited = set([pt])
        search = deque([pt])
        while search:
            current = search.popleft()
            for neighbor in self.get_point_value_nbrs(current, val):
                if neighbor not in visited:
                    visited.add(neighbor)
                    search.append(neighbor)
        return list(visited)

    def block_nbrs(self, block):
        """查找连通的棋块所有的行走的出路（气的位置）"""
        result = set()
        for t in block:
            for p in self.get_point_value_nbrs(t, 0):
                result.add(p)
        return list(result)

    def block_liberties(self, block):
        """Liberties 计算出路数量，气的个数"""
        return len(self.block_nbrs(block))

    def liberties_test(self, pt, val, robbery = None):
        """模拟并测试该点落子后的情况"""
        old_val = self.get_value(pt)
        if old_val == NullValue: return False
        self.set_value(pt, val, False)
        if self.block_liberties(self.search_block(pt)) != 0:
            self.set_value(pt, old_val, False)
            return True
        blocks = self.dead_nbrs(pt)
        if (l := len(blocks)) == 0:
            self.set_value(pt, old_val, False)
            return False
        elif l > 1 or len(blocks[0]) > 1:
            self.set_value(pt, old_val, False)
            return True
        # 打劫
        if robbery and blocks[0] == robbery:
            self.set_value(pt, old_val, False)
            return False
        self.set_value(pt, old_val, False)
        return True

    def dead_nbrs(self, pt):
        """无气的异值邻居"""
        if (val:= self.get_valid_value(pt)) == NullValue:
            return []
        visited = set()
        dead_blocks = []
        for p in self.get_point_nbrs(pt):
            if p in visited:
                continue
            if self.get_valid_value(p) in [NullValue, 0, val]:
                continue
            block = self.search_block(p)
            visited.update(block)
            if self.block_liberties(block) == 0:
                dead_blocks.append(block)
        return dead_blocks


    def search_skip(self, pt, value = NullValue):
        """隔一子跳"""
        pt = self.get_point(pt)
        vectors = [pointData.unit(v) for v in self.get_point_nbrs_vects(pt)]
        result = set()
        for v in vectors:
            pt0 = self.get_point(pt + v)
            if pt0 and ((value == NullValue and self.get_value(pt0) != 0) or value == self.get_value(pt0)):
                pt2 = self.get_point(pt0 + v)
                if pt2 and self.get_value(pt2) == 0:
                    result.add(pt2)
        return list(result)

    def search_value(self, value):
        for pt in self._region:
            if self.get_value(pt) == value:
                yield pt

    def search_in_row(self, pt, n = 5):
        """判断数子连珠 连珠个数不到n则返回[]"""
        assert n > 1, '连子数必须大于1！'
        rows = []
        for pair in self.point_vector_pairs(pt):
            pts = self.search_value_vector_pairs(pt, pair = pair, value = self.get_value(pt))
            if len(pts) >= n:
                rows.append(pts)
        return rows


    def search_to_face(self, pt, other, structure = 0):
        """判断棋子共线、照面， 即直线连接并且中间值为0
        """
        return bool(self.search_line(pt, other, val = 0, structure = structure))
    
    def search_shortest_path(self, pt1, pt2, skip = True, test_move = None):
        visited = {}  # 记录访问节点及其前驱
        queue = deque([pt1])   # BFS队列初始化
        while queue:
            pt = queue.popleft()
            if pt == pt2:
                # 回溯构建最短路径
                path = [pt]
                current = pt
                while current != pt1:
                    path.append(current)
                    current = visited[current]
                path.append(pt1)
                return list(reversed(path))
            pts = self.search_skip(pt) if skip else self.get_point_nbrs(pt)
            for p in pts:
                if p not in visited and (test_move(pt, p) if test_move else True):
                    visited[p] = pt  # 记录前驱节点
                    queue.append(p)
        return []


    @classmethod
    def structure_matrix(cls, size, structure = 0, **kwargs):
        region = kwargs.pop('region', RegionRect(size))
        if region.size != size:
            raise Exception('region.size != size')
        neighbortable = kwargs.pop('neighbortable', NeighborTable())
        neighbortable.nbrtype_map[NeighborTypeEnum.Structure] = True
        neighbortable.structure_map[region] = structure
        value_func = lambda i, j: 0
        return cls(size, region = region, neighbortable = neighbortable,
                    value_func = value_func, **kwargs)

    @classmethod
    def simple_matrix(cls, size, region, neighbortable):
        """简单矩阵"""
        return cls(size, region = region,
                neighbortable = neighbortable,
                value_func = lambda i, j: 0)






