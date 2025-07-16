
from .matrixgrid import Vector2D, AxisEnum
from typing import Callable
from enum import IntEnum


VectorMapText = Callable[[tuple[int, int]|Vector2D], str]


class LinePositionEnum(IntEnum):
    Null = 0
    Start = 1
    End = 2
    Both = 3


class Attribute:
    def copy(self, **kwargs):
        return self.__class__(**{**self.get_attr(), **kwargs})
    
    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_attr(self):
        return {k: getattr(self, k) for k in self.__slots__}
    
    def __iter__(self):
        for k in self.__slots__:
            yield getattr(self, k)
    
    def __repr__(self):
        return f'{self.__class__.__name__}_{self.get_attr()}'



class GridEdgesUi(Attribute):
    """网格线框"""
    __slots__ = ('color', 'thickness', 'fill', 'show')
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', (255, 255, 255, 0))        # 线颜色
        self.thickness = kwargs.get('thickness', 0)                 # 线宽
        self.fill = kwargs.get('fill', self.color)
        self.show = kwargs.get('show', AxisEnum.Null)


class GridLinesUi(Attribute):
    """网格线框"""
    __slots__ = ('color', 'thickness', 'fill')
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', (255, 255, 255, 0))        # 线颜色
        self.thickness = kwargs.get('thickness', 0)                 # 线宽
        self.fill = kwargs.get('fill', self.color)



class GridStarUi(Attribute):
    """网格星位"""
    __slots__ = ('color', 'radius', 'show')
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', (255, 255, 255, 0))        # 线颜色
        self.radius = kwargs.get('radius', 0)
        self.show = kwargs.get('show', False)



class GridCoorUi(Attribute):
    """网格坐标文字"""
    __slots__ = ('height', 'color', 'font', 'show')
    def __init__(self, **kwargs):
        self.height = kwargs.get('height', 10)
        self.color = kwargs.get('color', (255, 255, 255, 0))
        self.font = kwargs.get('font', None)
        self.show = kwargs.get('show', LinePositionEnum.Null)



class GridTagUi(Attribute):
    """网格标记，字母、三角形等"""
    __slots__ = ('text', 'icon', 'height', 'color', 'font',
                 'textfunc', 'iconfunc', 'iconsize')
    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.icon = kwargs.get('icon', '')
        self.height = kwargs.get('height', 10)
        self.color = kwargs.get('color', (255, 255, 255, 0))
        self.font = kwargs.get('font', None)
        self.iconsize = kwargs.get('iconsize', None)
        self.textfunc:VectorMapText = kwargs.get('textfunc', None)
        self.iconfunc:VectorMapText = kwargs.get('iconfunc', None)

    def get_text(self, pt):
        return self.text or self.textfunc(pt)

    def get_icon(self, pt):
        return self.icon or self.iconfunc(pt)



class PieceColor(Attribute):
    """棋子颜色"""
    __slots__ = ('color', 'fill', 'gradient', 'thickness', 'offset')
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', (255, 255, 255, 0))        # 描边颜色
        self.fill = kwargs.get('fill', (255, 255, 255, 0))          # 填充颜色
        self.gradient = kwargs.get('gradient', self.fill)           # 渐变颜色
        self.thickness = kwargs.get('thickness', 0)                 # 线宽
        self.offset = kwargs.get('offset', 0)


class PieceText(Attribute):
    """棋子文字"""
    __slots__ = ('text', 'height', 'color', 'font', 'show')
    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.height = kwargs.get('height', 10)
        self.color = kwargs.get('color', (255, 255, 255, 0))
        self.font = kwargs.get('font', None)
        self.show = kwargs.get('show', False)



class PieceUi(Attribute):
    """棋子属性"""
    __slots__ = ('icon', 'text', 'color', 'radius', 'index_text')
    def __init__(self, **kwargs):
        self.icon = kwargs.get('icon', None)            # 图标
        self.text = kwargs.get('text', None)            # 文字 PieceText
        self.color = kwargs.get('color', None)          # 描边颜色 PieceColor
        self.radius = kwargs.get('radius', 0)           # 半径
        self.index_text = ''



class DefaultPiecesUi:
    __slots__ = ('piecedata', 'pieceui')
    def __init__(self):
        self.piecedata = {}
        self.pieceui = {}

    def get(self, value: int):
        return self.pieceui.get(value)

    def set_data(self, data, radius = 0):
        self.piecedata = data
        for piece in self.piecedata.values():
            self.pieceui[piece.value] = PieceUi(radius = radius)

    @classmethod
    def get_tag(cls, tag):
        match tag:
            case "Win":
                return PieceWinUi()
            case "Lose":
                return PieceLoseUi()
            case "Draw":
                return PieceDrawUi()
            case "Active":
                return PieceActiveUi()
            case "Swap":
                return PieceSwapUi()
            case "Move":
                return PieceMoveUi()
            case "Add":
                return PieceAddUi()
            case "Change":
                return PieceChangeUi()
    
    @classmethod
    def get_symbol(cls, tag):
        return PieceSymbolUi(text = tag)



class PieceWinUi(Attribute):
    __slots__ = ('color', 'radius')
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', PieceColor(
                    fill = (0, 255, 255, 155)))
        self.radius = kwargs.get('radius', 10)


class PieceLoseUi(Attribute):
    __slots__ = ('color', 'radius')
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', PieceColor(
                    fill = (255, 0, 255, 155)))
        self.radius = kwargs.get('radius', 10)


class PieceDrawUi(Attribute):
    __slots__ = ('color', 'radius')
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', PieceColor(
                    fill = (255, 255, 0, 155)))
        self.radius = kwargs.get('radius', 10)


class PieceActiveUi(Attribute):
    __slots__ = ('color', 'radius')
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', PieceColor(
                    fill = (255, 111, 97, 155)))
        self.radius = kwargs.get('radius', 10)


class PieceAddUi(Attribute):
    __slots__ = ('color', 'radius')
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', PieceColor(
                    fill = (82, 217, 173, 155)))
        self.radius = kwargs.get('radius', 10)


class PieceSwapUi(Attribute):
    __slots__ = ('color', 'radius')
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', PieceColor(
                    fill = (63, 81, 181, 155)))
        self.radius = kwargs.get('radius', 10)


class PieceMoveUi(Attribute):
    __slots__ = ('color', 'radius')
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', PieceColor(
                    fill = (63, 81, 181, 155)))
        self.radius = kwargs.get('radius', 10)


class PieceChangeUi(Attribute):
    __slots__ = ('color', 'radius')
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', PieceColor(
                    fill = (63, 81, 181, 155)))
        self.radius = kwargs.get('radius', 10)


class PieceSymbolUi(Attribute):
    __slots__ = ('color', 'radius', 'text')
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', PieceColor(
                    fill = (255, 255, 255, 85)))
        self.radius = kwargs.get('radius', 10)
        self.text = PieceText(text = kwargs.get('text', ''), 
                              color = (0, 0, 255, 255),
                              height = 20,
                              show = True)