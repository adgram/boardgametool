from .blackwhite import PlayerBlackWhite, AppBlackWhite
from ...gridrule import *
from collections import deque


class Move_两吏拿一差(MoveManager):
    """两吏拿一差"""
    def init_data(self):
        self.step_func = {'move': self.step_move, 'remove': self.step_remove}
        self.reverse_func = {'move': self.reverse_move, 'remove': self.reverse_remove}

    def test_win(self, player, value):
        """模拟并测试该点落子后的情况"""
        if self.player_manager.pieces[value].num == 0:
            self._step_game_over(player, GameOverEnum.Lose)
        if self.player_manager.pieces[3-value].num == 0:
            self._step_game_over(player, GameOverEnum.Win)
        self.turn_active()

    def move_self_nil(self, player: 'PlayerData', active_piece, old_pt, new_pt):
        value = active_piece.value
        if not (links := self.get_move_links(active_piece, old_pt, new_pt)):
            return self.update_tag_pts(player, [], PieceTagEnum.Move)
        self._step_move(player, value, links)
        self.remove_step(player, old_pt, new_pt)
        self.test_win(player, value)

    def get_move_links(self, piece, old_pt, new_pt):
        if old_pt in self.matr.get_point_nbrs(new_pt):
            return [(old_pt, new_pt)]
        return []
    
    def remove_step(self, player, old_pt, new_pt):
        ps1 = self._remove_step(new_pt)
        ps2 = self._remove_step(old_pt)
        pts1 = ps1.get(1, []).extend(ps2.get(1, []))
        pts2 = ps1.get(2, []).extend(ps2.get(2, []))
        if pts1:
            self.step_remove(player, 1, pts1)
            self.add_move(player, 'remove', 1, pts1)
        if pts2:
            self.step_remove(player, 2, pts2)
            self.add_move(player, 'remove', 2, pts2)

    def _remove_step(self, pt):
        remvs = {1:[], 2:[]}
        pairs = self.matr.point_axis_pairs(pt)
        lines = [self.matr.search_endvalue_axis_pairs(pt, pair[0], NullValue, True) for pair in pairs]
        for line in lines:
            cl = self.matr.collection(line)
            ps1 = cl.get(1, [])
            ps2 = cl.get(2, [])
            if len(ps1) == 1 and len(ps2) == 2:
                remvs[1].append(ps1[0])
            elif len(ps2) == 1 and len(ps1) == 2:
                remvs[2].append(ps2[0])
        return remvs




class Game_两吏拿一差(GameData):
    """两吏拿一差"""
    def init_gridattr(self):
        self.default_piece_pts = {1: [(i, 0) for i in [0, 1, 3, 4, 6]],
                                  2: [(i, 4) for i in [0, 1, 3, 4, 6]]}
        pts1 = [(i, j) for i in [0, 1, 4, 6] for j in [0, 1, 3, 4]] + [(1, 2), (3, 0), (3, 4), (5, 2)]
        region = RegionPoints(pts1)
        neighbortable = NeighborTable.structure_only({region: 8})
        pts2 = [(i, j) for i in [0, 6] for j in [0, 1, 3, 4]] + [(i, j) for i in [1, 4] for j in [1, 3]]
        neighbortable.add_mathvector_map({RegionPoints(pts2): [(0, 2), (0, -2), (2, 0), (-2, 0)]})
        neighbortable.add_link_map({(2, 0): {(0, 0)}, (2, 4): {(0, 4)}, (4, 0): {(6, 0)}, (4, 4): {(6, 4)}})
        return {'matr': MatrixP((7, 5), region, neighbortable)}

    def init_move_manager(self):
        return Move_两吏拿一差(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': False,
                                        'movable': [MoveRuleEnum.Move, MoveRuleEnum.Kill]})



