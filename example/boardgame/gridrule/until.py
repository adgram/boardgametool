
from enum import IntEnum


class RegionModeEnum(IntEnum):
    """区域类型枚举"""
    Empty = 0   # 空
    Line = 1    # 直线
    Pline = 2   # 多段线
    Rect = 3    # 矩形
    Mline = 4   # 多直线
    Points = 5  # 散点
    Polygon = 6 # 多边形
    Flaw = 7    # 缺失某些点
    Other = 8   # 其他


class RegionCircleEnum(IntEnum):
    """区域循环类型：无循环，x循环，y循环，xy双循环"""
    P = 0
    X = 1
    Y = 2
    XY = 3


class RectangleAxisEnum(IntEnum):
    """矩形轴类型：x轴，y轴。数据的折叠方式为沿y+排列向x+堆叠，即左下角指向右上角。"""
    X = 0
    Y = 1


class ExtendModeEnum(IntEnum):
    """扩展模式"""
    N = 0
    X = 1
    XP = 2
    XS = 3
    Y = 4
    YP = 5
    YS = 6


class MoveModeEnum(IntEnum):
    """移动模式：交换、占用、复制、不占位纯移动"""
    Swap = 0
    Occupy = 1
    Copy = 2
    Null = 3



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


class LinePositionEnum(IntEnum):
    Null = 0
    Start = 1
    End = 2
    Both = 3

