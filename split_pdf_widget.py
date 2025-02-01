import os
import PyPDF2
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QMessageBox, QDateEdit, QLineEdit
)

class SplitPDFWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pdf_path = ""
        self.excel_path = ""
        self.names_list = []  # Lista de nombres extraídos del Excel
        self.pdf_save_folder = ""  # Carpeta donde se guardarán los PDFs divididos
        self.new_dirs_folder = ""  # Carpeta donde se crearán las carpetas nuevas
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Botón para seleccionar el PDF a dividir
        self.select_pdf_btn = QPushButton("Selecciona el PDF a dividir")
        self.select_pdf_btn.clicked.connect(self.select_pdf)
        layout.addWidget(self.select_pdf_btn)

        self.pdf_label = QLabel("No se ha seleccionado ningún PDF")
        layout.addWidget(self.pdf_label)

        # Selección de fecha mediante QDateEdit
        layout.addWidget(QLabel("Selecciona la fecha:"))
        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.date_edit.setCalendarPopup(True)
        layout.addWidget(self.date_edit)

<<<<<<< HEAD
=======
        # Botón para seleccionar el archivo Excel de nombres (incluye *.xlsm*)
        self.select_excel_btn = QPushButton("Selecciona el archivo Excel")
        self.select_excel_btn.clicked.connect(self.select_excel)
        layout.addWidget(self.select_excel_btn)

        self.excel_label = QLabel("No se ha seleccionado ningún archivo Excel")
        layout.addWidget(self.excel_label)