class App_两吏拿一差(AppBlackWhite):
    """两吏拿一差游戏规则"""
    def init_rule(self):
        self.name = '两吏拿一差'
        return Game_两吏拿一差()
    
    def grid_attr(self):
        return {'size': (7, 5), 'canvas_size': (750, 750),
                'padding': (80, 80), 'is_net': True}

    def canvas_attr(self):
        yls = [((i, 0), (i, 4)) for i in [0, 1, 4, 6]]
        yls.extend([[(0, j), (6, j)] for j in [0, 1, 3, 4]])
        return {'coor_show': LinePositionEnum.Null, 'bgedges_show': AxisEnum.Null,
            'canvas_lines': [*yls, ((0, 1), (3, 4)), ((0, 5), (3, 0)),
                             ((3, 0), (6, 5)), ((3, 4), (6, 1))]
            }


class Move_犀牛遇山羊(Move_两吏拿一差):
    """犀牛遇山羊"""
    def _remove_step(self, pt):
        remvs = {1:[], 2:[]}
        pairs = self.matr.point_axis_pairs(pt)
        lines = [self.matr.search_endvalue_axis_pairs(pt, pair[0], NullValue, True) for pair in pairs]
        for line in lines:
            cl = self.matr.collection(line)
            ps1 = cl.get(1, [])
            ps2 = cl.get(2, [])
            if len(ps1) == 1 and len(ps2) == 2:
                remvs[1].append(ps1[0])
            elif len(ps2) == 1 and len(ps1) == 2:
                remvs[2].append(ps2[0])
            elif len(ps1) == 1 and len(ps2) == 4:
                remvs[1].append(ps1[0])
            elif len(ps2) == 1 and len(ps1) == 4:
                remvs[2].append(ps2[0])
            elif len(ps1) == 2 and len(ps2) == 3:
                remvs[1].extend(ps1)
            elif len(ps2) == 2 and len(ps1) == 3:
                remvs[2].extend(ps2)
        return remvs




class Game_犀牛遇山羊(GameData):
    """犀牛遇山羊"""
    def init_gridattr(self):
        self.default_piece_pts = {1: [(i, 0) for i in range(5)] + [(0, 1), (4, 1)],
                                  2: [(i, 4) for i in range(5)] + [(0, 3), (4, 3)]}
        region = RegionRect((5, 5))
        region2 = RegionPoints([(i, j) for i in range(5) for j in range(5) if (i+j+1)%2])
        neighbortable = NeighborTable.structure_only({region: 4, region2: 8})
        return {'matr': MatrixP((5, 5), region, neighbortable)}

    def init_move_manager(self):
        return Move_犀牛遇山羊(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': False,
                                        'movable': [MoveRuleEnum.Move, MoveRuleEnum.Kill]})



class App_犀牛遇山羊(AppBlackWhite):
    """犀牛遇山羊游戏规则"""
    def init_rule(self):
        self.name = '犀牛遇山羊'
        return Game_犀牛遇山羊()
    
    def grid_attr(self):
        return {'size': (5, 5), 'canvas_size': (750, 750),
                'padding': (100, 100), 'is_net': True}

    def canvas_attr(self):
        pts = [((0, 2), (2, 4)), ((0, 0), (4, 4)), ((2, 0), (4, 2)),
               ((2, 0), (0, 2)), ((4, 0), (0, 4)), ((2, 4), (4, 2))]
        return {'coor_show': LinePositionEnum.Null,
            'bgedges_show': AxisEnum.XY,
            'canvas_lines': pts}





class Move_炮棋(Move_两吏拿一差):
    """炮棋"""
    def _remove_step(self, pt):
        value = self.matr.get_value(pt)
        ovlue = 3 - value
        if value == 0:
            return {}
        remvs = {1:[], 2:[]}
        if self.player_manager.pieces[value].num == 1:
            if self.matr.get_value(pt + (1, 0)) == ovlue and self.matr.get_value(pt + (-1, 0)) == ovlue:
                remvs[ovlue].extend([pt + (1, 0), pt + (-1, 0)])
            if self.matr.get_value(pt + (0, 1)) == ovlue and self.matr.get_value(pt + (0, -1)) == ovlue:
                remvs[ovlue].extend([pt + (0, 1), pt + (0, -1)])
            return remvs
        pts1 = self.matr.get_point_value_nbrs(pt, value)
        for n in pts1:
            v = n - pt
            if self.matr.get_value(n + v) == ovlue and self.matr.get_value(n + v + v) == 0:
                remvs[ovlue].append(n + v)
            if self.matr.get_value(pt - v) == ovlue and self.matr.get_value(pt - v - v) == 0:
                remvs[ovlue].append(pt - v)
        return remvs

    def get_move_links(self, piece, old_pt, new_pt):
        if old_pt in self.matr.get_point_nbrs(new_pt):
            return [(old_pt, new_pt)]
        if piece.num == 1:
            if new_pt[0] == old_pt[0] or new_pt[1] == old_pt[1]:
                return [(old_pt, new_pt)]
        return []



