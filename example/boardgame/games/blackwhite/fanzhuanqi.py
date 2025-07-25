
from .blackwhite import *
from collections import deque



class Game_黑白棋(GameBlackWhite):
    """黑白棋"""
    def init_pieceattr_group(self):
        return {'placeable': True}

    def init_matr(self):
        return MatrixData((8, 8), structure = 8)
    
    def init_matr_pts(self):
        return {1: [(3,3), (4,4)], 2: [(3,4), (4,3)]}

    def init_step_func(self):
        return {'change': (self.step_change, self.reverse_change),
                'add': (self.step_add, self.reverse_add)}

    def test_win(self, player: PlayerData, piece: PieceData, value, other_val):
        """模拟并测试该点落子后的情况"""
        if self.matr.all_filled():
            return self.do_game_over(player.name, self.win_test(piece))
        if piece.num == 0:
            return self.do_game_over(player.name, GameOverEnum.Lose)
        elif self.pieces[other_val].num == 0:
            return self.do_game_over(player.name, GameOverEnum.Win)
        for pt in self.matr.search_value(value):
            for p in self.matr.get_point_value_nbrs(pt, 0):
                if bool(self.move_test(p, value, other_val)):
                    return self.turn_active()
        return self.do_game_over(player.name, GameOverEnum.Win)

    def win_test(self, piece:PieceData):
        """模拟并测试该点落子后的情况"""
        if piece.value + piece.num > 33:
            return GameOverEnum.Win
        return GameOverEnum.Lose

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        value = active_piece.value
        other_value = 3 - value
        if not (row := self.move_test(new_pt, other_value, value)):
            return self.update_tag_pts(player.name, [], "Move")
        self.do_add(player.name, value, [new_pt], other_value, row)
        self.test_win(player, active_piece, value, other_value)

    def move_test(self, pt, value, end_value):
        """模拟并测试该点落子后的情况"""
        rows = self.matr.search_pincer(pt, value, end_value)
        return matrixgrid.flatten_as_vector([row[1:-1] for row in rows])

    def do_add(self, player_name: str, val, pts, old_val, row):
        """绘制棋盘上的棋子"""
        self.move_over(player_name, 'add', val, pts)
        self.add_move(player_name, 'change', old_val, val, row)
        self.step_add(player_name, (val, pts))
        self.step_change(player_name, (old_val, val, row))





class App_黑白棋(AppBlackWhite):
    """黑白棋游戏规则"""
    def init_rule(self):
        self.name = '黑白棋'
        return Game_黑白棋()
    
    def grid_attr(self):
        return {'size': (8, 8), 'canvas_size': (750, 750),
                'padding': (60, 60), 'is_net': False}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null}






class Game_俘虏棋(GameBlackWhite):
    """俘虏棋"""
    def init_pieceattr_group(self):
        return {'placeable': True}
    
    def init_matr(self):
        return MatrixData((8, 8), structure = 8)

    def init_step_func(self):
        return {'change': (self.step_change, self.reverse_change),
                'add': (self.step_add, self.reverse_add)}

    def test_win(self, player: PlayerData, piece: PieceData):
        """模拟并测试该点落子后的情况"""
        if self.matr.all_filled():
            tag = GameOverEnum.Win if piece.value + piece.num > 33 else GameOverEnum.Lose
            return self.do_game_over(player.name, tag)
        self.turn_active()

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        value = active_piece.value
        other_value = 3 - value
        row = self.move_test(new_pt, other_value, value)
        self.do_add(player.name, value, [new_pt], other_value, row)
        self.test_win(player, active_piece)

    def move_test(self, pt, value, end_value):
        """模拟并测试该点落子后的情况"""
        visited = set()  # 记录访问节点及其前驱
        queue = deque([pt])   # BFS队列初始化
        while queue:
            pt = queue.popleft()
            if pt in visited:
                continue
            visited.add(pt)
            rows = self.matr.search_pincer(pt, value, end_value)
            queue.extend(matrixgrid.flatten_as_vector([row[1:-1] for row in rows]))
        return list(visited)

    def do_add(self, player_name: str, val, pts, old_val, row):
        """绘制棋盘上的棋子"""
        self.move_over(player_name, 'add', val, pts)
        self.step_add(player_name, (val, pts))
        if row:
            self.add_move(player_name, 'change', old_val, val, row)
            self.step_change(player_name, (old_val, val, row))




class App_俘虏棋(App_黑白棋):
    """俘虏棋游戏规则"""
    def init_rule(self):
        self.name = '俘虏棋'
        return Game_俘虏棋()







