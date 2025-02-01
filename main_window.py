from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from split_pdf_widget import SplitPDFWidget
from merge_pdf_widget import MergePDFWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Easy PDF")
        self.resize(500, 400)
        layout = QVBoxLayout()
        tabs = QTabWidget()

        # Agregar pestaña para Dividir PDF
        self.split_tab = SplitPDFWidget()
        tabs.addTab(self.split_tab, "Dividir PDF")

        # Agregar pestaña para Unir PDFs con PDF fijo
        self.merge_tab = MergePDFWidget()
        tabs.addTab(self.merge_tab, "Unir PDFs con un PDF fijo")

        layout.addWidget(tabs)
        self.setLayout(layout)
