
from .blackwhite import *
from pathlib import Path
from collections import deque






class Game_憋死牛(GameBlackWhite):
    """憋死牛"""
    def init_matr(self):
        region = RegionPoints([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)])
        neighbortable = NeighborTable.link_only(
                    {Vector2D(0, 0): {Vector2D(0, 2), Vector2D(2, 0), Vector2D(1, 1)},
                    Vector2D(0, 2): {Vector2D(0, 0), Vector2D(1, 1)},
                    Vector2D(1, 1): {Vector2D(0, 0), Vector2D(2, 0), Vector2D(0, 2), Vector2D(2, 2)},
                    Vector2D(2, 0): {Vector2D(0, 0), Vector2D(2, 2), Vector2D(1, 1)},
                    Vector2D(2, 2): {Vector2D(2, 0), Vector2D(1, 1)}}
               )
        return MatrixData((3, 3), region, neighbortable)
    
    def init_matr_pts(self):
        return {1: [(0, 0), (2, 0)], 2: [(0, 2), (2, 2)]}

    def init_step_func(self):
        return {'move': (self.step_move, self.reverse_move)}

    def test_win(self, player: PlayerData, value):
        """模拟并测试该点落子后的情况"""
        for pt in self.matr.search_value(value):
            if bool(self.matr.get_point_value_nbrs(pt, 0)):
                return self.turn_active()
        self.do_game_over(player.name, GameOverEnum.Win)

    def move_self_nil(self, player: PlayerData, active_piece: 'PieceData', old_pt, new_pt):
        value = active_piece.value
        if not (links := self.get_move_links(old_pt, new_pt)):
            return self.update_tag_pts(player.name, [], "Move")
        self.do_move(player.name, value, links)
        self.test_win(player, 3 - value)

    def get_move_links(self, old_pt, new_pt):
        if old_pt in self.matr.get_point_nbrs(new_pt):
            return [(old_pt, new_pt)]
        return []




class App_憋死牛(AppBlackWhite):
    """憋死牛游戏规则"""
    def init_rule(self):
        self.name = '憋死牛'
        return Game_憋死牛()
    
    def grid_attr(self):
        return {'size': (3, 3), 'canvas_size': (750, 750),
                'padding': (200, 200), 'is_net': True}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 10,
            'bgedges_show': AxisEnum.Null,
            'canvas_lines': [((0, 0), (2, 0)), ((0, 2), (0, 0)), ((0, 0), (2, 2)),
                             ((0, 2), (2, 0)), ((2, 0), (2, 2))],
            'cell_tags': [(1, 2)], 'tagicon': Path(__file__).parent/'images/椭圆.svg'}





class Game_井棋(Game_憋死牛):
    """井棋"""
    def init_matr(self):
        neighbortable = NeighborTable.structure_only({RegionRect((3, 2)): 4,
                                                      RegionRect((0, 2), (3, 3)): -2})
        return MatrixData((3, 3), RegionRect((3, 3)), neighbortable)

    def init_matr_pts(self):
        return {1: [(0, 0), (0, 1), (0, 2)], 2: [(2, 0), (2, 1), (2, 2)]}


class App_井棋(AppBlackWhite):
    """井棋游戏规则"""
    def init_rule(self):
        self.name = '井棋'
        return Game_井棋()
    
    def grid_attr(self):
        return {'size': (3, 3), 'canvas_size': (750, 750),
                'padding': (180, 180), 'is_net': True}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 10,
            'bgedges_show': AxisEnum.Y,
            'canvas_lines': [((0, 1), (2, 1)), ((0, 0), (2, 0))]}





