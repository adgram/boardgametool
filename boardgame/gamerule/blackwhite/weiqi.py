
from .blackwhite import PlayerBlackWhite, AppBlackWhite
from ...gridrule import pointData, PieceTagEnum, MoveManager, GameData, MatrixP, CanvasGrid


class Move_围棋19(MoveManager):
    """围棋19"""
    def init_data(self):
        self.step_func = {'add': self.step_add,
                          'remove': self.step_remove,
                          'robbery': self.step_robbery,
                          'pass': self.step_pass}
        self.reverse_func = {'add': self.reverse_add,
                            'remove': self.reverse_remove,
                            'robbery': self.reverse_robbery,
                            'pass': self.reverse_pass}

    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        value = active_piece.value
        if not self.move_test(new_pt, value):
            return self.update_tag_pts(player, [], PieceTagEnum.Move)
        self._step_add(player, value, [new_pt])

    def move_test(self, pt, value):
        """模拟并测试该点落子后的情况"""
        robbery = self.grid.history.current_data.get('robbery', [None])
        return self.matr.liberties_test(pt, value, robbery = robbery[0])

    def liberties_dead(self, player, pt, opval):
        """判断多点是否存无气邻居"""
        liberties_dead = pointData.flatten(self.matr.dead_nbrs(pt),
                            to_vector = False)
        if bool(liberties_dead):
            self.step_remove(player, opval, liberties_dead)
            self.add_move(player, 'remove', opval, liberties_dead)
            robbery = pt if len(liberties_dead) == 1 else None
            # 设置打劫
            self.add_move(player, 'robbery', robbery)

    def _step_add(self, player, val, pts):
        self.step_add(player, val, pts)
        self.move_over(player, 'add', val, pts)
        self.liberties_dead(player, pts[0], 3 - val)
        self.turn_active(player = player)

    def step_robbery(self, player, pt):
        pass

    def reverse_robbery(self, player, pt):
        pass




class Game_围棋19(GameData):
    """围棋19"""
    def init_gridattr(self):
        return {'matr': MatrixP.structure_matrix((19, 19), structure = 4)}

    def init_move_manager(self):
        return Move_围棋19(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': True})



class App_围棋19(AppBlackWhite):
    """围棋19游戏规则"""
    def init_rule(self):
        self.name = '围棋'
        return Game_围棋19()

    def init_grid(self):
        return CanvasGrid(size = (19, 19), padding = (40, 40), canvas_size = (800, 800))

    def canvas_attr(self):
        return {'star_show': True}





class Game_围棋13(Game_围棋19):
    """围棋13"""
    def init_gridattr(self):
        return {'matr': MatrixP.structure_matrix((13, 13), structure = 4)}



class App_围棋13(AppBlackWhite):
    """围棋13游戏规则"""
    def init_rule(self):
        self.name = '围棋'
        return Game_围棋13()

    def init_grid(self):
        return CanvasGrid(size = (13, 13), canvas_size = (750, 750))

    def canvas_attr(self):
        return {'star_show': True}






class Game_围棋9(Game_围棋19):
    """围棋9"""
    def init_gridattr(self):
        return {'matr': MatrixP.structure_matrix((9, 9), structure = 4)}



class App_围棋9(AppBlackWhite):
    """围棋9游戏规则"""
    def init_rule(self):
        self.name = '围棋'
        return Game_围棋9()

    def init_grid(self):
        return CanvasGrid(size = (9, 9), padding = (90, 90), 
                          canvas_size = (750, 750))

    def canvas_attr(self):
        return {'star_show': True}

