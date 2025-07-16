from ...gridrule import *
from pathlib import Path
import random




class BlackWhiteUi(DefaultPiecesUi):
    def set_data(self, data, radius = 0):
        self.piecedata = data
        self.pieceui[1] = PieceUi(
                color = PieceColor(color = (255, 255, 255, 200),
                                   fill = (20, 20, 20, 200),
                                   gradient = (50, 50, 50, 170)),
                text = PieceText(text = '黑', height = 20,
                                 color = (255, 255, 255, 200)),
                radius = radius
               )
        self.pieceui[2] = PieceUi(
                color = PieceColor(color = (0, 0, 0, 200),
                                   fill = (255, 255, 255, 200),
                                   gradient = (225, 225, 225, 170)),
                text = PieceText(text = '白', height = 20,
                                 color = (0, 0, 0, 200)),
                radius = radius
               )




class GameBlackWhite(GameData):
    """黑白棋"""
    def init_pieceattr_group(self):
        return {"placeable": True}

    def init_players(self):
        return [self.player_black(), self.player_white()]

    def player_black(self, **kwargs):
        """黑棋玩家"""
        player = self.player_define(**{'name': '黑', **kwargs})
        attr = {'value':1, 'name':'黑', "squeeze": [2], "occupy": [2], 
                **self.init_pieceattr_group()}
        player.add_piece(self.piece_define(**attr))
        return player

    def player_white(self, **kwargs):
        """白棋玩家"""
        player = self.player_define(**{'name': '白', **kwargs})
        attr = {'value':2, 'name':'白', "squeeze": [2], "occupy": [2], 
                **self.init_pieceattr_group()}
        player.add_piece(self.piece_define(**attr))
        return player




class AppBlackWhite(Application):
    """黑白棋游戏规则"""
    def init_pieceuis(self):
        return BlackWhiteUi()
    
    def init_canvasattr(self):
        canvas = {'color': (23, 140, 205, 200),
            'fill': (23, 140, 205, 60),
            'coor_show': LinePositionEnum.Both,
            'bgedges_show': AxisEnum.XY,
            'canvas_image': Path(__file__).parent/'images/background.jpg'
            }
        canvas.update(self.canvas_attr())
        return canvas
    
    def canvas_attr(self):
        return {}






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
            self.step_remove(player_name, (opval, liberties_dead))
            self.add_move(player_name, 'remove', opval, liberties_dead)
            robbery = [pt] if len(liberties_dead) == 1 else []
            # 设置打劫
            self.add_move(player_name, 'robbery', robbery)

    def do_add(self, player_name: str, val, pts):
        self.move_over(player_name, 'add', val, pts)
        self.step_add(player_name, (val, pts))
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