class Game_斜方棋(Game_憋死牛):
    """斜方棋"""
    def init_matr(self):
        region = RegionPoints([(i, j) for i in range(5) for j in range(5) if (i+j+1)%2])
        neighbortable = NeighborTable.mathvector_only({
                RegionPoints(((0, 0), (0, 4), (4, 0), (4, 4), (0, 2), (4, 2))): [(0, 2), (0, -2)],
                RegionPoints(((0, 0), (0, 4), (4, 0), (4, 4), (2, 0), (2, 4))): [(2, 0), (-2, 0)],
                RegionPoints(((0, 2), (1, 3), (2, 4), (2, 2), (2, 0), (3, 1), (4, 2))): [(1, 1), (-1, -1)],
                RegionPoints(((0, 2), (1, 1), (2, 0), (2, 2), (2, 4), (3, 3), (4, 2))): [(1, -1), (-1, 1)],
                RegionPoints(((1, 1), )): [(1, 1)], RegionPoints(((3, 1), )): [(-1, 1)],
                RegionPoints(((1, 3), )): [(1, -1)], RegionPoints(((3, 3), )): [(-1, -1)]})
        return MatrixData((5, 5), region, neighbortable)

    def init_matr_pts(self):
        return {1: [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
                                  2: [(0, 4), (1, 3), (2, 4), (3, 3), (4, 4)]}




class App_斜方棋(AppBlackWhite):
    """斜方棋游戏规则"""
    def init_rule(self):
        self.name = '斜方棋'
        return Game_斜方棋()
    
    def grid_attr(self):
        return {'size': (5, 5), 'canvas_size': (750, 750),
                'padding': (110, 110), 'is_net': True}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 7,
            'bgedges_show': AxisEnum.Null,
            'canvas_lines': [((0, 0), (4, 0)), ((0, 4), (4, 4)), ((4, 0), (4, 4)), ((0, 0), (0, 4)),
                             ((0, 2), (2, 4)), ((1, 1), (3, 3)), ((2, 0), (4, 2)),
                             ((0, 2), (2, 0)), ((1, 3), (3, 1)), ((2, 4), (4, 2)),]}






class Game_四和棋(Game_憋死牛):
    """四和棋"""
    def init_pieceattr_group(self):
        return {'placeable': True, 'moverules': [MoveRuleEnum.Move]}

    def init_piece_count(self):
        return {1: 4, 2: 4}

    def init_matr(self):
        region = RegionPoints([(0, 0), (0, 2),
                               (1, 0), (1, 1), (1, 2),
                               (2, 0), (2, 1), (2, 2),
                               (3, 0), (3, 2)])
        neighbortable = NeighborTable.link_only(
                    {Vector2D(0, 0): {Vector2D(0, 2), Vector2D(1, 0)},
                     Vector2D(0, 2): {Vector2D(0, 0), Vector2D(1, 2)},
                     Vector2D(1, 0): {Vector2D(0, 0), Vector2D(2, 0), Vector2D(1, 1)},
                     Vector2D(1, 1): {Vector2D(1, 2), Vector2D(1, 0), Vector2D(2, 1)},
                     Vector2D(1, 2): {Vector2D(0, 2), Vector2D(1, 1), Vector2D(2, 2)},
                     Vector2D(2, 0): {Vector2D(1, 0), Vector2D(3, 0), Vector2D(2, 1)},
                     Vector2D(2, 1): {Vector2D(2, 2), Vector2D(2, 0), Vector2D(1, 1)},
                     Vector2D(2, 2): {Vector2D(1, 2), Vector2D(2, 1), Vector2D(3, 2)},
                     Vector2D(3, 0): {Vector2D(3, 2), Vector2D(2, 0)},
                     Vector2D(3, 2): {Vector2D(2, 2), Vector2D(3, 0)}}
               )
        return MatrixData((4, 3), region, neighbortable)
    
    def init_matr_pts(self):
        return {1: [(0, 0)], 2: [(3, 2)]}

    def init_step_func(self):
        return {'move': (self.step_move, self.reverse_move),
                'add': (self.step_add, self.reverse_add)}

    def test_win(self, player: PlayerData, value):
        """模拟并测试该点落子后的情况"""
        if self.pieces[value].num != 4:
            return self.turn_active()
        super().test_win(player, value)

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        value = active_piece.value
        self.do_add(player.name, value, [new_pt])
        self.test_win(player, 3 - value)




class App_四和棋(AppBlackWhite):
    """四和棋游戏规则"""
    def init_rule(self):
        self.name = '四和棋'
        return Game_四和棋()
    
    def grid_attr(self):
        return {'size': (4, 3), 'canvas_size': (750, 750),
                'padding': (100, 190), 'is_net': True}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 10,
            'bgedges_show': AxisEnum.Y,
            'canvas_lines': [((0, 0), (3, 0)), 
                ((0, 2), (3, 2)), ((1, 1), (2, 1))]}





