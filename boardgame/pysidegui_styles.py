
QMainWindowStyle ="""
    background: transparent;
    QMenuBar { background: rgba(255,255,255,0.7); }
    QStatusBar { background: rgba(255,255,255,0.7); }
"""

PenToolBarStyle = """
    QPushButton {
        border-radius: 4px;
        padding: 6px;
        margin: 1px;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
    }
    QPushButton:hover {
        background-color: #e9ecef;
    }
    QPushButton:checked {
        background-color: #B0C4DE;
        border: 1px solid #2080FF;
    }
"""


QDialogStyle ="""
    QDialog {
        background-color: #f8f9fa;
    }
"""

GameAskStyle ="""
    QMessageBox {
        background-color: rgba(248, 249, 250, 0.95);
        border: 1px solid #dee2e6;
        border-radius: 8px;
        font-family: "Microsoft YaHei";
    }
    QLabel {
        color: #495057;
        font-size: 14px;
        margin: 15px;
    }
    QPushButton {
        background-color: #e9ecef;
        border: 1px solid #ced4da;
        border-radius: 4px;
        min-width: 80px;
        padding: 6px 12px;
        color: #212529;
    }
    QPushButton:hover {
        background-color: #dee2e6;
    }
    QPushButton:pressed {
        background-color: #ced4da;
    }
"""


GameLauncherStyle = """
    QDialog {
        background-color: #f8f9fa;
    }
    QLabel {
        color: #333;
    }
    QComboBox {
        padding: 5px;
        border: 1px solid #ced4da;
        border-radius: 4px;
        background-color: white;
    }
    QPushButton {
        background-color: #B0C4DE;
        color: white;
        border-radius: 4px;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #3399ff;
    }
"""