class Game_炮棋(GameData):
    """炮棋"""
    def init_gridattr(self):
        self.default_piece_pts = {1: [(i, 0) for i in range(4)] + [(0, 1), (4, 1)],
                                  2: [(i, 3) for i in range(4)] + [(0, 2), (4, 2)]}
        return {'matr': MatrixP((4, 4), structure = 4)}

    def init_move_manager(self):
        return Move_炮棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': False,
                                        'movable': [MoveRuleEnum.Move, MoveRuleEnum.Kill]})



class App_炮棋(AppBlackWhite):
    """炮棋游戏规则"""
    def init_rule(self):
        self.name = '炮棋'
        return Game_炮棋()
    
    def grid_attr(self):
        return {'size': (4, 4), 'canvas_size': (750, 750),
                'padding': (110, 110), 'is_net': True}

    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'bgedges_show': AxisEnum.XY,
            'thickness': 10}




class Move_蒸架棋之三步吃子法(Move_两吏拿一差):
    """蒸架棋之三步吃子法"""
    def init_data(self):
        self.step_func = {'move': self.step_move, 'kill': self.step_kill}
        self.reverse_func = {'move': self.reverse_move, 'kill': self.reverse_kill}

    def move_self_other(self, player: 'PlayerData', active_piece, old_pt, new_pt, new_val):
        value = active_piece.value
        if not (link := self.kill_test(player, old_pt, new_pt)):
            return self.update_tag_pts(player, [], PieceTagEnum.Move)
        self._step_kill(player, value, new_val, [link])
        self.test_win(player, value)
    
    def remove_step(self, player, old_pt, new_pt):
        pass
    
    def kill_test(self, player, old_pt, new_pt):
        if player.temporary['step'] == 0:
            return []
        if new_pt[0] == old_pt[0] and abs(new_pt[1] - old_pt[1]) == 2:
            player.temporary['step'] = 1
            return (old_pt, new_pt)
        if new_pt[1] == old_pt[1] and abs(new_pt[0] - old_pt[0]) == 2:
            player.temporary['step'] = 1
            return (old_pt, new_pt)
        return []



class Player_蒸架棋之三步吃子法(PlayerBlackWhite):
    def init_player_temporary(self):
        return {{'黑':{'step': 0}, '白':{'step': 0}}}
    
    def init_pieceattr_group(self):
        return {'placeable': False, 
                'movable': [MoveRuleEnum.Move, MoveRuleEnum.Kill]}


class Game_蒸架棋之三步吃子法(GameData):
    """蒸架棋之三步吃子法"""
    def init_gridattr(self):
        self.default_piece_pts = {1: [(i, j) for i in [1, 2] for j in [0, 1]],
                                  2: [(i, j) for i in [1, 2] for j in [2, 3]]}
        region = RegionPoints([(i, j) for i in [1, 2] for j in range(4)] + [((i, j) for i in [0, 4] for j in [1, 2])])
        return {'matr': MatrixP((4, 4), region, NeighborTable.structure_only({region: 4}))}

    def init_move_manager(self):
        return Move_蒸架棋之三步吃子法(self)

    def init_player_manager(self):
        return Player_蒸架棋之三步吃子法(self)