class Game_翻田棋(GameBlackWhite):
    """翻田棋"""

    def init_matr(self):
        return MatrixData((3, 3), structure = 4)
    
    def init_matr_pts(self):
        return { 1: [(0, 0), (1, 0), (2, 0)],
                2: [(0, 2), (1, 2), (2, 2)]}

    def init_step_func(self):
        return {'change': (self.step_change, self.reverse_change),
                'move': (self.step_move, self.reverse_move)}

    def test_win(self, player: PlayerData, value):
        """模拟并测试该点落子后的情况"""
        pts = self.matr.search_value(value)
        for pt in pts:
            if self.matr.get_point_value_nbrs(pt, 0):
                return self.turn_active()
        for pt in pts:
            if self.matr.search_skip(pt):
                return self.turn_active()
        self.do_game_over(player.name, GameOverEnum.Win)
        self.turn_active()

    def move_self_nil(self, player: PlayerData, active_piece: 'PieceData', old_pt, new_pt):
        value = active_piece.value
        if old_pt in self.matr.get_point_nbrs(new_pt) or \
                    self.matr.skip_test(old_pt, new_pt, 3-value):
            self.do_move(player.name, value, [(old_pt, new_pt)])
            if (pts := self.matr.get_point_value_nbrs(old_pt, 3-value)):
                self.move_manager.change_value_pts(value, pts)
                self.add_move(player.name, 'change', value, 3-value, pts)
            self.test_win(player, 3-value)
            return
        self.update_tag_pts(player.name, [], "Move")



class App_翻田棋(AppBlackWhite):
    """翻田棋游戏规则"""
    def init_rule(self):
        self.name = '翻田棋'
        return Game_翻田棋()
    
    def grid_attr(self):
        return {'size': (3, 3), 'canvas_size': (750, 750),
                'padding': (110, 110), 'is_net': False}

    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null, 'thickness': 10}





class Game_耕作棋(GameBlackWhite):
    """耕作棋"""
    def init_matr(self):
        return MatrixData((5, 5), structure = 4)
    
    def init_matr_pts(self):
        return { 1: [(i, 0) for i in range(5)],
                2: [(i, 4) for i in range(5)]}
    

    def init_step_func(self):
        return {'change': (self.step_change, self.reverse_change),
                'move': (self.step_move, self.reverse_move)}

    def test_win(self, player: PlayerData, piece: PieceData, value):
        """模拟并测试该点落子后的情况"""
        for pt in self.matr.search_value(value):
            if self.matr.get_point_value_nbrs(pt, 0):
                return self.turn_active()
        self.do_game_over(player.name, GameOverEnum.Win if piece.num > 5 else GameOverEnum.Lose)
        self.turn_active()

    def move_self_nil(self, player: PlayerData, active_piece: 'PieceData', old_pt, new_pt):
        value = active_piece.value
        b, pts = self.move_test(3 - value, old_pt, new_pt)
        if not b:
            return self.update_tag_pts(player.name, [], "Move")
        self.do_move(player.name, value, [(old_pt, new_pt)])
        if pts:
            self.move_manager.change_value_pts(value, pts)
            self.add_move(player.name, 'change', value, 3-value, pts)
        self.test_win(player, active_piece, 3-value)

    def move_test(self, value, old_pt, new_pt):
        unit = matrixgrid.vector_unit(new_pt - old_pt)
        if old_pt + unit not in self.matr.get_point_nbrs(old_pt):
            return False, []
        line = self.matr.collection_line(old_pt, new_pt)
        opts = line.pop(0, [])
        if len(line):
            return False, []
        pts = []
        for pt in opts:
            pts.extend(self.matr.get_point_value_nbrs(pt, value))
        pts.extend(self.matr.get_point_value_nbrs(new_pt, value))
        pp = new_pt + unit
        if pp in pts:
            pts.remove(pp)
        return True, pts




class App_耕作棋(AppBlackWhite):
    """耕作棋游戏规则"""
    def init_rule(self):
        self.name = '耕作棋'
        return Game_耕作棋()
    
    def grid_attr(self):
        return {'size': (5, 5), 'canvas_size': (750, 750),
                'padding': (90, 90), 'is_net': False}

    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null, 'thickness': 5}







