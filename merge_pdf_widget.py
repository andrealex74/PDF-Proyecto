import os
import PyPDF2
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QMessageBox
)

class MergePDFWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pdf_folder = ""
        self.fixed_pdf = ""
        self.output_folder = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Seleccionar carpeta de PDFs base
        self.folder_btn = QPushButton("Seleccionar Carpeta de PDFs")
        self.folder_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_btn)
        self.folder_label = QLabel("No se ha seleccionado ninguna carpeta.")
        layout.addWidget(self.folder_label)

        # Seleccionar PDF fijo
        self.fixed_btn = QPushButton("Seleccionar PDF Fijo")
        self.fixed_btn.clicked.connect(self.select_fixed_pdf)
        layout.addWidget(self.fixed_btn)
        self.fixed_label = QLabel("No se ha seleccionado ningún PDF fijo.")
        layout.addWidget(self.fixed_label)

        # Seleccionar carpeta de salida (ahora obligatorio)
        self.output_btn = QPushButton("Seleccionar Carpeta de Salida")
        self.output_btn.clicked.connect(self.select_output_folder)
        layout.addWidget(self.output_btn)
        self.output_label = QLabel("No se ha seleccionado ninguna carpeta de salida.")
        layout.addWidget(self.output_label)

        # Botón para unir los PDFs
        self.merge_btn = QPushButton("Unir PDFs")
        self.merge_btn.clicked.connect(self.merge_pdfs)
        self.merge_btn.setObjectName("primaryButton")
        layout.addWidget(self.merge_btn)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Seleccionar Carpeta de PDFs"
        )
        if folder:
            self.pdf_folder = folder
            self.folder_label.setText(folder)

    def select_fixed_pdf(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar PDF Fijo", "", "Archivos PDF (*.pdf)"
        )
        if file:
            self.fixed_pdf = file
            self.fixed_label.setText(file)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Seleccionar Carpeta de Salida"
        )
        if folder:
            self.output_folder = folder
            self.output_label.setText(folder)

    def merge_pdfs(self):
        # Validar selecciones
        if not self.pdf_folder:
            QMessageBox.warning(
                self, "Error", "Por favor, selecciona la carpeta que contiene los PDFs."
            )
            return
        if not self.fixed_pdf:
            QMessageBox.warning(
                self, "Error", "Por favor, selecciona el PDF fijo."
            )
            return
        if not self.output_folder:
            QMessageBox.warning(
                self, "Error", "Por favor, selecciona la carpeta de salida."
            )
            return
        
        output_dir = self.output_folder
        pdf_files = [f for f in os.listdir(self.pdf_folder) if f.lower().endswith(".pdf")]
        if not pdf_files:
            QMessageBox.warning(
                self, "Error", "No se encontraron archivos PDF en la carpeta seleccionada."
            )
            return

        try:
            fixed_reader = PyPDF2.PdfReader(self.fixed_pdf)
            count = 0
            for pdf_file in pdf_files:
                base_pdf_path = os.path.join(self.pdf_folder, pdf_file)
                base_reader = PyPDF2.PdfReader(base_pdf_path)
                pdf_writer = PyPDF2.PdfWriter()
                for page in base_reader.pages:
                    pdf_writer.add_page(page)
                for page in fixed_reader.pages:
                    pdf_writer.add_page(page)
                base_name = os.path.splitext(pdf_file)[0]
                output_filename = os.path.join(output_dir, f"{base_name}.pdf")
                with open(output_filename, "wb") as out_file:
                    pdf_writer.write(out_file)
                count += 1

            QMessageBox.information(
                self, "Éxito", f"Se han generado {count} PDFs fusionados."
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error al unir los PDFs:\n{str(e)}"
            )
