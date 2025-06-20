
from .blackwhite import PlayerBlackWhite
from ...gridrule import *
from pathlib import Path
from .wuziqi import Move_五子棋, App_五子棋



class ThreesUi(DefultPiecesUi):
    def set_data(self, data, radius = 0):
        self.piecedata = data
        self.pieceui[self.piecedata[1].value] = PieceUi(
                color = PieceColor(color = (255, 255, 255, 200),
                                   fill = (20, 20, 20, 200),
                                   gradient = (50, 50, 50, 170)),
                text = PieceText(text = '黑',
                                 height = 20,
                                 color = (255, 255, 255, 200)),
                radius = radius
               )
        self.pieceui[self.piecedata[2].value] = PieceUi(
                color = PieceColor(color = (0, 0, 0, 200),
                                   fill = (255, 255, 255, 200),
                                   gradient = (225, 225, 225, 170)),
                text = PieceText(text = '白',
                                 height = 20,
                                 color = (0, 0, 0, 200)),
                radius = radius
               )
        self.pieceui[self.piecedata[-1].value] = PieceUi(
                color = PieceColor(color = (0, 0, 0, 200),
                                   fill = (125, 125, 125, 200),
                                   gradient = (105, 105, 105, 170)),
                text = PieceText(text = '灰',
                                 height = 20,
                                 color = (0, 0, 0, 200)),
                radius = radius
               )



class Player_同步五子棋(PlayerBlackWhite):
    def init_pieceattr_group(self):
        return {'placeable': True}

    def init_common_pieces(self):
        return {-1: self.piece_define(**{'value': -1, 'name':'灰', **{**self.pieceattr_group}})}



class Move_同步五子棋(Move_五子棋):
    """同步五子棋"""
    def test_win(self, pl1, pt1, pl2, pt2):
        """判断是否存在连子"""
        row1 = matrixgrid.flatten_as_vector(self.in_row(pt1))
        row2 = matrixgrid.flatten_as_vector(self.in_row(pt2))
        if len(row1) > len(row2):
            self.update_tag_pts(pl1, row1, PieceTagEnum.Win)
            self._step_game_over(pl1, GameOverEnum.Win)
        elif len(row1) < len(row2):
            self.update_tag_pts(pl2, row2, PieceTagEnum.Win)
            self._step_game_over(pl2, GameOverEnum.Win)
        elif len(row1) > 0:
            common = self.player_manager.common_player
            self.step_change(common, pl1.active, -1, row1)
            self.step_change(common, pl2.active, -1, row2)
            self.move_over(common, 'change', pl1.active, -1, row1)
            self.add_move(common, 'change', pl1.active, -1, row2)

    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        if self.grid.temporary.get('pt', None) is None:
            self.grid.temporary['pt'] = new_pt
        else:
            pt1 = self.grid.temporary['pt']
            self.grid.temporary['pt'] = None
            if pt1 == new_pt:
                self._step_add(self.player_manager.common_player, -1, [new_pt])
            else:
                val1 = 3 - active_piece.value
                pl1 = self.player_manager.get_player(val = val1)
                self.move_over(pl1, 'add', val1, [pt1])
                self.move_over(player, 'add', active_piece.value, [new_pt])
                self.step_add(pl1, val1, [pt1])
                self.step_add(player, active_piece.value, [new_pt])
                self.test_win(pl1, pt1, player, new_pt)
        self.turn_active(player = player)



class Game_同步五子棋(GameData):
    """同步五子棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((15, 15), structure = 8)}

    def init_move_manager(self):
        return Move_同步五子棋(self)

    def init_player_manager(self):
        return Player_同步五子棋(self)



class App_同步五子棋(App_五子棋):
    """同步五子棋游戏规则"""
    def init_rule(self):
        self.name = '同步五子棋'
        return Game_同步五子棋()
    
    def init_pieceuis(self):
        return ThreesUi()