class Game_翻箱倒柜棋(Game_耕作棋):
    """翻箱倒柜棋"""
    def init_matr(self):
        pts =  [(j, i) for i in range(4) for j in range(3-i, 4+i)]
        pts.extend([(j, i+4) for i in range(3) for j in range(1+i, 6-i)])
        region = RegionPoints(pts)
        neighbortable = NeighborTable.structure_only({region: 4})
        return MatrixData((7, 7), region, neighbortable)

    def init_matr_pts(self):
        return  {1: [(3, 0), (2, 1), (3, 1), (4, 1), (1, 2), (5, 2)],
                2: [(3, 6), (2, 5), (3, 5), (4, 5), (1, 4), (5, 4)]}

    def test_win(self, player: PlayerData, piece: PieceData, value):
        """模拟并测试该点落子后的情况"""
        if piece.num >= 10:
            self.do_game_over(player.name, GameOverEnum.Win)
            self.turn_active()
            return
        for pt in self.matr.search_value(value):
            if self.matr.get_point_value_nbrs(pt, 0):
                return self.turn_active()
        self.do_game_over(player.name, GameOverEnum.Win)
        self.turn_active()


class App_翻箱倒柜棋(AppBlackWhite):
    """翻箱倒柜棋游戏规则"""
    def init_rule(self):
        self.name = '翻箱倒柜棋'
        return Game_翻箱倒柜棋()
    
    def grid_attr(self):
        return {'size': (7, 7), 'canvas_size': (750, 750),
                'padding': (80, 80), 'is_net': False}

    def canvas_attr(self):
        pts =  [((3-i, i), (4+i, i)) for i in range(4)]
        pts.extend([((i, i+4), (7-i, i+4)) for i in range(4)])
        pts.extend([((i, 3-i), (i, 4+i)) for i in range(4)])
        pts.extend([((i+4, i), (i+4, 7-i)) for i in range(4)])
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 7, 'bgedges_show': AxisEnum.Null,
            'canvas_lines': pts}






class Game_翻子棋(GameBlackWhite):
    """翻子棋"""
    def init_matr(self):
        region = RegionRect((5, 5))
        region2 = RegionPoints([(i, j) for i in range(5) for j in range(5) if (i+j+1)%2])
        neighbortable = NeighborTable.structure_only({region: 4, region2: 8})
        return MatrixData((5, 5), region, neighbortable)
    
    def init_matr_pts(self):
        return {1: [(i, 0) for i in range(5)],
                2: [(i, 4) for i in range(5)]}

    def test_win(self, player: PlayerData, piece: PieceData, value):
        """模拟并测试该点落子后的情况"""
        if piece.num == 9:
            for pt in self.matr.search_value(value):
                if self.matr.get_point_value_nbrs(pt, 0):
                    return self.turn_active()
            return  # pass, pass
        elif piece.num == 10:
            self.do_game_over(player.name, GameOverEnum.Win)
        elif piece.num == 0:
            self.do_game_over(player.name, GameOverEnum.Lose)
        self.turn_active()

    def move_test(self, ovalue, old_pt, new_pt):
        if old_pt + matrixgrid.vector_unit(new_pt - old_pt) not in self.matr.get_point_nbrs(old_pt):
            return False, []
        line = self.matr.collection_line(old_pt, new_pt)
        line.pop(0, [])
        if len(line):
            return False, []
        nbrs = self.matr.get_point_value_nbrs(new_pt, ovalue)
        # 两人抬
        pts = []
        for pt1 in nbrs:
            for pt2 in self.matr.get_point_value_nbrs(pt1, 3 - ovalue):
                if pt2 - pt1 == pt1 - new_pt:
                    pts.append(pt1)
                    break
        # 挑担子
        pairs = []
        for pt1 in nbrs:
            for pt2 in nbrs:
                if pt1 == pt2:
                    continue
                if (pt1, pt2) in pairs or (pt2, pt1) in pairs:
                    continue
                if pt2 - new_pt == new_pt - pt1:
                    pairs.append((pt1, pt2))
        return True, list(set(pts + matrixgrid.flatten_as_vector(pairs)))





class App_翻子棋(AppBlackWhite):
    """翻子棋游戏规则"""
    def init_rule(self):
        self.name = '翻子棋'
        return Game_翻子棋()
    
    def grid_attr(self):
        return {'size': (5, 5), 'canvas_size': (750, 750),
                'padding': (100, 100), 'is_net': True}

    def canvas_attr(self):
        pts = [((0, 2), (2, 4)), ((0, 0), (4, 4)), ((2, 0), (4, 2)),
               ((2, 0), (0, 2)), ((4, 0), (0, 4)), ((2, 4), (4, 2))]
        return {'coor_show': LinePositionEnum.Null, 'thickness': 5, 'canvas_lines': pts}

