
from .matrixData import MatrixP, Vector2D
from .until import (GenericSignal, ClockStrSignals,
                    MoveRuleEnum, GameOverEnum, PieceTagEnum,
                    History, MoveNode, ClockManager)
from typing import Union


_PtType_ = Union[tuple[int, int], Vector2D]

PieceIntPointsSignals = GenericSignal[int, list[_PtType_]]
PiecePointsSignals = GenericSignal[list[_PtType_]]
PieceTransSignals = GenericSignal[list[list[_PtType_]]]
PlayerSignals = GenericSignal[str]
PlayerIntSignals = GenericSignal[str, int]
Player2Signals = GenericSignal[str, str]
PlayerStrSignals = GenericSignal[str, str]
Player2Piece2Signals = GenericSignal[str, int, str, int]
PlayerPtsTagSignals = GenericSignal[str, list[_PtType_], PieceTagEnum]




class GridData:
    """棋盘属性"""
    __slots__ = ('name', 'matr', 'over', 'history', 'temporary', 'clock')
    def __init__(self, name = '棋盘', matr = None, over = False,
                 history = None, temporary = None,
                 clock_signals: ClockStrSignals = None):
        self.name = name                    # 名称
        self.matr = matr or MatrixP(3)      # 坐标对象
        self.over = over                    # 游戏是否结束
        # 对局历史，对局分为 局(game)、回合(round)、手（move）、步(step)。
        # 手是最基本的操作，一手可以分为多步，每手后进行终局判断。一手棋记录为若干个棋子添加和删除(+,-,+)
        self.history = history or History() # 历史记录，以手为单位进行记录，悔棋会产生分支[]
        self.temporary = temporary or {}    # 临时数据
        self.clock = ClockManager(clock_signals or ClockStrSignals()) # 倒计时

    @property
    def size(self):
        return self.matr.size

    def get_valid_value(self, pt):
        return self.matr.get_valid_value(pt)

    def get_value(self, pt):
        # player可能输入pt为None
        if pt is not None:
            return self.matr.get_value(pt)

    def set_value(self, pt, val, check = True):
        return self.matr.set_value(pt, val, check)

    def value_to_0(self, pt):
        return self.matr.to_0(pt)

    def step_move(self, name, move_data):
        """执行一手操作"""
        self.history.move(name, move_data)

    def add_move(self, name, move_data):
        """执行一手操作"""
        self.history.add_move(name, move_data)

    def retract(self, name)-> list[MoveNode]:
        """全局的撤销最后一手"""
        return self.history.retract(name)

    def step_back(self)-> tuple[str, MoveNode]:
        """返回上一步。返回上一步玩家和撤回的数据"""
        return self.history.back()
    
    def step_forward(self)-> tuple[str, MoveNode]:
        """跳到下一步。返回下一步玩家和下一步的数据"""
        return self.history.forward()

    def set_temporary(self, **kwargs):
        """添加临时数据"""
        self.temporary.update(kwargs)

    def remove_temporary(self, *keys):
        """移除临时数据"""
        for k in keys:
            if k in self.temporary:
                self.temporary.pop(k)

    def set_clock(self, players: list['PlayerData']):
        for player in players:
            self.clock.set_clock(player.name, player.time)




class PieceData:
    """棋子属性"""
    __slots__ = ('value', 'name', 'player', 'count', 'num',
                 'placeable', 'movable', 'occupy', 'squeeze')
    def __init__(self, player, **kwargs):
        self.value = kwargs.get('value', 1)             # 棋子的值
        self.name = kwargs.get('name','棋子')           # 名称
        self.player = player                            # 棋手
        self.count = kwargs.get('count', None)          # 剩余数量
        self.num = 0                                    # 棋盘棋子总数
        self.placeable = kwargs.get('placeable', True)  # 可以放置
        self.movable = kwargs.get('movable', [])        # 可以移动的方式，移动自身、移动击杀，移动对手，移动对手击杀
        self.occupy = kwargs.get('occupy', [])          # 可以落子占位击杀的对象列表
        self.squeeze = kwargs.get('squeeze', [])        # 可以移动占位击杀的对象列表

    def add(self, pts):
        """绘制棋盘上的棋子"""
        n = len(pts)
        if self.count is not None:
            self.count -= n
        self.num += n

    def remove(self, pts):
        """清除棋盘上的棋子"""
        self.num -= len(pts)

    def change(self, pts, n_piece):
        n = len(pts)
        if self.count is not None:
            self.count -= n
        self.num += n
        n_piece.num -= n

    def swap(self, pts_links, n_piece):
        pass
    
    def move(self, pts_links):
        pass
    
    def can_placeable(self):
        return self.placeable and (self.count is None or self.count > 0)

    def can_occupyable(self, val):
        return self.placeable and (
                val in self.occupy or 0 in self.occupy) and (
                self.count is None or self.count > 0)

    def can_squeezable(self, val):
        return val in self.squeeze or 0 in self.squeeze

    def __repr__(self):
        """打印"""
        return 'piece_' + self.name
    


