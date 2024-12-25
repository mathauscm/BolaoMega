import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QFormLayout,
                             QLineEdit, QDialog, QVBoxLayout, QPushButton, QWidget,
                             QLabel, QTableWidget, QTableWidgetItem, QMenuBar)


class InsertDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Inserir Apostador')
        self.setGeometry(100, 100, 300, 200)

        # Layout para formulário
        layout = QFormLayout()

        self.name_field = QLineEdit(self)
        self.number_fields = [QLineEdit(self) for _ in range(6)]

        layout.addRow('Nome do Apostador:', self.name_field)
        for i, field in enumerate(self.number_fields, start=1):
            layout.addRow(f'Número {i}:', field)

        self.submit_button = QPushButton('Inserir', self)
        self.submit_button.clicked.connect(self.submit_info)

        # Configurando o layout principal
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.submit_button)
        self.setLayout(main_layout)

    def submit_info(self):
        name = self.name_field.text()
        numbers = [field.text() for field in self.number_fields]
        self.parent().add_apostador(name, numbers)
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Sistema de Loteria'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.apostadores = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Barra de menu
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('Arquivo')

        # Adicionar apostador
        insertAction = QAction('Inserir Apostador', self)
        insertAction.triggered.connect(self.openInsertDialog)
        fileMenu.addAction(insertAction)

        # Ver relatório
        viewAction = QAction('Ver Relatório', self)
        viewAction.triggered.connect(self.openReportDialog)
        fileMenu.addAction(viewAction)

        # Edição
        viewAction = QAction('Editar Apostador', self)
        viewAction.triggered.connect(self.openReportDialog)
        fileMenu.addAction(viewAction)

        # Mostrar janela
        self.show()

    def openInsertDialog(self):
        dialog = InsertDialog(self)
        dialog.exec_()

    def openReportDialog(self):
        dialog = ReportDialog(self.apostadores, self)
        dialog.exec_()

    def add_apostador(self, name, numbers):
        # Simulando TOTAL_ACERTO como a quantidade de números inseridos (modifique conforme a lógica necessária)
        total_acerto = len(numbers)
        self.apostadores.append((name, numbers, total_acerto))


class ReportDialog(QDialog):
    def __init__(self, apostadores, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Relatório de Apostadores')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Nome', 'Números Escolhidos', 'Total Acerto'])

        self.table.setRowCount(len(apostadores))
        for i, (name, numbers, total_acerto) in enumerate(apostadores):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(', '.join(numbers)))
            self.table.setItem(i, 2, QTableWidgetItem(str(total_acerto)))

        layout.addWidget(self.table)
        self.setLayout(layout)


# Main function to run the application
def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
