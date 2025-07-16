
from .wuziqi import *



class Game_反五子棋(GameBlackWhite):
    """反五子棋"""
    def init_pieceattr_group(self):
        return {"placeable": True, "moverules": [MoveRuleEnum.Omove]}
    
    def init_matr(self):
        return MatrixData((15, 15), structure = 8)

    def init_step_func(self):
        return {'add': (self.step_add, self.reverse_add),
                'move': (self.step_move, self.reverse_move)}

    def test_win1(self, player: PlayerData, pt):
        """判断是否存在连子"""
        orows = self.matr.search_in_row(pt, 5)
        if bool(rows := matrixgrid.flatten_as_vector(orows)) and not self.move_manager.is_over:
            self.update_tag_pts(player.name, rows, "Lose")
            self.do_game_over(player.name, GameOverEnum.Lose)
        self.turn_active()

    def test_win2(self, player: PlayerData, new_pt, old_pt, new_val):
        """判断是否存在连子"""
        orows = self.matr.search_in_row(new_pt, 5)
        if bool(rows := matrixgrid.flatten_as_vector(orows)) and not self.move_manager.is_over:
            self.update_tag_pts(player.name, rows, "Lose")
            self.do_game_over(player.name, GameOverEnum.Win)
        self.do_add(player.name, new_val, [old_pt], follow = True)
        self.test_win1(player, old_pt)

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        self.do_add(player.name, active_piece.value, [new_pt], follow = False)
        self.test_win1(player, new_pt)

    def move_other_nil(self, player: PlayerData, active_piece: 'PieceData', old_pt, new_pt):
        """移动到; 落子"""
        if not self.matr.search_line(old_pt, new_pt, 0, 8):
            return self.update_tag_pts(player.name, [], "Move")
        self.do_move(player.name, active_piece.value, [(old_pt, new_pt)])
        self.test_win2(player, new_pt, old_pt, player.get_active())

    def do_add(self, player_name: str, val, pts, follow):
        """绘制棋盘上的棋子"""
        if follow:
            self.add_move(player_name, 'add', val, pts)
        else:
            self.move_over(player_name, 'add', val, pts)
        self.step_add(player_name, (val, pts))




class App_反五子棋(App_五子棋):
    """反五子棋游戏规则"""
    def init_rule(self):
        self.name = '反五子棋'
        return Game_反五子棋()





class Game_玉攻棋(Game_五子棋):
    """玉攻棋"""
    def init_step_func(self):
        return {'add': (self.step_add, self.reverse_add),
                'remove': (self.step_remove, self.reverse_remove)}

    def pincer_test(self, player: PlayerData, value, pt):
        rows = self.matr.search_pincer(pt, 3 - value, value)
        nrows = [r for row in rows if len(r := row[1:-1]) == 2]
        pts = matrixgrid.flatten_as_vector(nrows)
        player.score += len(pts)
        return pts

    def test_win2(self, player: PlayerData):
        if player.score >= 10:
            self.do_game_over(player.name, GameOverEnum.Win)

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        value = active_piece.value
        if (pts := self.pincer_test(player, value, new_pt)):
            self.do_remove(player.name, 3-value, pts)
            self.test_win2(player)
        self.do_add(player.name, value, [new_pt])
        self.test_win(player, new_pt)



class App_玉攻棋(App_五子棋):
    """玉攻棋游戏规则"""
    def init_rule(self):
        self.name = '玉攻棋'
        return Game_玉攻棋()