class PlayerData:
    """棋手属性"""
    __slots__ = ('pieces', 'current_pt', 'active', 'name',
                 'time', 'score', 'temporary')
    def __init__(self, **kwargs):
        self.pieces: {int, PieceData} = kwargs.get('pieces', {})    # 棋子 值：棋子
        for piece in self.pieces.values():
            piece.player = self
        self.current_pt: Vector2D = None                # 当前点击的坐标
        self.active: int = None                         # 当前选择的棋子的值
        self.name:str = kwargs.get('name','棋手')       # 名称
        self.score = 0                                  # 得分
        self.temporary = kwargs.get('temporary', {})    # 临时数据


    def reset(self, temporary = None, piece_count = None):
        self.temporary = self.temporary.copy()
        self.temporary.update(temporary or {})
        self.current_pt = None      # 当前点击的坐标
        self.active = None          # 当前选择的棋子的值
        self.score = 0              # 得分
        for piece in self.pieces.values():
            piece.count = piece_count.get(piece.value, None) # 剩余数量
            piece.num = 0           # 棋盘棋子总数

    def get_active(self, val = None):
        """设置当前棋子"""
        self.active = val or self.pieces.keys().__iter__().__next__()
        return self.active

    def clear_current(self):
        """清除临时坐标"""
        self.current_pt = None

    def __repr__(self):
        """打印"""
        return 'player_'+self.name

    def set_temporary(self, **kwargs):
        """添加临时数据"""
        self.temporary.update(kwargs)

    def remove_temporary(self, *keys):
        """移除临时数据"""
        for k in keys:
            if k in self.temporary:
                self.temporary.pop(k)
    
    def has_piece(self, val):
        if val == 0 or val is None:
            return 0
        elif val in self.pieces:
            return 1
        else:
            return -1

    def move_point(self, pt, game: 'GameData'):
        """玩家点击棋盘的行为"""
        new_pt = pt
        new_val = game.grid.get_valid_value(new_pt)
        old_pt = self.current_pt
        old_val = game.grid.get_value(old_pt)
        self.clear_current()
        if old_val in self.pieces:
            piece:PieceData = self.pieces[self.get_active(old_val)]
        elif new_val in self.pieces:
            piece:PieceData = self.pieces[self.get_active(new_val)]
        else:
            piece:PieceData = self.pieces[self.get_active()]
        if old_pt == new_pt:
            game.set_active_pt(piece.player, None)
            return
        match (self.has_piece(old_val), self.has_piece(new_val)):
            case (0, 0):
                piece:PieceData = self.pieces[self.get_active()]
                if piece.can_placeable():
                    game.move_manager.move_nil_nil(self, piece, new_pt)
            case (0, 1):
                piece:PieceData = self.pieces[self.get_active(new_val)]
                if MoveRuleEnum.Move in piece.movable or MoveRuleEnum.Kill in piece.movable:
                    game.move_manager.move_nil_self(self, piece, new_pt)
                    game.set_active_pt(piece.player, new_pt)
            case (0, -1):
                if piece.can_occupyable(new_val):
                    game.move_manager.move_nil_other(self, piece, new_pt, new_val)
                if MoveRuleEnum.Omove in piece.movable or MoveRuleEnum.Okill in piece.movable:
                    game.set_active_pt(piece.player, new_pt)
            case (1, 0):
                if MoveRuleEnum.Move in piece.movable:
                    game.move_manager.move_self_nil(self, piece, new_pt, old_pt)
            case (1, 1):
                game.move_manager.move_nil_self(self, piece, new_pt)
            case (1, -1):
                if MoveRuleEnum.Kill in piece.movable and piece.can_squeezable(new_val):
                    game.move_manager.move_self_other(self, piece, new_pt, new_val, old_pt)
            case (-1, 0):
                if MoveRuleEnum.Omove in piece.movable:
                    game.move_manager.move_other_nil(self, piece, new_pt, old_pt, old_val)
            case (-1, 1):
                if MoveRuleEnum.Okill in piece.movable and \
                            game.player_manager.get_piece(val = old_val).can_squeezable(piece.value):
                    game.move_manager.move_other_self(self, piece, new_pt, old_pt, old_val)
            case (-1, -1):
                game.move_manager.move_nil_other(self, piece, new_pt, new_val)




