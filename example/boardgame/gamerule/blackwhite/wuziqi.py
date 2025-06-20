
from .blackwhite import PlayerBlackWhite, AppBlackWhite
from ...gridrule import *



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
        if bool(rows := matrixgrid.flatten_as_vector(self.in_row(pt))):
            self.update_tag_pts(player, rows, PieceTagEnum.Win)
            self._step_game_over(player, GameOverEnum.Win)
        self.turn_active(player = player)

    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        self._step_add(player, active_piece.value, [new_pt])
        self.test_win(player, new_pt)



class Game_五子棋(GameData):
    """五子棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((15, 15), structure = 8)}

    def init_move_manager(self):
        return Move_五子棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': True})



class App_五子棋(AppBlackWhite):
    """五子棋游戏规则"""
    def init_rule(self):
        self.name = '五子棋'
        return Game_五子棋()
    
    def grid_attr(self):
        return {'size': (15, 15), 'canvas_size': (750, 750),
                'padding': (80, 80), 'is_net': True}
    
    def canvas_attr(self):
        return {'star_show': True, 'show_piece_index': True}




class Move_六连棋(Move_五子棋):
    """六连棋"""
    def test_win(self, player, pt):
        """判断是否存在连子"""
        orows = self.in_row(pt, n = 6)
        if bool(rows := matrixgrid.flatten_as_vector(orows)):
            self.update_tag_pts(player, rows, PieceTagEnum.Win)
            self._step_game_over(player, GameOverEnum.Win)
        if player.temporary['move_num'] <= 1:
            player.temporary['move_num'] = 2
            self.turn_active(player = player)
        else:
            player.temporary['move_num'] -= 1



class Player_六连棋(PlayerBlackWhite):
    def init_player_temporary(self):
        return {'黑':{'move_num': 1}, '白':{'move_num': 2}}
    
    def init_pieceattr_group(self):
        return {'placeable': True}




class Game_六连棋(GameData):
    """六连棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((15, 15), structure = 8)}

    def init_move_manager(self):
        return Move_六连棋(self)

    def init_player_manager(self):
        return Player_六连棋(self)



class App_六连棋(App_五子棋):
    """六连棋游戏规则"""
    def init_rule(self):
        self.name = '六连棋'
        return Game_六连棋()




class Move_反五子棋(Move_五子棋):
    """反五子棋"""
    def init_data(self):
        self.step_func = {'add': self.step_add, 'move': self.step_move}
        self.reverse_func = {'add': self.reverse_add, 'move': self.reverse_move}

    def test_win1(self, player, pt):
        """判断是否存在连子"""
        orows = self.in_row(pt)
        if bool(rows := matrixgrid.flatten_as_vector(orows)) and not self.grid.over:
            self.update_tag_pts(player, rows, PieceTagEnum.Lose)
            self._step_game_over(player, GameOverEnum.Lose)
        self.turn_active(player = player)

    def test_win2(self, player, new_pt, old_pt, val):
        """判断是否存在连子"""
        orows = self.in_row(new_pt)
        if bool(rows := matrixgrid.flatten_as_vector(orows)) and not self.grid.over:
            self.update_tag_pts(player, rows, PieceTagEnum.Lose)
            self._step_game_over(player, GameOverEnum.Win)
        self._step_add(player, val, [old_pt], follow = True)
        self.test_win1(player, old_pt)

    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        self._step_add(player, active_piece.value, [new_pt], follow = False)
        self.test_win1(player, new_pt)

    def move_other_nil(self, player, active_piece, old_pt, old_val, new_pt):
        """移动到; 落子"""
        if not self.matr.search_line(old_pt, new_pt, 0, 8):
            return self.update_tag_pts(player, [], PieceTagEnum.Move)
        self._step_move(player, old_val, [(old_pt, new_pt)])
        self.test_win2(player, new_pt, old_pt, active_piece.value)

    def _step_add(self, player, val, pts, follow):
        """绘制棋盘上的棋子"""
        if follow:
            self.add_move(player, 'add', val, pts)
        else:
            self.move_over(player, 'add', val, pts)
        self.step_add(player, val, pts)



