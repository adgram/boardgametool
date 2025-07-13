
from .wuziqi import *




class Game_重力四子棋(Game_五子棋):
    """重力四子棋"""
    def init_matr(self):
        return MatrixData((7, 6), structure = 8)

    def in_row(self, pt):
        """判断是否存在连子"""
        return self.matr.search_in_row(pt, n = 4)

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        pt0 = self.matr.mapping_point((new_pt[0], 0))
        npt = self.matr.search_value_vector(pt0, Vector2D(0,1), 0)[-1]
        self.do_add(player.name, active_piece.value, pt0, npt)
        self.test_win(player, npt)

    def do_add(self, player_name: str, val, pt0, npt):
        """绘制棋盘上的棋子"""
        self.add_move(player_name, 'add', val, [npt])
        self.move_manager.add_value_pts(player_name, [pt0], val = val)
        self.move_manager.links_move([(pt0, npt)])





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




class Game_引力四子棋(Game_重力四子棋):
    """引力四子棋"""
    def init_temporary(self):
        return {'vect': Vector2D(0, 1)}

    def init_matr(self):
        return MatrixData((8, 8), 8)

    def init_step_func(self):
        return {'add': (self.step_add, self.reverse_add),
                'moves': (self.step_moves, self.reverse_moves)}

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        if (npts := self.matr.search_value_vector(new_pt, self.temporary['vect'], 0)):
            npt = npts[-1]
        else:
            npt = new_pt
        self.do_add(player.name, active_piece.value, new_pt, npt)
        self.test_win(player, npt)

    def move_site(self, player: PlayerData, pt):
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
        self.add_move(player.name, 'moves', vect)
        if self.temporary['vect'] != vect:
            self.step_moves(vect)
            self.test_win2(player)
        self.temporary['vect'] = vect
        self.turn_active()

    def test_win2(self, player: PlayerData):
        """判断是否存在连子"""
        dc = self.matr.collection()
        for pt in dc.get(player.active, []):
            if bool(rows := matrixgrid.flatten_as_vector(self.in_row(pt))):
                self.update_tag_pts(player.name, rows, "Win")
                self.do_game_over(player.name, GameOverEnum.Win)
                return
        for pt in dc.get(3 - player.active, []):
            if bool(rows := matrixgrid.flatten_as_vector(self.in_row(pt))):
                self.update_tag_pts(player.name, rows, "Lose")
                self.do_game_over(player.name, GameOverEnum.Lose)
                return

    def step_moves(self, vect):
        links = []
        def _move(pt, vect, links):
            if (val := self.matr.get_value(pt)) == 0:
                return
            if (npts := self.matr.search_value_vector(pt, vect, 0)):
                npt = npts[-1]
            else:
                return
            if npt != pt:
                self.matr.set_value(npt, val, False)
                self.matr.set_value(pt, 0, False)
                links.append((pt, npt))
        match vect.point:
            case (0, 1): # y增大
                # 每一列进行变换
                for i in range(self.matr.size[0]):
                    for j in reversed(range(self.matr.size[1])):
                        _move(Vector2D(i, j), vect, links)
            case (1, 0):
                for j in range(self.matr.size[1]):
                    for i in reversed(range(self.matr.size[0])):
                        _move(Vector2D(i, j), vect, links)
            case (0, -1):
                for i in range(self.matr.size[0]):
                    for j in range(self.matr.size[1]):
                        _move(Vector2D(i, j), vect, links)
            case (-1, 0):
                for j in range(self.matr.size[1]):
                    for i in range(self.matr.size[0]):
                        _move(Vector2D(i, j), vect, links)
        self.call_signal('move', links)

    def reverse_moves(self, vect):
        self.step_moves(-vect)




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

