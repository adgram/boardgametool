from .matrixgrid import MatrixData, NullValue, Vector2D
from .signals import TSignals
from enum import Enum
from typing import Callable


CommonPlayer = "_CommonPlayer_"
AutoPlayer = "_AutoPlayer_"
NullCount = -9999



class GameOverEnum(Enum):
    """游戏结束状态"""
    Going = 0
    Win = 1
    Lose = 2
    Draw = 3  # 平局
    Stop = 4  # 意外停止


'''可以移动的方式，移动自身、移动击杀，移动对手，移动对手击杀'''
class MoveRuleEnum(Enum):
    Move = 0
    Kill = 1
    Omove = 2
    Okill = 3


class MoveIndexNode:
    """某手棋的数据节点"""
    __slots__ = ('player_name', 'index', 'next', 'prev')
    def __init__(self, player_name = '', index:int = -1):
        self.player_name:str = player_name
        self.index:int = index
        self.next: list[MoveIndexNode] = []
        self.prev: MoveIndexNode|None = None


class MoveHistory:
    """行棋历史记录"""
    __slots__ = ('head', 'current', 'history_data', 'branches', 'symbols')
    def __init__(self):
        self.head:MoveIndexNode = MoveIndexNode()  # 默认头节点
        self.current:MoveIndexNode = self.head
        self.branches: list[MoveIndexNode] = []
        self.symbols:list[str] = []
        self.history_data:list = []
    
    def at_symbol(self, index):
        ...
    
    def at_move_data(self, index):
        ...
    
    def move_step(self, index):
        ...

    def add_move(self, index):
        ...

    @property
    def current_move_data(self):
        ...

    @property
    def current_symbol(self):
        ...

    @property
    def prev_move_data(self):
        ...


    def move(self, player_name, index):
        """执行节点"""
        ...

    def undo(self)-> tuple[str, int]:
        """悔棋一步"""
        ...

    def retract(self, player_name)-> list[tuple[str, int]]:
        """悔棋到上次这个玩家行棋前"""
        ...

    def back(self)-> tuple[str, MoveIndexNode]:
        """返回上一步。返回上一步玩家和撤回的数据"""
        ...

    def forward(self)-> tuple[str, MoveIndexNode]:
        """跳到下一步。返回下一步玩家和下一步的数据"""
        ...

    def jump_to_path(self, path):
        """跳转到指定路径
        """
        ...

    def current_index(self)->int:
        """获取当前数据"""
        ...

    def current_player(self)->str:
        """获取当前数据"""
        ...

    def current_path(self)->list:
        """获取当前路径"""
        ...
    
    def prev_move(self) -> list:
        ...
    
    def prev_player(self) -> str:
        ...

    def prev_index(self) -> dict:
        ...
    
    def to_json(self, current = None) -> list:
        """序列化历史记录树结构"""
        ...

    @classmethod
    def from_json(cls, data: list, head_begin = False) -> 'MoveHistory':
        """反序列化历史记录"""
        ...

    def find_depth_node(self) -> MoveIndexNode:
        """通过遍历找到最长路径末端作为当前节点"""
        ...

    def search(self, index:int) -> MoveIndexNode:
        """通过遍历找到最长路径末端作为当前节点"""
        ...

    def get_path(self, item : MoveIndexNode) -> list[int]:
        """获取指定节点的完整路径"""
        ...

    def get_branch_path(self, item : MoveIndexNode) -> tuple[MoveIndexNode, int]:
        """获取指定节点的局部位置"""
        ...

    def get_path_length(self, index:int) -> int:
        ...

    def get_current_path_length(self) -> int:
        ...

    def from_path(self, path: list[int]) -> MoveIndexNode:
        ...
    
    def create_linear_history(self, target_node:  MoveIndexNode) -> 'MoveHistory':
        '''根据目标节点提取简化的历史记录'''
        ...

    def simplify_history(self) -> 'MoveHistory':
        '''根据当前节点提取简化的历史记录'''
        ...
    
    def current_path_length_from_branch(self) -> int:
        ...




class MoveTurns:
    __slots__ = ('turns', 'active_turn')
    def __init__(self, turns: list[str], active_turn = 0) -> None:
        self.turns:list[str] = turns
        self.active_turn:int = active_turn
    
    def active_player(self):
        ...
    
    def set_turns(self, turns: list[str]) -> None:
        ...

    # def make_turn(self, turn = -1, reverse = False):
    #     ...

    def player_index(self, player_name, reverse = False):
        ...
    
    # def make_player_turn(self, player = AutoPlayer, reverse = False):
    #     ...

    # def turned_player(self, player = AutoPlayer, reverse = False):
    #     ...

    # def set_active_player(self, player = CommonPlayer):
    #     ...

    def remove_player(self, player_name):
        ...



class PieceData:
    __slots__ = ('value', 'name', 'count', 'num', 'piaceable', 'occupy', 'squeeze')
    def __init__(self, value = 1, name = "", player = None,
                  count = NullCount, placeable = False,
                  moverules = [], occupy = [], squeeze = []):
        self.value:int = value
        self.name:str = name
        self.count:int = count
        self.num:int = 0
        self.placeable:bool = placeable
        self.occupy:list[MoveRuleEnum] = occupy
        self.squeeze:list[int] = squeeze

    @property
    def player(self)->PlayerData:
        ...
    
    def set_player(self, player):
        ...
    
    def clone(self):
        ...
    
    def add(self, pts):
        ...
    
    def remove(self, pts):
        ...
    
    def change(self, pts, npiece):
        ...
    
    def get_flag(self, type):
        ...
    
    def set_flag(self, type, state: bool):
        ...
    
    # def is_placeable(self, value):
    #     ...
    
    # def is_occupyable(self, value):
    #     ...
    
    # def is_squeezable(self, value):
    #     ...



