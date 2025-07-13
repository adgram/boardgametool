
from .matrixgrid import MatrixData, Vector2D
from .moverule import (AutoPlayer, NullCount, PieceData, PlayerData, MoveManager,
                       PlayersManager, MoveHistory, MatrixCallback)
from .clocktool import ClockManager


class GameData:
    """
    游戏的基本数据常量
    """
    __slots__ = ('move_manager', 'clock_manager', 'temporary', 'lag_temporary')
    def __init__(self):
        self.matr: MatrixData = None
        self.move_manager = MoveManager()
        self.clock_manager = ClockManager()
        self.temporary = {}
        self.lag_temporary = {}
        self.begin()

    @property
    def players_manager(self)->PlayersManager:
        return self.move_manager.players_manager

    @property
    def pieces(self):
        return self.move_manager.players_manager.pieces
    
    @property
    def players(self):
        return self.move_manager.players_manager.players

    @property
    def active_player(self):
        """获取当前棋手"""
        return self.move_manager.players_manager.active_player
    
    @property
    def active_player_name(self):
        return self.move_manager.players_manager.active_player_name
    
    def begin(self):
        self.temporary = self.init_temporary()
        self.matr = self.init_matr()
        self._init_players_manager()
        self._init_move_manager()
        self._init_clock_manager()
        self.lag_temporary = self.init_lag_temporary()

    def rebegin(self):
        self.temporary = self.init_temporary()
        self.matr = self.init_matr()
        self.move_manager.players_manager.reset(self.init_piece_count())
        self.move_manager.reset(True, False, self.init_matr_pts())
        self.clock_manager.reset_clocks({player.name: player.time_num
                    for player in self.players.values()})
        if self.move_manager.start_clock: self.clock_manager.start_clock()
        self.lag_temporary = self.init_lag_temporary()

    def after_begin(self):
        self.call_signal('active_player', self.active_player_name)
        self.call_signal('info_piece', self.active_player_name,
                    self.active_player.pieces.keys().__iter__().__next__())

    def player_define(self, **kwargs):
        """默认玩家"""
        attr = {'name': '玩家', **kwargs}
        return PlayerData(**attr)

    def piece_define(self, **kwargs):
        """默认棋子"""
        attr = {'value':1, 'name':'棋子', 'count': NullCount,
                'placeable':False, 'moverules':[], 'occupy':[],
                'squeeze':[], **kwargs}
        return PieceData(**attr)

    def init_pieceattr_group(self):
        return {}

    def init_piece_count(self):
        return {}

    def init_common_pieces(self):
        return []
    
    def init_move_turns(self):
        return [player.name for player in self.init_players()]

    def init_players(self):
        return []

    def init_matr(self):
        return MatrixData((9, 9))

    def init_matr_pts(self):
        return {}
    
    def init_step_func(self):
        return {}
    
    def init_temporary(self):
        return {}
    
    def init_lag_temporary(self):
        return {}
    
    def _init_move_functions(self):
        self.move_manager.add_move_function(0, self.move_nil_nil)
        self.move_manager.add_move_function(1, self.move_nil_self)
        self.move_manager.add_move_function(-1, self.move_nil_other)
        self.move_manager.add_move_function(10, self.move_self_nil)
        self.move_manager.add_move_function(-10, self.move_other_nil)
        self.move_manager.add_move_function(11, self.move_self_self)
        self.move_manager.add_move_function(-11, self.move_other_other)
        self.move_manager.add_move_function(9, self.move_self_other)
        self.move_manager.add_move_function(-9, self.move_other_self)
    
    def _init_matr_functions(self):
        cb = MatrixCallback()
        cb.collection = self.matr.collection
        cb.contains = self.matr.region.contains
        cb.get_valid_value = self.matr.get_valid_value
        cb.get_value = self.matr.get_value
        cb.set_value = self.matr.set_value
        self.move_manager.set_matr_callback(cb)
    
    def _init_clock_manager(self):
        self.clock_manager.set_clocks({player.name: player.time_num
                    for player in self.players.values()})
        if self.move_manager.start_clock: self.clock_manager.start_clock()
        def _clock_func(player_name, tag):
            if tag == "start": self.clock_manager.start_clock(player_name)
            elif tag == "over": self.clock_manager.over_clock(player_name)
            else: raise Exception("clock_func tag error")
        self.move_manager.clock_func = _clock_func

    def _init_move_manager(self):
        self._init_matr_functions()
        self.move_manager.reset(True, False, self.init_matr_pts())
        for name, funcs in self.init_step_func().items():
            self.move_manager.add_step_function(name, *funcs)
        self._init_move_functions()
        self.move_manager.move_site_func = self.move_site

    def _init_players_manager(self):
        self.move_manager.players_manager.init(self.init_players(),
                            self.init_common_pieces(), 
                            self.init_move_turns(),
                            self.init_piece_count())
    
    def move_site(self, player: PlayerData, pt: 'Vector2D'):
        """点击特殊点"""
        pass

    def move_nil_nil(self, player: PlayerData, active_piece: PieceData, pt):
        """在空点落子"""
        pass

    def move_nil_self(self, player: PlayerData, active_piece: PieceData, pt, old_val):
        """选中棋子"""
        pass

    def move_nil_other(self, player: PlayerData, active_piece: PieceData, pt, old_val):
        """落子击杀；选中棋子"""
        pass

    def move_self_nil(self, player: PlayerData, active_piece: PieceData, old_pt, new_pt):
        """移动到; 落子"""
        pass
    
    def move_self_self(self, player: PlayerData, active_piece: PieceData, old_pt, new_pt, new_val):
        """移动到"""
        pass

    def move_self_other(self, player: PlayerData, active_piece: PieceData, old_pt, new_pt, new_val):
        """移子击杀；选中棋子"""
        pass

    def move_other_nil(self, player: PlayerData, active_piece: PieceData, old_pt, new_pt):
        """移动到; 落子"""
        pass

    def move_other_self(self, player: PlayerData, active_piece: PieceData, old_pt, new_pt, new_val):
        """移子击杀；选中棋子"""
        pass

    def move_other_other(self, player: PlayerData, active_piece: PieceData, old_pt, new_pt, new_val):
        """移动到"""
        pass
    
    def turn_active(self, player_name = AutoPlayer, reverse = False):
        """棋手轮换规则"""
        return self.move_manager.turn_active(name = player_name, reverse = reverse)
    
    def move_over(self, player_name: str, tag, *data):
        return self.move_manager.move_over(player_name, tag, data)
    
    def add_move(self, player_name: str, tag, *data):
        return self.move_manager.add_move(player_name, tag, data)
    
    def update_tag_pts(self, player_name: str, pts, tag):
        return self.move_manager.update_tag_pts(player_name, pts, tag)
    
    def remove_tag_pts(self, player_name: str, tag):
        return self.move_manager.remove_tag_pts(player_name, tag)
    
    def add_tag_pts(self, player_name: str, pts, tag):
        return self.move_manager.add_tag_pts(player_name, pts, tag)

    def do_add(self, player_name: str, val, pts):
        """绘制棋盘上的棋子"""
        self.move_over(player_name, 'add', val, pts)
        self.step_add(player_name, val, pts)

    def step_add(self, player_name: str, val, pts):
        """绘制棋盘上的棋子"""
        self.move_manager.add_value_pts(player_name, pts, val)
        self.update_tag_pts(player_name, pts, "Add")

    def reverse_add(self, player_name: str, val, pts):
        """绘制棋盘上的棋子"""
        self.update_tag_pts(player_name, [], "Add")
        self.move_manager.remove_value_pts(val, pts)

    def do_adds(self, player_name: str, pts_map):
        """绘制棋盘上的棋子"""
        self.move_over(player_name, 'adds', pts_map)
        self.step_adds(player_name, pts_map)

    def step_adds(self, player_name: str, pts_map):
        """绘制棋盘上的棋子"""
        self.move_manager.pts_add(pts_map)
        self.update_tag_pts(player_name, sum(pts_map.values(), []), "Add")

    def reverse_adds(self, player_name: str, pts_map):
        """绘制棋盘上的棋子"""
        self.update_tag_pts(player_name, [], "Add")
        self.move_manager.pts_remove(sum(pts_map.values(), []))

    def do_move(self, player_name: str, val, links):
        self.step_move(player_name, val, links)
        self.move_over(player_name, 'move', val, links)
    
    def step_move(self, player_name: str, val, links):
        self.move_manager.links_move(links)
        self.update_tag_pts(player_name, [ps[-1] for ps in links], "Move")
    
    def reverse_move(self, player_name: str, val, links):
        self.update_tag_pts(player_name, [], "Move")
        new_links = [tuple(reversed(link)) for link in links[::-1]]
        self.move_manager.links_move(new_links)

    def do_kill(self, player_name: str, val, new_val, links):
        """绘制棋盘上的棋子"""
        self.step_kill(player_name, val, new_val, links)
        self.move_over(player_name, 'kill', val, new_val, links)

    def step_kill(self, player_name: str, val, new_val, links):
        """绘制棋盘上的棋子"""
        newpts = [pts[-1] for pts in links]
        self.move_manager.remove_value_pts(new_val, newpts)
        self.move_manager.links_move(links)
        self.update_tag_pts(player_name, newpts, "Move")

    def reverse_kill(self, player_name: str, val, new_val, links):
        """绘制棋盘上的棋子"""
        self.update_tag_pts(player_name, [], "Move")
        new_links = [tuple(reversed(link)) for link in links[::-1]]
        oldpts = [pts[0] for pts in new_links]
        self.move_manager.links_move(new_links)
        self.move_manager.add_value_pts(None, oldpts, new_val)

    def do_remove(self, player_name: str, val, pts):
        self.step_remove(player_name, val, pts)
        self.move_over(player_name, 'remove', val, pts)

    def step_remove(self, player_name: str, val, pts):
        self.move_manager.remove_value_pts(val, pts)

    def reverse_remove(self, player_name: str, val, pts):
        self.update_tag_pts(player_name, [], "Add")
        self.move_manager.add_value_pts(player_name, pts, val)

    def do_change(self, player_name: str, val, new_val, pts):
        """绘制棋盘上的棋子"""
        self.step_change(player_name, new_val, val, pts)
        self.move_over(player_name, 'change', new_val, val, pts)

    def step_change(self, player_name: str, old_val, val, pts):
        """绘制棋盘上的棋子"""
        self.move_manager.change_value_pts(val, pts)
        self.update_tag_pts(player_name, pts, "Change")

    def reverse_change(self, player_name: str, old_val, val, pts):
        """绘制棋盘上的棋子"""
        self.move_manager.change_value_pts(old_val, pts)

    def do_game_over(self, player_name: str, tag, single = False):
        self.move_manager.do_game_over(player_name, tag, single)

    def do_pass(self, player_name: str):
        """围棋的虚招，或不限手数的游戏结束本回合行棋"""
        self.move_manager.do_pass(self, player_name, True)

    def call_signal(self, key, *args):
        if key in ['active_player', 'ask_retract',
                   'be_asked_retract', "add_player",
                   'agree_retract','remove_player',
                   "give_up", "active_piece",
                   "info_piece", "swap_player", 
                   "information", "swap_pieces"]:
            self.move_manager.players_manager.call_signal(key, args)
        elif key in ["add_tag_pts", "update_tag_pts",
                "remove_tag_pts", "game_over", "game_start",
                "add", "change", "remove", "swap", "move",
                "update_symbol", "remove_symbol", "clear_symbol"]:
            self.move_manager.call_signal(key, args)
        elif key in ["time_stop", "time_start",
                   "time_running", "time_over"]:
            self.clock_manager.call_signal(key, args)

    def set_signal(self, key, func):
        if key in ['active_player', 'ask_retract',
                   'be_asked_retract', "add_player",
                   'agree_retract','remove_player',
                   "give_up", "active_piece",
                   "info_piece", "swap_player", 
                   "information", "swap_pieces"]:
            self.move_manager.players_manager.set_signal(key, func)
        elif key in ["add_tag_pts", "update_tag_pts",
                "remove_tag_pts", "game_over", "game_start",
                "add", "change", "remove", "swap", "move",
                "update_symbol", "remove_symbol", "clear_symbol"]:
            self.move_manager.set_signal(key, func)
        elif key in ["time_stop", "time_start",
                   "time_running", "time_over"]:
            self.clock_manager.set_signal(key, func)

    def _get_game_data(self, current = True):
        """保存游戏"""
        data = {}
        data['matr'] = self.matr.array2d
        data['over'] = self.move_manager.is_over
        if current:
            data['history'] = self.move_manager.history.simplify_history().to_json()
        else:
            data['history'] = self.move_manager.history.to_json()
        data['temporary'] = self.temporary
        data['lag_temporary'] = self.lag_temporary
        return data
    
    def get_game_data(self):
        """保存游戏"""
        return self._get_game_data(current = False)
    
    def get_current_game_data(self):
        """保存游戏"""
        return self._get_game_data(current = True)
    
    def load_data(self, data):
        self.matr.set_array2d(data['matr'])
        self.move_manager.is_over = data['over']
        self.move_manager.set_history(MoveHistory.from_json(data['history'], False))
        self.temporary = data['temporary']
        self.lag_temporary = data['lag_temporary']
