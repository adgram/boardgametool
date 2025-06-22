
from ...gridrule import *
from pathlib import Path




class BlackWhiteUi(DefaultPiecesUi):
    def set_data(self, data, radius = 0):
        self.piecedata = data
        self.pieceui[1] = PieceUi(
                color = PieceColor(color = (255, 255, 255, 200),
                                   fill = (20, 20, 20, 200),
                                   gradient = (50, 50, 50, 170)),
                radius = radius
               )
        self.pieceui[2] = PieceUi(
                color = PieceColor(color = (0, 0, 0, 200),
                                   fill = (255, 255, 255, 200),
                                   gradient = (225, 225, 225, 170)),
                radius = radius
               )



class PlayerBlackWhite(PlayerManager):
    """黑白双色棋"""
    def init_player_group(self):
        return {'黑':self.player_black(), '白':self.player_white()}

    def player_black(self, **kwargs):
        """黑棋玩家"""
        player = self.player_define(**{'name': '黑', **kwargs})
        player.pieces = {1: self.piece_black(player = player,
                                    squeeze = [2], occupy = [2])}
        return player

    def player_white(self, **kwargs):
        """白棋玩家"""
        player = self.player_define(**{'name': '白', **kwargs})
        player.pieces = {2: self.piece_white(player = player,
                                    squeeze = [1], occupy = [1])}
        return player

    def piece_black(self, **kwargs):
        """黑棋子"""
        attr = {'value':1, 'name':'黑', **{**self.pieceattr_group, **kwargs}}
        return self.piece_define(**attr)

    def piece_white(self, **kwargs):
        """白棋子"""
        attr = {'value':2, 'name':'白', **{**self.pieceattr_group, **kwargs}}
        return self.piece_black(**attr)




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


