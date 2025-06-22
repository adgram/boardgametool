
from .blackwhite import PlayerBlackWhite, AppBlackWhite
from ...gridrule import *
from pathlib import Path
from .wuziqi import Move_五子棋



class QuanchaUi(DefaultPiecesUi):
    def set_data(self, data, radius = 0):
        self.piecedata = data
        self.pieceui[self.piecedata[1].value] = PieceUi(
                icon = Path(__file__).parent/'images/叉.svg',
                radius = radius
               )
        self.pieceui[self.piecedata[2].value] = PieceUi(
                icon = Path(__file__).parent/'images/圈.svg',
                radius = radius
               )


class Move_井字棋(Move_五子棋):
    """井字棋"""
    def in_row(self, pt):
        """判断是否存在连子"""
        return super().in_row(pt, n = 3)


class Game_井字棋(GameData):
    """井字棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((3, 3), structure = 8)}

    def init_move_manager(self):
        return Move_井字棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': True})



class App_井字棋(AppBlackWhite):
    """井字棋游戏规则"""
    def init_rule(self):
        self.name = '井字棋'
        return Game_井字棋()
    
    def init_pieceuis(self):
        return QuanchaUi()

    def grid_attr(self):
        return {'size': (3, 3), 'canvas_size': (750, 750),
                'padding': (130, 130), 'is_net': False}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 10,
            'bgedges_show': AxisEnum.Null,
            'canvas_lines': [((0, 1), (3, 1)), ((0, 2), (3, 2)),
                             ((1, 0), (1, 3)), ((2, 0), (2, 3))],
            }




class Move_六消井字棋(Move_井字棋):
    """六消井字棋"""
    def init_data(self):
        self.step_func = {'add': self.step_add, 'remove': self.step_remove}
        self.reverse_func = {'add': self.reverse_add, 'remove': self.reverse_remove}

    def _step_add(self, player, val, pts):
        player.temporary['pieces'].append(pts[0])
        self.move_over(player, 'add', val, pts)
        self.step_add(player, val, pts)
        if len(player.temporary['pieces']) >= 4:
            old = player.temporary['pieces'].popleft()
            self.step_remove(player, val, [old])
            self.add_move(player, 'remove', val, [old])

    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        self._step_add(player, active_piece.value, [new_pt])
        self.test_win(player, new_pt)





class Player_六消井字棋(PlayerBlackWhite):
    def init_player_temporary(self):
        from collections import deque
        return {'黑': {'pieces': deque()},
                '白': {'pieces': deque()}}
    
    def init_pieceattr_group(self):
        return {'placeable': True}



class Game_六消井字棋(GameData):
    """六消井字棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((3, 3), structure = 8)}

    def init_move_manager(self):
        return Move_六消井字棋(self)

    def init_player_manager(self):
        return Player_六消井字棋(self)



class App_六消井字棋(App_井字棋):
    """六消井字棋游戏规则"""
    def init_rule(self):
        self.name = '六消井字棋'
        return Game_六消井字棋()




class 套娃井字棋Ui(DefaultPiecesUi):
    def set_data(self, data, radius = 0):
        self.piecedata = data
        color1 = PieceColor(color = (255, 255, 255, 200),
                fill = (20, 20, 20, 200), gradient = (50, 50, 50, 170))
        color2 = PieceColor(color = (0, 0, 0, 200),
                fill = (255, 255, 255, 200), gradient = (225, 225, 225, 170))
        for i in range(1, 6, 2):
            self.pieceui[i] = PieceUi(color = color1, radius = radius*(0.3 + 0.08*i))
            self.pieceui[i+1] = PieceUi(color = color2, radius = radius*(0.3 + 0.08*i))




class Move_套娃井字棋(Move_井字棋):
    """套娃井字棋"""
    def init_data(self):
        self.step_func = {'add': self.step_add}
        self.reverse_func = {'add': self.reverse_add}

    def in_row(self, pt, n = 5):
        """判断是否存在连子"""
        return self.matr.search_in_row(pt, n = n)

    def test_win(self, player, pt):
        """判断是否存在连子"""
        # if bool(rows := matrixgrid.flatten_as_vector(self.in_row(pt))):
        #     self.update_tag_pts(player, rows, PieceTagEnum.Win)
        #     self._step_game_over(player, GameOverEnum.Win)
        self.turn_active()

    def move_nil_nil(self, player: 'PlayerData', active_piece, pt):
        """在空点落子"""
        self._step_add(player, active_piece.value, [pt])
        self.test_win(player, pt)

    def move_nil_self(self, player: 'PlayerData', active_piece, pt, old_val):
        """在空点落子"""
        self._step_change(player, old_val, active_piece.value, [pt])

    def move_nil_other(self, player: 'PlayerData', active_piece, pt, old_val):
        """在空点落子"""
        self._step_change(player, old_val, active_piece.value, [pt])
        self.test_win(player, pt)



class Player_套娃井字棋(PlayerManager):
    """黑白双色棋"""
    def init_player_group(self):
        return {'黑':self.player_black(), '白':self.player_white()}

    def player_black(self, **kwargs):
        """黑棋玩家"""
        player = self.player_define(**{'name': '黑', **kwargs})
        player.pieces = {1: self.piece_define(player = player,
                                placeable = True, value = 1),
                         3: self.piece_define(player = player,
                                occupy = [1, 2],
                                placeable = True, value = 3),
                         5: self.piece_define(player = player,
                                occupy = [1, 2, 3, 4],
                                placeable = True, value = 5)}
        return player

    def player_white(self, **kwargs):
        """白棋玩家"""
        player = self.player_define(**{'name': '白', **kwargs})
        player.pieces = {2: self.piece_define(player = player,
                                placeable = True, value = 2),
                         4: self.piece_define(player = player,
                                occupy = [1, 2],
                                placeable = True, value = 4),
                         6: self.piece_define(player = player,
                                occupy = [1, 2, 3, 4],
                                placeable = True, value = 6)}
        return player



class Game_套娃井字棋(GameData):
    """套娃井字棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((3, 3), structure = 8)}

    def init_move_manager(self):
        return Move_套娃井字棋(self)

    def init_player_manager(self):
        return Player_套娃井字棋(self)



class App_套娃井字棋(AppBlackWhite):
    """套娃井字棋游戏规则"""
    def init_rule(self):
        self.name = '套娃井字棋'
        return Game_套娃井字棋()

    def init_pieceuis(self):
        return 套娃井字棋Ui()

    def grid_attr(self):
        return {'size': (3, 3), 'canvas_size': (750, 750),
                'padding': (180, 120), 'is_net': False, 'centered': False}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 10,
            'bgedges_show': AxisEnum.Null,
            'canvas_lines': [((0, 1), (3, 1)), ((0, 2), (3, 2)),
                             ((1, 0), (1, 3)), ((2, 0), (2, 3))],
            'pieces_values': [1, 3, 5, 2, 4, 6],
            }