class Game_反五子棋(GameData):
    """反五子棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((15, 15), structure = 8)}

    def init_move_manager(self):
        return Move_反五子棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': True,
                        'movable': [MoveRuleEnum.Omove]})



class App_反五子棋(App_五子棋):
    """反五子棋游戏规则"""
    def init_rule(self):
        self.name = '反五子棋'
        return Game_反五子棋()







class Move_重力四子棋(Move_五子棋):
    """重力四子棋"""
    def in_row(self, pt):
        """判断是否存在连子"""
        return self.matr.search_in_row(pt, n = 4)

    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        pt0 = self.matr.mapping_point((new_pt[0], 0))
        npt = self.matr.search_value_vector(pt0, Vector2D(0,1), 0)[-1]
        self._step_add(player, active_piece.value, pt0, npt)
        self.test_win(player, npt)

    def _step_add(self, player, val, pt0, npt):
        """绘制棋盘上的棋子"""
        self.move_over(player, 'add', val, [npt])
        self.add_pts_piece(player, [pt0], val = val)
        self.move_piece_pts([(pt0, npt)])



class Game_重力四子棋(GameData):
    """重力四子棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((7, 6), structure = 8)}

    def init_move_manager(self):
        return Move_重力四子棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': True})



class App_重力四子棋(AppBlackWhite):
    """重力四子棋游戏规则"""
    def init_rule(self):
        self.name = '重力四子棋'
        return Game_重力四子棋()
    
    def grid_attr(self):
        return {'size': (7, 6), 'canvas_size': (750, 750),
                'padding': (80, 80), 'is_net': False}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null}




class Move_斜胜棋(MoveManager):
    """斜胜棋"""
    def init_data(self):
        self.step_func = {'move': self.step_move, 'kill': self.step_kill}
        self.reverse_func = {'move': self.reverse_move, 'kill': self.reverse_kill}
    
    def _game_win(self, player, pts):
        self.update_tag_pts(player, pts, PieceTagEnum.Win)
        self._step_game_over(player, GameOverEnum.Win)
        if pts:
            self.turn_active(player = player)

    def test_win(self, player, piece, pt):
        """模拟并测试该点落子后的情况"""
        if self.player_manager.pieces[3 - piece.value].num == 0:
            return self._game_win(player, [])
        pts1 = self.matr.search_value_axis_pairs(pt, 3, piece.value, True)
        pts2 = self.matr.search_value_axis_pairs(pt, 4, piece.value, True)
        pts = pts1 if len(pts1) > len(pts2) else pts2
        if len(pts) == piece.num and not self.grid.over:
            if piece.num >= 4:
                return self._game_win(player, pts)
            elif piece.num >= 2:
                for p in pts:
                    if p[0] in [0, 4]:
                        return self._game_win(player, pts)
            else:
                for p in pts:
                    if p[0] in [0, 4] and p[1] in [0, 4]:
                        return self._game_win(player, pts)
        self.turn_active(player = player)

    def move_self_nil(self, player: 'PlayerData', active_piece, old_pt, new_pt):
        if old_pt not in self.matr.get_point_nbrs(new_pt):
            return self.update_tag_pts(player, [], PieceTagEnum.Move)
        self._step_move(player, active_piece.value, [(old_pt, new_pt)])
        self.test_win(player, active_piece, new_pt)

    def move_self_other(self, player: 'PlayerData', active_piece, old_pt, new_pt, new_val):
        if old_pt not in self.matr.get_point_nbrs(new_pt):
            return self.update_tag_pts(player, [], PieceTagEnum.Move)
        self._step_kill(player, active_piece.value, new_val, [(old_pt, new_pt)])
        if (p := self.matr.search_value(new_val)):
            if (q := p.__iter__().__next__()):
                piece = self.player_manager.pieces[new_val]
                self.test_win(piece.player, piece, q)
        self.test_win(player, active_piece, new_pt)



class Game_斜胜棋(GameData):
    """斜胜棋"""
    def init_gridattr(self):
        self.default_piece_pts = { 1: [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
                                2: [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]}
        return {'matr': MatrixP((5, 5), structure = 4)}

    def init_move_manager(self):
        return Move_斜胜棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': False,
                        'movable': [MoveRuleEnum.Move, MoveRuleEnum.Kill]})



