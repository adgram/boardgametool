
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


class PointMirrorEnum(IntEnum):
    """对称类型：无对称，中心对称，x轴对称，y轴对称，x=y轴对称，-x=y轴对称"""
    P = 0
    X = 1
    Y = 2
    XPY = 3
    XSY = 4
    O = 5


class RectangleAxisEnum(IntEnum):
    """矩形轴类型：x轴，y轴。数据的折叠方式为沿y+排列向x+堆叠，即左下角指向右上角。"""
    X = 0
    Y = 1


class AxisEnum(IntEnum):
    Null = 0
    X = 1
    Y = 2
    XY = 3


class NeighborTypeEnum(IntEnum):
    """NeighborTableDataType数据模式"""
    Structure = 0
    Direction = 1
    Mathvector = 2
    Link = 3


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


class MoveRuleEnum(IntEnum):
    """可以移动的方式，移动自身、移动击杀，移动对手，移动对手击杀"""
    Move = 0
    Kill = 1
    Omove = 2
    Okill = 3


class GameOverEnum(IntEnum):
    """游戏结束状态"""
    Going = 0
    Win = 1
    Lose = 2
    Draw = 3  # 平局
    Stop = 4  # 意外停止


class PieceTagEnum(IntEnum):
    """棋子标记"""
    Active = 0
    Win = 1
    Lose = 2
    Draw = 3  # 平局
    Stop = 4  # 意外停止
    Add = 5
    Change = 6
    Swap = 7
    Move = 8


class LinePositionEnum(IntEnum):
    Null = 0
    Start = 1
    End = 2
    Both = 3





from typing import Generic, TypeVarTuple
Ts = TypeVarTuple('Ts')


"""信号与槽的类"""
class SimpleSignals:
    """矩阵模板"""
    __slots__ = ('_direct_listener',)
    def __init__(self):
        self._direct_listener: dict[str, set] = {}

    def connect(self, key, callback):
        if key not in self._direct_listener:
            self._direct_listener[key] = set()
        self._direct_listener[key].add(callback)

    def disconnect(self, key, callback):
        if key in self._direct_listener:
            self._direct_listener[key].remove(callback)

    def clear(self):
        for key in self._direct_listener:
            self._direct_listener[key] = set()
    
    def register_keys(self, keys: list[str]):
        for key in keys:
            if key not in self._direct_listener:
                self._direct_listener[key] = set()
    
    def keys(self):
        return list(self._direct_listener.keys())

    def direct_listener(self, key):
        return self._direct_listener.get(key, set())

    def call(self, key):
        for callback in self.direct_listener(key):
            callback()


class GenericSignal(SimpleSignals, Generic[*Ts]):
    def call(self, key: str, *args: *Ts) -> None:
        for callback in self.direct_listener(key):
            callback(*args)





class MoveNode:
    """某手棋的数据节点"""
    __slots__ = ('player', 'data', 'next', 'prev')
    def __init__(self, player = '', move_data:dict = None):
        self.player = player
        self.data = move_data or {}
        self.next: list[MoveNode] = []
        self.prev: MoveNode|None = None


