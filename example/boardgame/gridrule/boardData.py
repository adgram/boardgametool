"""
    棋盘坐标点的操作
    PieceUi
"""
from .matrixgrid import CanvasGrid, AxisEnum, Vector2D, MatrixP, RegionBase, CommonPlayer
from . import matrixgrid
from .until import LinePositionEnum, GameOverEnum
from .boardUiData import (PieceUi, DefaultPiecesUi, GridCoorUi, 
                        GridEdgesUi, GridStarUi, GridTagUi)
from .gameData import GameData
import json




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
        pt1 = matrixgrid.as_point(pt1)
        pt2 = matrixgrid.as_point(pt2)
        return {'pt1': pt1, 'pt2': pt2, 'ui':self.edgeui}

    def add_line(self, pt1, pt2):
        pt1 = matrixgrid.as_point(pt1)
        pt2 = matrixgrid.as_point(pt2)
        return {'pt1': pt1, 'pt2': pt2, 'ui':self.edgeui}

    def add_cell(self, pt1, pt2, pt3, pt4):
        pt1 = matrixgrid.as_point(pt1)
        pt2 = matrixgrid.as_point(pt2)
        pt3 = matrixgrid.as_point(pt3)
        pt4 = matrixgrid.as_point(pt4)
        return {'pt1': pt1, 'pt2': pt2, 'pt3': pt3, 'pt4': pt4, 'ui':self.edgeui}

    def add_coor(self, pt, axis, n):
        """绘制文字"""
        pt = matrixgrid.as_point(pt)
        if axis == AxisEnum.X:
            text = str(n+1)
        elif axis == AxisEnum.Y:
            text = chr(ord('A') + (n +2 if n >= 14 else n +1 if n >= 8 else n))
        return {'pt': pt, 'text': text, 'ui':self.coorui}

    def add_star(self, pt):
        """绘制圆点"""
        pt = matrixgrid.as_point(pt)
        return {'pt': pt, 'ui':self.starui}

    def add_tag(self, pt):
        """绘制圆点"""
        pt = matrixgrid.as_point(pt)
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
        pt = matrixgrid.as_point(pt)
        return {'pt': pt, 'ui':pieceui}

    def add_piece(self, value, pt):
        """绘制棋子"""
        pieceui = self.pieceuis.get(value)
        return self.put_piece(pieceui, pt)

    def add_pieces(self, pts_map):
        """绘制棋子"""
        return

    def remove_pieces(self, pts):
        """清除棋盘上的棋子"""
        pass
    
    def change_pieces(self, pts_map):
        pass
    
    def swap_pieces(self, pts_linkss):
        pass
    
    def move_pieces(self, pts_linkss):
        pass

    @property
    def player_names(self):
        return [name for name in self.gamerule.players.keys() if name != CommonPlayer]
    
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
            