class App_斜胜棋(AppBlackWhite):
    """斜胜棋游戏规则"""
    def init_rule(self):
        self.name = '斜胜棋'
        return Game_斜胜棋()
    
    def grid_attr(self):
        return {'size': (5, 5), 'canvas_size': (750, 750),
                'padding': (130, 130), 'is_net': False}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null, 'show_piece_index': True}




class Move_玉攻棋(Move_五子棋):
    """玉攻棋"""
    def init_data(self):
        self.step_func = {'add': self.step_add, 'remove': self.step_remove}
        self.reverse_func = {'add': self.reverse_add, 'remove': self.reverse_remove}

    def pincer_test(self, player, value, pt):
        rows = self.matr.search_pincer(pt, 3 - value, value)
        nrows = [r for row in rows if len(r := row[1:-1]) == 2]
        pts = matrixgrid.flatten_as_vector(nrows)
        player.score += len(pts)
        return pts

    def test_win2(self, player):
        if player.score >= 10:
            self._step_game_over(player, GameOverEnum.Win)

    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        value = active_piece.value
        if (pts := self.pincer_test(player, value, new_pt)):
            self._step_remove(player, 3-value, pts)
            self.test_win2(player)
        self._step_add(player, value, [new_pt])
        self.test_win(player, new_pt)



class Game_玉攻棋(Game_五子棋):
    """玉攻棋"""
    def init_move_manager(self):
        return Move_玉攻棋(self)



class App_玉攻棋(App_五子棋):
    """玉攻棋游戏规则"""
    def init_rule(self):
        self.name = '玉攻棋'
        return Game_玉攻棋()






class Move_三六九棋(Move_五子棋):
    """三六九棋"""
    def compute_score(self, player, pt, n):
        """计算得分"""
        rows = self.in_row(pt, n = n)
        for row in rows:
            if len(row) != n:
                continue
            flag = False
            for _row in player.temporary[f'rows{n}']:
                if row[0] in _row and row[1] in _row:
                    flag = True
                    break
            if not flag:
                player.temporary[f'rows{n}'].append(row)
                self.update_tag_pts(player, row, PieceTagEnum.Win)
                player.score += n

    def test_win(self, player, pt):
        """判断是否存在连子"""
        self.compute_score(player, pt, 3)
        self.compute_score(player, pt, 6)
        self.compute_score(player, pt, 9)
        if player.name == '黑' and player.pieces[1].num >= 41:
            other = self.player_manager.get_player(name = '白')
            if player.score >= other.score:
                self._step_game_over(player, GameOverEnum.Win)
        self.turn_active(player = player)



class Player_三六九棋(PlayerBlackWhite):
    def init_player_temporary(self):
        return {'黑':{'rows3': [], 'rows6': [], 'rows9': []},
                '白':{'rows3': [], 'rows6': [], 'rows9': []}}
    
    def init_pieceattr_group(self):
        return {'placeable': True}


