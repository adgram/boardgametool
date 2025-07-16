"""
    棋盘坐标点的操作
    PieceUi
"""
from .matrixgrid import CanvasGrid, AxisEnum, Vector2D, MatrixData, RegionBase
from . import matrixgrid
from .boardUiData import (PieceUi, DefaultPiecesUi, GridCoorUi, GridLinesUi,
                        GridEdgesUi, GridStarUi, GridTagUi, LinePositionEnum)
from .gameData import GameData
from .moverule import GameOverEnum, CommonPlayer, AutoPlayer
import json
from enum import IntEnum


class RegionCircleEnum(IntEnum):
    """区域循环类型：无循环，x循环，y循环，xy双循环"""
    P = 0
    X = 1
    Y = 2
    XY = 3


# class PieceTagEnum(IntEnum):
#     """棋子标记"""
#     Active = 0
#     Win = 1
#     Lose = 2
#     Draw = 3  # 平局
#     Stop = 4  # 意外停止
#     Add = 5
#     Change = 6
#     Swap = 7
#     Move = 8




class CanvasBoard:
    """画板"""
    __slots__ = ('canvas_grid', 'canvas_lines', 'canvas_cells', 'cell_tags',
                 'bgedgeui', 'coorui', 'utedgeui', 'starui', 'tagui', 
                 'until_background', 'canvas_image', "image_dsize", "image_origin",
                 'canvas_background', "show_piece_index", 'pieces_values')
    def __init__(self, canvas_grid = None, **kwargs):
        self.canvas_grid = canvas_grid or CanvasGrid()          # 背景格线对象
        self.canvas_lines = kwargs.get('canvas_lines', [])      # 网格格线坐标
        self.canvas_cells = kwargs.get('canvas_cells', [])      # 网格填充
        self.cell_tags = kwargs.get('cell_tags', [])            # 网格标记
        self.bgedgeui = kwargs.get('bgedgeui', GridEdgesUi(
                color = kwargs.get('color', (0, 0, 0, 255)),
                fill = kwargs.get('fill', kwargs.get('color', (0, 0, 0, 255))),
                thickness = kwargs.get('thickness', 3),
                show = kwargs.get('bgedges_show', AxisEnum.Null),
               ))
        self.utedgeui = kwargs.get('utedgeui', GridLinesUi(
                color = kwargs.get('color', (0, 0, 0, 255)),
                fill = kwargs.get('fill', kwargs.get('color', (0, 0, 0, 255))),
                thickness = kwargs.get('thickness', 5)
               ))
        self.coorui = kwargs.get('coorui', GridCoorUi(
                color = self.bgedgeui.color,
                height = kwargs.get('coor_height', self.canvas_grid.x_cell//3),
                show = kwargs.get('coor_show', LinePositionEnum.Null)
               ))
        self.starui = kwargs.get('starui', GridStarUi(
                color = self.bgedgeui.color,
                show = kwargs.get('star_show', False),
                radius = kwargs.get('star_radius', self.canvas_grid.x_cell//5)
               ))
        self.tagui = kwargs.get('tagui', GridTagUi(
                color = self.bgedgeui.color,
                height = self.canvas_grid.x_cell//3,
                text = kwargs.get('tagtext', ''),
                icon = kwargs.get('tagicon', ''),
                iconsize = kwargs.get('iconsize', (self.canvas_grid.x_cell,
                                                   self.canvas_grid.x_cell)),
                textfunc = kwargs.get('tagtextfunc', lambda pt: ''),
                iconfunc = kwargs.get('tagiconfunc', lambda pt: '')
               ))
        self.until_background = {'edges':[], 'stars':[], 
                               'cells':[], 'cltags':[]}    # 自定义棋盘格线
        self.canvas_image = kwargs.get('canvas_image', None)    # 背景图片
        self.image_dsize = kwargs.get('image_dsize', (0, 0))    # 
        self.image_origin = kwargs.get('image_origin', (0, 0))  # 
        self.canvas_background = {'edges':[], 'stars':[], 'coors':[],
                               'cells':[], 'cltags':[], 'pieces': []}    # 自定义棋盘格线
        self.show_piece_index = kwargs.get('show_piece_index', False)
        self.pieces_values = kwargs.get('pieces_values', [])

    @property
    def size(self):
        return self.canvas_grid.canvas_size

    def get_dot(self, pt, dot = None):
        """获取dot坐标"""
        return dot or self.canvas_grid.get_dot(pt, self.canvas_grid.is_net)

    def dot_to_point(self, dot):
        """根据棋盘坐标获取所在顶点"""
        return self.canvas_grid.close_point(Vector2D(dot))

    def add_edge(self, pt1, pt2, ui):
        """绘制直线段"""
        return {'pt1': pt1, 'pt2': pt2, 'ui': ui}

    def add_cell(self, pt1, pt2, pt3, pt4, ui):
        return {'pt1': pt1, 'pt2': pt2, 'pt3': pt3, 'pt4': pt4, 'ui': ui}

    def add_coor(self, pt, axis, n):
        """绘制文字"""
        if axis == AxisEnum.X:
            text = str(n+1)
        elif axis == AxisEnum.Y:
            text = chr(ord('A') + (n +2 if n >= 14 else n +1 if n >= 8 else n))
        return {'pt': pt, 'text': text, 'ui':self.coorui}

    def add_star(self, pt):
        """绘制圆点"""
        return {'pt': pt, 'ui':self.starui}

    def add_tag(self, pt):
        """绘制圆点"""
        return {'pt': pt, 'ui':self.tagui}

    def draw_background_grid(self):
        grid = self.canvas_grid
        background = self.canvas_background
        for ln in grid.get_axis_edges(self.bgedgeui.show):
            background['edges'].append(self.add_edge(*ln, self.bgedgeui))
        for ln in grid.get_lines(self.canvas_lines):
            background['edges'].append(self.add_edge(*ln, self.bgedgeui))
        for pts in grid.get_cells(self.canvas_cells):
            background['cells'].append(self.add_cell(*pts, self.bgedgeui))
        for pt in grid.get_cltags(self.cell_tags):
            background['cltags'].append(self.add_tag(pt))
        match self.coorui.show:
            case LinePositionEnum.Start:
                for pt1, pt2, axis, n in grid.get_coors():
                    background['coors'].append(self.add_coor(pt1, axis, n))
            case LinePositionEnum.End:
                for pt1, pt2, axis, n in grid.get_coors():
                    background['coors'].append(self.add_coor(pt2, axis, n))
            case LinePositionEnum.Both:
                for pt1, pt2, axis, n in grid.get_coors():
                    background['coors'].append(self.add_coor(pt1, axis, n))
                    background['coors'].append(self.add_coor(pt2, axis, n))
            case _:
                pass
        if self.starui.show:
            for pt in grid.get_stars():
                background['stars'].append(self.add_star(pt))
        if self.pieces_values:
            for i, dot in enumerate(grid.get_pieces_box(len(self.pieces_values))):
                background['pieces'].append((self.pieces_values[i], dot))

    def until_background_grid(self, **kwargs):
        grid = self.canvas_grid
        background = self.until_background
        for ln in grid.get_lines(kwargs.get('esges', [])):
            background['edges'].append(self.add_edge(*ln, self.utedgeui))
        for pts in grid.get_cells(kwargs.get('cells', [])):
            background['cells'].append(self.add_cell(*pts, self.utedgeui))
        for pt in grid.get_cltags(kwargs.get('cltags', [])):
            background['cltags'].append(self.add_tag(pt))
        for pt in grid.get_cltags(kwargs.get('stars', [])):
            background['stars'].append(self.add_star(pt))


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
                radius = x_cell//2-x_cell//15 or 50)
        self.tagui = tagui or GridTagUi(
                color = self.canvasboard.bgedgeui.color,
                height = x_cell//3
               )
        self.canvasboard.draw_background_grid()
        self.set_piece_default_signal()

    def init_rule(self):
        return
    
    def init_pieceuis(self):
        return

    def grid_attr(self):
        return {}
    
    def init_canvasattr(self):
        return {}

    def get_canvas(self):
        grid = {'size': (9, 9), 'canvas_size': (750, 750), 'padding': (80, 80), 
                'is_net': True, 'boundless': True, 'coordinate': None,
                'origin': (0, 0), 'obliquity': 1j, 'centered': True}
        grid.update(self.grid_attr())
        grid['size'] = Vector2D(grid['size'])
        grid['canvas_size'] = Vector2D(grid['canvas_size'])
        grid['padding'] = Vector2D(grid['padding'])
        grid['origin'] = Vector2D(grid['origin'])
        return CanvasBoard(canvas_grid = CanvasGrid(**grid), **self.init_canvasattr())
    
    def set_signal(self, key, func):
        self.gamerule.set_signal(key, func)
    
    def set_piece_default_signal(self):
        return

    def refresh_matr_pts(self):
        """添加默认棋子"""
        self.gamerule.move_manager.refresh_matr_pts()

    def click_board(self, pt = None, dot = None, name = None):
        """点击棋盘 点击组合：己方、对方、空白"""
        if dot and self.canvasboard.canvas_background['pieces']:
            x_cell = (self.canvasboard.canvas_grid.x_cell//2)**2
            ps = {}
            for _val, _dot in self.canvasboard.canvas_background['pieces']:
                if (l := (Vector2D(dot) - _dot).length_sqr) <= x_cell:
                    ps[_val] = l
            if ps:
                val = list(sorted(ps.keys(), key = lambda x: ps[x]))[0]
                return self.gamerule.move_manager.set_active_piece(name or AutoPlayer, val)
        if (pt is None) and (dot is not None):
            pt = self.get_point(dot)
        if self.canvasboard.canvas_grid.pt_in_size(pt):
            return self.gamerule.move_manager.move_point(name or AutoPlayer, pt)
        return self.gamerule.move_manager.move_site(name or AutoPlayer, pt)
    
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
        pt = matrixgrid.as_point(pt)
        return {'pt': pt, 'ui':pieceui}

    def add_piece(self, value, pt):
        """绘制棋子"""
        pieceui = self.pieceuis.get(value)
        return self.put_piece(pieceui, pt)

    @property
    def player_names(self):
        return [name for name in self.gamerule.players.keys() if name != CommonPlayer]
    
    @property
    def active_player_name(self):
        return self.gamerule.active_player_name
    
    def gameover_tag(self, tag):
        match tag:
            case GameOverEnum.Win:
                return '获胜'
            case GameOverEnum.Lose:
                return '失败'
            case GameOverEnum.Draw:
                return '平局'
            case GameOverEnum.Stop:
                return '棋局终止'

    def set_race_mode(self, is_race):
        """比赛、打谱模式"""
        self.gamerule.move_manager.set_race_mode(is_race)

    def give_up(self):
        self.gamerule.move_manager.give_up()

    def ask_retract(self):
        return self.gamerule.move_manager.ask_retract()

    def agree_retract(self, askname):
        return self.gamerule.move_manager.agree_retract(askname)

    def pass_move(self):
        return self.gamerule.move_manager.pass_move()

    def on_player(self, name):
        """设置当前棋手为1棋手"""
        self.gamerule.players_manager.on_player(name)
    
    def on_turns(self):
        """轮换执棋"""
        self.gamerule.players_manager.on_turn()

    def set_symbol_tag(self, tag):
        """设置当前棋手为1棋手"""
        self.gamerule.move_manager.set_symbol_tag(tag)
    
    def turn_player(self):
        """切换棋手"""
        self.gamerule.turn_active()

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
        return self.gamerule.move_manager.history.get_current_path_length()



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
            elif list(data.keys())[0] == "MatrixData":
                return MatrixData.from_json(data)
            elif list(data.keys())[0] == "RegionBase":
                return RegionBase.from_json(data)
        return data
            