class MoveManager:
    __slots__ = ('game', 'player_signals',
                 'player_pts_tag_signals', 'step_func',
                 'piece_int_pts_signals', 'piece_pts_signals',
                 'piece_trans_signals', 'reverse_func')
    def __init__(self, game: 'GameData'):
        self.game = game
        self.player_signals = PlayerSignals()
        self.player_pts_tag_signals = PlayerPtsTagSignals()
        self.piece_int_pts_signals = PieceIntPointsSignals()
        self.piece_pts_signals = PiecePointsSignals()
        self.piece_trans_signals = PieceTransSignals()
        # 默认参数
        self.step_func = {}
        self.reverse_func = {}
        self.init_data()

    def init_data(self):
        self.step_func = {}
        self.reverse_func = {}
    
    @property
    def grid(self):
        return self.game.grid
    
    @property
    def matr(self):
        return self.game.grid.matr
    
    @property
    def player_manager(self):
        return self.game.player_manager

    def pass_move(self):
        """围棋的虚招，或不限手数的游戏结束本回合行棋"""
        player = self.game.active_player
        return self._step_pass(player)
    
    def ask_retract(self):
        """悔棋，仅在自己行棋的环节开始，需要对方同意"""
        if not self.game.in_race:
            return
        # 询问是否同意
        self.call_signal('ask_retract', self.game.active_player_name)
        for name in self.game.players.keys():
            if name != self.game.active_player_name:
                self.call_signal('be_asked_retract', name)

    def agree_retract(self, askname):
        """同意对手的悔棋"""
        if not self.game.in_race:
            return
        # 同意后自动撤回一回合
        self.call_signal('agree_retract', askname)
        for node in self.grid.retract(askname):
            for move, data in node.data.items():
                self.reverse_func[move](self.game.players[node.player], *data)
        self.player_manager.set_active(name = node.player)
        self.turn_active(reverse = True, player = self.game.players[node.player])

    def swap_piece_pts(self, pts_links):
        """交换棋子"""
        for pt1, pt2 in pts_links:
            val1,val2 = self.grid.get_value(pt1), self.grid.get_value(pt2)
            self.grid.set_value(pt1, val2, True)
            self.grid.set_value(pt2, val1, True)
        if val1 and val2:
            self.call_piece_signal('swap', pts_links)
            return
        if val1:
            self.call_piece_signal('move', pts_links)
        else:
            npts_links = [(p2,p1) for p1,p2 in pts_links]
            self.call_piece_signal('move', npts_links)

    def move_piece_pts(self, pts_links):
        """移动棋子"""
        move_links = []
        moved_pts_vals = []
        move_pts = []
        remove_pts = []
        for link in pts_links:
            remove_pt, pt = link[0], link[-1]
            val1 = self.grid.get_value(remove_pt)
            val2 = self.grid.get_value(pt)
            if not val1 and not val2: continue
            if val1:
                move_links.append(link)
                moved_pts_vals.append((pt, val1, val2))
                move_pts.append(remove_pt)
            else:
                remove_pts.append(pt)
        self.call_piece_signal('move', move_links)
        for pt in move_pts:
            self.grid.value_to_0(pt)
        for pt, val1, val2 in moved_pts_vals:
            self.grid.set_value(pt, val1, True)
            if pt not in move_pts and val2:
                self.game.get_piece(val = val2).num -= 1
        self.remove_pts_piece(remove_pts)

    def remove_pts_piece(self, pts):
        """清除棋盘上的棋子"""
        temp = {}
        for pt in pts:
            piece = self.game.get_piece(pt = pt)
            temp.setdefault(piece, []).append(pt)
            self.grid.value_to_0(pt)
        for piece,pts in temp.items():
            if piece:
                piece.remove(pts)
                self.call_piece_signal('remove', pts)

    def remove_piece_pts(self, val, pts):
        """清除棋盘上的棋子"""
        if (piece := self.game.get_piece(val = val)):
            piece.remove(pts)
            for pt in pts:
                self.grid.value_to_0(pt)
            self.call_piece_signal('remove', pts)

    def change_pts_piece(self, val, pts):
        """改变多点为棋子val"""
        n_piece = self.game.get_piece(val = val)
        if not n_piece:
            self.remove_pts_piece(pts)
            return
        temp = {}
        for pt in pts:
            piece = self.game.get_piece(pt = pt)
            temp.setdefault(piece, []).append(pt)
            self.grid.set_value(pt, val, True)
        for piece,pts in temp.items():
            if piece:
                piece.remove(pts)
                n_piece.add(pts)
                self.call_piece_signal('change', n_piece.value, pts)
            else:
                n_piece.add(pts)
                self.call_piece_signal('add', n_piece.value, pts)

    def add_pts_piece(self, player, pts, val = None):
        """绘制棋盘上的棋子"""
        if val is None:
            val = player.active
        if val == 0:
            self.remove_pts_piece(pts)
            return
        for pt in pts:
            self.grid.set_value(pt, val, True)
        self.player_manager.pieces[val].add(pts)
        self.call_piece_signal('add', val, pts)

    def add_tag_pts(self, player, pts, tag:PieceTagEnum):
        """标记棋子"""
        self.player_pts_tag_signals.call('add_tag_pts', player.name, pts, tag)
    
    def update_tag_pts(self, player, pts, tag:PieceTagEnum):
        """标记棋子"""
        self.player_pts_tag_signals.call('update_tag_pts', player.name, pts, tag)
    
    def remove_tag_pts(self, player, tag:PieceTagEnum):
        """标记棋子"""
        self.player_pts_tag_signals.call('remove_tag_pts', player.name, tag)

    def move_over(self, player, tag, *data):
        """记录行棋"""
        self.grid.step_move(player.name, {tag: data})
    
    def add_move(self, player, tag, *data):
        """添加行棋"""
        self.grid.add_move(player.name, {tag: data})

    def step_back(self)-> tuple[str, MoveNode]:
        """返回上一步。返回上一步玩家和撤回的数据"""
        prevname, node = self.grid.step_back()
        for move, data in reversed(node.data.items()):
            self.reverse_func[move](self.game.players[node.player], *data)
        self.player_manager.set_active(name = prevname or self.player_manager.turns[-1])
        self.turn_active(player = self.game.active_player)
    
    def step_forward(self)-> tuple[str, MoveNode]:
        """跳到下一步。返回下一步玩家和下一步的数据"""
        name, node = self.grid.step_forward()
        if name:
            for move,data in node.data.items():
                self.step_func[move](self.game.players[name], *data)
            self.player_manager.set_active(name = name)

    def call_signal(self, key, *args):
        if key in ['ask_retract', 'agree_retract',
                   'pass_move', 'be_asked_retract']:
            self.player_signals.call(key, *args)
        elif key in ['add_tag_pts', 'update_tag_pts', 'remove_tag_pts']:
            self.player_pts_tag_signals.call(key, *args)
    
    def set_signal(self, key, func):
        if key in ['ask_retract', 'agree_retract',
                   'pass_move', 'be_asked_retract']:
            self.player_signals.connect(key, func)
        elif key in ['add_tag_pts', 'update_tag_pts', 'remove_tag_pts']:
            self.player_pts_tag_signals.connect(key, func)

    def call_piece_signal(self, key, *args):
        if key in ['change', 'add']:
            self.piece_int_pts_signals.call(key, *args)
        elif key == 'remove':
            self.piece_pts_signals.call(key, *args)
        elif key in ['swap', 'move']:
            self.piece_trans_signals.call(key, *args)
    
    def set_piece_signal(self, key, func):
        if key in ['change', 'add']:
            self.piece_int_pts_signals.connect(key, func)
        elif key == 'remove':
            self.piece_pts_signals.connect(key, func)
        elif key in ['swap', 'move']:
            self.piece_trans_signals.connect(key, func)

    def move_nil_nil(self, player, active_piece, new_pt):
        """在空点落子"""
        self.update_tag_pts(player, [], PieceTagEnum.Add)

    def move_nil_self(self, player, active_piece, new_pt):
        """选中棋子"""
        self.update_tag_pts(player, [], PieceTagEnum.Add)

    def move_nil_other(self, player, active_piece, new_pt, new_val):
        """落子击杀；选中棋子"""
        self.update_tag_pts(player, [], PieceTagEnum.Add)

    def move_self_nil(self, player, active_piece, new_pt, old_pt):
        """移动到; 落子"""
        self.update_tag_pts(player, [], PieceTagEnum.Add)

    def move_self_other(self, player, active_piece, new_pt, new_val, old_pt):
        """移子击杀；选中棋子"""
        self.update_tag_pts(player, [], PieceTagEnum.Add)

    def move_other_nil(self, player, active_piece, new_pt, old_pt, old_val):
        """移动到; 落子"""
        self.update_tag_pts(player, [], PieceTagEnum.Add)

    def move_other_self(self, player, active_piece, new_pt, old_pt, old_val):
        """移子击杀；选中棋子"""
        self.update_tag_pts(player, [], PieceTagEnum.Add)

    def move_button(self, player, pt):
        """移子击杀；选中棋子"""
        self.update_tag_pts(player, [], PieceTagEnum.Add)

    def _step_pass(self, player):
        """围棋的虚招，或不限手数的游戏结束本回合行棋"""
        self.step_pass(player)
        if self.grid.history.prev_player != player.name and \
                self.grid.history.prev_data.get('pass', False):
            self.game_over(player, GameOverEnum.Stop)
        self.move_over(player, 'pass')
        pass

    def step_pass(self, player):
        """围棋的虚招，或不限手数的游戏结束本回合行棋"""
        self.turn_active(player = player)

    def reverse_pass(self, player):
        """围棋的虚招，或不限手数的游戏结束本回合行棋"""
        self.turn_active(player = player, reverse = True)

    def _step_add(self, player, val, pts):
        """绘制棋盘上的棋子"""
        self.step_add(player, val, pts)
        self.move_over(player, 'add', val, pts)

    def step_add(self, player, val, pts):
        """绘制棋盘上的棋子"""
        self.add_pts_piece(player, pts, val = val)
        self.update_tag_pts(player, pts, PieceTagEnum.Add)

    def reverse_add(self, player, val, pts):
        """绘制棋盘上的棋子"""
        self.update_tag_pts(player, [], PieceTagEnum.Add)
        self.remove_piece_pts(val, pts)
    
    def _step_move(self, player, val, links):
        self.step_move(player, val, links)
        self.move_over(player, 'move', val, links)
    
    def step_move(self, player, val, links):
        self.move_piece_pts(links)
        self.update_tag_pts(player, [ps[-1] for ps in links], PieceTagEnum.Move)
    
    def reverse_move(self, player, val, links):
        self.update_tag_pts(player, [], PieceTagEnum.Move)
        new_links = [tuple(reversed(link)) for link in links[::-1]]
        self.move_piece_pts(new_links)

    def _step_kill(self, player, val, new_val, links):
        """绘制棋盘上的棋子"""
        self.step_kill(player, val, new_val, links)
        self.move_over(player, 'kill', val, new_val, links)

    def step_kill(self, player, val, new_val, links):
        """绘制棋盘上的棋子"""
        newpts = [pts[-1] for pts in links]
        self.remove_piece_pts(new_val, newpts)
        self.move_piece_pts(links)
        self.update_tag_pts(player, newpts, PieceTagEnum.Move)

    def reverse_kill(self, player, val, new_val, links):
        """绘制棋盘上的棋子"""
        self.update_tag_pts(player, [], PieceTagEnum.Move)
        new_links = [tuple(reversed(link)) for link in links[::-1]]
        oldpts = [pts[0] for pts in new_links]
        self.move_piece_pts(new_links)
        self.add_pts_piece(None, oldpts, new_val)

    def _step_remove(self, player, val, pts):
        self.step_remove(player, val, pts)
        self.move_over(player, 'remove', val, pts)

    def step_remove(self, player, val, pts):
        self.remove_piece_pts(val, pts)

    def reverse_remove(self, player, val, pts):
        self.update_tag_pts(player, [], PieceTagEnum.Add)
        self.add_pts_piece(player, pts, val = val)

    def _step_change(self, player, val, new_val, pts):
        """绘制棋盘上的棋子"""
        self.step_change(player, val, new_val, pts)
        self.move_over(player, 'change', val, new_val, pts)

    def step_change(self, player, val, old_val, pts):
        """绘制棋盘上的棋子"""
        self.change_pts_piece(val, pts)
        self.update_tag_pts(player, pts, PieceTagEnum.Change)

    def reverse_change(self, player, val, old_val, pts):
        """绘制棋盘上的棋子"""
        self.change_pts_piece(old_val, pts)

    def game_over(self, player, tag):
        return self.game.game_over(player, tag)

    def turn_active(self, reverse = False, player = None):
        return self.game.player_manager.turn_active(reverse = reverse, player = player)




