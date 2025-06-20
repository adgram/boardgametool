import sys
from .gridrule import PieceTagEnum, ObjJson
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QComboBox,
                               QHBoxLayout, QPushButton, QLabel, QWidget,
                               QDialog, QMessageBox, QGraphicsItem, QFileDialog,
                               QGraphicsView, QGraphicsScene, QGraphicsObject)
from PySide6.QtGui import QPainter, QPen, QColor, QRadialGradient, QPixmap, QFont
from PySide6.QtCore import (Qt, QRectF, QPropertyAnimation, QPointF,
                            QEasingCurve, QAbstractAnimation, QTimer,
                            QSequentialAnimationGroup)
from pathlib import Path
from .gamerule import APPS
from .pysidegui_styles import *


ANIM_TIME = 400
LAYER_BACKGROUND = -100  # 背景层（网格、纹理等）
LAYER_PIECES = 0         # 棋子层（主游戏对象）
LAYER_SYMBOL = 10        # 符号层（棋子序号）
LAYER_TAGS = 20          # 标记层（特殊标记）
LAYER_ANIMATION = 30     # 动画层（最高层）



class BoardGameApp(QMainWindow):
    '''
    游戏主窗口
    '''
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.background_image = QPixmap('.')
        self.setWindowTitle(app.name)
        self.create_menu()
        self.create_status()
        self.init_ui()
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 必须开启
        self.setStyleSheet(QMainWindowStyle)
        self.app.set_signal('game_over', self.game_over)
        self.app.set_signal('active_player', self.show_active_player)
        self.app.set_signal('info_piece', self.show_info_piece)
        self.app.set_signal('be_asked_retract', self.be_asked_retract)
        self.app.after_begin()

    def init_ui(self):
        '''
        初始化游戏界面
        '''
        # 主容器使用水平布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        self.qapp_canvas = AppCanvas(app = self.app)
        layout.addWidget(self.qapp_canvas)
        self.tool_bar = PenToolBar(100, self.app.canvasboard.size[1], 
                                   self, self.app.player_names)
        layout.addWidget(self.tool_bar)
        self.resize_to_canvas()

    def resize_to_canvas(self):
        """根据画布尺寸调整主窗口大小"""
        canvas_width = self.qapp_canvas.width()
        canvas_height = self.qapp_canvas.height()
        toolbar_width = self.tool_bar.width()
        menu_height = self.menuBar().height()
        status_height = self.statusBar().height()
        margins = 10  # 布局边距
        total_width = canvas_width + toolbar_width + margins
        total_height = canvas_height + menu_height + status_height + margins
        self.setFixedSize(total_width, total_height)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = (screen_geometry.width() - total_width) // 2
        y = (screen_geometry.height() - total_height) // 2
        self.move(x, y)

    def create_menu(self):
        '''创建菜单栏'''
        # 添加菜单栏
        menu_bar = self.menuBar()
        game_menu = menu_bar.addMenu("游戏")
        game_menu.addAction("新游戏", self.new_game)
        game_menu.addAction("切换游戏", self.switch_game)
        game_menu.addSeparator()
        game_menu.addAction("退出", self.exit_game)
        file_menu = menu_bar.addMenu("文件")
        file_menu.addAction("打开棋谱", self.open_game)
        file_menu.addAction("保存棋谱", self.save_game)
        file_menu.addAction("导出当前分支", self.save_current_game)
        help_menu = menu_bar.addMenu("帮助")
        help_menu.addAction("关于", self.show_about)
        help_menu.addAction("提示", self.get_nxet_move)

    def create_status(self):
        '''创建状态栏'''
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("开始游戏")
        
    def game_over(self, name, tag):
        '''游戏结束弹窗'''
        about_dialog = GameDialog(self, "游戏结束", f"{name}{\
                            self.app.gameover_tag_name(tag)}")
        about_dialog.exec()

    def new_game(self):
        """新游戏"""
        self.qapp_canvas.clear_all()
        self.tool_bar.reset_btns()
        self.app.rebegin()
        self.app.add_default_piece_pts()
        self.resize_to_canvas()  # 添加这一行
    
    def switch_game(self):
        """切换游戏"""
        # 创建启动器窗口
        launcher = GameLauncher(APPS, self)
        if launcher.exec() == QDialog.Accepted:
            # 获取选择的游戏名称
            game_name = launcher.start_game()
            current_pos = self.pos()
            # 关闭当前游戏窗口
            self.close()
            # 启动新游戏
            new_win = BoardGameApp(APPS[game_name]())
            new_win.move(current_pos)
            new_win.show()
            new_win.resize_to_canvas()  # 添加这一行
    
    def _save_data(self, data):
        '''保存数据'''
        path, _ = QFileDialog.getSaveFileName(
            self, "保存棋谱", "", "JSON Files (*.json)")
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    ObjJson.dump(data, f)
                self.status_bar.showMessage(f"棋谱已保存到：{path}")
            except Exception as e:
                dialog = GameDialog(self, "保存失败", f"保存文件时发生错误：{str(e)}")
                dialog.exec()
    
    def _open_data(self):
        '''打开数据'''
        path, _ = QFileDialog.getOpenFileName(
            self, "打开棋谱", "", "JSON Files (*.json)")
        if not path:
            return {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return ObjJson.load(f)
            self.status_bar.showMessage(f"已加载棋谱：{Path(path).name}")
        except Exception as e:
            dialog = GameDialog(self, "打开失败", f"读取文件时发生错误：{str(e)}")
            dialog.exec()

    def save_game(self):
        """保存游戏"""
        data = self.app.get_game_data()
        self._save_data(data)
        
    def save_current_game(self):
        """保存游戏"""
        data = self.app.get_current_game_data()
        self._save_data(data)

    def open_game(self):
        """打开棋谱"""
        self.qapp_canvas.clear_all()
        self.app.rebegin()
        self.app.load_data(self._open_data())
        self.app.add_default_piece_pts()

    def exit_game(self):
        """退出游戏"""
        self.close()

    def on_race(self):
        """比赛"""
        self.app.on_race()

    def out_race(self):
        """打谱"""
        self.app.out_race()

    def show_about(self):
        """显示关于信息"""
        about_dialog = GameDialog(self, "关于", self.app.about_info)
        about_dialog.exec()
    
    def get_nxet_move(self):
        """显示关于信息"""
        return

    def show_active_player(self, player):
        '''显示当前棋手'''
        self.status_bar.showMessage(f"当前棋手：{player}")

    def show_info_piece(self, name, val = None):
        '''显示棋子信息'''
        ui = self.app.pieceuis.get(val or 1)
        self.tool_bar.piece_tool.show_piece(ui)

    def on_player(self, name):
        """设置当前棋手为1棋手"""
        self.app.on_player(name)
    
    def on_turns(self):
        """轮换执棋"""
        self.app.on_turns()
    
    def on_symbol_tag(self, tag):
        self.app.on_symbol_tag(tag)
    
    def turn_player(self):
        """切换棋手"""
        self.app.turn_player()

    def ask_retract(self):
        """悔棋逻辑"""
        self.app.ask_retract()

    def step_back(self):
        """返回上一步"""
        self.app.step_back()
    
    def step_forward(self):
        """加载下一步"""
        self.app.step_forward()

    def be_asked_retract(self, name):
        """悔棋逻辑"""
        ask = GameAsk(self, f"{name}申请悔棋", "是否同意？")
        if ask.exec() == QMessageBox.Yes:
            self.app.agree_retract(name)

    def pass_move(self):
        """虚着"""
        return self.app.pass_move()

    def resign_game(self):
        """认输逻辑"""
        ask = GameAsk(self, "认输", "是否认输？")
        if ask.exec() == QMessageBox.Yes:
            self.app.give_up()

    def paintEvent(self, event):
        """重写绘制事件实现背景"""
        painter = QPainter(self)
        if self.background_image.isNull() and \
                self.app.canvasboard.canvas_image \
                and Path(self.app.canvasboard.canvas_image).exists():
            self.background_image = QPixmap(self.app.canvasboard.canvas_image)
        if not self.background_image.isNull():
            w,h = self.app.canvasboard.image_dsize
            scaled_pix = self.background_image.scaled(
                self.size().width() + w, self.size().height() + h,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
           )
            painter.drawPixmap(*self.app.canvasboard.image_origin, scaled_pix)
        super().paintEvent(event)



class AppCanvas(QGraphicsView):
    """画布"""
    def __init__(self, parent = None, app = None):
        super().__init__(parent)
        self.app = app
        self.canvasboard = app.canvasboard
        self.scene = QGraphicsScene(self)  # 创建场景
        self.setScene(self.scene)          # 关联场景到视图
        self.pt_pieces = {}
        self.taging_pieces = {}
        self.taging_symbol = {}
        self._current_anim = {}
        # 设置尺寸时补偿1像素
        view_width = self.canvasboard.size[0] + 5
        view_height = self.canvasboard.size[1] + 5
        self.setFixedSize(view_width, view_height)
        self.setSceneRect(0, 0, *self.canvasboard.size)   # (x, y, width, height)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)     # 对齐方式
        # 消除所有边距影响
        self.setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.set_piece_default_signal()
        self.app.add_default_piece_pts()

    @classmethod
    def draw_line(cls, painter: QPainter, pt1, pt2, ui):
        pen = QPen(QColor(*ui.color), ui.thickness)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)  # 关键设置
        painter.setPen(pen)
        painter.drawLine(pt1[0], pt1[1], pt2[0], pt2[1])

    @classmethod
    def draw_cell(cls, painter: QPainter, pt1, pt2, pt3, pt4, ui):
        pen = QPen(QColor(*ui.color), ui.thickness)
        painter.setBrush(QColor(*ui.fill))
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        points = [
            QPointF(*pt1), QPointF(*pt2),
            QPointF(*pt3), QPointF(*pt4)
        ]
        painter.drawPolygon(points)

    @classmethod
    def draw_circle(cls, painter: QPainter, pt, ui):
        pen = QPen(QColor(*ui.color), ui.thickness)
        painter.setPen(pen)
        painter.setBrush(QColor(*ui.fill))
        painter.drawEllipse(pt[0] - ui.radius, pt[1] - ui.radius,
                           ui.radius*2, ui.radius*2)

    @classmethod
    def draw_dot(cls, painter: QPainter, pt, ui):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(*ui.color))
        painter.drawEllipse(
            pt[0] - ui.radius, pt[1] - ui.radius,
            ui.radius*2, ui.radius*2)

    @classmethod
    def draw_text(cls, painter: QPainter, pt, text, ui):
        font = ui.font or painter.font()            # 获取当前字体
        font.setPointSize(ui.height)                # 设置字号
        painter.setFont(font)                       # 应用新字体
        painter.setPen(QColor(*ui.color))
        x,y = pt
        painter.drawText(x - ui.height*len(text)//2, y + ui.height//2, text)

    @classmethod
    def draw_icon(cls, painter: QPainter, pt, icon, w, h):
        if Path(icon).exists():
            pixmap = QPixmap(icon)
            scaled_pixmap = pixmap.scaled(
                w, h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
           )
            x = pt[0] - scaled_pixmap.width() // 2
            y = pt[1] -scaled_pixmap.height() // 2
            painter.drawPixmap(x, y, scaled_pixmap)

    def draw_tag(self, painter: QPainter, pt, ui):
        if (text := ui.get_text(self.app.get_point(pt))):
            self.draw_text(painter, pt, text, ui)
        if (icon := ui.get_icon(self.app.get_point(pt))):
            self.draw_icon(painter, pt, icon, *ui.iconsize)

    def mousePressEvent(self, event):
        """鼠标左击事件"""
        if event.button() == Qt.LeftButton:
            self.app.click_board(dot = (event.x(), event.y()))

    def drawBackground(self, painter: QPainter, rect: QRectF):
        super().drawBackground(painter, rect)
        for bglines in self.canvasboard.bg_edges:
            self.draw_line(painter, **bglines)
        for lines in self.canvasboard.canvas_texture['gr_lines']:
            self.draw_line(painter, **lines)
        for cell in self.canvasboard.canvas_texture['gr_cells']:
            self.draw_cell(painter, **cell)
        for tag in self.canvasboard.canvas_texture['gr_cltags']:
            self.draw_tag(painter, **tag)
        for tags in self.canvasboard.canvas_texture['gr_coors']:
            self.draw_text(painter, **tags)
        for stars in self.canvasboard.canvas_texture['gr_stars']:
            self.draw_dot(painter, **stars)
    
    def set_piece_default_signal(self):
        self.app.set_piece_signal('add', self.add_pieces)
        self.app.set_piece_signal('remove', self.remove_pieces)
        self.app.set_piece_signal('change', self.change_pieces)
        self.app.set_piece_signal('swap', self.swap_pieces)
        self.app.set_piece_signal('move', self.move_pieces)
        self.app.set_signal('add_tag_pts', self.add_tag_pts)
        self.app.set_signal('update_tag_pts', self.update_tag_pts)
        self.app.set_signal('remove_tag_pts', self.remove_tag_pts)
        self.app.set_signal('update_symbol', self.update_symbol)
        self.app.set_signal('remove_symbol', self.remove_symbol)
        self.app.set_signal('clear_symbol', self.clear_symbol)

    def add_pieces(self, value, pts):
        pieceui = self.app.pieceuis.get(value).copy()
        for pt in pts:
            if self.app.show_piece_index:
                pieceui.index_text = str(self.app.get_piece_index(pt))
                if pieceui.index_text == '1':
                    self.clear_index_text()
            new_piece = PieceItem(pieceui = pieceui)
            new_piece.setZValue(LAYER_PIECES)
            dot = self.app.get_dot(pt = pt)
            new_piece.setPos(*dot)
            self.scene.addItem(new_piece)
            self.pt_pieces[pt] = new_piece

    def remove_pieces(self, pts):
        """清除棋盘上的棋子"""
        for pt in pts:
            piece = self.pt_pieces.pop(pt)
            self.scene.removeItem(piece)
    
    def clear_index_text(self):
        for piece in self.pt_pieces.values():
            piece.pieceui.index_text = ''
            piece.update()

    def clear_pieces(self):
        """清除棋盘上的棋子"""
        self._current_anim.clear()
        for piece in self.pt_pieces.values():
            self.scene.removeItem(piece)
        self.pt_pieces.clear()

    def change_pieces(self, value, pts):
        self.remove_pieces(pts)
        self.add_pieces(value, pts)
    
    def swap_pieces(self, pts_links):
        for pt1, pt2 in pts_links:
            dot1 = self.app.get_dot(pt = pt1)
            dot2 = self.app.get_dot(pt = pt2)
            piece1 = self.pt_pieces.pop(pt1)
            piece2 = self.pt_pieces.pop(pt1)
            self.piece_animation(piece1, [dot1, dot2])
            self.piece_animation(piece2, [dot2, dot1])
            self.pt_pieces[pt1] = piece2
            self.pt_pieces[pt2] = piece1
    
    def move_pieces(self, pts_links):
        move_pts = [link[0] for link in pts_links]
        moved_pts = [link[-1] for link in pts_links]
        for pt in moved_pts:
            if pt not in move_pts and (
                        piece := self.pt_pieces.pop(pt, None)):
                self.scene.removeItem(piece)
        pieces = [self.pt_pieces.pop(pt, None) for pt in move_pts]
        for link, pc in zip(pts_links, pieces):
            dots = [self.app.get_dot(pt = pt) for pt in link]
            self.piece_animation(pc, dots)
            self.pt_pieces[link[-1]] = pc

    def piece_animation(self, piece, path_dots):
        # 创建动画组
        anim_group = QSequentialAnimationGroup()
        # 遍历路径点生成连续动画
        for i in range(1, len(path_dots)):
            anim = QPropertyAnimation(piece, b"pos")
            anim.setDuration(ANIM_TIME // len(path_dots))  # 均分总时间
            anim.setStartValue(QPointF(*path_dots[i-1]))
            anim.setEndValue(QPointF(*path_dots[i]))
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            anim_group.addAnimation(anim)
        # 动画结束后自动清理
        anim_group.finished.connect(lambda: (self._current_anim.pop(piece, None), 
                 piece.setZValue(LAYER_PIECES)))
        anim_group.start(QAbstractAnimation.DeleteWhenStopped)
        self._current_anim[piece] = anim_group

    def _create_tag_piece(self, tag, dot = (0, 0), show = False):
        tag_item = PieceTagItem(pieceui = self.app.pieceuis.get_tag(tag))
        tag_item.setZValue(LAYER_TAGS)
        tag_item.setPos(*dot)
        self.scene.addItem(tag_item)
        if not show:
            tag_item.hide()
        return tag_item
    
    def _add_tag_pts(self, player, pts, tag):
        self.taging_pieces.setdefault(tag, []).extend(
            self._create_tag_piece(tag,
            dot = self.app.get_dot(pt = pt), show = True
           ) for pt in pts)
    
    def add_tag_pts(self, player, pts, tag):
        if tag in [PieceTagEnum.Swap, PieceTagEnum.Move]:
            QTimer.singleShot(ANIM_TIME, lambda ps = [pt for pt in pts], t = tag: \
                    self._add_tag_pts(player, ps, t))
        else:
            self._add_tag_pts(player, pts, tag)
    
    def update_tag_pts(self, player, pts, tag):
        self.clear_tags(player)
        self.add_tag_pts(player, pts, tag)

    def remove_tag_pts(self, player, tag):
        for piece in self.taging_pieces.get(tag, []):
            self.scene.removeItem(piece)
        self.taging_pieces.get(tag, []).clear()

    def clear_tags(self, player):
        for tag in self.taging_pieces:
            self.remove_tag_pts(player, tag)

    def clear_all(self):
        self.clear_pieces()
        self.clear_tags('')
        self.clear_symbol(0, 0)
    
    def update_symbol(self, pt, tag):
        tag_item = PieceTagItem(pieceui = self.app.pieceuis.get_symbol(tag))
        tag_item.setZValue(LAYER_SYMBOL)
        tag_item.setPos(*self.app.get_dot(pt = pt))
        self.scene.addItem(tag_item)
        self.taging_symbol.setdefault(pt, []).append(tag_item)
    
    def remove_symbol(self, pt, tag):
        for piece in self.taging_symbol.get(pt, []):
            self.scene.removeItem(piece)
    
    def clear_symbol(self, pt, tag):
        for pieces in self.taging_symbol.values():
            for piece in pieces:
                self.scene.removeItem(piece)
        self.taging_symbol.clear()



class PenToolBar(QWidget):
    """侧边工具栏"""
    def __init__(self, width: int, height: int, qapp: BoardGameApp,
                 players: list[str]):  # 添加默认尺寸参数
        super().__init__()
        self.setFixedSize(width, height)
        self.qapp = qapp
        self.active_buttons = {}
        self.condition_buttons = {"race": [], "drace": []}
        self.btn_race = None
        self.setStyleSheet(PenToolBarStyle)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.create_piece_box(width)
        self.layout.addStretch(1)  # 新增的拉伸因子
        self.create_rule_buttons()
        self.create_player_buttons(players)
        self.create_move_buttons()
        self.create_history_buttons()
        self.create_tags_buttons()
        self.layout.addStretch(1)
        QTimer.singleShot(0, self.btn_race.click)  # 延迟执行确保UI加载完成

    def create_piece_box(self, width: int):
        ''' 棋子展示区域 '''
        piece_box = QWidget()
        piece_box.setFixedHeight(60)
        piece_layout = QHBoxLayout(piece_box)
        piece_layout.setContentsMargins(0, 0, 0, 0)
        self.piece_tool = PieceTool(width = width)
        piece_layout.addWidget(self.piece_tool)
        self.layout.addWidget(piece_box)
        self.layout.addSpacing(20)
    
    def reset_btns(self):
        self.btn_race.click()
    
    def create_rule_buttons(self):
        ''' 规则按钮 '''
        btn_new = QPushButton("新游戏")
        btn_new.clicked.connect(self.qapp.new_game)
        btn_race = QPushButton("比赛")
        btn_race.clicked.connect(self.qapp.on_race)
        btn_race.clicked.connect(lambda *k, g = 'rule',
                            b = btn_race: self._handle_checked(g, b))
        btn_race.clicked.connect(self.on_race)
        btn_race.setCheckable(True)  # 启用可选中状态
        self.btn_race = btn_race
        btn_drace = QPushButton("打谱")
        btn_drace.clicked.connect(self.qapp.out_race)
        btn_drace.clicked.connect(lambda *k, g = 'rule',
                            b = btn_drace: self._handle_checked(g, b))
        btn_drace.clicked.connect(self.out_race)
        btn_drace.setCheckable(True)  # 启用可选中状态
        self.layout.addWidget(btn_new)
        self.layout.addWidget(btn_race)
        self.layout.addWidget(btn_drace)
        self.layout.addSpacing(10)
    
    def create_player_buttons(self, players):
        ''' 玩家按钮 '''
        btn_container = QWidget()
        btn_container_layout = QHBoxLayout(btn_container)
        btn_container_layout.setContentsMargins(0, 0, 0, 0)
        # 创建左列布局
        left_col = QVBoxLayout()
        left_col.setSpacing(5)  # 设置按钮间距
        # 创建右列布局
        right_col = QVBoxLayout()
        right_col.setSpacing(5)  # 设置按钮间距
        for i, player in enumerate(players):
            btn_player = QPushButton(f"{player}")
            btn_player.clicked.connect(lambda *k, p=player: self.qapp.on_player(p))
            btn_player.setFixedSize(30, 30)
            self.condition_buttons['drace'].append(btn_player)
            if i % 2 == 0:
                left_col.addWidget(btn_player)
            else:
                right_col.addWidget(btn_player)
        # 将两列添加到容器
        btn_container_layout.addLayout(left_col)
        btn_container_layout.addSpacing(0)  # 列间距
        btn_container_layout.addLayout(right_col)
        self.layout.addWidget(btn_container)

        btn_turn = QPushButton("轮换执棋")
        btn_turn.clicked.connect(self.qapp.on_turns)
        btn_turn2 = QPushButton("切换棋手")
        btn_turn2.clicked.connect(self.qapp.turn_player)
        self.condition_buttons['drace'].append(btn_turn)
        self.condition_buttons['drace'].append(btn_turn2)
        self.layout.addWidget(btn_turn)
        self.layout.addWidget(btn_turn2)
        self.layout.addSpacing(10)
    
    def create_move_buttons(self):
        ''' 行棋按钮 '''
        btn_pass = QPushButton("停一手")
        btn_pass.clicked.connect(self.qapp.pass_move)
        btn_retract = QPushButton("悔棋")
        btn_retract.clicked.connect(self.qapp.ask_retract)
        btn_resign = QPushButton("认输")
        btn_resign.clicked.connect(self.qapp.resign_game)
        self.condition_buttons['race'].append(btn_retract)
        self.condition_buttons['race'].append(btn_resign)
        self.layout.addWidget(btn_pass)
        self.layout.addWidget(btn_retract)
        self.layout.addWidget(btn_resign)
        self.layout.addSpacing(10)
    
    def create_history_buttons(self):
        ''' 打谱按钮 '''
        btn_back = QPushButton("上一步")
        btn_back.clicked.connect(self.qapp.step_back)
        btn_forward = QPushButton("下一步")
        btn_forward.clicked.connect(self.qapp.step_forward)
        self.condition_buttons['drace'].append(btn_back)
        self.condition_buttons['drace'].append(btn_forward)
        self.layout.addWidget(btn_back)
        self.layout.addWidget(btn_forward)
        self.layout.addSpacing(10)

    def create_tags_buttons(self):
        ''' 标记按钮 '''
        btn_container = QWidget()
        btn_container_layout = QHBoxLayout(btn_container)
        btn_container_layout.setContentsMargins(0, 0, 0, 0)
        symbol_font = QFont("Segoe UI Symbol", 10)  # 使用系统内置符号字体
        # 创建列布局
        left_col = self._vbox_buttons('A△☆×', symbol_font, self.qapp.on_symbol_tag)
        right_col = self._vbox_buttons('1▲★√', symbol_font, self.qapp.on_symbol_tag)
        # 将两列添加到容器
        btn_container_layout.addLayout(left_col)
        btn_container_layout.addSpacing(0)  # 列间距
        btn_container_layout.addLayout(right_col)
        self.layout.addWidget(btn_container)
        btn_cl = QPushButton("清除标记")
        btn_cl.clicked.connect(lambda *k, p = "remove": self.qapp.on_symbol_tag(p))
        btn_cl.clicked.connect(lambda *k, g = 'symbols',
                            b = btn_cl: self._handle_checked(g, b))
        btn_cl.setCheckable(True)  # 启用可选中状态
        self.layout.addWidget(btn_cl)
        self.condition_buttons['drace'].append(btn_cl)
        self.layout.addSpacing(10)

    def _vbox_buttons(self, symbols, font, func):
        _col = QVBoxLayout()
        _col.setSpacing(3)  # 设置按钮间距
        for t in symbols:
            btn_tag = QPushButton(t)
            btn_tag.setFont(font)
            btn_tag.setFixedSize(30, 30)
            btn_tag.setCheckable(True)  # 启用可选中状态
            btn_tag.clicked.connect(lambda *k, p = t: func(p))
            btn_tag.clicked.connect(lambda *k, g = 'symbols',
                            b = btn_tag: self._handle_checked(g, b))
            _col.addWidget(btn_tag)
            self.condition_buttons['drace'].append(btn_tag)
        return _col

    def _handle_checked(self, group, btn):
        '''处理按钮点击事件'''
        is_checked = btn.isChecked()
        if is_checked and btn != (act := self.active_buttons.get(group, None)):
            if act:
                act.setChecked(False)
            self.active_buttons[group] = btn
    
    def on_race(self):
        for btn in self.condition_buttons['drace']:
            btn.setEnabled(False)
        for btn in self.condition_buttons['race']:
            btn.setEnabled(True)
    
    def out_race(self):
        for btn in self.condition_buttons['drace']:
            btn.setEnabled(True)
        for btn in self.condition_buttons['race']:
            btn.setEnabled(False)



class PieceTool(QGraphicsView):
    '''侧边栏，用于显示当前棋手的棋子图标'''
    def __init__(self, parent = None, width = None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)  # 创建场景
        self.setScene(self.scene)          # 关联场景到视图
        self.width = width
        self.setFixedSize(width, width)
        self.setSceneRect(0, 0, width, width)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)     # 对齐方式
        # 消除所有边距影响
        self.setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.piece = None

    def show_piece(self, pieceui):
        if self.piece:
            self.piece.pieceui = pieceui.copy(radius = self.width//4)
            self.piece.update()
            return 
        self.piece = PieceItem(pieceui = pieceui.copy(radius = self.width//4))
        self.piece.setPos(self.width//3 + self.width//20, self.width//4 + self.width//20)
        self.scene.addItem(self.piece)



class GameDialog(QDialog):
    '''弹窗'''
    def __init__(self, parent = None, title = "关于", text = ""):
        super().__init__(parent)
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(text))
        self.setLayout(layout)
        self.setStyleSheet(QDialogStyle)



class GameAsk(QMessageBox):
    """弹窗"""
    def __init__(self, parent = None, title = "标题", text = ""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QMessageBox.Icon.Information)
        self.setStandardButtons(QMessageBox.Yes |
                                QMessageBox.No)
        self.setDefaultButton(QMessageBox.Yes)
        self.setStyleSheet(GameAskStyle)
        


class PieceItem(QGraphicsObject):
    '''棋子'''
    def __init__(self, parent = None, pieceui = None):
        super().__init__(parent)
        self.pieceui = pieceui
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
    
    @property
    def radius(self):
        return self.pieceui.radius

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.update()
        return super().itemChange(change, value)
    
    def boundingRect(self) -> QRectF:
        return QRectF(-self.radius, -self.radius,
                      self.radius*2, self.radius*2)

    def paint(self, painter: QPainter, option, widget = None):
        painter.setRenderHint(QPainter.Antialiasing)
        if self.pieceui.icon:
            AppCanvas.draw_icon(painter, (0, 0), self.pieceui.icon,
                            2 * self.radius, 2 * self.radius)
        else:
            color, fill, gradientc, thickness, offset = self.pieceui.color
            painter.setPen(QPen(QColor(*color), 0))
            gradient = QRadialGradient(0, 0, self.radius)
            gradient.setColorAt(0.3, QColor(*gradientc))
            gradient.setColorAt(1, QColor(*fill))
            painter.setBrush(gradient)
            painter.drawEllipse(-self.radius, -self.radius,
                            self.radius*2, self.radius*2)
            painter.setPen(QPen(QColor(*color), thickness))
            painter.drawEllipse(-self.radius + offset, -self.radius + offset,
                        self.radius*2 - offset*2, self.radius*2 - offset*2)
        if self.pieceui.text and (self.pieceui.text.show or self.pieceui.index_text):
            text, height, color, font, show = self.pieceui.text
            font = font or painter.font()
            font.setPixelSize(height)
            painter.setFont(font)
            painter.setPen(QColor(*color))
            painter.drawText(self.boundingRect(), Qt.AlignCenter, 
                             text if show else self.pieceui.index_text)




class PieceTagItem(QGraphicsItem):
    '''棋盘上的标识，当做非棋手棋子来显示'''
    def __init__(self, parent = None, pieceui = None):
        super().__init__(parent)
        self.pieceui = pieceui
    
    @property
    def radius(self):
        return self.pieceui.radius
    
    def boundingRect(self) -> QRectF:
        """定义 Qt 的边界矩形"""
        return QRectF(-self.radius, -self.radius,
                      self.radius*2, self.radius*2)

    def paint(self, painter: QPainter, option, widget = None):
        painter.setRenderHint(QPainter.Antialiasing)
        color, fill, gradientc, thickness, offset = self.pieceui.color
        painter.setPen(QPen(QColor(*color), thickness))
        gradient = QRadialGradient(0, 0, self.radius)
        gradient.setColorAt(0.3, QColor(*gradientc))
        gradient.setColorAt(1, QColor(*fill))
        painter.setBrush(gradient)
        painter.drawEllipse(-self.radius, -self.radius,
                        self.radius*2, self.radius*2)
        if hasattr(self.pieceui, 'text') and self.pieceui.text:
            text, height, color, font, show = self.pieceui.text
            font = font or painter.font()
            font.setPixelSize(height)
            painter.setFont(font)
            painter.setPen(QColor(*color))
            painter.drawText(self.boundingRect(), Qt.AlignCenter, text)



class GameLauncher(QDialog):
    """游戏启动器窗口"""
    def __init__(self, apps, parent=None):
        super().__init__(parent)
        self.apps = apps  # 游戏字典
        self.setWindowTitle("游戏启动器")
        self.setFixedSize(300, 160)  # 设置固定大小
        layout = QVBoxLayout(self)
        
        # 标题标签
        title_label = QLabel("请选择游戏")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(title_label)
        self.game_combo = QComboBox()
        self.game_combo.addItems(apps.keys())  # 添加所有游戏名称
        self.game_combo.setFixedHeight(30)  # 设置固定高度
        layout.addWidget(self.game_combo)
        # 添加间距
        layout.addSpacing(5)
        
        # 按钮区域 - 使用网格布局使按钮居中
        button_container = QWidget()
        btn_layout = QHBoxLayout(button_container)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        self.start_btn = QPushButton("开始游戏")
        self.start_btn.setFixedSize(100, 35)  # 设置固定尺寸
        self.start_btn.clicked.connect(self.start_game)
        
        self.exit_btn = QPushButton("退出程序")
        self.exit_btn.setFixedSize(100, 35)  # 设置固定尺寸
        self.exit_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.start_btn)
        btn_layout.addSpacing(10)  # 增加按钮间距
        btn_layout.addWidget(self.exit_btn)
        layout.addWidget(button_container)
        
        # 设置整体布局边距
        layout.setContentsMargins(20, 20, 20, 20)  # 上、下、左、右
        # 设置样式
        self.setStyleSheet(GameLauncherStyle)
    
    def start_game(self):
        """开始选中的游戏"""
        selected_game = self.game_combo.currentText()
        self.accept()  # 关闭启动器
        return selected_game

    @classmethod
    def game_start(cls, name = ''):
        '''游戏启动入口'''
        qapp = QApplication(sys.argv)
        if name:
            mainWin = BoardGameApp(APPS[name]())
            mainWin.show()
            sys.exit(qapp.exec())
        else:
            # 创建启动器窗口
            launcher = cls(APPS)
            if launcher.exec() == QDialog.Accepted:
                # 获取选择的游戏名称
                game_name = launcher.start_game()
                # launcher.deleteLater()
                # QApplication.processEvents()
                # 启动游戏主窗口
                mainWin = BoardGameApp(APPS[game_name]())
                mainWin.show()
                sys.exit(qapp.exec())
            else:
                # 用户选择退出
                sys.exit(0)
