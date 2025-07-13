from ...gridrule import *
from pathlib import Path




class BlackWhiteUi(DefaultPiecesUi):
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




class Game_五子棋(GameBlackWhite):
    """五子棋"""
    def init_matr(self):
        return MatrixData((15, 15), structure = 8)

    def init_step_func(self):
        return {'add': (self.step_add, self.reverse_add)}

    def in_row(self, pt, n = 5):
        """判断是否存在连子"""
        return self.matr.search_in_row(pt, n)

    def test_win(self, player: PlayerData, pt):
        """判断是否存在连子"""
        if bool(rows := matrixgrid.flatten_as_vector(self.in_row(pt))):
            self.update_tag_pts(player.name, rows, "Win")
            self.do_game_over(player.name, GameOverEnum.Win)
        self.turn_active()

    def move_nil_nil(self, player: PlayerData, active_piece: 'PieceData', new_pt):
        """在空点落子"""
        self.do_add(player.name, active_piece.value, [new_pt])
        self.test_win(player, new_pt)



class App_五子棋(AppBlackWhite):
    """五子棋游戏规则"""
    def init_rule(self):
        self.name = '五子棋'
        return Game_五子棋()
    
    def grid_attr(self):
        return {'size': (15, 15), 'canvas_size': (750, 750),
                'padding': (80, 80), 'is_net': True}
    
    def canvas_attr(self):
        return {'star_show': True, 'show_piece_index': True}


