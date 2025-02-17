from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTabWidget, QWidget, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import Qt, QPoint

from split_pdf_widget import SplitPDFWidget
from merge_pdf_widget import MergePDFWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.oldPos = self.pos()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setWindowTitle("PODIF")
        self.setFixedSize(400, 700)  # Fija el tamaño de la ventana

        # Aplicar estilos
        self.apply_styles()

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(10)  # Espacio entre widgets
        layout.setContentsMargins(20, 0, 20, 20)  # Márgenes del layout

        # Barra de título personalizada
        self.setup_custom_title_bar(layout)

        # Pestañas para diferentes funciones
        tabs = QTabWidget()
        tabs.addTab(SplitPDFWidget(), "Dividir PDF")
        tabs.addTab(MergePDFWidget(), "Unir PDFs")
        layout.addWidget(tabs)

        # Asignar layout al widget central
        central_widget.setLayout(layout)


    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border-radius: 15px;
            }
            QLineEdit {
                background-color: #2d2d2d;  /* Fondo más oscuro para mayor contraste */
                color: #d0d0d0;  /* Color de texto gris claro */
                border: 2px solid #555555;  /* Borde sutil */
                padding: 5px;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3949ab;  /* Borde azul cuando el campo está enfocado */
            }
            QPushButton {
                background-color: #3949ab;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5c6bc0;
            }
            QPushButton#minButton {
            background-color: transparent;
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 8px 18px;
            border-radius: 8px;  /* Bordes más redondeados */
            }
            QPushButton#primaryButton {
            background-color: #123456;
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 12px 24px;
            border-radius: 8px;  /* Bordes más redondeados */
            }
            QPushButton#primaryButton:hover {
                background-color: #123446;
            }
            QPushButton#closeButton {
            background-color: transparent;  /* Rojo oscuro */
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 8px;  /* Bordes más redondeados */
            }
            QPushButton#closeButton:hover {
                background-color: #d32f2f;  /* Rojo más claro */
            }
            QLabel {
                color: #e0e0e0; /* Color letras */
            }
            QTabWidget::pane {
                border: 0px solid #444;
                border-radius: 5px;
                padding: 10px;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background: #6a1b9a;
                color: #e0e0e0;
                padding: 10px 20px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 5px;
            }
            QTabBar::tab:selected {
                background: #2d2d2d;
                color: white;
            }

        """)

    def setup_custom_title_bar(self, layout):
        title_bar = QWidget()
        title_layout = QHBoxLayout()
        title_bar.setLayout(title_layout)
        title_bar.setObjectName("titleBar")
        title_bar.setMouseTracking(True)

        title_label = QLabel("PODIF")
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        minimize_button = QPushButton("─")
        minimize_button.clicked.connect(self.showMinimized)
        title_layout.addWidget(minimize_button)
        minimize_button.setObjectName("minButton")

        close_button = QPushButton("✕")
        close_button.clicked.connect(self.close)
        title_layout.addWidget(close_button)
        close_button.setObjectName("closeButton")

        layout.addWidget(title_bar)



    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
