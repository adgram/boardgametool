
from PySide6.QtWidgets import (QVBoxLayout, QGraphicsView, QGraphicsScene,
                               QHBoxLayout, QPushButton, QWidget)
from PySide6.QtGui import QPainter,  QFont
from PySide6.QtCore import Qt
from .pysidegui_styles import *
from .pysidecanvas import PieceItem




class PenToolBar(QWidget):
    """侧边工具栏"""
    def __init__(self, width: int, height: int, qapp: 'BoardGameApp',
                 players: list[str]):  # 添加默认尺寸参数
        super().__init__()
        self.setFixedSize(width, height)
        self.qapp = qapp
        self.active_buttons = {}
        self.condition_buttons = {"race": [], "drace": []}
        self.btn_race_mode = None
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
        self.reset_btns()

    def create_piece_box(self, width: int):
        ''' 棋子展示区域 '''
        piece_box, piece_layout = self._create_hbox_container()
        piece_box.setFixedHeight(60)
        self.piece_tool = PieceTool(width = width)
        piece_layout.addWidget(self.piece_tool)
        self.layout.addWidget(piece_box)
        self.layout.addSpacing(20)
    
    def reset_btns(self):
        self.btn_race_mode.setText("比赛")
        self._toggle_race_mode()
    
    def create_rule_buttons(self):
        ''' 规则按钮 '''
        self._create_button("新游戏", self.qapp.new_game)
        self.btn_race_mode = self._create_button("打谱", self._toggle_race_mode)
        self.layout.addSpacing(10)
    
    def _toggle_race_mode(self):
        """切换比赛/打谱模式"""
        b = (self.btn_race_mode.text() == "比赛")
        self.btn_race_mode.setText("打谱" if b else "比赛")
        self.qapp.set_race_mode(b)
        self._set_race_mode(b)
        
    def create_player_buttons(self, players):
        ''' 玩家按钮 '''
        btn_container, btn_container_layout = self._create_hbox_container()
        # 创建左列布局
        left_col = QVBoxLayout()
        left_col.setSpacing(5)  # 设置按钮间距
        # 创建右列布局
        right_col = QVBoxLayout()
        right_col.setSpacing(5)  # 设置按钮间距
        for i, player in enumerate(players):
            btn_player = QPushButton(f"{player}")
            btn_player.clicked.connect(self._handle_checked('player', btn_player, player = player))
            btn_player.setFixedSize(30, 30)
            self._register_button('drace', btn_player)
            if i % 2 == 0:
                left_col.addWidget(btn_player)
            else:
                right_col.addWidget(btn_player)
        # 将两列添加到容器
        btn_container_layout.addLayout(left_col)
        btn_container_layout.addSpacing(0)  # 列间距
        btn_container_layout.addLayout(right_col)
        self.layout.addWidget(btn_container)
        on_turns_btn = self._create_button("轮换执棋", None, 'drace')
        turn_btn = self._create_button("切换棋手", None, 'drace')
        on_turns_btn.clicked.connect(self._handle_checked('player', on_turns_btn, player = '_on_turns_'))
        turn_btn.clicked.connect(self._handle_checked('player', turn_btn, player = '_turn_player_'))
        self.layout.addSpacing(10)
    
    def create_move_buttons(self):
        ''' 行棋按钮 '''
        self._create_button("停一手", self.qapp.pass_move)
        self._create_button("悔棋", self.qapp.ask_retract, 'race')
        self._create_button("认输", self.qapp.resign_game, 'race')
        self.layout.addSpacing(10)
    
    def create_history_buttons(self):
        ''' 打谱按钮 '''
        self._create_button("上一步", self.qapp.step_back, 'drace')
        self._create_button("下一步", self.qapp.step_forward, 'drace')
        self.layout.addSpacing(10)

    def create_tags_buttons(self):
        ''' 标记按钮 '''
        btn_container, btn_container_layout = self._create_hbox_container()
        symbol_font = QFont("Segoe UI Symbol", 10)  # 使用系统内置符号字体
        # 创建列布局
        left_col = self._vbox_buttons('A△☆×', symbol_font, self.qapp.set_symbol_tag)
        right_col = self._vbox_buttons('1▲★√', symbol_font, self.qapp.set_symbol_tag)
        # 将两列添加到容器
        btn_container_layout.addLayout(left_col)
        btn_container_layout.addSpacing(0)  # 列间距
        btn_container_layout.addLayout(right_col)
        self.layout.addWidget(btn_container)
        btn_cl = self._create_button("清除标记", None, 'drace')
        btn_cl.clicked.connect(self._handle_checked('symbols', btn_cl, symbol = 'remove'))
        btn_pen = self._create_button("画笔", None, 'drace')
        btn_pen.clicked.connect(self._handle_checked('pens', btn_pen))
        btn_es = self._create_button("橡皮擦", None, 'drace')
        btn_es.clicked.connect(self._handle_checked('pens', btn_es))
        self.layout.addSpacing(10)

    def _vbox_buttons(self, symbols, font, func):
        _col = QVBoxLayout()
        _col.setSpacing(3)  # 设置按钮间距
        for t in symbols:
            btn_tag = QPushButton(t)
            btn_tag.setFont(font)
            btn_tag.setFixedSize(30, 30)
            btn_tag.setCheckable(True)  # 启用可选中状态
            btn_tag.clicked.connect(self._handle_checked('symbols', btn_tag, symbol = t))
            _col.addWidget(btn_tag)
            self._register_button('drace', btn_tag)
        return _col

    def _handle_checked(self, group, btn, symbol = '', player = ''):
        '''处理按钮点击事件'''
        btn.setCheckable(True)  # 启用可选中状态
        def func(*k, group = group, btn = btn):
            self.clear_checked()
            if btn.isChecked():
                if group == 'pens':
                    self._symbols_clicked(btn)
                self.active_buttons[group] = btn
                if symbol:
                    self.qapp.set_symbol_tag(symbol)
                if player:
                    self.qapp.on_player(player)
        return func
    
    def _symbols_clicked(self, btn):
        if btn.text() == "画笔":
            self.qapp.qapp_canvas.painting.set_drawing_mode('pen')
        elif btn.text() == "橡皮擦":
            self.qapp.qapp_canvas.painting.set_drawing_mode('eraser')
        elif btn.text() == "清空画布":
            self.qapp.qapp_canvas.painting.clear_drawings()
    
    def clear_checked(self):
        self.qapp.qapp_canvas.painting.set_drawing_mode(None)
        self.qapp.set_symbol_tag('')
        for btn in self.active_buttons.values():
            if btn:
                btn.setChecked(False)
        self.active_buttons.clear()

    def _set_race_mode(self, is_race):
        for btn in self.condition_buttons['drace']:
            btn.setVisible(not is_race)
        for btn in self.condition_buttons['race']:
            btn.setVisible(is_race)
            btn.setChecked(False)
    
    def _create_hbox_container(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        return container, layout

    def _register_button(self, group, button):
        self.condition_buttons[group].append(button)

    def _create_button(self, text, callback, group = None):
        btn = QPushButton(text)
        if callback:
            btn.clicked.connect(callback)
        if group:
            self._register_button(group, btn)
        self.layout.addWidget(btn)
        return btn




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