class PlayerManager:
    __slots__ = ('game', 'players', 'pieces',
                  'turns', 'active', 'in_turns',
                 'player_signals', 'player_int_signals', 
                 'player_2_signals', 'player_piece_2_signals',
                 'pieceattr_group', 'player_group',
                 'player_temporary', 'piece_count')
    def __init__(self, game: 'GameData', **kwargs):
        self.game = game
        # 玩家对象 玩家名称：玩家对象
        self.players: dict[str, PlayerData] = {}
        # 值：对象
        self.pieces: dict[int, PieceData] = {}
        # 轮流落子模式的棋手顺序，为棋手名称序列
        self.turns = []
        self.in_turns = True
        # 当前活动的棋手，在turns中的序号
        self.active = 0
        self.player_signals = PlayerSignals()
        self.player_int_signals = PlayerIntSignals()
        self.player_2_signals = Player2Signals()
        self.player_piece_2_signals = Player2Piece2Signals()
        # 默认参数
        self.pieceattr_group = kwargs.get('pieceattr_group', {})
        self.player_group = kwargs.get('player_group', {})
        self.player_temporary = kwargs.get('player_temporary', {})
        self.piece_count = kwargs.get('piece_count', {})
        self.begin()

    def begin(self):
        self.pieceattr_group.update(self.init_pieceattr_group())
        self.player_group.update(self.init_player_group())
        self.player_temporary.update(self.init_player_temporary())
        self.piece_count.update(self.init_piece_count())
        self.add_players(**self.player_group)
        for player in self.player_group.values():
            player.temporary.update(self.player_temporary.get(player.name, {}))
            for piece in player.pieces.values():
                piece.count = self.piece_count.get(piece.value, piece.count)

    def rebegin(self):
        self.active = 0
        self.in_turns = True
        self.player_temporary.update(self.init_player_temporary())
        self.piece_count.update(self.init_piece_count())
        for player in self.player_group.values():
            player.reset(self.player_temporary, self.piece_count)

    def init_pieceattr_group(self):
        return {}

    def init_player_group(self):
        return {}

    def init_player_temporary(self):
        return {}

    def init_piece_count(self):
        return {}
    
    @property
    def grid(self):
        return self.game.grid
    
    def set_active_piece(self, val = None):
        """设置当前棋子"""
        self.pieces[val].player.get_active(val)
        self.call_signal('active_piece', self.pieces[val].player.name, val)

    def set_active(self, val = None, name = None, player = None):
        """设置当前棋手"""
        name = self.get_player(val = val, name = name, player = player).name
        if not name:
            return
        if self.active_player.name == name:
            return
        self.active = self.turns.index(name)
        active_player = self.active_player
        for p in self.players.values():
            if p != active_player:
                p.clear_current()
        self.call_signal('active_player', active_player.name)
        self.call_signal('info_piece', active_player.name,
                    active_player.pieces.keys().__iter__().__next__())

    def get_player(self, val = None, name = None, player = None):
        """获取棋手对象"""
        return player or self.players.get(name, None) or self.pieces.get(val, None).player

    def get_piece(self, pt = None, val = None, piece = None) -> PieceData:
        """获取棋子"""
        return piece or self.pieces.get(val or self.grid.get_value(pt), None)

    @property
    def active_player(self):
        """获取当前棋手"""
        return self.players[self.turns[self.active]]
    
    @property
    def active_player_name(self):
        return self.active_player.name
    
    def add_player(self, name = None, player = None):
        """加入棋手"""
        if not name:
            name = player.name
        if name not in self.players:
            self.turns.append(name)
        self.players[name] = player
        self.add_player_pieces(player = player)
        self.call_signal('add_player', name)
    
    def add_players(self, **players):
        for name, player in players.items():
            self.add_player(name = name, player = player)

    def remove_player(self, name = None):
        """移除棋手，并给移除其在轮换规则中的位置"""
        self.turns = [v for v in self.turns if v != name]
        for val in self.players[name].pieces:
            self.pieces.pop(val)
        self.players.pop(name)
        self.call_signal('remove_player', name)

    def add_player_pieces(self, player = None):
        """加入棋子"""
        self.pieces.update(player.pieces)
        for piece in player.pieces.values():
            piece.player = player

    def remove_piece(self, val = None, deep = True):
        """移除棋子对象，并给移除其在轮换规则中的位置"""
        if deep:
            self.pieces[val].player.pieces.pop(val)
        self.pieces.pop(val)

    def swap_player(self, name1 = None, name2 = None):
        """交换棋手，交换棋手的名称"""
        player1 = self.players[name1]
        player2 = self.players[name2]
        player1.name,player2.name = name2,name1
        player1.time,player2.time = player2.time,player1.time
        player1.score,player2.score = player2.score,player1.score
        self.players[name1],self.players[name2] = player2,player1
        self.call_signal('swap_player', name1, name2)

    def swap_pieces(self, val1 = None, val2 = None):
        """交换棋手，交换棋子的所属"""
        piece1 = self.pieces[val1]
        piece2 = self.pieces[val2]
        player1 = piece1.player
        player2 = piece2.player
        piece1.player,piece2.player = player2,player1
        player1.pop(val1); player1[val2] = piece2
        player2.pop(val2); player2[val1] = piece1
        self.call_signal.call('swap_player', player1.name, piece1.value,
                              player2.name, piece2.value)

    def on_player(self, name):
        """设置当前棋手为1棋手"""
        self.in_turns = False
        self.set_active(name = name)
    
    def on_turns(self):
        """轮换执棋"""
        self.in_turns = True

    def get_turn_player(self, reverse = False, player = None):
        """棋手轮换规则"""
        active = self.turns.index(player.name) if player else self.active
        if reverse:
            return active-1 if active>0 else len(self.turns)-1
        return active+1 if active<len(self.turns)-1 else 0

    def turn_player(self, reverse = False, player = None):
        """棋手轮换规则"""
        self.active = self.get_turn_player(reverse = reverse, player = player)
        self.call_signal('active_player', self.active_player_name)
        self.call_signal('info_piece', self.active_player.name,
                    self.active_player.pieces.keys().__iter__().__next__())

    def turn_active(self, reverse = False, player = None):
        """棋手轮换规则"""
        if self.game.in_race and not self.in_turns:
            return
        self.turn_player(reverse = reverse, player = player)

    def player_define(self, **kwargs):
        """默认玩家"""
        attr = {'name': '玩家', **kwargs}
        return PlayerData(**attr)

    def piece_define(self, player, **kwargs):
        """默认棋子"""
        attr = {'value':1, 'name':'棋子', 'count':None, 'placeable':False, 
                'movable':[], 'occupy':[], 'squeeze':[],
                **kwargs}
        return PieceData(player, **attr)
    
    def call_signal(self, key, *args):
        if key in ['active_player']:
            self.player_signals.call(key, *args)
        elif key in ['active_piece', 'info_piece']:
            self.player_int_signals.call(key, *args)
        elif key in ['swap_player']:
            self.player_2_signals.call(key, *args)
        elif key in ['swap_pieces']:
            self.player_piece_2_signals.call(key, *args)
    
    def set_signal(self, key, func):
        if key in ['active_player']:
            self.player_signals.connect(key, func)
        elif key in ['active_piece', 'info_piece']:
            self.player_int_signals.connect(key, func)
        elif key in ['swap_player']:
            self.player_2_signals.connect(key, func)
        elif key in ['swap_pieces']:
            self.player_piece_2_signals.connect(key, func)





