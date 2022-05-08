from PyQt5 import uic, QtWidgets
import mysql.connector

conexao = mysql.connector.Connect(
    host='localhost',
    user='root',
    password='',
    database='bd_megacar',
)

def cadastrar():
    placa = tela_veiculo.lineEdit.text()
    cor = tela_veiculo.lineEdit_2.text()
    modelo = tela_veiculo.lineEdit_3.text()
    marca = tela_veiculo.lineEdit_4.text()
    categoria = tela_veiculo.lineEdit_5.text()
    renavam = tela_veiculo.lineEdit_6.text()
    diaria = tela_veiculo.lineEdit_7.text()
    status = tela_veiculo.lineEdit_8.text()
    #print(placa)
    #print(cor)
    #print(modelo)
    #print(marca)
    #print(categoria)
    #print(renavam)
    #print(diaria)
    #print(status)
    with conexao.cursor() as cursor:
        sql = "INSERT INTO tb_veiculos (placa, cor, modelo, marca, categoria, renavam, diaria, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (placa, cor, modelo, marca, categoria, renavam, diaria, status))
        conexao.commit()
    tela_veiculo.label_10.setText("Veículo Cadastrado com Sucesso!!")
    tela_veiculo.lineEdit.setText("")
    tela_veiculo.lineEdit_2.setText("")
    tela_veiculo.lineEdit_3.setText("")
    tela_veiculo.lineEdit_4.setText("")
    tela_veiculo.lineEdit_5.setText("")
    tela_veiculo.lineEdit_6.setText("")
    tela_veiculo.lineEdit_7.setText("")
    tela_veiculo.lineEdit_8.setText("")


"""    
def voltar():
    tela_veiculo.close()
    tela_login.show()"""



app = QtWidgets.QApplication([])
tela_veiculo = uic.loadUi("tela_veiculo.ui")
tela_veiculo.pushButton.clicked.connect(cadastrar)
#tela_veiculo.pushButton_2.clicked.connect(voltar)

tela_veiculo.show()
app.exec()