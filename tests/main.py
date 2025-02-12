import sys
import os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QTableWidgetItem,
    QAbstractItemView, QHeaderView
)
from PySide6.QtUiTools import QUiLoader
from database import Database


class ProductApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        interface_path = os.path.join(os.path.dirname(__file__), "interface.ui")
        self.ui = loader.load(interface_path, None)
        self.db = Database()

        self.ui.pushButton.clicked.connect(self.canvi_pestanya)

        # Amagar la columna ID (columna 0)
        self.ui.tableWidget.setColumnHidden(0, True)

        # Seleccionar tota la fila quan es fa clic
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Deshabilitar l'edició directa a la taula
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Configurar el redimensionament de les columnes
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.load_products()

        # Assignació dels botons i esdeveniments
        self.ui.btnAfegir_2.clicked.connect(self.add_product)
        self.ui.btnModificar_2.clicked.connect(self.update_product)
        self.ui.btnEliminar_2.clicked.connect(self.delete_product)
        self.ui.tableWidget.itemSelectionChanged.connect(self.load_selected_product)

        self.ui.show()
        
    def canvi_pestanya(self):
        """Accedir a la nova pestanya"""
        self.ui.tabWidget.setCurrentIndex(1)

    def load_products(self):
        """Carrega els productes a la taula."""
        self.ui.tableWidget.setRowCount(0)
        products = self.db.get_all_products()

        for row_index, product in enumerate(products):
            self.ui.tableWidget.insertRow(row_index)
            for col_index, data in enumerate(product):
                self.ui.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(data)))

    def add_product(self):
        """Afegeix un nou producte."""
        nom = self.ui.txtNom.text()
        preu = self.ui.txtPreu.text()
        quantitat = self.ui.txtQuantitat.text()

        if nom and preu and quantitat:
            self.db.add_product(nom, float(preu), int(quantitat))
            self.load_products()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Error", "Tots els camps són obligatoris")

    def update_product(self):
        """Modifica el producte seleccionat."""
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un producte per modificar")
            return

        reply = QMessageBox.question(self, "Confirmar", 
                                    "Vols modificar aquest producte?",
                                    QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            product_id = int(self.ui.tableWidget.item(selected_row, 0).text())
            nom = self.ui.txtNom.text()
            preu = self.ui.txtPreu.text()
            quantitat = self.ui.txtQuantitat.text()

            if nom and preu and quantitat:
                self.db.update_product(product_id, nom, float(preu), int(quantitat))
                self.load_products()
                self.clear_inputs()
            else:
                QMessageBox.warning(self, "Error", "Tots els camps són obligatoris")

    def delete_product(self):
        """Elimina el producte seleccionat."""
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un producte per eliminar")
            return
        
        reply = QMessageBox.question(self, "Confirmar", 
                                    "Vols eliminar aquest producte?",
                                    QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
                product_id = int(self.ui.tableWidget.item(selected_row, 0).text())
                self.db.delete_product(product_id)
                self.load_products()
                self.clear_inputs()
        


        product_id = int(self.ui.tableWidget.item(selected_row, 0).text())
        self.db.delete_product(product_id)
        self.load_products()
        self.clear_inputs()

    def load_selected_product(self):
        """Carrega les dades del producte seleccionat als camps d’entrada."""
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row != -1:
            self.ui.txtNom.setText(self.ui.tableWidget.item(selected_row, 1).text())
            self.ui.txtPreu.setText(self.ui.tableWidget.item(selected_row, 2).text())
            self.ui.txtQuantitat.setText(self.ui.tableWidget.item(selected_row, 3).text())

    def clear_inputs(self):
        """Buida els camps d’entrada."""
        self.ui.txtNom.clear()
        self.ui.txtPreu.clear()
        self.ui.txtQuantitat.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductApp()
    sys.exit(app.exec())