class Game_三六九棋(GameData):
    """三六九棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((9, 9), structure = 8)}

    def init_move_manager(self):
        return Move_三六九棋(self)

    def init_player_manager(self):
        return Player_三六九棋(self)




class App_三六九棋(AppBlackWhite):
    """三六九棋游戏规则"""
    def init_rule(self):
        self.name = '三六九棋'
        return Game_三六九棋()
    
    def grid_attr(self):
        return {'size': (9, 9), 'canvas_size': (750, 750),
                'padding': (80, 80), 'is_net': True}
    
    def canvas_attr(self):
        return {'star_show': True, 'show_piece_index': True}




class Move_旋转五子棋(MoveManager):
    """旋转五子棋"""
    def init_data(self):
        self.step_func = {'add': self.step_add, 'rotate': self.step_rotate}
        self.reverse_func = {'add': self.reverse_add, 'rotate': self.reverse_rotate}

    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        if player.temporary['rotated']:
            self._step_add(player, active_piece.value, [new_pt])
            player.temporary['rotated'] = False

    def test_win(self, player, bl):
        """判断是否存在连子"""
        result = {1: set(), 2: set()}
        for pt in bl:
            if bool(rows := matrixgrid.flatten_as_vector(self.matr.search_in_row(pt, 5))):
                if (val := self.matr.get_value(pt)):
                    result[val].update(rows)
        if bool(rows := result[player.active]):
            self.update_tag_pts(player, rows, PieceTagEnum.Win)
            self._step_game_over(player, GameOverEnum.Win)
        elif bool(rows := result[3 - player.active]):
            self.update_tag_pts(player, rows, PieceTagEnum.Lose)
            self._step_game_over(player, GameOverEnum.Lose)
        self.turn_active(player = player)

    def move_button(self, player, pt):
        """移子击杀；选中棋子"""
        if player.temporary['rotated']:
            return
        xc = yc = (0, 0, 1)
        if pt[0] in [-1, 1]:
            xc = (0, 3, 1)
        elif pt[0] in [4, 6]:
            xc = (3, 6, 1)
        if pt[1] in [-1, 1]:
            yc = (0, 3, 1)
        elif pt[1] in [4, 6]:
            yc = (3, 6, 1)
        r = 0
        if pt in [(-1, 1), (4, -1), (1, 6), (6, 4)]:
            r = -1j
        elif pt in [(1, -1), (-1, 4), (6, 1), (4, 6)]:
            r = 1j
        else:
            return
        player.temporary['rotated'] = True
        block = self.get_block(xc, yc)
        self._step_rotate(player, block, (matrixgrid.as_vector(block[0])+block[-1])//2, r)
        for k,v in self.grid.history.current_data:
            if k == 'add':
                self.test_win(player, block + v[1])
                return

    def _step_rotate(self, player, block, origin, r):
        self.step_rotate(player, block, origin, r)
        self.add_move(player, 'rotate', block, origin, r)

    def step_rotate(self, player, block, origin, r):
        self.update_tag_pts(player, [], PieceTagEnum.Add)
        pts_links = [(pt, matrixgrid.point_rotate(pt, origin, r))
                     for pt in block]
        self.move_piece_pts(pts_links)

    def reverse_rotate(self, player, block, origin, r):
        self.update_tag_pts(player, [], PieceTagEnum.Add)
        pts_links = [(pt, matrixgrid.point_rotate(pt, origin, -r))
                     for pt in block]
        self.move_piece_pts(pts_links)

    def get_block(self, xc, yc):
        func = lambda i,j: Vector2D(i, j)
        return matrixgrid.flatten_as_vector(matrixgrid.array2d_slice(self.matr.array2d, xc, yc, func))



class Player_旋转五子棋(PlayerBlackWhite):
    def init_player_temporary(self):
        return {'黑':{'rotated': True}, '白':{'rotated': True}}
    
    def init_pieceattr_group(self):
        return {'placeable': True}


class Game_旋转五子棋(GameData):
    """旋转五子棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((6, 6), 8)}

    def init_move_manager(self):
        return Move_旋转五子棋(self)

    def init_player_manager(self):
        return Player_旋转五子棋(self)



class App_旋转五子棋(AppBlackWhite):
    """旋转五子棋游戏规则"""
    def init_rule(self):
        self.name = '旋转五子棋'
        return Game_旋转五子棋()
    
    def grid_attr(self):
        return {'size': (6, 6), 'canvas_size': (750, 750),
                'padding': (80, 80), 'is_net': False}
    
    def canvas_attr(self):
        cells = [(i, j) for i in range(3) for j in range(3)]
        cells.extend([(i, j) for i in range(3, 6) for j in range(3, 6)])
        return {'coor_show': LinePositionEnum.Null, 'star_show': False,
                'bgedges_show': AxisEnum.XY, 'canvas_cells': cells, 
                'cell_tags': [(-1, 1), (-1, 4), (6, 1), (6, 4),
                    (1, -1), (4, -1), (1, 6), (4, 6)],
                'tagtextfunc': self.tag_func}
    
    def tag_func(self, pt):
        if pt in [(-1, 4), (6, 4)]:
            return '↑'
        elif pt in [(-1, 1), (6, 1)]:
            return '↓'
        elif pt in [(1, -1), (1, 6)]:
            return '→'
        elif pt in [(4, -1), (4, 6)]:
            return '←'




