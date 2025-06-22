
from .blackwhite import PlayerBlackWhite
from ...gridrule import *
from .wuziqi import Move_五子棋, App_五子棋



class ThreesUi(DefaultPiecesUi):
    def set_data(self, data, radius = 0):
        self.piecedata = data
        self.pieceui[self.piecedata[1].value] = PieceUi(
                color = PieceColor(color = (255, 255, 255, 200),
                                   fill = (20, 20, 20, 200),
                                   gradient = (50, 50, 50, 170)),
                text = PieceText(text = '黑',
                                 height = 20,
                                 color = (255, 255, 255, 200)),
                radius = radius
               )
        self.pieceui[self.piecedata[2].value] = PieceUi(
                color = PieceColor(color = (0, 0, 0, 200),
                                   fill = (255, 255, 255, 200),
                                   gradient = (225, 225, 225, 170)),
                text = PieceText(text = '白',
                                 height = 20,
                                 color = (0, 0, 0, 200)),
                radius = radius
               )
        self.pieceui[self.piecedata[3].value] = PieceUi(
                color = PieceColor(color = (0, 0, 0, 200),
                                   fill = (125, 125, 125, 200),
                                   gradient = (105, 105, 105, 170)),
                text = PieceText(text = '灰',
                                 height = 20,
                                 color = (0, 0, 0, 200)),
                radius = radius
               )



class Player_同步五子棋(PlayerBlackWhite):
    def init_pieceattr_group(self):
        return {'placeable': True}

    def init_player_group(self):
        return {'黑':self.player_black(), '白':self.player_white(), '灰': self.player_same()}

    def player_same(self, **kwargs):
        """黑棋玩家"""
        player = self.player_define(**{'name': '灰', **kwargs})
        player.pieces = {3: self.piece_define(player = player, value = 3, name = '灰')}
        return player
    
    def same_player(self):
        return self.players['灰']



class Move_同步五子棋(Move_五子棋):
    """同步五子棋"""
    def test_win(self, pl1, pt1, pl2, pt2):
        """判断是否存在连子"""
        row1 = matrixgrid.flatten_as_vector(self.in_row(pt1))
        row2 = matrixgrid.flatten_as_vector(self.in_row(pt2))
        if len(row1) > len(row2):
            self.update_tag_pts(pl1, row1, PieceTagEnum.Win)
            self._step_game_over(pl1, GameOverEnum.Win)
        elif len(row1) < len(row2):
            self.update_tag_pts(pl2, row2, PieceTagEnum.Win)
            self._step_game_over(pl2, GameOverEnum.Win)
        elif len(row1) > 0:
            same = self.player_manager.same_player()
            self.step_change(same, pl1.active, 3, row1)
            self.step_change(same, pl2.active, 3, row2)
            self.move_over(same, 'change', pl1.active, 3, row1)
            self.add_move(same, 'change', pl1.active, 3, row2)

    def move_nil_nil(self, player: 'PlayerData', active_piece, new_pt):
        """在空点落子"""
        same = self.player_manager.same_player()
        if self.grid.temporary.get('pt', None) is None:
            self.grid.temporary['pt'] = new_pt
        else:
            pt1 = self.grid.temporary['pt']
            self.grid.temporary['pt'] = None
            if pt1 == new_pt:
                self._step_add(same, {3: [new_pt]})
            else:
                val1 = 3 - active_piece.value
                pl1 = self.player_manager.get_player(val = val1)
                self._step_add(same, {val1: [pt1], active_piece.value: [new_pt]})
                self.test_win(pl1, pt1, player, new_pt)
        self.turn_active()
        if self.player_manager.active_player == same:
            self.turn_active()

    def _step_add(self, player, pts_map):
        """绘制棋盘上的棋子"""
        self.move_over(player, 'add', pts_map)
        self.step_add(player, pts_map)

    def step_add(self, player, pts_map):
        """绘制棋盘上的棋子"""
        self.add_pts_map_piece(pts_map)
        self.update_tag_pts(player, sum(pts_map.values(), []), PieceTagEnum.Add)

    def reverse_add(self, player, pts_map):
        """绘制棋盘上的棋子"""
        self.update_tag_pts(player, [], PieceTagEnum.Add)
        self.remove_pts_piece(sum(pts_map.values(), []))



class Game_同步五子棋(GameData):
    """同步五子棋"""
    def init_gridattr(self):
        return {'matr': MatrixP((15, 15), structure = 8)}

    def init_move_manager(self):
        return Move_同步五子棋(self)

    def init_player_manager(self):
        return Player_同步五子棋(self)



class App_同步五子棋(App_五子棋):
    """同步五子棋游戏规则"""
    def init_rule(self):
        self.name = '同步五子棋'
        return Game_同步五子棋()
    
    def init_pieceuis(self):
        return ThreesUi()


