import sys
from ..gridrule import ObjJson, CommonPlayer
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QComboBox,
                               QHBoxLayout, QPushButton, QLabel, QWidget,
                               QDialog, QMessageBox, QFileDialog)
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt
from pathlib import Path
from ..games import APPS
from .pysidegui_styles import *
from .pysidecanvas import AppCanvas
from .pysidetoobar import PenToolBar






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
        menu_bar.setStyleSheet(MenuBarStyle)
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
        help_menu.addAction("提示", self.get_next_move)

    def create_status(self):
        '''创建状态栏'''
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("开始游戏")
        
    def game_over(self, name, tag):
        '''游戏结束弹窗'''
        if name == CommonPlayer: name = self.app.active_player_name
        about_dialog = GameDialog(self, "游戏结束", f"{name}{\
                            self.app.gameover_tag(tag)}")
        about_dialog.exec()

    def new_game(self):
        """新游戏"""
        self.qapp_canvas.pieces_manager.clear_all()
        self.tool_bar.reset_btns("比赛")
        self.app.rebegin()
        self.app.refresh_matr_pts()
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
        self.qapp_canvas.pieces_manager.clear_all()
        self.app.rebegin()
        self.app.load_data(self._open_data())
        self.app.refresh_matr_pts()
        self.tool_bar.reset_btns("打谱")

    def exit_game(self):
        """退出游戏"""
        self.close()

    def set_race_mode(self, is_race):
        """比赛, 打谱"""
        self.app.set_race_mode(is_race)

    def show_about(self):
        """显示关于信息"""
        about_dialog = GameDialog(self, "关于", self.app.about_info)
        about_dialog.exec()
    
    def get_next_move(self):
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
        if name == '_on_turns_':
            self.app.on_turns()
        elif name == '_turn_player_':
            self.app.turn_player()
        else:
            self.app.on_player(name)
    
    def set_symbol_tag(self, tag):
        self.app.set_symbol_tag(tag)

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
                # 启动游戏主窗口
                mainWin = BoardGameApp(APPS[game_name]())
                mainWin.show()
                sys.exit(qapp.exec())
            else:
                # 用户选择退出
                sys.exit(0)