from PyQt5 import uic, QtWidgets
import mysql.connector
from PyQt5.QtWidgets import QMessageBox

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
    nascimento = tela_usuario.lineEdit_4.text()
    endereço = tela_usuario.lineEdit_5.text()
    nome = tela_usuario.lineEdit_6.text()
    CPF = tela_usuario.lineEdit_7.text()
    RG = tela_usuario.lineEdit_8.text()
    CNH = tela_usuario.lineEdit_9.text()

    if (senha == senhacf):
        try:
            with conexao.cursor() as cursor:
                sql = "INSERT INTO tb_usuario (email, senha, nascimento, endereço, nome, CPF, RG, CNH) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (email, senha, nascimento, endereço, nome, CPF, RG, CNH))
                conexao.commit()
                tela_usuario.label_21.setText("Usuario Cadastrado com Sucesso!")
                tela_usuario.lineEdit.setText("")
                tela_usuario.lineEdit_2.setText("")
                tela_usuario.lineEdit_3.setText("")
                tela_usuario.lineEdit_4.setText("")
                tela_usuario.lineEdit_6.setText("")
                tela_usuario.lineEdit_7.setText("")
                tela_usuario.lineEdit_8.setText("")
                tela_usuario.lineEdit_5.setText("")
                tela_usuario.lineEdit_9.setText("")
        except mysql.connector.Error as erro:
            print("Erro ao inserir os Dados: ", erro)

    else:
        tela_usuario.label_21.setText("As Senhas Digitadas não Coincidem!")
        tela_usuario.lineEdit_2.setText("")
        tela_usuario.lineEdit_3.setText("")
def consultar():
    tela_usuario.close()
    tela_consulta.show()
    with conexao.cursor() as cursor:
        cursor.execute("Select * from tb_usuario order by id_usuario asc limit 100")
        resultado = cursor.fetchall()
        tela_consulta.tableWidget.setRowCount(len(resultado))
        tela_consulta.tableWidget.setColumnCount(8)
        for i in range(0, len(resultado)):
            for j in range(0, 8):
                tela_consulta.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(resultado[i][j])))

def retornar():
    tela_consulta.close()
    tela_usuario.show()

def deletar():
    linha = tela_consulta.tableWidget.currentRow()
    with conexao.cursor() as cursor:
        cursor.execute("Select * from tb_usuario order by id_usuario asc limit 100")
        resultado = cursor.fetchall()
        id_del = resultado[linha][0]
        id = str(id_del)

        msg = QMessageBox()
        msg.setWindowTitle("Excluir")
        msg.setText("Este dado será excluido.")
        msg.setInformativeText("Deseja excluir?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()

        if resp == QMessageBox.Yes:
            sql = "delete from tb_usuario where id_usuario = '" + id + "'"
            cursor.execute(sql)
            conexao.commit()
            tela_consulta.label_10.setText("Usuario Deletado com Sucesso!")
            consultar()

def editar():
    linha = tela_consulta.tableWidget.currentRow()
    with conexao.cursor() as cursor:
        cursor.execute("Select * from tb_usuario")
        resultado = cursor.fetchall()
        tela_consulta.lineEdit.setText(resultado[linha][1])
        tela_consulta.lineEdit_2.setText(resultado[linha][2])
        tela_consulta.lineEdit_3.setText(resultado[linha][3])
        tela_consulta.lineEdit_4.setText(resultado[linha][4])
        tela_consulta.lineEdit_5.setText(resultado[linha][5])
        tela_consulta.lineEdit_6.setText(resultado[linha][6])
        tela_consulta.lineEdit_7.setText(resultado[linha][7])
        tela_consulta.lineEdit_8.setText(resultado[linha][8])
        
def atualizar():
    linha = tela_consulta.tableWidget.currentRow()
    print(linha)
    with conexao.cursor() as cursor:
        cursor.execute("Select * from tb_usuario")
        resultado = cursor.fetchall()
        id_at = str(resultado[linha][0])
        msg = QMessageBox()
        msg.setWindowTitle("Atualização")
        msg.setText("Este dado será atualizado.")
        msg.setInformativeText("Deseja atualizar?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
    senha = tela_consulta.lineEdit.text()
    nome = tela_consulta.lineEdit_2.text()
    nascimento = tela_consulta.lineEdit_3.text()
    CPF = tela_consulta.lineEdit_4.text()
    RG = tela_consulta.lineEdit_5.text()
    CNH = tela_consulta.lineEdit_6.text()
    endereço = tela_consulta.lineEdit_7.text()
    email = tela_consulta.lineEdit_8.text()

    if resp == QMessageBox.Yes:
        with conexao.cursor() as cursor:
            sql = "UPDATE tb_usuario SET senha= %s, nome= %s, nascimento= %s, CPF= %s, RG= %s, CNH= %s, endereço= %s, email= %s where id_usuario = '" + id_at + "'"
            cursor.execute(sql, (senha, nome, nascimento, CPF, RG, CNH, endereço, email))
            conexao.commit()
            tela_consulta.label_10.setText("Usuario Atualizado com Sucesso!")
            consultar()



app = QtWidgets.QApplication([])
tela_usuario = uic.loadUi("tela_usuario.ui")
tela_consulta = uic.loadUi("consulta_usuario.ui")
tela_usuario.pushButton.clicked.connect(cadastro)
#tela_usuario.pushButton2.clicked.connect(voltar)
tela_usuario.pushButton_3.clicked.connect(consultar)
tela_consulta.pushButton.clicked.connect(retornar)
tela_consulta.pushButton_2.clicked.connect(editar)
tela_consulta.pushButton_3.clicked.connect(atualizar)
tela_consulta.pushButton_4.clicked.connect(deletar)



tela_usuario.show()
app.exec()