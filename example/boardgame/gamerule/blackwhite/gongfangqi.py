from .blackwhite import PlayerBlackWhite, AppBlackWhite
from ...gridrule import *



class Move_攻防棋(MoveManager):
    """攻防棋"""
    def init_data(self):
        self.step_func = {'move': self.step_move}
        self.reverse_func = {'move': self.reverse_move}

    def test_win(self, player, pt):
        if pt.y == 8 if player.name == '黑' else 0:
            self._step_game_over(player, GameOverEnum.Win)
        self.turn_active(player = player)

    def move_self_nil(self, player: 'PlayerData', active_piece, old_pt, new_pt):
        """在空点落子"""
        value = active_piece.value
        if not self.move_test(value, old_pt, new_pt):
            return self.update_tag_pts(player, [], PieceTagEnum.Move)
        self._step_move(player, value, [(old_pt, new_pt)])
        player.temporary['pt'] = new_pt
        player.temporary['step'] = abs((new_pt - old_pt).x)
        self.test_win(player, new_pt)

    def move_test(self, value, pt1, pt2):
        other_player = self.player_manager.get_piece(val = 3-value).player
        if pt2.is_diagonal(pt1) or \
                    ((pt2[0] in [0, 8] or pt2[1] in [0, 8]) and pt2.is_lattice(pt1)):
            l = abs((pt2 - pt1).x)
            if l > 3: return False
            if l == other_player.temporary['step']: return False
            pt3 = other_player.temporary['pt']
            if pt2.is_diagonal(pt3) or \
                    ((pt2[0] in [0, 8] or pt2[1] in [0, 8]) and pt2.is_lattice(pt3)):
                return False
        return True


class Player_攻防棋(PlayerBlackWhite):
    def init_player_temporary(self):
        return {'黑':{'pt': Vector2D(4, 0), 'step': 0},
                '白':{'pt': Vector2D(4, 8), 'step': 0}}
    
    def init_pieceattr_group(self):
        return {'placeable': False, 'movable': [MoveRuleEnum.Move]}


class Game_攻防棋(GameData):
    """攻防棋"""
    def init_gridattr(self):
        self.default_piece_pts = {1: [(4, 0)], 2: [(4, 8)]}
        return {'matr': MatrixP((9, 9), -4, value_func = lambda x,y: 0)}

    def init_move_manager(self):
        return Move_攻防棋(self)

    def init_player_manager(self):
        return Player_攻防棋(self)



class App_攻防棋(AppBlackWhite):
    """攻防棋游戏规则"""
    def init_rule(self):
        self.name = '攻防棋'
        return Game_攻防棋()
    
    def grid_attr(self):
        return {'size': (9, 9), 'canvas_size': (750, 750),
                'padding': (80, 80), 'is_net': True}

    def canvas_attr(self):
        yls = [((i, 0), (0, i)) for i in range(2, 9, 2)]
        yls.extend([((i, 8), (8, i)) for i in range(2, 9, 2)])
        yls.extend([((i-1, 8), (0, 9 - i)) for i in range(1, 8, 2)])
        yls.extend([((i-1, 0), (8, 9 - i)) for i in range(1, 8, 2)])
        return {'coor_show': LinePositionEnum.Null,
            'bgedges_show': AxisEnum.Null,
            'canvas_lines': [*yls, ((0, 0), (8, 0)), ((0, 0), (0, 8)),
                             ((8, 8), (8, 0)), ((8, 8), (0, 8))]
            }