class Move_九宫棋(MoveManager):
    """九宫棋"""
    def init_data(self):
        self.step_func = {'move': self.step_move, 'add': self.step_add}
        self.reverse_func = {'move': self.reverse_move, 'add': self.reverse_add}

    def test_win(self, player, pt):
        """判断是否存在连子"""
        if bool(rows := matrixgrid.flatten_as_vector(self.matr.search_in_row(pt, 3))):
            self.update_tag_pts(player, rows, PieceTagEnum.Win)
            self._step_game_over(player, GameOverEnum.Win)
        self.turn_active(player = player)

    def move_self_nil(self, player: 'PlayerData', active_piece, old_pt, new_pt):
        value = active_piece.value
        if active_piece.num != 3 or old_pt not in self.matr.get_point_nbrs(new_pt):
            return self.update_tag_pts(player, [], PieceTagEnum.Move)
        self._step_move(player, value, [(old_pt, new_pt)])
        self.test_win(player, new_pt)

    def move_nil_nil(self, player, active_piece, new_pt):
        """在空点落子"""
        value = active_piece.value
        self._step_add(player, value, [new_pt])
        self.test_win(player, new_pt)



class Game_九宫棋(GameData):
    """九宫棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((3, 3), structure = 8)}

    def init_move_manager(self):
        return Move_九宫棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, piece_count = {1: 3, 2: 3},
                    pieceattr_group = {'placeable': True, 'movable': [MoveRuleEnum.Move]})



class App_九宫棋(AppBlackWhite):
    """九宫棋游戏规则"""
    def init_rule(self):
        self.name = '九宫棋'
        return Game_九宫棋()
    
    def grid_attr(self):
        return {'size': (3, 3), 'canvas_size': (750, 750),
                'padding': (130, 130), 'is_net': False}

    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null, 'thickness': 10}
    




class Move_双线五子棋(Move_五子棋):
    """双线五子棋"""
    def test_win(self, player, pt):
        """判断是否存在连子"""
        opt = player.temporary['pt']
        if player.temporary['pt'] and (pt.is_diagonal(opt) or \
                                       pt.is_lattice(opt)):
            self.update_tag_pts(player, [pt, opt], PieceTagEnum.Lose)
            self._step_game_over(player, GameOverEnum.Lose)
        orows = self.in_row(pt, n = 5)
        if bool(rows := matrixgrid.flatten_as_vector(orows)):
            self.update_tag_pts(player, rows, PieceTagEnum.Win)
            self._step_game_over(player, GameOverEnum.Win)
        if player.temporary['move_num'] <= 1:
            player.temporary['move_num'] = 2
            player.temporary['pt'] = None
            self.turn_active(player = player)
        else:
            player.temporary['move_num'] -= 1
            player.temporary['pt'] = pt





class Player_双线五子棋(PlayerBlackWhite):
    def init_player_temporary(self):
        return {'黑':{'move_num': 1, 'pt': None}, '白':{'move_num': 2, 'pt': None}}
    
    def init_pieceattr_group(self):
        return {'placeable': True}




class Game_双线五子棋(GameData):
    """双线五子棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((15, 15), structure = 8)}

    def init_move_manager(self):
        return Move_双线五子棋(self)

    def init_player_manager(self):
        return Player_双线五子棋(self)



class App_双线五子棋(App_五子棋):
    """双线五子棋游戏规则"""
    def init_rule(self):
        self.name = '双线五子棋'
        return Game_双线五子棋()





