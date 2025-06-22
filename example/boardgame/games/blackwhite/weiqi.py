
from .blackwhite import PlayerBlackWhite, AppBlackWhite
from ...gridrule import *
import random


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
        for k,v in self.grid.history.current_data:
            if k == 'robbery':
                return self.matr.liberties_test(pt, value, (v or [[]])[0])
        return True

    def liberties_dead(self, player, pt, opval):
        """判断多点是否存无气邻居"""
        liberties_dead = matrixgrid.flatten_as_vector(self.matr.dead_nbrs(pt))
        if bool(liberties_dead):
            self.step_remove(player, opval, liberties_dead)
            self.add_move(player, 'remove', opval, liberties_dead)
            robbery = [pt] if len(liberties_dead) == 1 else []
            # 设置打劫
            self.add_move(player, 'robbery', robbery)

    def _step_add(self, player, val, pts):
        self.move_over(player, 'add', val, pts)
        self.step_add(player, val, pts)
        self.liberties_dead(player, pts[0], 3 - val)
        self.turn_active()

    def step_robbery(self, player, pt):
        pass

    def reverse_robbery(self, player, pt):
        pass




class Game_围棋19(GameData):
    """围棋19"""
    def init_gridattr(self):
        return {'matr': MatrixP((19, 19), structure = 4)}

    def init_move_manager(self):
        return Move_围棋19(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': True})



class App_围棋19(AppBlackWhite):
    """围棋19游戏规则"""
    def init_rule(self):
        self.name = '围棋'
        return Game_围棋19()
    
    def grid_attr(self):
        return {'size': (19, 19), 'canvas_size': (800, 800),
                'padding': (60, 60), 'is_net': True}

    def canvas_attr(self):
        return {'star_show': True, 'show_piece_index': True}





class Game_围棋13(Game_围棋19):
    """围棋13"""
    def init_gridattr(self):
        return {'matr': MatrixP((13, 13), structure = 4)}



class App_围棋13(AppBlackWhite):
    """围棋13游戏规则"""
    def init_rule(self):
        self.name = '围棋'
        return Game_围棋13()

    def grid_attr(self):
        return {'size': (13, 13), 'canvas_size': (750, 750),
                'padding': (80, 80), 'is_net': True}

    def canvas_attr(self):
        return {'star_show': True, 'show_piece_index': True}






class Game_围棋9(Game_围棋19):
    """围棋9"""
    def init_gridattr(self):
        return {'matr': MatrixP((9, 9), structure = 4)}



class App_围棋9(AppBlackWhite):
    """围棋9游戏规则"""
    def init_rule(self):
        self.name = '围棋'
        return Game_围棋9()
    
    def grid_attr(self):
        return {'size': (9, 9), 'canvas_size': (750, 750),
                'padding': (80, 80), 'is_net': True}

    def canvas_attr(self):
        return {'star_show': True, 'show_piece_index': True}




class Move_围棋吃子(Move_围棋19):
    def step_remove(self, player, val, pts):
        self.remove_piece_pts(val, pts)
        player.score += len(pts)
        self.test_win(player)

    def test_win(self, player):
        if player.score >= 5:
            self._step_game_over(player, GameOverEnum.Win)



class Game_围棋吃子(GameData):
    """围棋吃子"""
    def init_gridattr(self):
        self.default_piece_pts = {1: [(3, 3), (4, 4)], 2: [(3, 4), (4, 3)]}
        return {'matr': MatrixP((9, 9), structure = 4)}

    def init_move_manager(self):
        return Move_围棋吃子(self)

    def init_player_manager(self):
        return PlayerBlackWhite(self, pieceattr_group = {'placeable': True})



class App_围棋吃子(App_围棋9):
    """围棋9游戏规则"""
    def init_rule(self):
        self.name = '围棋吃子'
        return Game_围棋吃子()





class Game_无边界围棋(Game_围棋19):
    """无边界围棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((16, 16), structure = 4,
                    region = RegionRect((16, 16), RegionCircleEnum.XY))}



class App_无边界围棋(AppBlackWhite):
    """无边界围棋游戏规则"""
    def init_rule(self):
        self.name = '无边界围棋'
        return Game_无边界围棋()
    
    def grid_attr(self):
        return {'size': (16, 16), 'canvas_size': (800, 800),
                'padding': (40, 40), 'is_net': True, 'boundless': False}

    def canvas_attr(self):
        return {'star_show': True, 'show_piece_index': True}
    





class Move_翻转围棋(Move_围棋19):
    """翻转围棋"""
    def init_data(self):
        self.step_func = {'add': self.step_add,
                          'change': self.step_change,
                          'pass': self.step_pass}
        self.reverse_func = {'add': self.reverse_add,
                            'change': self.reverse_change,
                            'pass': self.reverse_pass}

    def move_test(self, pt, value):
        """模拟并测试该点落子后的情况"""
        return self.matr.liberties_test(pt, value)

    def liberties_dead(self, player, pt, opval):
        """判断多点是否存无气邻居"""
        liberties_dead = matrixgrid.flatten_as_vector(self.matr.dead_nbrs(pt))
        if bool(liberties_dead):
            self.step_change(player, opval, 3 - opval, liberties_dead)
            self.add_move(player, 'change', opval, 3 - opval, liberties_dead)



class Game_翻转围棋(Game_围棋19):
    """翻转围棋"""
    def init_move_manager(self):
        return Move_翻转围棋(self)



class App_翻转围棋(App_围棋19):
    """围棋9游戏规则"""
    def init_rule(self):
        self.name = '翻转围棋'
        return Game_翻转围棋()






class Move_二子围棋(Move_围棋19):
    """二子围棋"""
    def _step_add(self, player, val, pts):
        self.move_over(player, 'add', val, pts)
        self.step_add(player, val, pts)
        self.liberties_dead(player, pts[0], 3 - val)
        self.turn_active()


class Player_二子围棋(PlayerBlackWhite):
    def init_pieceattr_group(self):
        return {'placeable': True}

    def init_move_turns(self):
        self.move_turns.active_turn = 1
        return [n for n in self.player_group.keys() for _ in range(2)]


class Game_二子围棋(GameData):
    """二子围棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((19, 19), structure = 4)}

    def init_move_manager(self):
        return Move_二子围棋(self)

    def init_player_manager(self):
        return Player_二子围棋(self)



