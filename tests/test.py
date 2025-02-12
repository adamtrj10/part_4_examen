import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from database import Database
from main import ProductApp

@pytest.fixture
def app(qtbot):
    
    # aquesta part la he fet amb IA perquè no sabia com fer el test sense tocar la base de dades existent, 
    # és una base de dades "temporal" que agafa la que ja tenim pero no la modifica ni res.
    test_db = Database(":memory:")  
    test_app = ProductApp()
    test_app.db = test_db  
    qtbot.addWidget(test_app.ui)
    return test_app

def test_add_product(app, qtbot):
    
    # camps que tenim en add_product
    app.ui.txtNom.setText("Cocacola")
    app.ui.txtPreu.setText("2.20")
    app.ui.txtQuantitat.setText("5")

    qtbot.mouseClick(app.ui.btnAfegir_2, Qt.LeftButton)

    products = app.db.get_all_products()
    
    assert len(products) == 1
    assert products[0][1] == "Cocacola" 
    assert products[0][2] == 2.20  
    assert products[0][3] == 5 

    assert app.ui.tableWidget.rowCount() == 1
    assert app.ui.tableWidget.item(0, 1).text() == "Cocacola"
    assert app.ui.tableWidget.item(0, 2).text() == "2.20"
    assert app.ui.tableWidget.item(0, 3).text() == "5"
