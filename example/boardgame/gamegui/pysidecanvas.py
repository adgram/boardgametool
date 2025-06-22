
from ..gridrule import PieceTagEnum
from PySide6.QtWidgets import (QGraphicsItem, QGraphicsView, QGraphicsScene,
                               QGraphicsObject, QGraphicsPathItem)
from PySide6.QtGui import QPainter, QPen, QColor, QRadialGradient, QPixmap, QPainterPath
from PySide6.QtCore import (Qt, QRectF, QPropertyAnimation, QPointF,
                            QEasingCurve, QAbstractAnimation, QTimer,
                            QSequentialAnimationGroup)
from pathlib import Path
from .pysidegui_styles import *


ANIM_TIME = 400
LAYER_BACKGROUND = -100  # 背景层（网格、纹理等）
LAYER_PIECES = 0         # 棋子层（主游戏对象）
LAYER_SYMBOL = 10        # 符号层（棋子序号）
LAYER_TAGS = 20          # 标记层（特殊标记）
LAYER_ANIMATION = 30     # 动画层
LAYER_PEN = 40          # 标记层（画笔）




class AppCanvas(QGraphicsView):
    """画布"""
    def __init__(self, parent = None, app = None):
        super().__init__(parent)
        self.app = app
        self.canvasboard = app.canvasboard
        self.scene = QGraphicsScene(self)  # 创建场景
        self.setScene(self.scene)          # 关联场景到视图
        # 画笔状态
        self.painting = Painting(self)
        self.pieces_manager = PiecesManager(self)
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
        points = [QPointF(*pt1), QPointF(*pt2),
            QPointF(*pt3), QPointF(*pt4)]
        painter.drawPolygon(points)

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
        if self.painting.drawing_mode:
            self.painting.mouse_press(event)
        else:
            if event.button() == Qt.LeftButton:
                self.app.click_board(dot = (event.x(), event.y()))

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        self.painting.mouse_move(event)

    def mouseReleaseEvent(self, event):
        self.painting.mouse_release(event)

    def drawBackground(self, painter: QPainter, rect: QRectF):
        super().drawBackground(painter, rect)
        background = self.canvasboard.canvas_background
        for edges in background['edges']:
            self.draw_line(painter, **edges)
        for cell in background['cells']:
            self.draw_cell(painter, **cell)
        for tag in background['cltags']:
            self.draw_tag(painter, **tag)
        for tags in background['coors']:
            self.draw_text(painter, **tags)
        for stars in background['stars']:
            self.draw_dot(painter, **stars)
        for dot_pair in background['pieces']:
            self.pieces_manager.add_dot_piece(*dot_pair)
            painter.drawEllipse(
                dot_pair[1][0] - 4, dot_pair[1][1] - 4,
                8, 8)

    def update_background(self):
        painter = QPainter(self)
        background = self.canvasboard.until_background
        for edges in background['edges']:
            self.draw_line(painter, **edges)
        for cell in background['cells']:
            self.draw_cell(painter, **cell)
        for tag in background['cltags']:
            self.draw_tag(painter, **tag)
        for stars in background['stars']:
            self.draw_dot(painter, **stars)
    


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



class Painting:
    def __init__(self, canvas = None):
        self.canvas = canvas
        self.scene = self.canvas.scene
        self.drawing_mode = None  # None/'pen'/'eraser'
        self.last_pos = None
        self.current_path = None  # 用于跟踪当前绘制路径
        self.path_items = []  # 存储所有绘制路径项
        self.pen_color = Qt.red
        self.pen_size = 3

    def mouse_press(self, event):
        """鼠标左击事件"""
        if self.drawing_mode == 'pen' and event.button() == Qt.LeftButton:
            # 开始新的绘制路径
            self.last_pos = self.canvas.mapToScene(event.pos())
            self.current_path = QPainterPath()
            self.current_path.moveTo(self.last_pos)
            # 创建新的路径项并添加到场景
            path_item = QGraphicsPathItem(self.current_path)
            path_item.setPen(QPen(self.pen_color, self.pen_size, 
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            path_item.setZValue(LAYER_PEN)  # 在画笔层绘制
            self.scene.addItem(path_item)
            self.path_items.append(path_item)
        elif self.drawing_mode == 'eraser' and event.button() == Qt.LeftButton:
            # 橡皮擦模式：删除鼠标位置下的路径项
            pos = self.canvas.mapToScene(event.pos())
            self.erase_at_position(pos)

    def mouse_move(self, event):
        """鼠标移动事件"""
        if self.drawing_mode == 'pen' and event.buttons() & Qt.LeftButton and self.current_path:
            current_pos = self.canvas.mapToScene(event.pos())
            self.current_path.lineTo(current_pos)
            # 更新最后一条路径项的路径
            if self.path_items:
                self.path_items[-1].setPath(self.current_path)
            self.last_pos = current_pos
        elif self.drawing_mode == 'eraser' and event.buttons() & Qt.LeftButton:
            # 橡皮擦模式：删除鼠标移动路径上的路径项
            pos = self.canvas.mapToScene(event.pos())
            self.erase_at_position(pos)

    def mouse_release(self, event):
        self.last_pos = None
        self.current_path = None

    def erase_at_position(self, pos):
        """在指定位置擦除绘制内容"""
        # 查找鼠标位置下的所有项目
        items = self.scene.items(pos)
        # 只删除画笔层的路径项
        for item in items:
            if isinstance(item, QGraphicsPathItem) and item.zValue() == LAYER_PEN:
                # 从场景和路径项列表中移除
                self.scene.removeItem(item)
                if item in self.path_items:
                    self.path_items.remove(item)

    def set_drawing_mode(self, mode):
        """设置绘制模式"""
        self.drawing_mode = mode

    def clear_drawings(self):
        """清除所有绘制内容"""
        # 遍历所有路径项
        for item in self.path_items[:]:  # 使用切片创建副本，避免修改过程中遍历问题
            # 从场景中移除项
            self.scene.removeItem(item)
            # 从列表中移除
            self.path_items.remove(item)



class PiecesManager:
    """管理所有棋子"""
    def __init__(self, canvas = None):
        self.canvas = canvas
        self.app = self.canvas.app
        self.scene = self.canvas.scene
        self.pt_pieces = {}
        self.taging_pieces = {}
        self.taging_symbol = {}
        self._current_anim = {}
        self.set_piece_default_signal()
        self.app.add_default_piece_pts()

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

    def add_pieces(self, pts_map):
        tag = True
        for value, pts in pts_map.items():
            pieceui = self.app.pieceuis.get(value).copy()
            for pt in pts:
                if self.app.show_piece_index:
                    pieceui.index_text = str(self.app.get_piece_index(pt))
                    if tag and pieceui.index_text in ['1', '0']:
                        self.clear_index_text()
                        tag = False
                new_piece = PieceItem(pieceui = pieceui)
                new_piece.setZValue(LAYER_PIECES)
                dot = self.app.get_dot(pt = pt)
                new_piece.setPos(*dot)
                self.scene.addItem(new_piece)
                self.pt_pieces[pt] = new_piece

    def add_dot_piece(self, value, dot):
        pieceui = self.app.pieceuis.get(value).copy()
        new_piece = PieceItem(pieceui = pieceui)
        new_piece.setZValue(LAYER_PIECES)
        new_piece.setPos(*dot)
        self.scene.addItem(new_piece)

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

    def change_pieces(self, pts_map):
        self.remove_pieces(sum(pts_map.values(), []))
        self.add_pieces(pts_map)
    
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
