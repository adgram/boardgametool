
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



class Player_六消井字棋(PlayerBlackWhite):
    def init_player_temporary(self):
        from collections import deque
        return {'黑': {'pieces': deque()},
                '白': {'pieces': deque()}}
    
    def init_pieceattr_group(self):
        return {'placeable': True}



class Game_六消井字棋(Game_井字棋):
    """六消井字棋"""
    def init_move_manager(self):
        return Move_六消井字棋(self)

    def init_player_manager(self):
        return Player_六消井字棋(self)



class App_六消井字棋(App_井字棋):
    """六消井字棋游戏规则"""
    def init_rule(self):
        self.name = '六消井字棋'
        return Game_六消井字棋()


