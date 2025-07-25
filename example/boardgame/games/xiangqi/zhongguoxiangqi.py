
from ...gridrule import *
from pathlib import Path




class 象棋Ui(DefaultPiecesUi):
    def set_data(self, data, radius = 0):
        self.piecedata = data
        piece_map1 = {1: '車', 2: '馬', 3: '炮', 
            4: '仕', 5: '相', 6: '帅', 7: '兵'}
        piece_map2 = {11: '車', 12: '馬', 13: '炮',
            14: '士', 15: '象', 16: '将', 17: '卒'}
        for v,k in piece_map1.items():
            self.pieceui[v] = PieceUi(
                color = PieceColor(color = (255, 40, 40, 205),
                                   fill = (240, 200, 200, 150),
                                   thickness = 2, offset = 4),
                text = PieceText(text = k, height = 30,
                                 color = (220, 30, 30, 220),
                                 show = True),
                radius = radius
           )
        for v,k in piece_map2.items():
            self.pieceui[v] = PieceUi(
                color = PieceColor(color = (20, 20, 20, 205),
                                   fill = (60, 60, 60, 150),
                                   thickness = 2, offset = 4),
                text = PieceText(text = k, height = 30,
                                 color = (220, 220, 220, 220),
                                 show = True),
                radius = radius
           )




class Game_象棋(GameData):
    """象棋"""
    def init_players(self):
        return [self.player_red(), self.player_black()]

    def player_red(self, **kwargs):
        """红棋玩家"""
        player = self.player_define(**{'name': '红', **kwargs})
        for i in range(1, 8):
            player.add_piece(self.piece_define(value = i, squeeze = [0],
                            moverules = [MoveRuleEnum.Move, MoveRuleEnum.Kill]))
        return player

    def player_black(self, **kwargs):
        """黑棋玩家"""
        player = self.player_define(**{'name': '黑', **kwargs})
        for i in range(11, 18):
            player.add_piece(self.piece_define(value = i, squeeze = [0],
                            moverules = [MoveRuleEnum.Move, MoveRuleEnum.Kill]))
        return player

    def init_matr(self):
        matr = MatrixData((9, 10), structure = 4)
        matr_region = RegionRect((9, 10))
        # 車、炮
        cross_vects = [Vector2D(0, i) for i in range(-9, 9)] +\
                        [Vector2D(i, 0) for i in range(-9, 9)]
        cross_region = RegionPoints(cross_vects)
        cross_dest1 = MoveDest(region = matr_region, mathvector = cross_region)
        matr.set_dests({1: cross_dest1, 11: cross_dest1, 3: cross_dest1, 13: cross_dest1})
        # 马
        cross_dest2 = MoveDest(region = matr_region,
                mathvector = RegionPoints([(1, 2), (1, -2), (-1, 2), (-1, -2),
                                           (2, 1), (-2, 1), (2, -1), (-2, -1)]))
        matr.set_dests({2: cross_dest2, 12: cross_dest2})
        # 相
        mathvector5 = RegionPoints([(2, 2), (2, -2), (-2, 2), (-2, -2)])
        region5 = RegionRect((0, 5), (9, 10))
        region15 = RegionRect((0, 0), (9, 5))
        matr.set_dests({5: MoveDest(region = region5, mathvector = mathvector5),
                        15: MoveDest(region = region15, mathvector = mathvector5)})
        # 士
        mathvector4 = RegionPoints([(1, 1), (1, -1), (-1, 1), (-1, -1)])
        region4 = RegionRect((3, 7), (6, 10))
        region14 = RegionRect((3, 0), (6, 3))
        matr.set_dests({4: MoveDest(region = region4, mathvector = mathvector4),
                        14: MoveDest(region = region14, mathvector = mathvector4)})
        # 将帅
        mathvector6 = RegionPoints([(1, 0), (0, -1), (-1, 0), (0, 1)])
        matr.set_dests({6: MoveDest(region = region4, mathvector = mathvector6),
                        16: MoveDest(region = region14, mathvector = mathvector6)})
        # 兵卒
        mathvector7 = RegionPoints([(1, 0), (-1, 0), (0, -1)])
        mathvector17 = RegionPoints([(1, 0), (-1, 0), (0, 1)])
        matr.set_dests({7: MoveDest(region = matr_region, mathvector = mathvector7),
                        17: MoveDest(region = matr_region, mathvector = mathvector17)})
        return matr
    
    def init_matr_pts(self):
        return {
            # 红方棋子（1-7）
            1: [(0, 9), (8, 9)],   # 車
            2: [(1, 9), (7, 9)],   # 馬
            3: [(1, 7), (7, 7)],   # 炮
            4: [(3, 9), (5, 9)],   # 仕
            5: [(2, 9), (6, 9)],   # 相
            6: [(4, 9)],           # 帅
            7: [(0, 6), (2, 6), (4, 6), (6, 6), (8, 6)],  # 兵
            # 黑方棋子（11-17）
            11: [(0, 0), (8, 0)],  # 車
            12: [(1, 0), (7, 0)],  # 馬
            13: [(1, 2), (7, 2)],  # 炮
            14: [(3, 0), (5, 0)],  # 士
            15: [(2, 0), (6, 0)],  # 象
            16: [(4, 0)],          # 将
            17: [(0, 3), (2, 3), (4, 3), (6, 3), (8, 3)]  # 卒
        }

    def init_step_func(self):
        return {'move': (self.step_move, self.reverse_move),
                'kill': (self.step_kill, self.reverse_kill)}

    def test_win(self, player: PlayerData, value):
        """模拟并测试该点落子后的情况"""
        match (player.name, value):
            case ('红', 16):
                return self.do_game_over(player.name, GameOverEnum.Win)
            case ('黑', 6):
                return self.do_game_over(player.name, GameOverEnum.Win)

    def test_win2(self, player: PlayerData, pt):
        """模拟并测试该点落子后的情况"""
        if pt[0] in [3, 4, 5]:
            for opt in self.matr.search_value(6):
                for npt in self.matr.search_value(16):
                    if self.matr.search_to_face(opt, npt, structure = 4):
                        return self.do_game_over(player.name, GameOverEnum.Lose)
        self.turn_active()
    
    def _move_test(self, value, old_pt, new_pt):
        if not self.matr.pt_in_value_dest(value, old_pt, new_pt):
            return False
        if value in [1, 11]:
            line = self.matr.collection_line(old_pt, new_pt)
            if 0 in line:
                line.pop(0)
            if line:
                return False
        elif value in [2, 12, 5, 15]:
            if self.matr.get_value(new_pt - ~(new_pt-old_pt)):
                return False
        elif value == 7:
            if new_pt[1] in [5, 6] and (new_pt-old_pt)[0]:
                return False
        elif value == 17:
            if new_pt[1] in [3, 4] and (new_pt-old_pt)[0]:
                return False
        return True
    
    def move_test(self, value, old_pt, new_pt):
        if not self._move_test(value, old_pt, new_pt):
            return False
        if value in [3, 13]:
            line = self.matr.collection_line(old_pt, new_pt)
            if 0 in line:
                line.pop(0)
            if line:
                return False
        return True

    def kill_test(self, value, old_pt, new_pt):
        if not self._move_test(value, old_pt, new_pt):
            return False
        if value in [3, 13]:
            line = self.matr.collection_line(old_pt, new_pt)
            if 0 in line:
                line.pop(0)
            if len(line) != 1:
                return False
        return True

    def move_self_nil(self, player: PlayerData, active_piece: 'PieceData', old_pt, new_pt):
        value = active_piece.value
        if not self.move_test(value, old_pt, new_pt):
            return self.update_tag_pts(player.name, [], "Move")
        self.do_move(player.name, value, [(old_pt, new_pt)])
        self.test_win2(player, old_pt)

    def move_self_other(self, player: PlayerData, active_piece: 'PieceData', old_pt, new_pt, new_val):
        value = active_piece.value
        if not self.kill_test(value, old_pt, new_pt):
            return self.update_tag_pts(player.name, [], "Move")
        self.do_kill(player.name, value, new_val, [(old_pt, new_pt)])
        self.test_win(player, new_val)
        self.test_win2(player, old_pt)

    def move_nil_self(self, player: PlayerData, active_piece: PieceData, pt, old_val):
        """选中棋子"""
        print(active_piece.get_flags(MoveRuleEnum.Move))