>>>>>>> 056375e8d43e107ba2b597490dcc457a89bd3031
        # Parámetros para extraer nombres del Excel: hoja, columna y fila de inicio
        excel_params_layout = QHBoxLayout()
        self.sheet_lineedit = QLineEdit()
        self.sheet_lineedit.setPlaceholderText("Nombre de Hoja (ej. Hoja1)")
        excel_params_layout.addWidget(self.sheet_lineedit)

        self.column_lineedit = QLineEdit()
        self.column_lineedit.setPlaceholderText("Columna (ej. G)")
        excel_params_layout.addWidget(self.column_lineedit)

        self.row_lineedit = QLineEdit()
        self.row_lineedit.setPlaceholderText("Fila inicio (ej. 1)")
        excel_params_layout.addWidget(self.row_lineedit)
        layout.addLayout(excel_params_layout)

        # Botón para seleccionar el archivo Excel de nombres (incluye *.xlsm*)
        self.select_excel_btn = QPushButton("Selecciona el archivo Excel")
        self.select_excel_btn.clicked.connect(self.select_excel)
        layout.addWidget(self.select_excel_btn)

        self.excel_label = QLabel("No se ha seleccionado ningún archivo Excel")
        layout.addWidget(self.excel_label)

        # Mostrar cantidad de nombres extraídos
        self.names_count_label = QLabel("Número de nombres extraídos: 0")
        layout.addWidget(self.names_count_label)

        # Seleccionar carpeta para guardar los PDFs divididos (Carpeta A)
        self.select_pdf_save_folder_btn = QPushButton("Selecciona la carpeta de destino")
        self.select_pdf_save_folder_btn.clicked.connect(self.select_pdf_save_folder)
        layout.addWidget(self.select_pdf_save_folder_btn)

        self.pdf_save_folder_label = QLabel("No se ha seleccionado la carpeta de destino")
        layout.addWidget(self.pdf_save_folder_label)

        # Seleccionar carpeta para crear las carpetas nuevas (Carpeta B)
        self.select_new_dirs_folder_btn = QPushButton("Carpeta de destino para crear subcarpetas")
        self.select_new_dirs_folder_btn.clicked.connect(self.select_new_dirs_folder)
        layout.addWidget(self.select_new_dirs_folder_btn)

        self.new_dirs_folder_label = QLabel("No se ha seleccionado ninguna carpeta")
        layout.addWidget(self.new_dirs_folder_label)

        # Botón para dividir el PDF
        self.split_btn = QPushButton("DIVIDIR Y CREAR")
        self.split_btn.clicked.connect(self.split_pdf)
        layout.addWidget(self.split_btn)

        self.setLayout(layout)

    def select_pdf(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar PDF a dividir", "", "Archivos PDF (*.pdf)"
        )
        if file:
            self.pdf_path = file
            self.pdf_label.setText(file)

    def select_excel(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo Excel", "", "Archivos Excel (*.xlsx *.xls *.xlsm)"
        )
        if file:
            self.excel_path = file
            self.excel_label.setText(file)
            self.extract_names_from_excel()

    def select_pdf_save_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Seleccionar carpeta para guardar PDFs"
        )
        if folder:
            self.pdf_save_folder = folder
            self.pdf_save_folder_label.setText(folder)

    def select_new_dirs_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Seleccionar carpeta para crear carpetas nuevas"
        )
        if folder:
            self.new_dirs_folder = folder
            self.new_dirs_folder_label.setText(folder)

    def extract_names_from_excel(self):
        sheet = self.sheet_lineedit.text().strip()
        column = self.column_lineedit.text().strip()
        row_str = self.row_lineedit.text().strip()
        if not sheet or not column or not row_str:
            QMessageBox.warning(
                self, "Parámetros incompletos",
                "Por favor, ingresa el nombre de la hoja, la columna y la fila de inicio para extraer los nombres."
            )
            return
        try:
            start_row = int(row_str)
        except ValueError:
            QMessageBox.warning(self, "Error", "La fila de inicio debe ser un número entero.")
            return
        try:
            # Leer el Excel sin header para que la fila 1 corresponda al índice 0
            df = pd.read_excel(self.excel_path, sheet_name=sheet, header=None, engine='openpyxl')
            col_index = self.column_letter_to_index(column)
            if col_index < 0 or col_index >= df.shape[1]:
                QMessageBox.warning(self, "Error", "La columna especificada no es válida.")
                return
            # Extraer nombres desde la fila indicada hasta el final
            names_series = df.iloc[start_row - 1:, col_index]
            names = names_series.dropna().tolist()
            names = [str(name).strip() for name in names if str(name).strip() != ""]
            # Procesar los nombres: si se repiten, se les agrega un índice solo a los duplicados
            names = self.process_duplicate_names(names)
            self.names_list = names
            self.names_count_label.setText(f"Número de nombres extraídos: {len(names)}")
        except Exception as e:
            QMessageBox.critical(self, "Error al leer Excel", f"No se pudieron extraer los nombres:\n{str(e)}")

    def column_letter_to_index(self, letter):
        letter = letter.upper().strip()
        result = 0
        for char in letter:
            if 'A' <= char <= 'Z':
                result = result * 26 + (ord(char) - ord('A') + 1)
            else:
                return -1
        return result - 1

    def process_duplicate_names(self, names):
        """
        Procesa una lista de nombres y agrega un índice secuencial solo a aquellos que se repiten.
        Si un nombre aparece una única vez, se conserva sin modificar.
        """
        frequency = {}
        for name in names:
            frequency[name] = frequency.get(name, 0) + 1

        result = []
        seen = {}
        for name in names:
            if frequency[name] > 1:
                seen[name] = seen.get(name, 0) + 1
                result.append(f"{name} {seen[name]}")
            else:
                result.append(name)
        return result

    def split_pdf(self):
        if not self.pdf_path:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un archivo PDF.")
            return
        if not self.names_list:
            QMessageBox.warning(self, "Error", "Por favor, selecciona y procesa el archivo Excel para obtener los nombres.")
            return
        if not self.pdf_save_folder:
            QMessageBox.warning(self, "Error", "Por favor, selecciona la carpeta para guardar los PDFs.")
            return
        if not self.new_dirs_folder:
            QMessageBox.warning(self, "Error", "Por favor, selecciona la carpeta para crear las carpetas nuevas.")
            return

        try:
            pdf_reader = PyPDF2.PdfReader(self.pdf_path)
            num_pages = len(pdf_reader.pages)
            if num_pages != len(self.names_list):
                QMessageBox.warning(
                    self, "Error",
                    f"El número de páginas del PDF ({num_pages}) no coincide con el número de nombres extraídos ({len(self.names_list)})."
                )
                return

            date_str = self.date_edit.date().toString("dd-MM-yyyy")

            for i in range(num_pages):
                pdf_writer = PyPDF2.PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[i])
                # Nombre del PDF: <fecha> RPV <nombre extraído>.pdf
                new_filename = f"{date_str} RPV {self.names_list[i]}.pdf"
                # Guardar el PDF en la carpeta seleccionada para PDFs
                output_pdf_path = os.path.join(self.pdf_save_folder, new_filename)
                with open(output_pdf_path, "wb") as out_file:
                    pdf_writer.write(out_file)
                # Crear la carpeta nueva en la carpeta designada para carpetas nuevas,
                # usando el nombre extraído (con índice si corresponde)
                new_folder_path = os.path.join(self.new_dirs_folder, self.names_list[i])
                if not os.path.exists(new_folder_path):
                    os.makedirs(new_folder_path)

            QMessageBox.information(
                self, "Éxito",
                f"El PDF se ha dividido en {num_pages} archivos."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al dividir el PDF:\n{str(e)}")