class Game_两三步困阻棋(Game_憋死牛):
    """两三步困阻棋"""
    def init_matr(self):
        region = RegionRect((5, 5))
        neighbortable = NeighborTable.structure_only({region: 4, RegionPoints(((2, 1), (1, 2), (3, 2), (2, 3))): 8})
        neighbortable.add_mathvector_map({RegionPoints(((0, 1), (1, 0), (3, 4), (4, 3))): {(1, 1), (-1, -1)},
                                         RegionPoints(((0, 3), (3, 0), (1, 4), (4, 1))): {(-1, 1), (1, -1)}})
        return MatrixData((5, 5), region, neighbortable)
    
    def init_matr_pts(self):
        return {1: [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (4, 1)],
                                  2: [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (0, 3), (4, 3)]}

    def get_move_links(self, old_pt, new_pt):
        nbs = self.matr.get_point_value_nbrs(old_pt, 0)
        nb_dict = {}
        for nb in nbs:
            nbs2 = self.matr.get_point_value_nbrs(nb, 0)
            if new_pt in nbs2:
                return [(old_pt, nb, new_pt)]
            nb_dict[nb] = nbs2
        for nb in nb_dict:
            for nb2 in nb_dict[nb]:
                if new_pt in self.matr.get_point_value_nbrs(nb2, 0):
                    return [(old_pt, nb, nb2, new_pt)]
        return []



class App_两三步困阻棋(AppBlackWhite):
    """两三步困阻棋游戏规则"""
    def init_rule(self):
        self.name = '两三步困阻棋'
        return Game_两三步困阻棋()
    
    def grid_attr(self):
        return {'size': (5, 5), 'canvas_size': (750, 750),
                'padding': (110, 110), 'is_net': True}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 7,
            'bgedges_show': AxisEnum.XY,
            'canvas_lines': [((0, 1), (3, 4)), ((1, 0), (4, 3)),
                             ((0, 3), (3, 0)), ((1, 4), (4, 1))]}






class Game_牵制棋(GameBlackWhite):
    """牵制棋"""
    def init_temporary(self):
        return {'step' : 0}

    def init_matr(self):
        return MatrixData((5, 6), 4)
    
    def init_matr_pts(self):
        return {1: [(i, j) for i in range(5) for j in range(2) if i != 2],
                                  2: [(i, j+4) for i in range(5) for j in range(2) if i != 2]}

    def get_move_links(self, old_pt, new_pt):# 计算当前回合要求的步数
        prev_step = self.temporary.get('step', 0)
        if prev_step == 0 and self.matr.get_point_value_nbrs(old_pt, 0):
            return [self.matr.search_shortest_path(old_pt, new_pt, False,
                                lambda pt, p: self.matr.get_value(p) == 0)]
        step = 1 if prev_step == 9 else prev_step + 1
        if (link := self.test_step(old_pt, new_pt, step)):
            self.temporary['step'] = step
            return [link]
        return []

    def test_step( self, old_pt, new_pt, step):
        if step == 1 and new_pt in self.matr.get_point_nbrs(old_pt):
            return (old_pt, new_pt)
        # BFS状态：(当前位置, 已走步数, 路径, 访问集合)
        queue = deque([(old_pt, 0, [old_pt], {old_pt})])
        while queue:
            pt, curr_steps, path, visited = queue.popleft()
            if curr_steps == step:
                if pt == new_pt:
                    return tuple(path)
                continue
            for neighbor in self.matr.get_point_value_nbrs(pt, 0):
                if neighbor in visited:
                    continue
                new_visited = visited | {neighbor}
                new_path = path + [neighbor]
                queue.append((neighbor, curr_steps + 1, new_path, new_visited))
        return []



class App_牵制棋(AppBlackWhite):
    """牵制棋游戏规则"""
    def init_rule(self):
        self.name = '牵制棋'
        return Game_牵制棋()
    
    def grid_attr(self):
        return {'size': (5, 6), 'canvas_size': (650, 750),
                'padding': (110, 110), 'is_net': False}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null, 'thickness': 7,
            'bgedges_show': AxisEnum.XY}







class Game_连步棋(Game_牵制棋):
    """连步棋"""
    def init_matr(self):
        return MatrixData((4, 7), 4)
    
    def init_matr_pts(self):
        return {1: [(i, 0) for i in range(4)],
                2: [(i, 6) for i in range(4)]}

    def get_move_links(self, old_pt, new_pt):
        coll = self.matr.collection(self.matr.get_point_nbrs(old_pt))
        step = len(coll.get(1, [])) + len(coll.get(2, []))
        if step == 0: step = 1
        if (link := self.test_step(old_pt, new_pt, step)):
            return [link]
        return []



class App_连步棋(AppBlackWhite):
    """连步棋游戏规则"""
    def init_rule(self):
        self.name = '连步棋'
        return Game_连步棋()
    
    def grid_attr(self):
        return {'size': (4, 7), 'canvas_size': (550, 750),
                'padding': (110, 110), 'is_net': False}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null, 'thickness': 7,
            'bgedges_show': AxisEnum.XY}