class App_象棋(Application):
    """象棋游戏规则"""
    def init_rule(self):
        self.name = '象棋'
        return Game_象棋()
    
    def init_pieceuis(self):
        return 象棋Ui()
    
    def grid_attr(self):
        return {'size': (9, 10), 'canvas_size': (750, 750),
                'padding': (70, 70), 'is_net': True}

    def init_canvasattr(self):
        self.about_info = '''象棋行棋规则

将/帅
    1. 只能在“九宫格”内活动
    2. 每次只能横向或纵向移动一格
    3. 不能“照面”（即双方将/帅不能在同一直线上无遮挡相对）
士/仕
    1. 只能在“九宫格”内活动
    2. 每次只能沿斜线移动一格
    3. 不能离开九宫格
象/相
    1. 每次沿“田”字对角线移动两格
    2. 不能过河（即只能在己方半边棋盘活动）
    3. 若“田”字中心有棋子阻挡（红、黑不限），则不能移动（称为“塞象眼”）
马
    1. 每次走“日”字形（先横向或纵向移动一格，再斜向移动一格）
    2. 若移动方向的第一格有棋子阻挡（红、黑不限），则不能移动（称为“蹩马腿”）
车
    1. 可以横向或纵向任意距离移动
    2. 不能跳过其他棋子
炮
    1. 移动方式与车相同，可以横向或纵向任意距离移动
    2. 吃子时，必须跳过一个棋子（称为“炮架”）
卒/兵
    1. 每次只能向前移动一格
    2. 过河后，可以横向移动一格
    3. 不能后退'''
        yls = [((i, 0), (i, 4)) for i in range(9)]
        yls.extend([((i, 5), (i, 9)) for i in range(9)])
        return {'color': (23, 140, 205, 200),
            'coor_show': LinePositionEnum.Null,
            'bgedges_show': AxisEnum.X,
            'canvas_image': Path(__file__).parent/'images/background.jpg',
            'canvas_lines': [*yls, ((3, 0), (5, 2)), ((3, 2), (5, 0)),
                                   ((3, 7), (5, 9)), ((3, 9), (5, 7)),
                                   ((0, 4), (0, 5)), ((8, 4), (8, 5))]
            }
