"""
    棋盘坐标点的操作
    PieceUi
"""
from .pointData import Vector2D, RegionBase
from . import pointData
from .matrixData import MatrixP
from .until import LinePositionEnum, GameOverEnum, AxisEnum
from .boardUiData import (PieceUi, DefaultPiecesUi, GridCoorUi, 
                        GridEdgesUi, GridStarUi, GridTagUi)
from .gameData import GameData
import json



class GridCoordinate:
    """格线坐标系"""
    __slots__ = ('grid_size', 'x_segments', 'y_segments')
    def __init__(self, grid_size = (15, 15), 
                 x_vects = [], y_vects = []):
        self.grid_size = grid_size
        # vects数量比size少1，size和segments数量一致
        self.x_segments = self.get_segments(x_vects, self.grid_size[0]-1, axis = AxisEnum.X)
        self.y_segments = self.get_segments(y_vects, self.grid_size[1]-1, axis = AxisEnum.Y)

    @classmethod
    def get_segments(self, vects: list[Vector2D], count = 0, axis = AxisEnum.X):
        if vects:
            n_vects = [pointData.as_vector(v) for v in vects]
            if len(vects) < count:
                n_vects.extend([n_vects[-1]] * (count-len(vects)))
            elif len(vects) > count:
                n_vects = n_vects[:count]
        else:
            if axis == AxisEnum.X:
                n_vects = [Vector2D(1, 0)]* count
            elif axis == AxisEnum.Y:
                n_vects = [Vector2D(0, 1)]* count
            else:
                raise ValueError('axis error')
        result = [Vector2D(0, 0)]
        for v in n_vects:
            result.append(result[-1] + v)
        return result

    def get_dot(self, pt):
        """获取格线坐标"""
        if pt[0] == -1:
            x = -self.x_segments[1]
        elif 0 <= pt[0] < self.grid_size[0]:
            x = self.x_segments[pt[0]]
        elif pt[0] == self.grid_size[0]:
            x = self.x_segments[-1]*2 - self.x_segments[-2]
        else:
            raise ValueError('pt error')
        if pt[1] == -1:
            y = -self.y_segments[1]
        elif 0 <= pt[1] < self.grid_size[1]:
            y = self.y_segments[pt[1]]
        elif pt[1] == self.grid_size[1]:
            y = self.y_segments[-1]*2 - self.y_segments[-2]
        else:
            raise ValueError('pt error')
        return x + y

    @classmethod
    def closet_index(cls, segments, count, n, side = 0):
        if n <= 0:
            if n <= -segments[1][side]//3:
                return -1
            return 0
        elif n >= segments[-1][side]:
            if n >= segments[-1][side] + segments[1][side]//3:
                return count
            return count - 1
        for i in range(count - 1):
            if segments[i][side] <= n <= segments[i+1][side]:
                ll = (segments[i+1][side] - segments[i][side])//3
                if n <= segments[i][side] + ll:
                    return i
                elif n >= segments[i+1][side] - ll:
                    return i + 1
                return -2
        return -2

    def get_pt(self, dot):
        """获取格线坐标"""
        """根据画布位置 查找坐标"""
        x, y = dot
        # 先判断y轴
        j = self.closet_index(self.y_segments, self.grid_size[1], y, 1)
        if 0 <= j < self.grid_size[1]:
            x -= self.y_segments[j][0]
        # 先判断x轴，x轴会由y轴偏移
        i = self.closet_index(self.x_segments, self.grid_size[0], x, 0)
        return Vector2D(i, j)



