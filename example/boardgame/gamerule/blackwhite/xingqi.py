
from .blackwhite import PlayerBlackWhite, AppBlackWhite
from ...gridrule import *



class Move_连方棋(MoveManager):
    """连方棋"""
    def init_data(self):
        self.step_func = {'move': self.step_move, 'add': self.step_add}
        self.reverse_func = {'move': self.reverse_move, 'add': self.reverse_add}

    def test_win(self, player, value):
        """模拟并测试该点落子后的情况"""
        if self.game.pieces[value].num != 4:
            return self.turn_active(player = player)
        pts = self.matr.search_value(value)
        if len(set([pt.x for pt in pts])) == 1 or\
                len(set([pt.y for pt in pts])) == 1:
            self.update_tag_pts(player, pts, PieceTagEnum.Win)
            self._step_game_over(player, GameOverEnum.Win)
            self.turn_active(player = player)
            return
        # 正方形必然为四短两长
        def distance(p1, p2):
            return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2
        lens = [distance(pts[3], pts[i]) for i in range(3)]
        lens.extend(distance(pts[2], pts[i]) for i in range(2))
        lens.append(distance(pts[0], pts[1]))
        if len(set(lens)) == 2:
            self.update_tag_pts(player, pts, PieceTagEnum.Win)
            self._step_game_over(player, GameOverEnum.Win)
        self.turn_active(player = player)

    def move_self_nil(self, player: 'PlayerData', active_piece, old_pt, new_pt):
        value = active_piece.value
        if self.game.pieces[value].num != 4:
            return self.move_nil_nil(player, active_piece, new_pt)
        if old_pt in self.matr.get_point_nbrs(new_pt) or \
                    self.matr.skip_test(old_pt, new_pt, 3-value):
            self._step_move(player, value, [(old_pt, new_pt)])
            self.test_win(player, value)
            return
        self.update_tag_pts(player, [], PieceTagEnum.Move)

    def move_nil_nil(self, player, active_piece, new_pt):
        """在空点落子"""
        value = active_piece.value
        self._step_add(player, value, [new_pt])
        self.test_win(player, value)




class Game_连方棋(GameData):
    """连方棋"""
    def init_gridattr(self):
        region = RegionRect(Vector2D(0, 0), Vector2D(4, 4))
        region2 = RegionPoints([(i, j) for i in range(4) for j in range(4) if not (i+j)%2])
        neighbortable = NeighborTable.structure_only({region: 4, region2: -4})
        return {'matr': MatrixP((4, 4), region, neighbortable)}

    def init_move_manager(self):
        return Move_连方棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, piece_count = {1: 4, 2: 4},
                    pieceattr_group = {'placeable': True, 'movable': [MoveRuleEnum.Move]})



class App_连方棋(AppBlackWhite):
    """连方棋游戏规则"""
    def init_rule(self):
        self.name = '连方棋'
        return Game_连方棋()
    
    def grid_attr(self):
        return {'size': (4, 4), 'canvas_size': (750, 750),
                'padding': (110, 110), 'is_net': True}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 10,
            'bgedges_show': AxisEnum.XY,
            'canvas_lines': [((0, 0), (3, 3)), 
                ((0, 2), (1, 3)), ((2, 0), (3, 1)), 
                ((0, 2), (2, 0)), ((1, 3), (3, 1))]}




class Move_直角五子棋(MoveManager):
    """直角五子棋"""
    def init_data(self):
        self.step_func = {'add': self.step_add}
        self.reverse_func = {'add': self.reverse_add}

    def test_win(self, player, pt):
        """判断是否存在连子"""
        bls = []
        for plum in self.get_shapes():
            for p in plum:
                d =  pt - p
                bl = [(d + q) for q in plum]
                if set(self.matr.get_value(q) for q in bl) == {self.matr.get_value(pt)}:
                    bls.extend(bl)
        if bls:
            self.update_tag_pts(player, bls, PieceTagEnum.Win)
            self._step_game_over(player, GameOverEnum.Win)
        self.turn_active(player = player)

    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        self._step_add(player, active_piece.value, [new_pt])
        self.test_win(player, new_pt)
    
    def get_shapes(self):
        return [[Vector2D(0, 0), x, x*2, y, y*2] for x,y in [
            (Vector2D(1, 1), Vector2D(1, -1)), (Vector2D(1, -1), Vector2D(-1, -1)),
            (Vector2D(-1, -1), Vector2D(-1, 1)), (Vector2D(-1, 1), Vector2D(1, 1)),
            (Vector2D(0, 1), Vector2D(1, 0)), (Vector2D(1, 0), Vector2D(0, -1)),
            (Vector2D(0, -1), Vector2D(-1, 0)), (Vector2D(-1, 0), Vector2D(0, 1))
        ]]



class Game_直角五子棋(GameData):
    """直角五子棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((9, 9), structure = 8)}

    def init_move_manager(self):
        return Move_直角五子棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': True})



class App_直角五子棋(AppBlackWhite):
    """直角五子棋游戏规则"""
    def init_rule(self):
        self.name = '直角五子棋'
        return Game_直角五子棋()
    
    def grid_attr(self):
        return {'size': (9, 9), 'canvas_size': (750, 750),
                'padding': (80, 80), 'is_net': True}
    
    def canvas_attr(self):
        return {'star_show': True}




class Move_梅花棋(Move_直角五子棋):
    """梅花棋"""
    def get_shapes(self):
        return [[(0, 0)] + [(i, j) for i in [-1, 1] for j in [-1, 1]],
                 [(0, 0)] + [(i, j) for i in [-2, 2] for j in [-2, 2]],
                 [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)],
                 [(0, 0), (2, 0), (-2, 0), (0, 2), (0, -2)]]



class Game_梅花棋(GameData):
    """梅花棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((19, 19), structure = 8)}

    def init_move_manager(self):
        return Move_梅花棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': True})



class App_梅花棋(AppBlackWhite):
    """梅花棋游戏规则"""
    def init_rule(self):
        self.name = '梅花棋'
        return Game_梅花棋()
    
    def grid_attr(self):
        return {'size': (19, 19), 'canvas_size': (750, 750),
                'padding': (40, 40), 'is_net': True}
    
    def canvas_attr(self):
        return {'star_show': True}