class PlayerData:
    __slots__ = ("name", "pieces", "current_pt", "time_num", "score", "active")  
    def __init__(self, name = "", pieces = {}, time_num = 0):
        self.name:str = name
        self.pieces:list[PieceData] = pieces
        self.current_pt:Vector2D|None = None
        self.active:int = NullValue
        self.time_num:int = time_num
        self.score:int = 0
    
    def clone(self):
        ...
    
    def get_active(self)->int:
        ...
    
    def clear_current(self):
        ...
    
    def has_piece(self, value):
        ...
    
    def add_piece(self, piece):
        ...
    
    def add_pieces(self, pieces):
        ...



class PlayersManager:
    __slots__ = ("players", "pieces", "move_turns", "in_turns")
    def __init__(self):
        self.players:list[PlayerData] = {}
        self.pieces:list[PieceData] = {}
        self.move_turns: MoveTurns = MoveTurns()
        self.in_turns: bool = True
    
    def set_turns(self, turns):
        ...
    
    def reset(self, pieces_count):
        ...
    
    def init(self, players, common_pieces, turns, pieces_count):
        ...
    
    def get_player(self, name)->PlayerData:
        ...
    
    def get_player(self, value)->PlayerData:
        ...
    
    def get_player(self, player_name)->PlayerData:
        ...
    
    def get_piece(self, piece)->PieceData:
        ...
    
    def get_piece(self, value)->PieceData:
        ...
    
    @property
    def common_player(self) -> PlayerData:
        ...
    
    @property
    def active_player(self) -> PlayerData:
        ...
    
    @property
    def active_player_name(self) -> str:
        ...
    
    def add_player(self, name = AutoPlayer, player = None):
        ...
    
    def add_common_player(self, piece: list[PieceData] = []):
        ...
    
    def add_players(self, piece: dict[str, PlayerData] = {}):
        ...
    
    def add_players(self, piece: list[PlayerData] = []):
        ...
    
    def remove_player(self, name):
        ...
    
    def remove_piece(self, value):
        ...
    
    # def set_active(self, name):
    #     ...
    
    def on_player(self, name):
        ...
    
    def on_turn(self):
        ...
    
    # def turn_player(self, player = AutoPlayer, reverse = False):
    #     ...
    
    def swap_players(self, name1, name2):
        ...
    
    def swap_pieces(self, value1, value2):
        ...
    
    def send_msg(self, player_name, msg):
        ...

    def get_signals(self, key): ...

    def set_signal(self, key, func): ...

    def call_signal(self, key, args): ...
    


class MatrixCallback:
    def __init__(self):
        self.collection: Callable = None
        self.contains: Callable = None
        self.get_valid_value: Callable = None
        self.get_value: Callable = None
        self.set_value: Callable = None



class MoveManager():
    def __init__(self):
        self.is_over:bool = False
        self.in_race:bool = True
        self.start_clock:bool = False
        self.step_funcs:dict[str, Callable] = {"game_over": self.step_game_over,
                                               "pass": self.step_pass}
        self.reverse_funcs:dict[str, Callable] = {"game_over": self.reverse_game_over,
                                                  "pass": self.reverse_pass}
        self.clock_func: Callable = lambda player_name, info: ...
        self.move_site_func: Callable = lambda player_name, pt: ...
    
    @property
    def history(self) -> MoveHistory: ...
    
    @property
    def players_manager(self) -> PlayersManager: ...

    def set_history(self, history: MoveHistory): ...
    
    def reset(self, in_race, start_clock, matr, pts_map):
        ...

    def set_matr_func(self, matr): ...
    def add_step_function(self, name, step_func, reverse_func): ...
    def remove_step_function(self, name): ...
    def add_value_pts(self, player_name, pts, val = NullValue): ...
    def remove_value_pts(self, val, pts): ...
    def change_value_pts(self, val, pts): ...
    def pts_add(self, pts_map): ...
    def pts_remove(self, pts): ...
    def links_swap(self, pts_links): ...
    def links_move(self, pts_links): ...
    def links_kill(self, player_name, pts_links): ...
    def add_tag_pts(self, player_name, pts, tag): ...
    def update_tag_pts(self, player_name, pts, tag): ...
    def remove_tag_pts(self, player_name, tag): ...
    def move_over(self, player_name, tag, data): ...
    def add_move(self, player_name, tag, data): ...
    def move_symbol_tag(self, pt, tag): ...
    def set_active_pt(self, player_name, pt): ...
    def turn_active(self, name = AutoPlayer, reverse = False): ...
    def ask_retract(self): ...
    def agree_retract(self, askname): ...
    def step_back(self): ...
    def step_forward(self): ...
    def set_race_mode(self, is_race, player = AutoPlayer): ...
    def do_game_over(self, player_name, tag, single = False): ...
    def step_game_over(self, player_name, data): ...
    def reverse_game_over(self, player_name, data): ...
    def do_pass(self, player_name = AutoPlayer, double_pass = False): ...
    def step_pass(self, player_name, data = tuple()): ...
    def reverse_pass(self, player_name, data = tuple()): ...
    def pass_move(self): ...
    def move_point(self, player_name, pt): ...
    def move_site(self, player_name, pt): ...
    def set_active_piece(self, player_name, value): ...
    def set_symbol_tag(self, tag): ...
    def give_up(self, player = AutoPlayer): ...
    def refresh_matr_pts(self): ...
    def add_move_function(self, tag, func): ...
    def get_signals(self, key) -> TSignals: ...

    def set_signal(self, key, func): ...

    def call_signal(self, key, args): ...