class Game_折行棋(Game_憋死牛):
    """折行棋"""
    def init_matr(self):
        return MatrixData((6, 6), 4)

    def init_matr_pts(self):
        return {1: [(i, 0) for i in range(6)],
                2: [(i, 5) for i in range(6)]}

    def get_move_links(self, old_pt, new_pt):
        val = self.active_player.active
        if not self.test_move(val, old_pt, new_pt):
            return []
        temp = [(old_pt[0], new_pt[1]), (new_pt[0], old_pt[1])]
        if self.matr.get_value(temp[0]) == 0 and \
                (l1 := self.matr.search_line(old_pt, temp[0], val = 0, structure = 4))and \
                (l2 := self.matr.search_line(temp[0], new_pt, val = 0, structure = 4)):
            return [l1 + l2]
        if self.matr.get_value(temp[1]) == 0 and \
                (l1 := self.matr.search_line(old_pt, temp[1], val = 0, structure = 4))and \
                (l2 := self.matr.search_line(temp[1], new_pt, val = 0, structure = 4)):
            return [l1 + l2]
        return []

    def test_move(self, val, pt1, pt2):
        if pt1[0] == pt2[0]:
            return False
        if val == 1 and pt2[1] > pt1[1]:
            return True
        if val == 2 and pt2[1] < pt1[1]:
            return True
        return False



class App_折行棋(AppBlackWhite):
    """折行棋游戏规则"""
    def init_rule(self):
        self.name = '折行棋'
        return Game_折行棋()
    
    def grid_attr(self):
        return {'size': (6, 6), 'canvas_size': (750, 750),
                'padding': (110, 110), 'is_net': False}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null, 'thickness': 7,
            'bgedges_show': AxisEnum.XY}




class Game_八角棋(Game_憋死牛):
    """八角棋"""
    def init_matr(self):
        region = RegionPoints([(2, 2), (0, 1), (1, 4), (3, 0), (4, 3), (0, 3), (1, 0), (3, 4), (4, 1)])
        neighbortable = NeighborTable.link_only(
                    {Vector2D(0, 1): {Vector2D(0, 3), Vector2D(1, 0), Vector2D(2, 2)},
                    Vector2D(0, 3): {Vector2D(0, 1), Vector2D(1, 4), Vector2D(2, 2)},
                    Vector2D(1, 0): {Vector2D(0, 1), Vector2D(3, 0), Vector2D(2, 2)},
                    Vector2D(1, 4): {Vector2D(0, 3), Vector2D(3, 4), Vector2D(2, 2)},
                    Vector2D(3, 0): {Vector2D(1, 0), Vector2D(4, 1), Vector2D(2, 2)},
                    Vector2D(3, 4): {Vector2D(1, 4), Vector2D(4, 3), Vector2D(2, 2)},
                    Vector2D(4, 1): {Vector2D(0, 3), Vector2D(4, 3), Vector2D(2, 2)},
                    Vector2D(4, 3): {Vector2D(4, 1), Vector2D(3, 4), Vector2D(2, 2)},
                    Vector2D(2, 2): {Vector2D(0, 1), Vector2D(1, 4), Vector2D(3, 0),
                                     Vector2D(4, 3), Vector2D(0, 3), Vector2D(1, 0),
                                     Vector2D(3, 4), Vector2D(4, 1)}}
               )
        return MatrixData((5, 5), region, neighbortable)
    
    def init_matr_pts(self):
        return {1: [(0, 1), (1, 4), (3, 0), (4, 3)],
                                  2: [(0, 3), (1, 0), (3, 4), (4, 1)]}



class App_八角棋(AppBlackWhite):
    """八角棋游戏规则"""
    def init_rule(self):
        self.name = '八角棋'
        return Game_八角棋()
    
    def grid_attr(self):
        return {'size': (5, 5), 'canvas_size': (750, 750),
                'padding': (100, 80), 'is_net': True}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 10,
            'bgedges_show': AxisEnum.Null,
            'canvas_lines': [((0, 1), (1, 0)), ((1, 0), (3, 0)), ((3, 0), (4, 1)),
                             ((4, 1), (4, 3)), ((4, 3), (3, 4)), ((3, 4), (1, 4)),
                             ((1, 4), (0, 3)), ((0, 3), (0, 1))],
            'cell_tags': [(2, 2)], 'tagicon': Path(__file__).parent/'images/圈.svg', 'iconsize': (200, 200)}