class CanvasGrid:
    """画布上的位置坐标系"""
    __slots__ = ('size', 'canvas_size', 'is_net', 'boundless',
                'temp_pts_dots', 'net_size', 'padding',
                'coordinate', 'origin')
    def __init__(self, size = (15,15), canvas_size = (900,900),
                    is_net = True, boundless = True,
                    padding = (80, 80),
                    coordinate = None, origin = (0,0), 
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
        self.size = pointData.as_vector(size)
        self.canvas_size = pointData.as_vector(canvas_size)
        self.is_net = bool(is_net)
        self.boundless = bool(boundless)
        self.temp_pts_dots = {}   # {{pt:dot}, ...}
        # 边框格子数
        self.net_size = self._net_size()
        # 小格子
        self.padding = pointData.as_vector(padding)
        self.coordinate:GridCoordinate = coordinate
        if not self.coordinate:
            self.compute_coordinate(obliquity)
        # 边框
        if centered:
            hx = (self.canvas_size[0] - self.coordinate.x_segments[-1][0] \
                   - self.coordinate.y_segments[-1][0])//2
            hy = (self.canvas_size[1] - self.coordinate.y_segments[-1][1])//2
            self.padding = Vector2D(hx, hy)
        # 画线起点
        self.origin = origin + self.padding
    
    def _net_size(self):
        """获取格子的总数量"""
        if self.is_net:
            if self.boundless:
                return self.size
            else:
                return self.size + (1, 1)
        if self.boundless:
            return self.size + (1, 1)
        else:
            return self.size + (2, 2)

    def compute_coordinate(self, obliquity:complex):
        """单个格子的尺寸，并修正padding"""
        # 确保虚部系数不为0
        if obliquity.imag == 0:
            obliquity += 1j
        # 格子净尺寸
        xc, yc = self.canvas_size - self.padding*2
        # 格子总数量
        x_size, y_size = self.net_size - (1, 1)
        # 倾斜变换
        if obliquity.imag > 0:
            dx = min(xc/(obliquity.real*y_size + x_size), yc/(obliquity.imag*y_size))
            dy = dx*obliquity
        else:
            dy = complex(obliquity.real, -obliquity.imag)*(-yc/(obliquity.imag*y_size))  # y方向铺满
            dx = (xc - dy.real*y_size)/x_size
        self.coordinate = GridCoordinate(self.net_size, [Vector2D(int(dx), 0)],
                                         [Vector2D(int(dy.real), int(dy.imag))])
    
    def pt_in_size(self, pt):
        """判断pt是否在size范围内"""
        if not pt:
            return False
        return pointData.as_vector(pt).in_size(self.size)

    def dot_in_canvas(self, dot):
        """判断是否在canvas_size范围内"""
        if not dot:
            return False
        return pointData.as_vector(dot).in_size(self.canvas_size)
    
    @property
    def x_segs(self):
        return self.coordinate.x_segments
    
    @property
    def y_segs(self):
        return self.coordinate.y_segments
    
    @property
    def x_cell(self):
        return self.coordinate.x_segments[1][0]
    
    @property
    def y_cell(self):
        return self.coordinate.y_segments[1][1]

    def _four_boundaries(self):
        """获取格线的扩展四至"""
        if self.is_net:
            if self.boundless:
                pad = (-self.x_cell, -self.y_cell)
            else:
                pad = (0, 0)
        else:
            if self.boundless:
                pad = (0, 0)
            else:
                pad = (self.x_cell, self.y_cell)
        vec1 = self.origin + pad
        vec2 = self.origin + self.canvas_size - self.padding - pad
        return Vector2D(vec1[0], vec2[0]), Vector2D(vec1[1], vec2[1])

    def dot_in_net(self, dot, e = 35):
        """判断是否在格线范围内"""
        if not dot:
            return False
        px, py = pointData.as_vector(dot)
        dx, dy = self._four_boundaries()
        return (dx[0]-e <= px <= dx[1]+e and dy[0]-e <= py <= dy[1]+e)
    
    def net_origin(self, is_net = None):
        """获取第一个有效的net点"""
        if is_net is None:
            is_net = self.is_net
        if is_net:
            if self.boundless:
                origin = self.origin
            else:
                origin = self.origin + \
                    self.x_segs[1]//2 + self.y_segs[1]//2
        else:
            if self.boundless:
                origin = self.origin + \
                    self.x_segs[1]//2 + self.y_segs[1]//2
            else:
                origin = self.origin + \
                    self.x_segs[1] + self.y_segs[1]
        return origin

    def get_dot(self, pt, is_net = None):
        """获取位置点"""
        if is_net is None:
            is_net = self.is_net
        if is_net == self.is_net:
            if pt in self.temp_pts_dots:
                return self.temp_pts_dots[pt]
        return self.net_origin(is_net) + self.coordinate.get_dot(pt)

    def close_point(self, dot):
        """根据画布位置 查找坐标"""
        # 减去边框
        dot -= self.net_origin(self.is_net)
        pt = self.coordinate.get_pt(dot)
        if pt[0] == -2 or pt[1] == -2:
            return pt, None
        return pt, self.get_dot(pt, self.is_net)

    def _edge_size(self):
        """获取格子的总数量"""
        if self.is_net:
            return self.size
        return self.size + (1, 1)

    def edge_origin(self, axis = AxisEnum.X):
        """获取格线的起点"""
        match axis:
            case AxisEnum.X:
                if self.boundless:
                    origin = self.origin
                else:
                    origin = self.origin + self.y_segs[1]//2
            case AxisEnum.Y:
                if self.boundless:
                    origin = self.origin
                else:
                    origin = self.origin + self.x_segs[1]//2
        return origin

    def get_axis_edge(self, index = 0, axis = AxisEnum.X):
        """获取格线的边缘点"""
        match axis:
            case AxisEnum.X:
                start = self.edge_origin(axis) + self.y_segs[index]
                end = start + self.x_segs[self._edge_size()[0]-1]
            case AxisEnum.Y:
                start = self.edge_origin(axis) + self.x_segs[index]
                end = start + self.y_segs[self._edge_size()[1]-1]
        return start, end

    def get_axis_edges(self, axis = AxisEnum.X):
        """获取格线的边缘点"""
        x,y = self._edge_size()
        edges = []
        match axis:
            case AxisEnum.X:
                for index in range(y):
                    start = self.edge_origin(axis) + self.y_segs[index]
                    end = start + self.x_segs[-1]
                    edges.append((start, end))
            case AxisEnum.Y:
                for index in range(x):
                    start = self.edge_origin(axis) + self.x_segs[index]
                    end = start + self.y_segs[-1]
                    edges.append((start, end))
            case AxisEnum.XY:
                return self.get_axis_edges(AxisEnum.X) + self.get_axis_edges(AxisEnum.Y)
        return edges

    def get_coors(self, axis = AxisEnum.XY, distance = 0.5):
        """计算网格坐标系坐标文字"""
        x,y = self._edge_size()
        tags = []
        match axis:
            case AxisEnum.X:
                _tag = lambda i: str(i+1)
                for index in range(y):
                    start = self.edge_origin(axis) + \
                        self.y_segs[index] - (round(self.x_cell*distance), 0)
                    end = start + self.x_segs[-1] + \
                        (round(self.x_cell*distance*2), 0)
                    tags.append((start, end, axis, index))
            case AxisEnum.Y:
                def _tag(i):
                    if i >= 8:
                        i += 1
                    if i >= 14:
                        i += 1
                    return chr(ord('A')+i)
                for index in range(x):
                    start = self.edge_origin(axis) + \
                        self.x_segs[index] - (0, round(self.y_cell*distance))
                    end = start + self.y_segs[-1] + \
                        (0, round(self.y_cell*distance*2))
                    tags.append((start, end, axis, index))
            case AxisEnum.XY:
                return self.get_coors(AxisEnum.X, distance) + \
                        self.get_coors(AxisEnum.Y, distance)
        return tags

    def get_stars(self):
        """计算网格坐标系星位"""
        if not self.is_net:
            return []
        stars = []
        def _star(n):
            if 12>= n >= 9:
                return 2, n-3
            elif n >= 13:
                return 3, n-4
            else:
                return None
        a, b = _star(self.size[0]), _star(self.size[1])
        if a and b:
            for i in a:
                for j in b:
                    stars.append(self.get_dot((i, j), is_net = True))
        return stars

    def get_line(self, edge):
        """计算网格坐标系线框"""
        dot1 = self.get_dot(edge[0], is_net = True)
        dot2 = self.get_dot(edge[1], is_net = True)
        return dot1, dot2

    def get_lines(self, edges):
        """计算网格坐标系线框"""
        return [self.get_line(edge) for edge in edges]

    def get_rect(self, pt):
        """获取格子矩形"""
        dots = []
        for j in range(2):
            y = pt[1] + j
            for i in range(2):
                x = pt[0] + i
                dots.append(self.get_dot((x, y), is_net = True))
        dots[2],dots[3] = dots[3],dots[2]
        return dots

    def get_cells(self, pts):
        """计算网格坐标系线框"""
        return [self.get_rect(pt) for pt in pts]

    def get_cltags(self, pts):
        """计算网格坐标系线框"""
        return [self.get_dot(pt) for pt in pts]





class CanvasBoard:
    """画板"""
    __slots__ = ('canvas_grid', 'canvas_lines', 'coorui', 'edgeui',
                 'starui', 'bg_color', 'canvas_image', 'canvas_cells',
                 'bg_edges', 'tagui', 'cell_tags', 'canvas_texture',
                 "show_piece_index", "image_dsize", "image_origin")
    def __init__(self, canvas_grid = None, **kwargs):
        self.canvas_grid = canvas_grid or CanvasGrid()          # 背景格线对象
        self.canvas_lines = kwargs.get('canvas_lines', [])      # 网格格线坐标
        self.canvas_cells = kwargs.get('canvas_cells', [])      # 网格填充
        self.cell_tags = kwargs.get('cell_tags', [])            # 网格标记
        self.edgeui = kwargs.get('edgeui', GridEdgesUi(
                color = kwargs.get('color', (0, 0, 0, 255)),
                fill = kwargs.get('fill', kwargs.get('color', (0, 0, 0, 255))),
                thickness = kwargs.get('thickness', 3),
                show = kwargs.get('bgedges_show', AxisEnum.Null),
               ))
        self.coorui = kwargs.get('coorui', GridCoorUi(
                color = self.edgeui.color,
                height = kwargs.get('coor_height', self.canvas_grid.x_cell//3),
                show = kwargs.get('coor_show', LinePositionEnum.Null)
               ))
        self.starui = kwargs.get('starui', GridStarUi(
                color = self.edgeui.color,
                show = kwargs.get('star_show', False),
                radius = kwargs.get('star_radius', self.canvas_grid.x_cell//5)
               ))
        self.tagui = kwargs.get('tagui', GridTagUi(
                color = self.edgeui.color,
                height = self.canvas_grid.x_cell//3,
                text = kwargs.get('tagtext', ''),
                icon = kwargs.get('tagicon', ''),
                iconsize = kwargs.get('iconsize', (self.canvas_grid.x_cell, self.canvas_grid.x_cell)),
                textfunc = kwargs.get('tagtextfunc', lambda pt: ''),
                iconfunc = kwargs.get('tagiconfunc', lambda pt: '')
               ))
        self.bg_color = kwargs.get('bg_color', self.edgeui.fill)# 背景颜色
        self.canvas_image = kwargs.get('canvas_image', None)    # 背景图片
        self.image_dsize = kwargs.get('image_dsize', (0, 0))    # 背景图片
        self.image_origin = kwargs.get('image_origin', (0, 0))  # 背景图片
        self.bg_edges = []                                      # 背景格线
        self.canvas_texture = {'gr_lines':[], 'gr_stars':[], 'gr_coors':[],
                               'gr_cells':[], 'gr_cltags':[]}    # 自定义棋盘格线
        self.show_piece_index = kwargs.get('show_piece_index', False)

    @property
    def size(self):
        return self.canvas_grid.canvas_size

    def get_dot(self, pt, dot = None):
        """获取dot坐标"""
        return dot or self.canvas_grid.get_dot(pt, self.canvas_grid.is_net)

    def dot_to_point(self, dot):
        """根据棋盘坐标获取所在顶点"""
        return self.canvas_grid.close_point(Vector2D(dot))

    def add_bgline(self, pt1, pt2):
        """绘制直线段"""
        pt1 = pointData.as_point(pt1)
        pt2 = pointData.as_point(pt2)
        return {'pt1': pt1, 'pt2': pt2, 'ui':self.edgeui}

    def add_line(self, pt1, pt2):
        pt1 = pointData.as_point(pt1)
        pt2 = pointData.as_point(pt2)
        return {'pt1': pt1, 'pt2': pt2, 'ui':self.edgeui}

    def add_cell(self, pt1, pt2, pt3, pt4):
        pt1 = pointData.as_point(pt1)
        pt2 = pointData.as_point(pt2)
        pt3 = pointData.as_point(pt3)
        pt4 = pointData.as_point(pt4)
        return {'pt1': pt1, 'pt2': pt2, 'pt3': pt3, 'pt4': pt4, 'ui':self.edgeui}

    def add_coor(self, pt, axis, n):
        """绘制文字"""
        pt = pointData.as_point(pt)
        if axis == AxisEnum.X:
            text = str(n+1)
        elif axis == AxisEnum.Y:
            text = chr(ord('A') + (n +2 if n >= 14 else n +1 if n >= 8 else n))
        return {'pt': pt, 'text': text, 'ui':self.coorui}

    def add_star(self, pt):
        """绘制圆点"""
        pt = pointData.as_point(pt)
        return {'pt': pt, 'ui':self.starui}

    def add_tag(self, pt):
        """绘制圆点"""
        pt = pointData.as_point(pt)
        return {'pt': pt, 'ui':self.tagui}

    def draw_background_grid(self):
        for ln in self.canvas_grid.get_axis_edges(self.edgeui.show):
            self.bg_edges.append(self.add_bgline(*ln))
        for ln in self.canvas_grid.get_lines(self.canvas_lines):
            self.canvas_texture['gr_lines'].append(self.add_line(*ln))
        for pts in self.canvas_grid.get_cells(self.canvas_cells):
            self.canvas_texture['gr_cells'].append(self.add_cell(*pts))
        for pt in self.canvas_grid.get_cltags(self.cell_tags):
            self.canvas_texture['gr_cltags'].append(self.add_tag(pt))
        match self.coorui.show:
            case LinePositionEnum.Start:
                for pt1, pt2, axis, n in self.canvas_grid.get_coors():
                    self.canvas_texture['gr_coors'].append(self.add_coor(pt1, axis, n))
            case LinePositionEnum.End:
                for pt1, pt2, axis, n in self.canvas_grid.get_coors():
                    self.canvas_texture['gr_coors'].append(self.add_coor(pt2, axis, n))
            case LinePositionEnum.Both:
                for pt1, pt2, axis, n in self.canvas_grid.get_coors():
                    self.canvas_texture['gr_coors'].append(self.add_coor(pt1, axis, n))
                    self.canvas_texture['gr_coors'].append(self.add_coor(pt2, axis, n))
            case _:
                pass
        if self.starui.show:
            for pt in self.canvas_grid.get_stars():
                self.canvas_texture['gr_stars'].append(self.add_star(pt))


APPS = {}


class Application:
    __slots__ = ('name', 'userdict', 'gamerule', 'canvasboard',
                  'tagui', 'pieceuis', 'about_info')
    def __init__(self, name = '', userdict = None,  pieceuis = None, 
                 tagui = None, gamerule = None, canvasboard = None):
        self.name = name
        self.about_info = '棋类游戏。'
        self.userdict = userdict or {}
        self.gamerule:GameData = gamerule or self.init_rule()
        self.pieceuis:DefaultPiecesUi = pieceuis or self.init_pieceuis()
        self.canvasboard = canvasboard or self.get_canvas()
        x_cell = self.canvasboard.canvas_grid.x_cell
        self.pieceuis.set_data(self.gamerule.pieces, 
                radius = x_cell//2-x_cell//20 or 50)
        self.tagui = tagui or GridTagUi(
                color = self.canvasboard.edgeui.color,
                height = x_cell//3
               )
        self.canvasboard.draw_background_grid()
        self.set_piece_default_signal()

    def init_rule(self):
        return
    
    def init_pieceuis(self):
        return

    def init_grid(self):
        grid = {'size': (9, 9), 'canvas_size': (750, 750), 'padding': (80, 80), 
                'is_net': True, 'boundless': True, 'coordinate': None,
                'origin': (0, 0), 'obliquity': 1j, 'centered': True}
        grid.update(self.grid_attr())
        grid['size'] = Vector2D(grid['size'])
        grid['canvas_size'] = Vector2D(grid['canvas_size'])
        grid['padding'] = Vector2D(grid['padding'])
        grid['origin'] = Vector2D(grid['origin'])
        return CanvasGrid(**grid)
    
    def grid_attr(self):
        return {}
    
    def init_canvasattr(self):
        return {}

    def get_canvas(self):
        return CanvasBoard(canvas_grid = self.init_grid(), **self.init_canvasattr())
    
    def set_signal(self, key, func):
        self.gamerule.set_signal(key, func)
    
    def set_piece_signal(self, key, func):
        self.gamerule.set_piece_signal(key, func)
    
    def set_piece_default_signal(self):
        self.gamerule.set_piece_signal('add', self.add_pieces)
        self.gamerule.set_piece_signal('remove', self.remove_pieces)
        self.gamerule.set_piece_signal('change', self.change_pieces)
        self.gamerule.set_piece_signal('swap', self.swap_pieces)
        self.gamerule.set_piece_signal('move', self.move_pieces)

    def add_default_piece_pts(self):
        """添加默认棋子"""
        self.gamerule.add_default_piece_pts()

    def click_board(self, pt = None, dot = None, name = None):
        """点击棋盘 点击组合：己方、对方、空白"""
        if (pt is None) and (dot is not None):
            pt = self.get_point(dot)
        if self.canvasboard.canvas_grid.pt_in_size(pt):
            return self.gamerule.move_point(pt = pt, name = name)
        return self.gamerule.move_site(pt = pt, name = name)
    
    def rebegin(self):
        self.gamerule.rebegin()
    
    def after_begin(self):
        self.gamerule.after_begin()
    
    def get_game_data(self):
        """保存游戏"""
        return self.gamerule.get_game_data()
    
    def get_current_game_data(self):
        """保存游戏"""
        return self.gamerule.get_current_game_data()
    
    def load_data(self, data):
        self.gamerule.load_data(data)
    
    def get_dot(self, pt, dot = None):
        """获取dot坐标"""
        return self.canvasboard.get_dot(pt, dot = dot)
    
    def get_point(self, dot):
        """获取dot坐标"""
        return self.canvasboard.dot_to_point((int(dot[0]), int(dot[1])))[0]

    def put_piece(self, pieceui:PieceUi, pt):
        """绘制棋子"""
        pt = pointData.as_point(pt)
        return {'pt': pt, 'ui':pieceui}

    def add_piece(self, value, pt):
        """绘制棋子"""
        pieceui = self.pieceuis.get(value)
        return self.put_piece(pieceui, pt)

    def add_pieces(self, value, pts):
        """绘制棋子"""
        return

    def remove_pieces(self, pts):
        """清除棋盘上的棋子"""
        pass
    
    def change_pieces(self, value, pts):
        pass
    
    def swap_pieces(self, pts_linkss):
        pass
    
    def move_pieces(self, pts_linkss):
        pass

    @property
    def player_names(self):
        return list(self.gamerule.players.keys())
    
    def gameover_tag_name(self, tag):
        match tag:
            case GameOverEnum.Win:
                return '获胜'
            case GameOverEnum.Lose:
                return '失败'
            case GameOverEnum.Draw:
                return '平局'
            case GameOverEnum.Stop:
                return '棋局终止'

    def on_race(self):
        """比赛"""
        self.gamerule.on_race()

    def out_race(self):
        """打谱"""
        self.gamerule.out_race()

    def give_up(self):
        self.gamerule.give_up()

    def ask_retract(self):
        return self.gamerule.move_manager.ask_retract()

    def agree_retract(self, askname):
        return self.gamerule.move_manager.agree_retract(askname)

    def pass_move(self):
        return self.gamerule.move_manager.pass_move()

    def on_player(self, name):
        """设置当前棋手为1棋手"""
        self.gamerule.player_manager.on_player(name)
    
    def on_turns(self):
        """轮换执棋"""
        self.gamerule.player_manager.on_turns()

    def on_symbol_tag(self, tag):
        """设置当前棋手为1棋手"""
        self.gamerule.on_symbol_tag(tag)
    
    def turn_player(self):
        """切换棋手"""
        self.gamerule.player_manager.turn_player()

    def step_back(self):
        """返回上一步"""
        self.gamerule.move_manager.step_back()
    
    def step_forward(self):
        """加载下一步"""
        self.gamerule.move_manager.step_forward()

    @property
    def show_piece_index(self):
        return self.canvasboard.show_piece_index

    def get_piece_index(self, pt):
        return self.gamerule.get_current_path_length_from_branch()


class ObjJson:
    @classmethod
    def dump(cls, data, filepath, **kwargs):
        nkwargs = {'ensure_ascii': False, 'indent': 2, 'default': cls.default_serializer, **kwargs}
        json.dump(data, filepath, **nkwargs)
    
    @classmethod
    def load(cls, filepath, **kwargs):
        return json.load(filepath, object_hook = cls.custom_decoder, **kwargs)

    @classmethod
    def default_serializer(cls, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        return obj
    
    @classmethod
    def custom_decoder(cls, data):
        if isinstance(data, dict) and len(data) == 1:
            if list(data.keys())[0] == "Vector2D":
                return Vector2D.from_json(data)
            elif list(data.keys())[0] == "MatrixP":
                return MatrixP.from_json(data)
            elif list(data.keys())[0] == "RegionBase":
                return RegionBase.from_json(data)
        return data
            
    __slots__ = ('name', 'userdict', 'gamerule', 'canvasboard',
                  'tagui', 'tags', 'pieceuis') 
    def __init__(self, name = '', userdict = None,  pieceuis = None, 
                 tagui = None, gamerule = None, canvasboard = None):
        self.name = name
        self.userdict = userdict or {}
        self.gamerule:GameData = gamerule or self.init_rule()
        self.pieceuis:DefaultPiecesUi = pieceuis or self.init_pieceuis()
        self.canvasboard = canvasboard or self.get_canvas()
        x_cell = self.canvasboard.canvas_grid.x_cell
        self.pieceuis.set_data(self.gamerule.pieces, 
                radius = x_cell//2-x_cell//20 or 50)
        self.tagui = tagui or GridTagUi(
                color = self.canvasboard.edgeui.color,
                height = x_cell//3
               )
        self.tags = {} # text,pts
        self.canvasboard.draw_background_grid()
        self.set_piece_default_signal()

    def init_rule(self):
        return
    
    def init_pieceuis(self):
        return
    
    def init_grid(self):
        return 
    
    def init_canvasattr(self):
        return {}

    def get_canvas(self):
        return CanvasBoard(canvas_grid = self.init_grid(), **self.init_canvasattr())
    
    def set_signal(self, key, func):
        self.gamerule.set_signal(key, func)
    
    def set_piece_signal(self, key, func):
        self.gamerule.set_piece_signal(key, func)
    
    def set_piece_default_signal(self):
        self.gamerule.set_piece_signal('add', self.add_pieces)
        self.gamerule.set_piece_signal('remove', self.remove_pieces)
        self.gamerule.set_piece_signal('change', self.change_pieces)
        self.gamerule.set_piece_signal('swap', self.swap_pieces)
        self.gamerule.set_piece_signal('move', self.move_pieces)

    def add_default_piece_pts(self):
        """添加默认棋子"""
        self.gamerule.add_default_piece_pts()

    def click_board(self, pt = None, dot = None, name = None):
        """点击棋盘 点击组合：己方、对方、空白"""
        if (pt is None) and (dot is not None):
            pt = self.get_point(dot)
        if self.canvasboard.canvas_grid.pt_in_size(pt):
            return self.gamerule.move_point(pt = pt, name = name)
        return self.gamerule.move_site(pt = pt, name = name)
    
    def rebegin(self):
        self.gamerule.rebegin()
    
    def after_begin(self):
        self.gamerule.after_begin()
    
    def get_dot(self, pt, dot = None):
        """获取dot坐标"""
        return self.canvasboard.get_dot(pt, dot = dot)
    
    def get_point(self, dot):
        """获取dot坐标"""
        return self.canvasboard.dot_to_point((int(dot[0]), int(dot[1])))[0]

    def put_piece(self, pieceui:PieceUi, pt):
        """绘制棋子"""
        pt = pointData.as_point(pt)
        return {'pt': pt, 'ui':pieceui}

    def add_piece(self, value, pt):
        """绘制棋子"""
        pieceui = self.pieceuis.get(value)
        return self.put_piece(pieceui, pt)

    def add_pieces(self, value, pts):
        """绘制棋子"""
        return

    def remove_pieces(self, pts):
        """清除棋盘上的棋子"""
        pass
    
    def change_pieces(self, value, pts):
        pass
    
    def swap_pieces(self, pts_linkss):
        pass
    
    def move_pieces(self, pts_linkss):
        pass

    @property
    def player_names(self):
        return list(self.gamerule.players.keys())
    
    def gameover_tag_name(self, tag):
        match tag:
            case GameOverEnum.Win:
                return '获胜'
            case GameOverEnum.Lose:
                return '失败'
            case GameOverEnum.Draw:
                return '平局'
            case GameOverEnum.Stop:
                return '棋局终止'

    def on_race(self):
        """比赛"""
        self.gamerule.on_race()

    def out_race(self):
        """打谱"""
        self.gamerule.out_race()

    def give_up(self):
        self.gamerule.give_up()

    def ask_retract(self):
        return self.gamerule.move_manager.ask_retract()

    def agree_retract(self, askname):
        return self.gamerule.move_manager.agree_retract(askname)

    def pass_move(self):
        return self.gamerule.move_manager.pass_move()

    def on_player(self, name):
        """设置当前棋手为1棋手"""
        self.gamerule.player_manager.on_player(name)
    
    def on_turns(self):
        """轮换执棋"""
        self.gamerule.player_manager.on_turns()
    
    def turn_player(self):
        """切换棋手"""
        self.gamerule.player_manager.turn_player()

    def step_back(self):
        """返回上一步"""
        self.gamerule.move_manager.step_back()
    
    def step_forward(self):
        """加载下一步"""
        self.gamerule.move_manager.step_forward()