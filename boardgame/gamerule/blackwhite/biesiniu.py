
from .blackwhite import PlayerBlackWhite, AppBlackWhite
from ...gridrule import (GameOverEnum, MoveRuleEnum,
                    GameData, MoveManager, AxisEnum,
                    LinePositionEnum, CanvasGrid, PieceTagEnum,
                    RegionPoints, NeighborTable, MatrixP)
from pathlib import Path






class Move_憋死牛(MoveManager):
    """憋死牛"""
    def init_data(self):
        self.step_func = {'move': self.step_move}
        self.reverse_func = {'move': self.reverse_move}

    def test_win(self, player, value):
        """模拟并测试该点落子后的情况"""
        for pt in self.matr.search_value(value):
            if bool(self.matr.get_point_value_nbrs(pt, 0)):
                return self.turn_active(player = player)
        self.game_over(player, GameOverEnum.Win)

    def move_self_nil(self, player: 'PlayerData', active_piece, new_pt, old_pt):
        value = active_piece.value
        if not (links := self.get_move_links(old_pt, new_pt)):
            return self.update_tag_pts(player, [], PieceTagEnum.Move)
        self._step_move(player, value, links)
        self.test_win(player, 3 - value)

    def get_move_links(self, old_pt, new_pt):
        if old_pt in self.matr.get_point_nbrs(new_pt):
            return [(old_pt, new_pt)]
        return []





class Game_憋死牛(GameData):
    """憋死牛"""
    def init_gridattr(self):
        self.default_piece_pts = {1: [(0, 0), (2, 0)], 2: [(0, 2), (2, 2)]}
        region = RegionPoints([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)])
        neighbortable = NeighborTable.create_from_edges(
                    {(0, 0): ((0, 2), (2, 0), (1, 1)),
                    (0, 2): ((0, 0), (1, 1)),
                    (1, 1): ((0, 0), (2, 0), (0, 2), (2, 2)),
                    (2, 0): ((0, 0), (2, 2), (1, 1)),
                    (2, 2): ((2, 0), (1, 1))}
               )
        return {'matr': MatrixP.simple_matrix((3, 3), region, neighbortable)}

    def init_move_manager(self):
        return Move_憋死牛(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': False,
                        'movable': [MoveRuleEnum.Move]})



class App_憋死牛(AppBlackWhite):
    """憋死牛游戏规则"""
    def init_rule(self):
        self.name = '憋死牛'
        return Game_憋死牛()
    
    def init_grid(self):
        return CanvasGrid(size = (3, 3), canvas_size = (750, 750), padding = (190, 190))
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 10,
            'bgedges_show': AxisEnum.Null,
            'canvas_lines': [((0, 0), (2, 0)), ((0, 2), (0, 0)), ((0, 0), (2, 2)),
                             ((0, 2), (2, 0)), ((2, 0), (2, 2))],
            'cell_tags': [(1, 2)], 'tagicon': Path(__file__).parent/'images/椭圆.svg'}


