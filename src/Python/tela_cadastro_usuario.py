from PyQt5 import uic, QtWidgets
import mysql.connector


conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='bd_megacar'
)




def cadastro():
    email = tela_usuario.lineEdit.text()
    senha = tela_usuario.lineEdit_2.text()
    senhacf = tela_usuario.lineEdit_3.text()
    datadenascimento = tela_usuario.lineEdit_4.text()
    endereço = tela_usuario.lineEdit_5.text()
    nome = tela_usuario.lineEdit_6.text()
    cpf = tela_usuario.lineEdit_7.text()
    rg = tela_usuario.lineEdit_8.text()
    cnh = tela_usuario.lineEdit_9.text()
    print(email)
    print(senha)
    print(senhacf)
    print(datadenascimento)
    print(endereço)
    print(nome)
    print(cpf)
    print(rg)
    print(cnh)

    with conexao.cursor() as cursor:
        sql = "INSERT INTO tb_usuarios (email, senha, datadenascimento, endereço, cpf, rg, cnh, nome) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (email, senha, datadenascimento, endereço, cpf, rg, cnh, nome))
        conexao.commit()

    tela_usuario.label_21.setText("Cliente cadastrado com sucesso!")


app = QtWidgets.QApplication([])
tela_usuario = uic.loadUi("tela_usuario.ui")
tela_usuario.pushButton.clicked.connect(cadastro)
#tela_usuario.pushButton2.clicked.connect(voltar)





tela_usuario.show()
app.exec()