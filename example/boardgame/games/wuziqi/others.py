
from .wuziqi import *



class Game_六连棋(Game_五子棋):
    """六连棋"""
    def init_move_turns(self):
        self.players_manager.move_turns.active_turn = 1
        return [player.name for player in self.init_players() for _ in range(2)]
    
    def init_matr(self):
        return MatrixData((15, 15), structure = 8)

    def test_win(self, player: PlayerData, pt):
        """判断是否存在连子"""
        orows = self.in_row(pt, n = 6)
        if bool(rows := matrixgrid.flatten_as_vector(orows)):
            self.update_tag_pts(player.name, rows, "Win")
            self.do_game_over(player.name, GameOverEnum.Win)
        self.turn_active()


class App_六连棋(App_五子棋):
    """六连棋游戏规则"""
    def init_rule(self):
        self.name = '六连棋'
        return Game_六连棋()



class Game_斜胜棋(GameBlackWhite):
    """斜胜棋"""
    def init_pieceattr_group(self):
        return {"placeable": True,
                'moverules': [MoveRuleEnum.Move, MoveRuleEnum.Kill]}

    def init_matr_pts(self):
        return { 1: [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
                2: [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]}

    def init_matr(self):
        return MatrixData((5, 5), structure = 4)

    def init_step_func(self):
        return {'move': (self.step_move, self.reverse_move),
                'kill': (self.step_kill, self.reverse_kill)}
    
    def _game_win(self, player: PlayerData, pts):
        self.update_tag_pts(player.name, pts, "Win")
        self.do_game_over(player.name, GameOverEnum.Win)
        if pts:
            self.turn_active()

    def test_win(self, player: PlayerData, piece: PieceData, pt):
        """模拟并测试该点落子后的情况"""
        if self.players_manager.pieces[3 - piece.value].num == 0:
            return self._game_win(player, [])
        pts1 = self.matr.search_value_axis_pairs(pt, 3, piece.value, True)
        pts2 = self.matr.search_value_axis_pairs(pt, 4, piece.value, True)
        pts = pts1 if len(pts1) > len(pts2) else pts2
        if len(pts) == piece.num and not self.move_manager.is_over:
            if piece.num >= 4:
                return self._game_win(player, pts)
            elif piece.num >= 2:
                for p in pts:
                    if p[0] in [0, 4]:
                        return self._game_win(player, pts)
            else:
                for p in pts:
                    if p[0] in [0, 4] and p[1] in [0, 4]:
                        return self._game_win(player, pts)
        self.turn_active()

    def move_self_nil(self, player: PlayerData, active_piece: 'PieceData', old_pt, new_pt):
        if old_pt not in self.matr.get_point_nbrs(new_pt):
            return self.update_tag_pts(player.name, [], "Move")
        self.do_move(player.name, active_piece.value, [(old_pt, new_pt)])
        self.test_win(player, active_piece, new_pt)

    def move_self_other(self, player: PlayerData, active_piece: 'PieceData', old_pt, new_pt, new_val):
        if old_pt not in self.matr.get_point_nbrs(new_pt):
            return self.update_tag_pts(player.name, [], "Move")
        self.do_kill(player.name, active_piece.value, new_val, [(old_pt, new_pt)])
        if (p := self.matr.search_value(new_val)):
            if (q := p.__iter__().__next__()):
                piece = self.players_manager.pieces[new_val]
                self.test_win(piece.player, piece, q)
        self.test_win(player, active_piece, new_pt)




class App_斜胜棋(AppBlackWhite):
    """斜胜棋游戏规则"""
    def init_rule(self):
        self.name = '斜胜棋'
        return Game_斜胜棋()
    
    def grid_attr(self):
        return {'size': (5, 5), 'canvas_size': (750, 750),
                'padding': (130, 130), 'is_net': False}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null, 'show_piece_index': True}



class Game_三六九棋(Game_五子棋):
    """三六九棋"""
    def init_temporary(self):
        return {'黑':{'rows3': [], 'rows6': [], 'rows9': []},
                '白':{'rows3': [], 'rows6': [], 'rows9': []}}
    
    def init_matr(self):
        return MatrixData((9, 9), structure = 8)

    def compute_score(self, player: PlayerData, pt, n):
        """计算得分"""
        rows = self.in_row(pt, n = n)
        for row in rows:
            if len(row) != n:
                continue
            flag = False
            for _row in self.temporary[player.name][f'rows{n}']:
                if row[0] in _row and row[1] in _row:
                    flag = True
                    break
            if not flag:
                self.temporary[player.name][f'rows{n}'].append(row)
                self.update_tag_pts(player.name, row, "Win")
                player.score += n

    def test_win(self, player: PlayerData, pt):
        """判断是否存在连子"""
        self.compute_score(player, pt, 3)
        self.compute_score(player, pt, 6)
        self.compute_score(player, pt, 9)
        if player.name == '黑' and player.pieces[1].num >= 41:
            other = self.players_manager.get_player('白')
            if player.score >= other.score:
                self.do_game_over(player.name, GameOverEnum.Win)
        self.turn_active()


class App_三六九棋(AppBlackWhite):
    """三六九棋游戏规则"""
    def init_rule(self):
        self.name = '三六九棋'
        return Game_三六九棋()
    
    def grid_attr(self):
        return {'size': (9, 9), 'canvas_size': (750, 750),
                'padding': (80, 80), 'is_net': True}
    
    def canvas_attr(self):
        return {'star_show': True, 'show_piece_index': True}






class Game_墨棋(Game_五子棋):
    """墨棋"""
    def init_temporary(self):
        return {'steps' : 0}

    def init_matr(self):
        return MatrixData((19, 19), structure = 8)

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        if self.temporary['steps'] < 2:
            self.temporary['steps'] += 1
        else:
            if not self.move_test(new_pt, active_piece.value):
                return
        super().move_nil_nil(player, active_piece, new_pt)

    def move_test(self, pt, value):
        values = []
        for i in range(1, 5):
            clls = self.matr.collection(self.matr.search_endvalue_axis_pairs(pt, i, -128, True))
            s = len(clls.get(1, [])) + len(clls.get(2, []))*2
            if s == 0:
                continue
            elif s%2 == 0:
                values.append(2)
            else:
                values.append(1)
        if value in values:
            return True
        return False



class App_墨棋(AppBlackWhite):
    """墨棋游戏规则"""
    def init_rule(self):
        self.name = '墨棋'
        return Game_墨棋()
    
    def grid_attr(self):
        return {'size': (19, 19), 'canvas_size': (750, 750),
                'padding': (60, 60), 'is_net': True}
    
    def canvas_attr(self):
        return {'star_show': True, 'show_piece_index': True}
