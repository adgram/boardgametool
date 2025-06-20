
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



from .matrixgrid import MoveHistory, MoveIndexNode


class History:
    """行棋历史记录"""
    __slots__ = ('move_history', 'data', 'symbols')
    def __init__(self):
        self.move_history = MoveHistory()
        self.data = []
        self.symbols = {}
    
    def get(self, index: int):
        if index == -1:
            return {}
        return self.data[index]
    
    def get_symbol(self, index: int):
        return self.symbols.get(index, [])

    def move_step(self, player, move_data):
        """执行节点"""
        n = len(self.data)
        self.data.append([move_data])
        self.move_history.move(player, n)

    def add_move(self, player, move_data):
        """执行节点"""
        if player == self.current_player:
            self.current_data.append(move_data)
        elif player == self.prev_player:
            self.prev_data.append(move_data)
        else:
            raise ValueError('玩家错误')

    def add_symbol(self, symbol):
        """执行节点"""
        self.symbols.setdefault(self.current_index, []).append(symbol)
    
    @property
    def current_symbol(self):
        return self.symbols.get(self.current_index, [])

    def undo(self)-> dict:
        """悔棋一步"""
        player, index = self.move_history.undo()
        if index == -1:
            return {}
        data = self.data[index]
        self.data[index] = {}
        return player, data

    def retract(self, player)-> list[tuple[str, dict]]:
        """悔棋到上次这个玩家行棋前"""
        pairs = []
        for player, index in self.move_history.retract(player):
            data = self.data[index]
            self.data[index] = {}
            pairs.append((player, data))
        return pairs

    def back(self)-> tuple[str, MoveIndexNode, dict]:
        """返回上一步。返回上一步玩家和撤回的数据"""
        player, node = self.move_history.back()
        return player, node, self.get(node.index), self.get_symbol(node.index-1)

    def forward(self)-> tuple[str, MoveIndexNode, dict]:
        """跳到下一步。返回下一步玩家和下一步的数据"""
        player, node = self.move_history.forward()
        return player, node, self.get(node.index), self.get_symbol(node.index)

    def jump_to_path(self, path):
        """跳转到指定路径
        """
        return self.move_history.jump_to_path(path)

    @property
    def current_index(self):
        """获取当前数据"""
        return self.move_history.current_index()

    @property
    def current_data(self):
        """获取当前数据"""
        index = self.move_history.current_index()
        return self.data[index] if index >= 0 else []

    @property
    def current_player(self):
        """获取当前数据"""
        return self.move_history.current_player()

    @property
    def current_path(self):
        """获取当前路径"""
        return self.move_history.current_path()
    
    @property
    def prev_move(self):
        return self.move_history.prev_move()
    
    @property
    def prev_player(self):
        return self.move_history.prev_player()

    @property
    def prev_index(self) -> int:
        return self.move_history.prev_index()

    @property
    def prev_data(self) -> list:
        index = self.move_history.prev_index()
        return self.data[index] if index >= 0 else {}
    
    def to_json(self) -> dict:
        """序列化历史记录树结构"""
        return {"data": self.data, "move_history": self.move_history.to_json(), 'symbols': self.symbols}

    @classmethod
    def from_json(cls, data: dict, head_begin = False) -> 'MoveHistory':
        """反序列化历史记录"""
        new = cls()
        new.move_history = MoveHistory.from_json(data["move_history"], head_begin)
        new.data = data["data"]
        new.symbols = data["symbols"]
        return new

    def find_depth_node(self) -> MoveIndexNode:
        """通过遍历找到最长路径末端作为当前节点"""
        return self.move_history.find_depth_node()

    def search(self, index:int) -> MoveIndexNode:
        """通过遍历找到最长路径末端作为当前节点"""
        return self.move_history.search(index)

    def get_path(self, item : MoveIndexNode) -> list[int]:
        """获取指定节点的完整路径"""
        return self.move_history.get_path(item)

    def get_path_from_branch(self, item : MoveIndexNode) -> tuple[MoveIndexNode, int]:
        """获取指定节点的局部位置"""
        return self.move_history.get_path_from_branch(item)

    def get_current_path_length(self) -> int:
        return self.move_history.get_current_path_length()
    
    def get_path_length(self, index:int) -> int:
        """获取指定节点的完整路径"""
        return self.move_history.get_path_length(index)

    def from_path(self, path: list[int]) -> MoveIndexNode:
        return self.move_history.from_path(path)
    
    def create_linear_history(self, target_node:  MoveIndexNode) -> 'MoveHistory':
        return self.move_history.create_linear_history(target_node)

    def simplify_history(self) -> 'MoveHistory':
        return self.move_history.simplify_history()

    def get_current_path_length_from_branch(self):
        node = self.move_history.current
        if node.index == -1:
            return 0
        return self.move_history.get_path_from_branch(node)[1]


ClockStrSignals = GenericSignal[str, str]


import time
import multiprocessing


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
