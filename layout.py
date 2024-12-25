import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QFormLayout,
                             QLineEdit, QDialog, QVBoxLayout, QPushButton, QWidget,
                             QLabel, QTableWidget, QTableWidgetItem, QMenuBar)
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class InsertDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Inserir Apostador')
        self.setGeometry(100, 100, 300, 200)

        layout = QFormLayout()
        self.name_field = QLineEdit(self)
        self.number_fields = [QLineEdit(self) for _ in range(6)]

        layout.addRow('Nome do Apostador:', self.name_field)
        for i, field in enumerate(self.number_fields, start=1):
            layout.addRow(f'Número {i}:', field)

        self.submit_button = QPushButton('Inserir', self)
        self.submit_button.clicked.connect(self.submit_info)

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

        # Configura a imagem de fundo
        self.setBackground()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('Arquivo')

        insertAction = QAction('Inserir Apostador', self)
        insertAction.triggered.connect(self.openInsertDialog)
        fileMenu.addAction(insertAction)

        viewAction = QAction('Ver Relatório', self)
        viewAction.triggered.connect(self.openReportDialog)
        fileMenu.addAction(viewAction)

        editAction = QAction('Editar Apostador', self)
        editAction.triggered.connect(self.openEditDialog)
        fileMenu.addAction(editAction)

        self.show()

    def setBackground(self):
        # Carrega a imagem e a define como fundo
        background = QPixmap('logo.png')
        backgroundLabel = QLabel(self)
        backgroundLabel.setPixmap(background)
        backgroundLabel.resize(self.width, self.height)
        backgroundLabel.setScaledContents(True)


    def openInsertDialog(self):
        dialog = InsertDialog(self)
        dialog.exec_()

    def openReportDialog(self):
        dialog = ReportDialog(self.apostadores, self)
        dialog.exec_()

    def openEditDialog(self):
        dialog = EditDialog(self.apostadores, self)
        dialog.populateTable(self.apostadores)
        dialog.exec_()

    def add_apostador(self, name, numbers):
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


class EditDialog(QDialog):
    def __init__(self, apostadores, parent=None):
        super().__init__(parent)
        self.apostadores = apostadores
        self.setWindowTitle('Editar Apostador')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Pesquise o nome do apostador...")
        self.search_button = QPushButton('Pesquisar', self)
        self.search_button.clicked.connect(self.searchApostador)

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Nome', 'Números Escolhidos', 'Ações'])
        self.populateTable(self.apostadores)

        layout.addWidget(self.search_field)
        layout.addWidget(self.search_button)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def populateTable(self, apostadores):
        self.table.setRowCount(len(apostadores))
        for i, (name, numbers, _) in enumerate(apostadores):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(', '.join(numbers)))
            btn_edit = QPushButton('Editar', self.table)
            btn_delete = QPushButton('Excluir', self.table)
            btn_edit.clicked.connect(lambda ch, index=i: self.editApostador(index))
            btn_delete.clicked.connect(lambda ch, index=i: self.deleteApostador(index))
            self.table.setCellWidget(i, 2, btn_edit)
            self.table.setCellWidget(i, 2, btn_delete)

    def editApostador(self, index):
        # Implementação da edição ainda não definida
        print(f"Editar apostador {index}")

    def deleteApostador(self, index):
        # Implementação da exclusão ainda não definida
        print(f"Excluir apostador {index}")

    def searchApostador(self):
        search_text = self.search_field.text().lower()
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if search_text in item.text().lower():
                self.table.showRow(i)
            else:
                self.table.hideRow(i)


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
