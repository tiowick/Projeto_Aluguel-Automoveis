from PyQt5 import uic, QtWidgets

def proximo():
    tela_leitura.close()
    tela_leitura_2.show()

def anterior():
    tela_leitura_2.close()
    tela_leitura.show()


def sair():
    tela_leitura.close()


app = QtWidgets.QApplication([])
tela_leitura = uic.loadUi("tela_leitura.ui")
tela_leitura_2 = uic.loadUi("tela_leitura_2.ui")
tela_leitura.pushButton_3.clicked.connect(sair)
tela_leitura.pushButton.clicked.connect(proximo)
tela_leitura_2.pushButton.clicked.connect(anterior)

tela_leitura.show()
app.exec()