class GameData:
    """
    游戏的基本数据常量
    """
    __slots__ = ('grid', 'start_clock', 'in_race',
                 'move_manager', 'player_manager', 
                 'default_piece_pts', 'player_signals', 
                 'player_int_signals', 'clock_signals',
                 'player_str_signals')
    def __init__(self):
        # 棋盘对象
        self.grid: GridData = None
        self.start_clock = False
        self.in_race = False
        self.move_manager:MoveManager = None
        self.player_manager:PlayerManager = None
        # 默认棋子，值:棋子坐标
        self.default_piece_pts = {}
        # 绑定事件
        self.player_signals = PlayerSignals()
        self.player_int_signals = PlayerIntSignals()
        self.player_str_signals = PlayerStrSignals()
        self.clock_signals = ClockStrSignals()
        # 默认参数
        self.begin()

    @property
    def matr(self):
        return self.grid.matr

    def begin(self):
        self.in_race = True
        self.move_manager = self.init_move_manager()
        self.player_manager = self.init_player_manager()
        self.set_borad()
        self.set_matr_default_piece_pts()

    def rebegin(self):
        self.in_race = True
        self.reset_borad()
        self.player_manager.rebegin()
        self.set_matr_default_piece_pts()

    def after_begin(self):
        self.call_signal('active_player', self.active_player_name)
        self.call_signal('info_piece', self.active_player.name,
                    self.active_player.pieces.keys().__iter__().__next__())

    def init_gridattr(self):
        return {}

    def init_move_manager(self):
        return MoveManager(self)

    def init_player_manager(self):
        return PlayerManager(self)

    def set_borad(self):
        self.grid = GridData(clock_signals = self.clock_signals,
                             **self.init_gridattr())
        if self.start_clock and self.in_race:
            self.grid.clock.start_clock()

    def reset_borad(self):
        if self.start_clock:
            self.grid.clock.over_clock()
        self.set_borad()

    def get_edges(self):
        """获取边缘点"""
        return self.matr.get_edges()

    def turn_active(self, reverse = False, player = None):
        """棋手轮换规则"""
        return self.player_manager.turn_active(reverse = reverse, player = player)

    def move_point(self, pt = None, name = None):
        """点击棋盘 点击组合：己方、对方、空白"""
        # print(pt)
        if self.grid.over and self.in_race:
            return
        if pt not in self.matr.region:
            return
        player = self.player_manager.players.get(name, None) or self.player_manager.active_player
        player.move_point(pt, self)

    def move_site(self, pt = None, name = None):
        """点击非格点行为"""
        if self.grid.over and self.in_race:
            return
        player = self.player_manager.players.get(name, None) or self.player_manager.active_player
        self.move_manager.move_button(player, pt)

    def set_matr_default_piece_pts(self):
        """设置默认棋子"""
        for val,pts in self.default_piece_pts.items():
            for pt in pts:
                self.grid.set_value(pt, val, True)

    def add_default_piece_pts(self):
        """设置默认棋子"""
        for val, pts in self.matr.collection().items():
            if val in [0, None]:
                continue
            self.move_manager.add_pts_piece(None, pts, val)
    
    def game_over(self, player, tag = GameOverEnum.Going):
        """结束游戏, 弹窗提醒, 停止计时"""
        if player and tag != GameOverEnum.Going and self.in_race:
            if self.start_clock:
                self.grid.clock.over_clock(player.name)
            self.grid.over = True
            self.call_signal('game_over', player.name, tag)

    def on_race(self):
        """比赛"""
        self.in_race = True
        if self.start_clock:
            self.grid.clock.start_clock()

    def out_race(self):
        """打谱"""
        if self.start_clock:
            self.grid.clock.over_clock()
        self.in_race = False

    def give_up(self, player = None):
        """认输"""
        if not self.in_race:
            return
        if player is None:
            player = self.player_manager.active_player
        self.call_signal('give_up', player.name)
        self.game_over(player, tag = GameOverEnum.Lose)

    def show_information(self, player = None, info = ''):
        """发送消息"""
        if player is None:
            player = self.player_manager.active_player
        self.call_signal('information', player.name, info)
    
    def set_active_pt(self, player:PlayerData, pt):
        player.current_pt = pt
        self.move_manager.update_tag_pts(player, [pt] if pt else [], PieceTagEnum.Active)
    
    def call_signal(self, key, *args):
        if key in ['game_begin', 'remove_player', 'give_up']:
            self.player_signals.call(key, *args)
        elif key in ['game_over']:
            self.player_int_signals.call(key, *args)
        elif key in ['information']:
            self.player_str_signals.call(key, *args)
        elif key in ['ask_retract', 'agree_retract',
                   'pass_move', 'be_asked_retract', 
                   'add_tag_pts', 'update_tag_pts',
                   'remove_tag_pts']:
            self.move_manager.call_signal(key, *args)
        elif key in ['active_player', 'active_piece',
                   'swap_player', 'swap_pieces', 'info_piece']:
            self.player_manager.call_signal(key, *args)

    def set_signal(self, key, func):
        if key in ['game_begin', 'remove_player', 'give_up']:
            self.player_signals.connect(key, func)
        elif key in ['game_over']:
            self.player_int_signals.connect(key, func)
        elif key in ['information']:
            self.player_str_signals.connect(key, func)
        elif key in ['ask_retract', 'agree_retract',
                   'pass_move', 'be_asked_retract',
                   'add_tag_pts', 'update_tag_pts',
                   'remove_tag_pts']:
            self.move_manager.set_signal(key, func)
        elif key in ['active_player', 'active_piece',
                   'swap_player', 'swap_pieces', 'info_piece']:
            self.player_manager.set_signal(key, func)

    def call_piece_signal(self, key, *args):
        if key in ['add', 'remove', 
                   'change', 'swap', 'move']:
            self.move_manager.call_piece_signal(key, *args)

    def set_piece_signal(self, key, func):
        if key in ['add', 'remove', 
                   'change', 'swap', 'move']:
            self.move_manager.set_piece_signal(key, func)

    @property
    def pieces(self):
        return self.player_manager.pieces
    
    @property
    def players(self):
        return self.player_manager.players

    def get_piece(self, pt = None, val = None, piece = None) -> PieceData:
        """获取棋子"""
        return self.player_manager.get_piece(pt = pt, val = val, piece = piece)

    @property
    def active_player(self):
        """获取当前棋手"""
        return self.player_manager.active_player
    
    @property
    def active_player_name(self):
        return self.player_manager.active_player.name