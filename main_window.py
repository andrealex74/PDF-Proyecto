from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QStatusBar
from PyQt5.QtGui import QFont
from split_pdf_widget import SplitPDFWidget
from merge_pdf_widget import MergePDFWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Aplicación de PDFs")
        self.resize(600, 500)

        # Fuente personalizada
        font = QFont("Arial", 12)
        self.setFont(font)

        # Estilos
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                color: #333333;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 10px;
            }
            QTabBar::tab:selected {
                background: #4CAF50;
                color: white;
            }
        """)

        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Pestañas
        tabs = QTabWidget()
        self.split_tab = SplitPDFWidget()
        self.merge_tab = MergePDFWidget()
        tabs.addTab(self.split_tab, "Dividir PDF")
        tabs.addTab(self.merge_tab, "Unir PDFs")

        # Barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Agregar pestañas al layout
        layout.addWidget(tabs)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