class App_二子围棋(App_围棋19):
    """二子围棋游戏规则"""
    def init_rule(self):
        self.name = '二子围棋'
        return Game_二子围棋()




class Move_环棋(Move_翻转围棋):
    """环棋"""
    def _step_add(self, player, val, pts):
        self.move_over(player, 'add', val, pts)
        self.step_add(player, val, pts)
        self.liberties_dead(player, pts[0], 3 - val)
        self.turn_active()



class Game_环棋(Game_二子围棋):
    """环棋"""
    def init_move_manager(self):
        return Move_环棋(self)



class App_环棋(App_围棋19):
    """环棋游戏规则"""
    def init_rule(self):
        self.name = '环棋'
        return Game_环棋()






class Move_九路飞刀(Move_围棋19):
    """九路飞刀"""
    def _step_add(self, player, val, pts):
        self.move_over(player, 'add', val, pts)
        self.step_add(player, val, pts)
        self.liberties_dead(player, pts[0], 3 - val)
        if not player.temporary['double']:
            self.turn_active()
            return
        player.temporary['double'][0] -= 1
        if player.temporary['double'][0] <= 0:
            player.temporary['double'].pop(0)
        else:
            self.turn_active()

    def _step_pass(self, player):
        """围棋的虚招，或不限手数的游戏结束本回合行棋"""
        pass


class Player_九路飞刀(PlayerBlackWhite):
    def init_player_temporary(self):
        return {'黑':{'double': self._double_steps()},
                '白':{'double': self._double_steps()}}
    
    def init_pieceattr_group(self):
        return {'placeable': True}

    def _double_steps(self):
        """生成飞刀触发步数，确保同一方的两次飞刀至少间隔5步"""
        triggers = set()
        while len(triggers) < 2:
            step = random.randint(6, 21)
            valid = True
            for existing in triggers:
                if abs(step - existing) < 5:
                    valid = False
                    break
            if valid:
                triggers.add(step)
        return list(triggers)


class Game_九路飞刀(GameData):
    """九路飞刀"""
    def init_gridattr(self):
        return {'matr': MatrixP((9, 9), structure = 4)}

    def init_move_manager(self):
        return Move_九路飞刀(self)

    def init_player_manager(self):
        return Player_九路飞刀(self)



class App_九路飞刀(App_围棋9):
    """九路飞刀游戏规则"""
    def init_rule(self):
        self.name = '九路飞刀'
        return Game_九路飞刀()





class Move_不围棋(MoveManager):
    """不围棋"""
    def init_data(self):
        self.step_func = {'add': self.step_add,
                          'remove': self.step_remove,
                          'pass': self.step_pass}
        self.reverse_func = {'add': self.reverse_add,
                            'remove': self.reverse_remove,
                            'pass': self.reverse_pass}

    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        val = active_piece.value
        pts = [new_pt]
        if not self.move_test(player, new_pt, val):
            return
        self.step_add(player, val, pts)
        self.move_over(player, 'add', val, pts)
        self.liberties_dead(player, pts[0], 3 - val)
        self.turn_active()

    def liberties_dead(self, player, pt, opval):
        """判断多点是否存无气邻居"""
        liberties_dead = matrixgrid.flatten_as_vector(self.matr.dead_nbrs(pt))
        if bool(liberties_dead):
            self.step_remove(player, opval, liberties_dead)
            self.add_move(player, 'remove', opval, liberties_dead)
            self._step_game_over(player, GameOverEnum.Lose)

    def _step_pass(self, player):
        self.step_pass(player)
        self.move_over(player, 'pass')
        self._step_game_over(player, GameOverEnum.Lose)
        pass

    def move_test(self, player, pt, value):
        """模拟并测试该点落子后的情况"""
        if not self.matr.liberties_test(pt, value, robbery = None):
            self._step_game_over(player, GameOverEnum.Lose)
            return False
        return True



class Game_不围棋(Game_围棋19):
    """不围棋"""
    def init_move_manager(self):
        return Move_不围棋(self)



class App_不围棋(App_围棋19):
    """围棋9游戏规则"""
    def init_rule(self):
        self.name = '不围棋'
        return Game_不围棋()



