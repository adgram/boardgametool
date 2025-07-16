
from .wuziqi import *



class QuanchaUi(DefaultPiecesUi):
    def set_data(self, data, radius = 0):
        self.piecedata = data
        self.pieceui[1] = PieceUi(
                icon = Path(__file__).parent/'images/叉.svg',
                radius = radius
               )
        self.pieceui[2] = PieceUi(
                icon = Path(__file__).parent/'images/圈.svg',
                radius = radius
               )


class Game_井字棋(Game_五子棋):
    """井字棋"""
    def init_matr(self):
        return MatrixData((3, 3), structure = 8)
    
    def in_row(self, pt):
        """判断是否存在连子"""
        return self.matr.search_in_row(pt, 3)



class App_井字棋(AppBlackWhite):
    """井字棋游戏规则"""
    def init_rule(self):
        self.name = '井字棋'
        return Game_井字棋()
    
    def init_pieceuis(self):
        return QuanchaUi()

    def grid_attr(self):
        return {'size': (3, 3), 'canvas_size': (750, 750),
                'padding': (130, 130), 'is_net': False}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 10,
            'bgedges_show': AxisEnum.Null,
            'canvas_lines': [((0, 1), (3, 1)), ((0, 2), (3, 2)),
                             ((1, 0), (1, 3)), ((2, 0), (2, 3))],
            }







class Game_六消井字棋(Game_井字棋):
    """六消井字棋"""
    def init_matr(self):
        return MatrixData((3, 3), structure = 8)

    def init_temporary(self):
        from collections import deque
        return {'pieces': {'黑': deque(), '白': deque()}}

    def init_step_func(self):
        return {'add': (self.step_add, self.reverse_add),
                'remove': (self.step_remove, self.reverse_remove)}

    def do_add(self, player_name: str, val, pts):
        dq = self.temporary['pieces'][player_name]
        dq.append(pts[0])
        self.move_over(player_name, 'add', val, pts)
        self.step_add(player_name, (val, pts))
        if len(dq) >= 4:
            old = dq.popleft()
            self.step_remove(player_name, (val, [old]))
            self.add_move(player_name, 'remove', val, [old])

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        self.do_add(player.name, active_piece.value, [new_pt])
        self.test_win(player, new_pt)



class App_六消井字棋(App_井字棋):
    """六消井字棋游戏规则"""
    def init_rule(self):
        self.name = '六消井字棋'
        return Game_六消井字棋()





class Game_九宫棋(GameBlackWhite):
    """九宫棋"""
    def init_piece_count(self):
        return {1: 3, 2: 3}

    def init_pieceattr_group(self):
        return  {'placeable': True, 'moverules': [MoveRuleEnum.Move]}

    def init_matr(self):
        return MatrixData((3, 3), structure = 8)

    def init_step_func(self):
        return {'move': (self.step_move, self.reverse_move),
                'add': (self.step_add, self.reverse_add)}

    def test_win(self, player: PlayerData, pt):
        """判断是否存在连子"""
        if bool(rows := matrixgrid.flatten_as_vector(self.matr.search_in_row(pt, 3))):
            self.update_tag_pts(player.name, rows, "Win")
            self.do_game_over(player.name, GameOverEnum.Win)
        self.turn_active()

    def move_self_nil(self, player: PlayerData, active_piece: 'PieceData', old_pt, new_pt):
        value = active_piece.value
        if active_piece.num != 3 or old_pt not in self.matr.get_point_nbrs(new_pt):
            return self.update_tag_pts(player.name, [], "Move")
        self.do_move(player.name, value, [(old_pt, new_pt)])
        self.test_win(player, new_pt)

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        value = active_piece.value
        self.do_add(player.name, value, [new_pt])
        self.test_win(player, new_pt)




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
    







class 套娃井字棋Ui(DefaultPiecesUi):
    def set_data(self, data, radius = 0):
        self.piecedata = data
        color1 = PieceColor(color = (255, 255, 255, 200),
                fill = (20, 20, 20, 200), gradient = (50, 50, 50, 170))
        color2 = PieceColor(color = (0, 0, 0, 200),
                fill = (255, 255, 255, 200), gradient = (225, 225, 225, 170))
        for i in range(1, 6, 2):
            self.pieceui[i] = PieceUi(color = color1, radius = radius*(0.3 + 0.08*i))
            self.pieceui[i+1] = PieceUi(color = color2, radius = radius*(0.3 + 0.08*i))




class Game_套娃井字棋(Game_井字棋):
    """套娃井字棋"""
    def player_black(self, **kwargs):
        """黑棋玩家"""
        player = self.player_define(**{'name': '黑', **kwargs})
        player.add_pieces(self.piece_define(value = 1),
                         self.piece_define(occupy = [1, 2], value = 3),
                         self.piece_define(occupy = [1, 2, 3, 4], value = 5))
        return player

    def player_white(self, **kwargs):
        """白棋玩家"""
        player = self.player_define(**{'name': '白', **kwargs})
        player.add_pieces(self.piece_define(value = 2),
                         self.piece_define(occupy = [1, 2], value = 4),
                         self.piece_define(occupy = [1, 2, 3, 4], value = 6))
        return player

    def init_matr(self):
        matr = MatrixData((3, 7), structure = 8)
        matr.to_null([(i, 3) for i in range(3)])
        return matr

    def init_step_func(self):
        return {'add': (self.step_add, self.reverse_add)}

    def test_win(self, player: PlayerData, pt):
        """判断是否存在连子"""
        # if bool(rows := matrixgrid.flatten_as_vector(self.matr.search_in_row(pt, 3))):
        #     self.update_tag_pts(player.name, rows, "Win")
        #     self.do_game_over(player.name, GameOverEnum.Win)
        self.turn_active()

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', pt):
        """在空点落子"""
        self.do_adds(player.name, active_piece.value, [pt])
        self.test_win(player, pt)

    def move_nil_self(self, player: PlayerData, active_piece: 'PieceData', pt, old_val):
        """在空点落子"""
        self.do_change(player.name, old_val, active_piece.value, [pt])

    def move_nil_other(self, player: PlayerData, active_piece: 'PieceData', pt, old_val):
        """在空点落子"""
        self.do_change(player.name, old_val, active_piece.value, [pt])
        self.test_win(player, pt)




class App_套娃井字棋(AppBlackWhite):
    """套娃井字棋游戏规则"""
    def init_rule(self):
        self.name = '套娃井字棋'
        return Game_套娃井字棋()

    def init_pieceuis(self):
        return 套娃井字棋Ui()

    def grid_attr(self):
        return {'size': (3, 3), 'canvas_size': (750, 750),
                'padding': (180, 120), 'is_net': False, 'centered': False}
    
    def canvas_attr(self):
        return {'coor_show': LinePositionEnum.Null,
            'thickness': 10,
            'bgedges_show': AxisEnum.Null,
            'canvas_lines': [((0, 1), (3, 1)), ((0, 2), (3, 2)),
                             ((1, 0), (1, 3)), ((2, 0), (2, 3))],
            'pieces_values': [1, 3, 5, 2, 4, 6],
            }


