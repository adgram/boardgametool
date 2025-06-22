
from ...gridrule import *
from pathlib import Path




class 六人跳棋Ui(DefaultPiecesUi):
    def set_data(self, data, radius = 0):
        self.piecedata = data
        # piece_map = { 1: '绿', 2: '橙', 3: '黄', 4: '红', 5: '蓝', 6: '紫'}
        color_map = {
            1: ((0, 128, 0, 200), (50, 205, 50, 200), (144, 238, 144, 170)),
            2: ((255, 165, 0, 200), (255, 140, 0, 200), (255, 215, 0, 170)),
            3: ((255, 255, 0, 200), (255, 215, 0, 200), (255, 255, 224, 170)),
            4: ((255, 0, 0, 200), (178, 34, 34, 200), (255, 99, 71, 170)),
            5: ((0, 0, 255, 200), (30, 144, 255, 200), (135, 206, 250, 170)),
            6: ((128, 0, 128, 200), (147, 112, 219, 200), (221, 160, 221, 170))
        }
        for v,colors in color_map.items():
            color, fill, gradient = colors
            self.pieceui[v] = PieceUi(
                color = PieceColor(color = color, fill = fill,
                                   gradient = gradient),
                radius = radius*0.7)



class Move_六人跳棋(MoveManager):
    """六人跳棋"""
    def init_data(self):
        self.step_func = {'move': self.step_move}
        self.reverse_func = {'move': self.reverse_move}

    def move_self_nil(self, player: 'PlayerData', active_piece, old_pt, new_pt):
        value = active_piece.value
        if not (links := self.get_move_links(old_pt, new_pt)):
            return self.update_tag_pts(player, [], PieceTagEnum.Move)
        self._step_move(player, value, links)
        self.test_win(player, value, new_pt)

    def get_move_links(self, old_pt, new_pt):
        if new_pt in self.matr.get_point_nbrs(old_pt):
            return [(old_pt, new_pt)]
        pts = self.matr.search_shortest_path(old_pt, new_pt, True)
        return [pts] if pts else []

    def test_win(self, player, value, pt):
        bl = self.game.default_piece_pts[player.temporary['aim']]
        if pt in bl and len(self.matr.collection(bl).get(value, [])) == 10:
            self._step_game_over(player, GameOverEnum.Win)
        self.turn_active()



class Player_六人跳棋(PlayerManager):
    """六人跳棋"""
    def init_player_group(self):
        piece_map = { 1: '绿', 2: '橙', 3: '黄', 4: '红', 5: '蓝', 6: '紫'}
        return {name: self.player_df(name, value) for value,name in piece_map.items()}

    def player_df(self, name, value):
        """玩家"""
        piece = self.piece_define(movable = [MoveRuleEnum.Move], value = value)
        player = self.player_define(name = name, pieces = {value: piece}, temporary = {
                        'aim': value - 3 if value > 3 else value + 3})
        return player



class Game_六人跳棋(GameData):
    """六人跳棋"""
    def init_gridattr(self):
        self.default_piece_pts = {
            1: [(i, j) for i in range(4, 8) for j in range(4, 12-i)],   # 绿
            2: [(i, j) for i in range(9, 13) for j in range(12-i, 4)],   # 橙
            3: [(i, j) for i in range(13, 17) for j in range(4, 21-i)],
            4: [(i, j) for i in range(9, 13) for j in range(21-i, 13)],
            5: [(i, j) for i in range(4, 8) for j in range(13, 21-i)],
            6: [(i, j) for i in range(0, 4) for j in range(12-i, 13)],
        }
        points = [(i, j) for i in range(4, 13) for j in range(4, 13)]
        for i in [2, 3, 5, 6]: 
            points.extend(self.default_piece_pts[i])
        region = RegionPoints(points)
        dr = Direction.create_from_axises({2, -2, 1, -1, 4, -4})
        neighbortable = NeighborTable.direction_only({region: dr})
        return {'matr': MatrixP((17, 17), region, neighbortable)}

    def init_move_manager(self):
        return Move_六人跳棋(self)

    def init_player_manager(self):
        return Player_六人跳棋(self)




class App_六人跳棋(Application):
    """六人跳棋游戏规则"""
    def init_rule(self):
        self.name = '六人跳棋'
        return Game_六人跳棋()
    
    def init_pieceuis(self):
        return 六人跳棋Ui()
    
    def grid_attr(self):
        return {'size': (17, 17), 'canvas_size': (800, 800), "origin": (18, 0),
                'padding': (-200, -200), 'obliquity': 0.5+3**0.5*0.5j}

    def init_canvasattr(self):
        return {'color': (23, 140, 205, 150),
            'coor_show': LinePositionEnum.Null,
            'bgedges_show': AxisEnum.Null, 
            'canvas_image': Path(__file__).parent/'images/六人跳棋棋盘.png',
            'image_dsize': (12, 0), "image_origin": (0, 0)
            }
