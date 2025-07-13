
from .blackwhite import *
from pathlib import Path




class Game_国象跳棋(GameBlackWhite):
    """国象跳棋"""
    def init_matr(self):
        return MatrixData((8, 8), structure = -4)
    
    def init_matr_pts(self):
        return {2: [(i, j) for i in range(8) for j in range(3) if (i+j)%2],
                1: [(i, j) for i in range(8) for j in range(5, 8) if (i+j)%2]}

    def init_step_func(self):
        return {'move': (self.step_move, self.reverse_move)}

    def test_win(self, player: PlayerData, value):
        """模拟并测试该点落子后的情况"""
        pt0s = self.matr.search_value(0)
        for pt0 in pt0s:
            for pt in self.matr.search_value(value):
                if bool(self.get_move_links(value, pt, pt0)):
                    return self.turn_active()
        self.do_game_over(player.name, GameOverEnum.Win)

    def move_self_nil(self, player: PlayerData, active_piece: 'PieceData', old_pt, new_pt):
        value = active_piece.value
        if not (links := self.get_move_links(value, old_pt, new_pt)):
            return self.update_tag_pts(player.name, [], "Move")
        self.do_move(player.name, value, links)
        self.test_win(player, 3 - value)

    def get_move_links(self, val, old_pt, new_pt):
        if not self.test_move(val, old_pt, new_pt):
            return []
        if new_pt in self.matr.get_point_nbrs(old_pt):
            return [(old_pt, new_pt)]
        pts = self.matr.search_shortest_path(old_pt, new_pt, True,
                            lambda pt, p: self.test_move(val, pt, p))
        return [pts] if pts else []

    def test_move(self, val, pt1, pt2):
        if val == 1 and pt2[1] < pt1[1]:
            return True
        if val == 2 and pt2[1] > pt1[1]:
            return True
        return False



class App_国象跳棋(AppBlackWhite):
    """国象跳棋游戏规则"""
    def init_rule(self):
        self.name = '国象跳棋'
        return Game_国象跳棋()
    
    def grid_attr(self):
        return {'size': (8, 8), 'canvas_size': (750, 750),
                'padding': (90, 90), 'is_net': False}
    
    def canvas_attr(self):
        cells = [(i, j) for i in range(8) for j in range(8) if (i+j+1)%2]
        return {'coor_show': LinePositionEnum.Null, 'bgedges_show': AxisEnum.XY,
            'canvas_cells': cells, }




class Game_卯兔争窝棋(Game_国象跳棋):
    """卯兔争窝棋"""
    def init_matr(self):
        region = RegionPoints([(i, j) for i in range(5) for j in range(5) if (i+j+1)%2])
        neighbortable = NeighborTable.structure_only({region: -4})
        neighbortable.add_mathvector_map({RegionPoints([(i, j) for i in range(0, 5, 2) 
                                for j in range(0, 5, 2)]): {(0, 2), (0, -2), (2, 0), (-2, 0)}})
        return MatrixData((5, 5), region, neighbortable)
    
    def init_matr_pts(self):
        return {1: [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
                2: [(0, 4), (1, 3), (2, 4), (3, 3), (4, 4)]}

    def get_move_links(self, val, old_pt, new_pt):
        if new_pt == (4, 2):
            return []
        pt0s = self.matr.search_value(0)
        pt0s.remove((4, 2))
        # 移子
        if pt0s[1] in self.matr.get_point_nbrs(pt0s[0]):
            if new_pt in self.matr.get_point_nbrs(old_pt):
                 return [(old_pt, new_pt)]
            return []
        # 跳子
        pts = self.matr.search_line(old_pt, new_pt, structure = 8)
        if len(pts) <= 2:
            return []
        if pt0s[0] == new_pt:
            if pt0s[1] in pts:
                return []
        if pt0s[1] == new_pt:
            if pt0s[0] in pts:
                return []
        return [(old_pt, new_pt)]




class App_卯兔争窝棋(AppBlackWhite):
    """卯兔争窝棋游戏规则"""
    def init_rule(self):
        self.name = '卯兔争窝棋'
        return Game_卯兔争窝棋()
    
    def grid_attr(self):
        return {'size': (5, 5), 'canvas_size': (750, 750), 'padding': (110, 110)}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null, 'thickness': 7, 'bgedges_show': AxisEnum.Null, 
            'canvas_lines': [((0, 0), (4, 0)), ((0, 4), (4, 4)), ((4, 0), (4, 1.5)), ((0, 0), (0, 4)),
                             ((0, 0), (4, 4)), ((4, 0), (0, 4)), ((0, 2), (3.5, 2)), ((2, 0), (2, 4)),
                             ((0, 2), (2, 4)), ((2, 0), (3.55, 1.55)), ((0, 2), (2, 0)),
                             ((2, 4), (3.55, 2.45)), ((4, 2.5), (4, 4))],
            'cell_tags': [(4, 2)], 'tagicon': Path(__file__).parent/'images/方.svg',
            'iconsize': (150, 150), 'tagtext': '阱'}




