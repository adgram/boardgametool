
from .blackwhite import *





class Game_连方棋(GameBlackWhite):
    """连方棋"""
    def init_pieceattr_group(self):
        return {'placeable': True, 'moverules': [MoveRuleEnum.Move]}

    def init_piece_count(self):
        return {1: 4, 2: 4}
    
    def init_matr(self):
        region = RegionRect(Vector2D(0, 0), Vector2D(4, 4))
        region2 = RegionPoints([(i, j) for i in range(4) for j in range(4) if not (i+j)%2])
        neighbortable = NeighborTable.structure_only({region: 4, region2: -4})
        return MatrixData((4, 4), region, neighbortable)

    def init_step_func(self):
        return {'move': (self.step_move, self.reverse_move),
                'add': (self.step_add, self.reverse_add)}

    def test_win(self, player: PlayerData, value):
        """模拟并测试该点落子后的情况"""
        if self.pieces[value].num != 4:
            return self.turn_active()
        pts = self.matr.search_value(value)
        if len(set([pt.x for pt in pts])) == 1 or\
                len(set([pt.y for pt in pts])) == 1:
            self.update_tag_pts(player.name, pts, "Win")
            self.do_game_over(player.name, GameOverEnum.Win)
            self.turn_active()
            return
        # 正方形必然为四短两长
        def distance(p1, p2):
            return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2
        lens = [distance(pts[3], pts[i]) for i in range(3)]
        lens.extend(distance(pts[2], pts[i]) for i in range(2))
        lens.append(distance(pts[0], pts[1]))
        if len(set(lens)) == 2:
            self.update_tag_pts(player.name, pts, "Win")
            self.do_game_over(player.name, GameOverEnum.Win)
        self.turn_active()

    def move_self_nil(self, player: PlayerData, active_piece: 'PieceData', old_pt, new_pt):
        value = active_piece.value
        if self.pieces[value].num != 4:
            return self.move_nil_nil(player, active_piece, new_pt)
        if old_pt in self.matr.get_point_nbrs(new_pt) or \
                    self.matr.skip_test(old_pt, new_pt, 3-value):
            self.do_move(player.name, value, [(old_pt, new_pt)])
            self.test_win(player, value)
            return
        self.update_tag_pts(player.name, [], "Move")

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        value = active_piece.value
        self.do_add(player.name, value, [new_pt])
        self.test_win(player, value)




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


