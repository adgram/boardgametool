
from .blackwhite import *
import random



class Game_围棋19(GameBlackWhite):
    """围棋19"""
    def init_matr(self):
        return MatrixData((19, 19), structure = 4)

    def init_step_func(self):
        return {'add': (self.step_add, self.reverse_add),
                'remove': (self.step_remove, self.reverse_remove),
                'robbery': (self.step_robbery, self.reverse_robbery),
                'pass': (self.move_manager.step_pass, self.move_manager.reverse_pass)}

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        value = active_piece.value
        if not self.move_test(new_pt, value):
            return self.update_tag_pts(player.name, [], "Move")
        self.do_add(player.name, value, [new_pt])

    def move_test(self, pt, value):
        """模拟并测试该点落子后的情况"""
        for k,v in self.move_manager.history.current_move_data:
            if k == 'robbery':
                return self.matr.liberties_test(pt, value, (v or [[]])[0])
        return True

    def liberties_dead(self, player_name: str, pt, opval):
        """判断多点是否存无气邻居"""
        liberties_dead = matrixgrid.flatten_as_vector(self.matr.dead_nbrs(pt))
        if bool(liberties_dead):
            self.step_remove(player_name, opval, liberties_dead)
            self.add_move(player_name, 'remove', opval, liberties_dead)
            robbery = [pt] if len(liberties_dead) == 1 else []
            # 设置打劫
            self.add_move(player_name, 'robbery', robbery)

    def do_add(self, player_name: str, val, pts):
        self.add_move(player_name, 'add', val, pts)
        self.step_add(player_name, val, pts)
        self.liberties_dead(player_name, pts[0], 3 - val)
        self.turn_active()

    def step_robbery(self, player: PlayerData, pt):
        pass

    def reverse_robbery(self, player: PlayerData, pt):
        pass




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
    def init_matr(self):
        return MatrixData((13, 13), structure = 4)



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
    def init_matr(self):
        return MatrixData((9, 9), structure = 4)



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




class Game_围棋吃子(Game_围棋9):
    """围棋吃子"""
    def init_matr(self):
        return MatrixData((9, 9), structure = 4)

    def init_matr_pts(self):
        return {1: [(3, 3), (4, 4)], 2: [(3, 4), (4, 3)]}

    def step_remove(self, player: PlayerData, val, pts):
        self.move_manager.remove_value_pts(val, pts)
        player.score += len(pts)
        self.test_win(player)

    def test_win(self, player: PlayerData):
        if player.score >= 5:
            self.do_game_over(player.name, GameOverEnum.Win)




class App_围棋吃子(App_围棋9):
    """围棋9游戏规则"""
    def init_rule(self):
        self.name = '围棋吃子'
        return Game_围棋吃子()





class Game_无边界围棋(Game_围棋19):
    """无边界围棋"""
    def init_matr(self):
        return MatrixData((16, 16), structure = 4,
                    region = RegionRect((16, 16), RegionCircleEnum.XY))



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
    






class Game_翻转围棋(Game_围棋19):
    """翻转围棋"""
    def init_step_func(self):
        return {'add': (self.step_add, self.reverse_add),
                'change': (self.step_change, self.reverse_change),
                'pass': (self.move_manager.step_pass, self.move_manager.reverse_pass)}

    def move_test(self, pt, value):
        """模拟并测试该点落子后的情况"""
        return self.matr.liberties_test(pt, value)

    def liberties_dead(self, player_name: str, pt, opval):
        """判断多点是否存无气邻居"""
        liberties_dead = matrixgrid.flatten_as_vector(self.matr.dead_nbrs(pt))
        if bool(liberties_dead):
            self.add_move(player_name, 'change', opval, 3 - opval, liberties_dead)
            self.step_change(player_name, opval, 3 - opval, liberties_dead)



class App_翻转围棋(App_围棋19):
    """围棋9游戏规则"""
    def init_rule(self):
        self.name = '翻转围棋'
        return Game_翻转围棋()







class Game_二子围棋(Game_围棋19):
    """二子围棋"""
    def init_move_turns(self):
        self.players_manager.move_turns.active_turn = 1
        return [player.name for player in self.init_players() for _ in range(2)]

    def init_matr(self):
        return MatrixData((19, 19), structure = 4)

    def do_add(self, player_name: str, val, pts):
        self.move_over(player_name, 'add', val, pts)
        self.step_add(player_name, val, pts)
        self.liberties_dead(player_name, pts[0], 3 - val)
        self.turn_active()




class App_二子围棋(App_围棋19):
    """二子围棋游戏规则"""
    def init_rule(self):
        self.name = '二子围棋'
        return Game_二子围棋()




class Game_环棋(Game_二子围棋):
    """环棋"""
    def do_add(self, player_name: str, val, pts):
        self.move_over(player_name, 'add', val, pts)
        self.step_add(player_name, val, pts)
        self.liberties_dead(player_name, pts[0], 3 - val)
        self.turn_active()



class App_环棋(App_围棋19):
    """环棋游戏规则"""
    def init_rule(self):
        self.name = '环棋'
        return Game_环棋()






class Game_九路飞刀(Game_围棋9):
    """九路飞刀"""
    def init_temporary(self):
        return {'double':{'黑': self._double_steps(), '白': self._double_steps()}}

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

    def do_add(self, player_name: str, val, pts):
        self.add_move(player_name, 'add', val, pts)
        self.step_add(player_name, val, pts)
        self.liberties_dead(player_name, pts[0], 3 - val)
        steps = self.temporary['double'][player_name]
        if not steps:
            self.turn_active()
            return
        steps[0] -= 1
        if steps[0] <= 0:
            steps.pop(0)
        else:
            self.turn_active()

    def do_pass(self, player_name):
        """围棋的虚招，或不限手数的游戏结束本回合行棋"""
        pass



class App_九路飞刀(App_围棋9):
    """九路飞刀游戏规则"""
    def init_rule(self):
        self.name = '九路飞刀'
        return Game_九路飞刀()




class Game_不围棋(Game_围棋19):
    """不围棋"""
    def init_step_func(self):
        return {'add': (self.step_add, self.reverse_add),
                'remove': (self.step_remove, self.reverse_remove),
                'pass': (self.move_manager.step_pass, self.move_manager.reverse_pass)}

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        val = active_piece.value
        pts = [new_pt]
        if not self.move_test(player, new_pt, val):
            return
        self.step_add(player.name, val, pts)
        self.move_over(player.name, 'add', val, pts)
        self.liberties_dead(player, pts[0], 3 - val)
        self.turn_active()

    def liberties_dead(self, player_name: PlayerData, pt, opval):
        """判断多点是否存无气邻居"""
        liberties_dead = matrixgrid.flatten_as_vector(self.matr.dead_nbrs(pt))
        if bool(liberties_dead):
            self.step_remove(player_name, opval, liberties_dead)
            self.add_move(player_name, 'remove', opval, liberties_dead)
            self.do_game_over(player_name, GameOverEnum.Lose)

    def do_pass(self, player_name):
        self.move_manager.step_pass(player_name)
        self.add_move(player_name, 'pass')
        self.do_game_over(player_name, GameOverEnum.Lose)
        pass

    def move_test(self, player: PlayerData, pt, value):
        """模拟并测试该点落子后的情况"""
        if not self.matr.liberties_test(pt, value, robbery = None):
            self.do_game_over(player.name, GameOverEnum.Lose)
            return False
        return True




class App_不围棋(App_围棋19):
    """围棋9游戏规则"""
    def init_rule(self):
        self.name = '不围棋'
        return Game_不围棋()