class Game_行蛙跳棋(Game_国象跳棋):
    """行蛙跳棋"""
    def init_matr(self):
        region = RegionPoints(self.default_piece_pts[1] +  self.default_piece_pts[2] + [(1, 3), (3, 3)])
        neighbortable = NeighborTable.structure_only({region: -4})
        return MatrixData((5, 7), region, neighbortable)
    
    def init_matr_pts(self):
        return {2: [(2, 0), (1, 1), (3, 1), (0, 2), (2, 2), (4, 2)],
                1: [(2, 6), (1, 5), (3, 5), (0, 4), (2, 4), (4, 4)]}

    def get_move_links(self, val, old_pt, new_pt):
        pts = self.matr.search_line(old_pt, new_pt, structure = -4)
        if 3 <= len(pts) <= 4 and self.matr.get_value(pts[1]) and self.matr.get_value(pts[-2]):
            return [(old_pt, new_pt)]
        return []



class App_行蛙跳棋(AppBlackWhite):
    """行蛙跳棋游戏规则"""
    def init_rule(self):
        self.name = '行蛙跳棋'
        return Game_行蛙跳棋()
    
    def grid_attr(self):
        return {'size': (5, 7), 'canvas_size': (550, 750),
                'padding': (80, 80), 'is_net': True}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null, 'thickness': 7, 'bgedges_show': AxisEnum.Null, 
            'canvas_lines': [((0, 2), (2, 0)), ((0, 4), (3, 1)), ((1, 5), (4, 2)), ((2, 6), (4, 4)),
                             ((2, 0), (4, 2)), ((1, 1), (4, 4)), ((0, 2), (3, 5)), ((2, 6), (0, 4))]}





class Game_中象跳棋(Game_国象跳棋):
    """中象跳棋"""
    def init_matr(self):
        return MatrixData((9, 10), 4)
    
    def init_matr_pts(self):
        return {1: [(i, j) for i in range(4) for j in range(4)],
                2: [(i, j) for i in range(5, 9) for j in range(6, 10)]}

    def test_win(self, player: PlayerData, value, count = 16):
        bl = self.init_matr_pts()[value]
        if len(self.matr.collection(bl).get(3 - value, [])) == count:
            self.do_game_over(player.name, GameOverEnum.Win)
        self.turn_active()

    def get_move_links(self, val, old_pt, new_pt):
        if new_pt in self.matr.get_point_nbrs(old_pt):
            return [(old_pt, new_pt)]
        pts = self.matr.search_shortest_path(old_pt, new_pt, True)
        return [pts] if pts else []



class App_中象跳棋(AppBlackWhite):
    """中象跳棋游戏规则"""
    def init_rule(self):
        self.name = '中象跳棋'
        return Game_中象跳棋()
    
    def grid_attr(self):
        return {'size': (9, 10), 'canvas_size': (750, 750),
                'padding': (80, 80), 'is_net': True}

    def canvas_attr(self):
        yls = [((i, 0), (i, 4)) for i in range(9)]
        yls.extend([((i, 5), (i, 9)) for i in range(9)])
        return {'coor_show': LinePositionEnum.Null,
            'bgedges_show': AxisEnum.X,
            'canvas_lines': [*yls, ((3, 0), (5, 2)), ((3, 2), (5, 0)),
                                   ((3, 7), (5, 9)), ((3, 9), (5, 7)),
                                   ((0, 4), (0, 5)), ((8, 4), (8, 5))]
            }




class Game_单线跳棋(Game_中象跳棋):
    """单线跳棋"""
    def init_matr(self):
        return MatrixData((18, 1), 2)
    
    def init_matr_pts(self):
        return {1: [(i, 0) for i in range(5)],
                2: [(i, 0) for i in range(13, 18)]}

    def test_win(self, player: PlayerData, value):
        super().test_win(player, value, 5)

    def get_move_links(self, val, old_pt, new_pt):
        if not self.test_move(val, old_pt, new_pt):
            return []
        if new_pt in self.matr.get_point_nbrs(old_pt):
            return [(old_pt, new_pt)]
        if (pts := self.matr.search_line(old_pt, new_pt, val = 3 - val, structure = 4))[1:-1]:
            return [pts]
        return []

    def test_move(self, val, pt1, pt2):
        if val == 1 and pt2[0] > pt1[0]:
            return True
        if val == 2 and pt2[0] < pt1[0]:
            return True
        return False


class App_单线跳棋(AppBlackWhite):
    """单线跳棋游戏规则"""
    def init_rule(self):
        self.name = '单线跳棋'
        return Game_单线跳棋()
    
    def grid_attr(self):
        return {'size': (18, 1), 'canvas_size': (900, 650),
                'padding': (40, 40), 'is_net': False}

    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null, 'bgedges_show': AxisEnum.XY}
