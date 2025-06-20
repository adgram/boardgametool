
from .blackwhite import PlayerBlackWhite, AppBlackWhite, 叉圈Ui
from ...gridrule import (MatrixP, pointData, GameOverEnum,
                    GameData, MoveManager, AxisEnum,
                    PieceTagEnum, LinePositionEnum, CanvasGrid)



class Move_五子棋(MoveManager):
    """五子棋"""
    def init_data(self):
        self.step_func = {'add': self.step_add}
        self.reverse_func = {'add': self.reverse_add}

    def in_row(self, pt, n = 5):
        """判断是否存在连子"""
        return self.matr.search_in_row(pt, n = n)

    def test_win(self, player, pt):
        """判断是否存在连子"""
        if bool(rows := pointData.flatten(self.in_row(pt))):
            self.update_tag_pts(player, rows, PieceTagEnum.Win)
            self.game_over(player, GameOverEnum.Win)
        self.turn_active(player = player)

    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        self._step_add(player, active_piece.value, [new_pt])
        self.test_win(player, new_pt)



class Game_五子棋(GameData):
    """五子棋"""
    def init_gridattr(self):
        return {'matr': MatrixP.structure_matrix((15, 15), structure = 8)}

    def init_move_manager(self):
        return Move_五子棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': True})



class App_五子棋(AppBlackWhite):
    """五子棋游戏规则"""
    def init_rule(self):
        self.name = '五子棋'
        return Game_五子棋()
    
    def init_grid(self):
        return CanvasGrid(size = (15, 15), canvas_size = (750, 750))
    
    def canvas_attr(self):
        return {'star_show': True}




class Move_井字棋(Move_五子棋):
    """井字棋"""
    def in_row(self, pt):
        """判断是否存在连子"""
        return super().in_row(pt, n = 3)


class Game_井字棋(GameData):
    """井字棋"""
    def init_gridattr(self):
        return {'matr': MatrixP.structure_matrix((3, 3), structure = 8)}

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
        return 叉圈Ui()
    
    def init_grid(self):
        return CanvasGrid(size = (3, 3),
                        canvas_size = (750, 750),
                        padding = (130, 130),
                        is_net = False)
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 10,
            'bgedges_show': AxisEnum.Null,
            'canvas_lines': [((0, 1), (3, 1)), ((0, 2), (3, 2)),
                             ((1, 0), (1, 3)), ((2, 0), (2, 3))],
            }