class Game_旋转五子棋(GameBlackWhite):
    """旋转五子棋"""
    def init_temporary(self):
        return {'rotated': {'黑': True, '白': True}}

    def init_matr(self):
        return MatrixData((6, 6), 8)

    def init_step_func(self):
        return {'add': (self.step_add, self.reverse_add), 
                'rotate': (self.step_rotate, self.reverse_rotate)}

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        if self.temporary['rotated'][player.name]:
            self.do_add(player.name, active_piece.value, [new_pt])
            self.temporary['rotated'][player.name] = False

    def test_win(self, player: PlayerData, bl):
        """判断是否存在连子"""
        result = {1: set(), 2: set()}
        for pt in bl:
            if bool(rows := matrixgrid.flatten_as_vector(self.matr.search_in_row(pt, 5))):
                if (val := self.matr.get_value(pt)):
                    result[val].update(rows)
        if bool(rows := result[player.active]):
            self.update_tag_pts(player.name, rows, "Win")
            self.do_game_over(player.name, GameOverEnum.Win)
        elif bool(rows := result[3 - player.active]):
            self.update_tag_pts(player.name, rows, "Lose")
            self.do_game_over(player.name, GameOverEnum.Lose)
        self.turn_active()

    def move_site(self, player: PlayerData, pt):
        """移子击杀；选中棋子"""
        if self.temporary['rotated'][player.name]:
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
        self.temporary['rotated'][player.name] = True
        block = self.get_block(xc, yc)
        self.do_rotate(player.name, block, (matrixgrid.as_vector(block[0])+block[-1])//2, r)
        for k,v in self.move_manager.history.current_move_data:
            if k == 'add':
                self.test_win(player, block + v[1])
                return

    def do_rotate(self, player_name: str, block, origin, r):
        self.add_move(player_name, 'rotate', block, origin, r)
        self.step_rotate(player_name, (block, origin, r))

    def step_rotate(self, player_name: str, block_origin_r):
        self.update_tag_pts(player_name, [], "Add")
        pts_links = [(pt, matrixgrid.point_rotate(pt, block_origin_r[1], block_origin_r[2]))
                     for pt in block_origin_r[0]]
        self.move_manager.links_move(pts_links)

    def reverse_rotate(self, player_name: str, block_origin_r):
        self.update_tag_pts(player_name, [], "Add")
        pts_links = [(pt, matrixgrid.point_rotate(pt, block_origin_r[1], -block_origin_r[2]))
                     for pt in block_origin_r[0]]
        self.move_manager.links_move(pts_links)

    def get_block(self, xc, yc):
        func = lambda i,j: Vector2D(i, j)
        return matrixgrid.flatten_as_vector(matrixgrid.array2d_slice(self.matr.array2d, xc, yc, func))




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




class Game_双线五子棋(Game_五子棋):
    """双线五子棋"""
    def init_temporary(self):
        return {'pt': {'黑': None, '白': None}}

    def init_move_turns(self):
        self.players_manager.move_turns.active_turn = 1
        return [player.name for player in self.init_players() for _ in range(2)]
    
    def init_matr(self):
        return MatrixData((15, 15), structure = 8)

    def test_win(self, player: PlayerData, pt: Vector2D):
        """判断是否存在连子"""
        opt = self.temporary['pt'][player.name]
        if opt:
            self.temporary['pt'][player.name] = None
        else:
            self.temporary['pt'][player.name] = pt
        if opt and (pt.is_diagonal(opt) or pt.is_lattice(opt)):
            self.update_tag_pts(player.name, [pt, opt], "Lose")
            self.do_game_over(player.name, GameOverEnum.Lose)
        orows = self.in_row(pt, n = 5)
        if bool(rows := matrixgrid.flatten_as_vector(orows)):
            self.update_tag_pts(player.name, rows, "Win")
            self.do_game_over(player.name, GameOverEnum.Win)
        self.turn_active()




class App_双线五子棋(App_五子棋):
    """双线五子棋游戏规则"""
    def init_rule(self):
        self.name = '双线五子棋'
        return Game_双线五子棋()




class ThreesUi(DefaultPiecesUi):
    def set_data(self, data, radius = 0):
        self.piecedata = data
        self.pieceui[1] = PieceUi(
                color = PieceColor(color = (255, 255, 255, 200),
                                   fill = (20, 20, 20, 200),
                                   gradient = (50, 50, 50, 170)),
                text = PieceText(text = '黑',
                                 height = 20,
                                 color = (255, 255, 255, 200)),
                radius = radius
               )
        self.pieceui[2] = PieceUi(
                color = PieceColor(color = (0, 0, 0, 200),
                                   fill = (255, 255, 255, 200),
                                   gradient = (225, 225, 225, 170)),
                text = PieceText(text = '白',
                                 height = 20,
                                 color = (0, 0, 0, 200)),
                radius = radius
               )
        self.pieceui[3] = PieceUi(
                color = PieceColor(color = (0, 0, 0, 200),
                                   fill = (125, 125, 125, 200),
                                   gradient = (105, 105, 105, 170)),
                text = PieceText(text = '灰',
                                 height = 20,
                                 color = (0, 0, 0, 200)),
                radius = radius
               )



class Game_同步五子棋(GameBlackWhite):
    """同步五子棋"""
    def init_players(self):
        return [self.player_black(), self.player_white(), self.player_same()]

    def player_same(self, **kwargs):
        """黑棋玩家"""
        player = self.player_define(**{'name': '灰', **kwargs})
        player.add_piece(self.piece_define(value = 3, name = '灰'))
        return player

    def init_temporary(self):
        return {'pt': None}

    def init_matr(self):
        return MatrixData((15, 15), structure = 8)

    def init_step_func(self):
        return {'adds': (self.step_adds, self.reverse_adds)}

    def test_win(self, pl1: PlayerData, pt1, pl2: PlayerData, pt2):
        """判断是否存在连子"""
        row1 = matrixgrid.flatten_as_vector(self.matr.search_in_row(pt1, 5))
        row2 = matrixgrid.flatten_as_vector(self.matr.search_in_row(pt2, 5))
        if len(row1) > len(row2):
            self.update_tag_pts(pl1.name, row1, "Win")
            self.do_game_over(pl1.name, GameOverEnum.Win)
        elif len(row1) < len(row2):
            self.update_tag_pts(pl2.name, row2, "Win")
            self.do_game_over(pl2.name, GameOverEnum.Win)
        elif len(row1) > 0:
            same = "灰"
            self.step_change(same, (pl1.active, 3, row1))
            self.step_change(same, (pl2.active, 3, row2))
            self.move_over(same, 'change', pl1.active, 3, row1)
            self.add_move(same, 'change', pl1.active, 3, row2)

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        same = "灰"
        if self.temporary.get('pt', None) is None:
            self.temporary['pt'] = new_pt
        else:
            pt1 = self.temporary['pt']
            self.temporary['pt'] = None
            if pt1 == new_pt:
                self.do_add(same, {3: [new_pt]})
            else:
                val1 = 3 - active_piece.value
                pl1 = self.players_manager.get_player(val1)
                self.do_add(same, {val1: [pt1], active_piece.value: [new_pt]})
                self.test_win(pl1, pt1, player, new_pt)
        self.turn_active()
        if self.active_player_name == same:
            self.turn_active()



class App_同步五子棋(App_五子棋):
    """同步五子棋游戏规则"""
    def init_rule(self):
        self.name = '同步五子棋'
        return Game_同步五子棋()
    
    def init_pieceuis(self):
        return ThreesUi()