class App_蒸架棋之三步吃子法(AppBlackWhite):
    """蒸架棋之三步吃子法游戏规则"""
    def init_rule(self):
        self.name = '蒸架棋之三步吃子法'
        return Game_蒸架棋之三步吃子法()
    
    def grid_attr(self):
        return {'size': (4, 4), 'canvas_size': (750, 750),
                'padding': (110, 110), 'is_net': True}

    def canvas_attr(self):
        yls = [((i, 0), (i, 3)) for i in [1, 2]]
        yls.extend([((0, i), (3, i)) for i in [1, 2]])
        yls.extend([((1, i), (2, i)) for i in [0, 3]])
        yls.extend([((i, 1), (i, 2)) for i in [0, 3]])
        return {'coor_show': LinePositionEnum.Null,
            'bgedges_show': AxisEnum.Null,
            'thickness': 10, 'canvas_lines': yls}




class Move_蒸架棋之五步吃子法(Move_蒸架棋之三步吃子法):
    """蒸架棋之五步吃子法"""
    def kill_test(self, player, old_pt, new_pt):
        # BFS状态：(当前位置, 已走步数, 路径, 访问集合)
        queue = deque([(old_pt, 0, [old_pt], {old_pt})])
        while queue:
            pt, curr_steps, path, visited = queue.popleft()
            if curr_steps == 4:
                if pt == new_pt:
                    return tuple(path)
                continue
            for neighbor in self.matr.get_point_nbrs(pt):
                if neighbor in visited:
                    continue
                new_visited = visited | {neighbor}
                new_path = path + [neighbor]
                queue.append((neighbor, curr_steps + 1, new_path, new_visited))
        return []



class Game_蒸架棋之五步吃子法(Game_蒸架棋之三步吃子法):
    """蒸架棋之五步吃子法"""
    def init_move_manager(self):
        return Move_蒸架棋之五步吃子法(self)



class App_蒸架棋之五步吃子法(App_蒸架棋之三步吃子法):
    """蒸架棋之五步吃子法游戏规则"""
    def init_rule(self):
        self.name = '蒸架棋之五步吃子法'
        return Game_蒸架棋之五步吃子法()




class Move_出奇制胜棋(Move_蒸架棋之三步吃子法):
    """出奇制胜棋"""
    def test_win(self, player, value):
        """模拟并测试该点落子后的情况"""
        if self.player_manager.pieces[value].num == 0:
            self._step_game_over(player, GameOverEnum.Lose)
        if self.player_manager.pieces[3-value].num == 0:
            self._step_game_over(player, GameOverEnum.Win)
        if len(pts := self.matr.search_value(value)) == 1 and \
                pts[0] == (0, 1) and self.matr.get_point_value_nbrs(pts[0], 3 - value) == []:
            self._step_game_over(player, GameOverEnum.Lose)
        if len(pts := self.matr.search_value(3 - value)) == 1 and \
                pts[0] == (0, 1) and self.matr.get_point_value_nbrs(pts[0], value) == []:
            self._step_game_over(player, GameOverEnum.Win)
        self.turn_active()
    
    def kill_test(self, player, old_pt, new_pt):
        if new_pt in self.matr.get_point_nbrs(old_pt):
            return (old_pt, new_pt)
        return []




class Game_出奇制胜棋(GameData):
    """出奇制胜棋"""
    def init_gridattr(self):
        self.default_piece_pts = {1: [(i, 0) for i in range(3)],
                                  2: [(i, 2) for i in range(3)]}
        return {'matr': MatrixP((3, 3), structure = 4)}

    def init_move_manager(self):
        return Move_出奇制胜棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': False,
                                        'movable': [MoveRuleEnum.Move, MoveRuleEnum.Kill]})



class App_出奇制胜棋(AppBlackWhite):
    """出奇制胜棋游戏规则"""
    def init_rule(self):
        self.name = '出奇制胜棋'
        return Game_出奇制胜棋()
    
    def grid_attr(self):
        return {'size': (3, 3), 'canvas_size': (750, 750),
                'padding': (130, 130), 'is_net': False}

    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'bgedges_show': AxisEnum.XY, 'thickness': 10,
            'cell_tags': [(0, 1)], 'tagtext': '出口'}