class Move_引力四子棋(Move_重力四子棋):
    """引力四子棋"""
    def init_data(self):
        self.step_func = {'add': self.step_add, 'moves': self.step_moves}
        self.reverse_func = {'add': self.reverse_add, 'moves': self.reverse_moves}

    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        if (npts := self.matr.search_value_vector(new_pt, self.grid.temporary.get('vect', Vector2D(0, 1)), 0)):
            npt = npts[-1]
        else:
            npt = new_pt
        self._step_add(player, active_piece.value, new_pt, npt)
        self.test_win(player, npt)

    def move_button(self, player, pt):
        """移子击杀；选中棋子"""
        vect = (0, 0)
        if pt[0] == -1:
            vect = Vector2D(-1, 0)
        elif pt[0] == 8:
            vect = Vector2D(1, 0)
        elif pt[1] == -1:
            vect = Vector2D(0, -1)
        elif pt[1] == 8:
            vect = Vector2D(0, 1)
        else:
            return
        self.move_over(player, 'moves', vect)
        if self.grid.temporary.get('vect', Vector2D(0, 1)) != vect:
            self.step_moves(vect)
            self.test_win2(player)
        self.grid.temporary['vect'] = vect
        self.turn_active(player = player)

    def test_win2(self, player):
        """判断是否存在连子"""
        dc = self.matr.collection()
        for pt in dc.get(player.active, []):
            if bool(rows := matrixgrid.flatten_as_vector(self.in_row(pt))):
                self.update_tag_pts(player, rows, PieceTagEnum.Win)
                self._step_game_over(player, GameOverEnum.Win)
                return
        for pt in dc.get(3 - player.active, []):
            if bool(rows := matrixgrid.flatten_as_vector(self.in_row(pt))):
                self.update_tag_pts(player, rows, PieceTagEnum.Lose)
                self._step_game_over(player, GameOverEnum.Lose)
                return

    def step_moves(self, vect):
        links = []
        def _move(pt, vect, links):
            if (val := self.grid.get_value(pt)) == 0:
                return
            if (npts := self.matr.search_value_vector(pt, vect, 0)):
                npt = npts[-1]
            else:
                return
            if npt != pt:
                self.grid.set_value(npt, val, False)
                self.grid.set_value(pt, 0, False)
                links.append((pt, npt))
        match vect.point:
            case (0, 1): # y增大
                # 每一列进行变换
                for i in range(self.grid.size[0]):
                    for j in reversed(range(self.grid.size[1])):
                        _move(Vector2D(i, j), vect, links)
            case (1, 0):
                for j in range(self.grid.size[1]):
                    for i in reversed(range(self.grid.size[0])):
                        _move(Vector2D(i, j), vect, links)
            case (0, -1):
                for i in range(self.grid.size[0]):
                    for j in range(self.grid.size[1]):
                        _move(Vector2D(i, j), vect, links)
            case (-1, 0):
                for j in range(self.grid.size[1]):
                    for i in range(self.grid.size[0]):
                        _move(Vector2D(i, j), vect, links)
        self.call_piece_signal('move', links)

    def reverse_moves(self, vect):
        self.step_moves(-vect)



class Game_引力四子棋(GameData):
    """引力四子棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((8, 8), 8)}

    def init_move_manager(self):
        return Move_引力四子棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': True})



class App_引力四子棋(AppBlackWhite):
    """引力四子棋游戏规则"""
    def init_rule(self):
        self.name = '引力四子棋'
        return Game_引力四子棋()
    
    def grid_attr(self):
        return {'size': (8, 8), 'canvas_size': (750, 750),
                'padding': (130, 130), 'is_net': False}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null, 'star_show': False,
                'bgedges_show': AxisEnum.XY, 
                'canvas_cells': [(j, i) for i in range(8) for j in (-1, 8)
                        ] + [(i, j) for i in range(8) for j in (-1, 8)]}



class Move_墨棋(Move_五子棋):
    """墨棋"""
    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        if self.grid.temporary.setdefault('steps', 0) < 2:
            self.grid.temporary['steps'] += 1
        else:
            if not self.move_test(new_pt, active_piece.value):
                return
        super().move_nil_nil(player, active_piece, new_pt)

    def move_test(self, pt, value):
        values = []
        for i in range(1, 5):
            clls = self.matr.collection(self.matr.search_endvalue_axis_pairs(pt, i, -128, True))
            s = len(clls.get(1, [])) + len(clls.get(2, []))*2
            if s == 0:
                continue
            elif s%2 == 0:
                values.append(2)
            else:
                values.append(1)
        if value in values:
            return True
        return False


class Game_墨棋(GameData):
    """墨棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((19, 19), structure = 8)}

    def init_move_manager(self):
        return Move_墨棋(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': True})



class App_墨棋(AppBlackWhite):
    """墨棋游戏规则"""
    def init_rule(self):
        self.name = '墨棋'
        return Game_墨棋()
    
    def grid_attr(self):
        return {'size': (19, 19), 'canvas_size': (750, 750),
                'padding': (60, 60), 'is_net': True}
    
    def canvas_attr(self):
        return {'star_show': True, 'show_piece_index': True}