class History:
    """行棋历史记录"""
    __slots__ = ('head', 'current')
    def __init__(self):
        self.head = MoveNode()  # 默认头节点
        self.current:MoveNode = self.head

    def move(self, player, move_data):
        """执行节点"""
        new_node = MoveNode(player, move_data)
        self.current.next.append(new_node)
        new_node.prev = self.current
        self.current = new_node

    def add_move(self, player, move_data):
        """添加节点"""
        if player == self.current.player:
            self.current.data.update(move_data)
        elif player == self.prev_player:
            self.prev_data.update(move_data)
        else:
            raise ValueError('玩家错误')

    def undo(self)-> MoveNode|None:
        """悔棋一步"""
        if self.current is not self.head:
            current = self.current
            prev_node = self.current.prev
            prev_node.next.remove(self.current)
            self.current = prev_node
            return current
        return None

    def retract(self, player)-> list[MoveNode]:
        """悔棋到上次这个玩家行棋前"""
        result = []
        while self.current.player != player and self.current is not self.head:
            undo = self.undo()
            if undo is None:
                return []
            result.append(self.undo())
        if self.current.player == player:
            result.append(self.undo())
        else:
            return []
        return result

    def back(self)-> tuple[str, MoveNode]:
        """返回上一步。返回上一步玩家和撤回的数据"""
        if self.current is not self.head:
            temp, self.current = self.current, self.current.prev
            return self.current.player, temp
        return '', self.current

    def forward(self)-> tuple[str, MoveNode]:
        """跳到下一步。返回下一步玩家和下一步的数据"""
        if self.current.next:
            self.current = self.current.next[0]
            return self.current.player, self.current
        return '', self.current

    def jump_to_path(self, path):
        """跳转到指定路径
        """
        node = self.head
        for index in path:
            if index < len(node.next):
                node = node.next[index]
            else:
                ValueError("路径错误")
        self.current = node

    @property
    def current_data(self):
        """获取当前数据"""
        return self.current.data

    @property
    def current_player(self):
        """获取当前数据"""
        return self.current.player

    @property
    def current_path(self):
        """获取当前路径"""
        path = []
        node = self.current
        while node.prev: # 直到self.head
            path.append(node.prev.next.index(node))
            node = node.prev
        return path[::-1]
    
    @property
    def prev_move(self):
        return self.current.prev
    
    @property
    def prev_player(self):
        if self.current is not self.head:
            return self.current.prev.player
        return ''

    @property
    def prev_data(self) -> dict:
        if self.current is not self.head:
            return self.current.prev.data
        return {}



import time
import multiprocessing


ClockStrSignals = GenericSignal[str, str]

class PlayerClock:
    __slots__ = ('player', 'num', 'event', 'process')
    def __init__(self, player:str, time_num: int, signals:ClockStrSignals):
        self.player = player
        self.num = time_num
        self.event = multiprocessing.Event()
        self.process = multiprocessing.Process(target = self.countdown, kargs = signals)

    def countdown(self, **signals):
        """倒计时"""
        if not self.event.is_set():
            signals.call('time_start', self.player)
        while self.num > 0:
            if self.event.is_set():
                # 如果事件被设置，暂停
                self.event.clear()
                signals.call('time_stop', self.player)
                # 等待恢复信号
                while not self.event.is_set():
                    time.sleep(1)
                signals.call('time_start', self.player)
            time.sleep(1)
            self.num -= 1
            signals.call('time_running', self.player)
        # 倒计时结束执行
        signals.call('time_over', self.player)


class ClockManager:
    """计时器"""
    __slots__ = ('game_time', 'signals')
    def __init__(self, signals:ClockStrSignals):
        self.game_time: dict[str, PlayerClock] = {}
        self.signals = signals

    def set_clock(self, player:str, time_num: int):
        """设置倒计时"""
        self.game_time[player] = PlayerClock(player, time_num, self.signals)

    def start_clock(self, player:str = ''):
        """开始倒计时"""
        if not player:
            for clock in self.game_time.values():
                clock.process.start()
            return
        if player in self.game_time:
            self.game_time[player].process.start()
        else:
            print(f"未开始计时或玩家 {player} 不存在，无法开始倒计时。")

    def change_clock(self, player:str = ''):
        """暂停或继续倒计时"""
        if not player:
            for clock in self.game_time.values():
                clock.event.set()
            return
        if player in self.game_time:
            self.game_time[player].event.set()
        else:
            print(f"未开始计时或玩家 {player} 不存在，无法暂停或继续倒计时。")

    def over_clock(self, player:str = ''):
        """结束倒计时"""
        if not player:
            for clock in self.game_time.values():
                clock.num = 0
            return
        if player in self.game_time:
            self.game_time[player].num = 0
        else:
            print(f"未开始计时或玩家 {player} 不存在，无法结束倒计时。")
