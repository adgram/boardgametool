
from .wuziqi import *



class Game_直角五子棋(GameBlackWhite):
    """直角五子棋"""
    def init_matr(self):
        return MatrixData((9, 9), structure = 8)

    def init_step_func(self):
        return {'add': (self.step_add, self.reverse_add)}

    def test_win(self, player: PlayerData, pt):
        """判断是否存在连子"""
        bls = []
        for plum in self.get_shapes():
            for p in plum:
                d =  pt - p
                bl = [(d + q) for q in plum]
                if set(self.matr.get_value(q) for q in bl) == {self.matr.get_value(pt)}:
                    bls.extend(bl)
        if bls:
            self.update_tag_pts(player.name, bls, "Win")
            self.do_game_over(player.name, GameOverEnum.Win)
        self.turn_active()

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        self.do_add(player.name, active_piece.value, [new_pt])
        self.test_win(player, new_pt)
    
    def get_shapes(self):
        return [[Vector2D(0, 0), x, x*2, y, y*2] for x,y in [
            (Vector2D(1, 1), Vector2D(1, -1)), (Vector2D(1, -1), Vector2D(-1, -1)),
            (Vector2D(-1, -1), Vector2D(-1, 1)), (Vector2D(-1, 1), Vector2D(1, 1)),
            (Vector2D(0, 1), Vector2D(1, 0)), (Vector2D(1, 0), Vector2D(0, -1)),
            (Vector2D(0, -1), Vector2D(-1, 0)), (Vector2D(-1, 0), Vector2D(0, 1))
        ]]




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




class Game_梅花棋(Game_直角五子棋):
    """梅花棋"""
    def init_matr(self):
        return MatrixData((19, 19), structure = 8)

    def get_shapes(self):
        return [[(0, 0)] + [(i, j) for i in [-1, 1] for j in [-1, 1]],
                 [(0, 0)] + [(i, j) for i in [-2, 2] for j in [-2, 2]],
                 [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)],
                 [(0, 0), (2, 0), (-2, 0), (0, 2), (0, -2)]]



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

