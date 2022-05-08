from PyQt5 import uic, QtWidgets
import mysql.connector
from PyQt5.QtWidgets import QMessageBox

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='bd_megacar'
)


def cadastrar():
    telefone = tela_cliente.lineEdit.text()
    nome = tela_cliente.lineEdit_2.text()
    datanasc = tela_cliente.lineEdit_3.text()
    cpf = tela_cliente.lineEdit_4.text()
    rg = tela_cliente.lineEdit_5.text()
    cnh = tela_cliente.lineEdit_6.text()
    endereco = tela_cliente.lineEdit_7.text()
    email = tela_cliente.lineEdit_8.text()
    with conexao.cursor() as cursor:
        sql = "INSERT INTO tb_cliente (telefone,nome, datanasc, cpf, rg, cnh, endereco, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
        cursor.execute(sql, (telefone, nome, datanasc, cpf, rg, cnh, endereco, email))
        conexao.commit()

    tela_cliente.label_10.setText("cliente cadastrado com sucesso!!")


# tela_cliente.lineEdit.text("")
# tela_cliente.lineEdit_2.text("")
# tela_cliente.lineEdit_3.text("")
# tela_cliente.lineEdit_4.text("")
# tela_cliente.lineEdit_5.text("")
# tela_cliente.lineEdit_6.text("")
# tela_cliente.lineEdit_7.text("")
# tela_cliente.lineEdit_8.text("")

def consultar():
    with conexao.cursor() as cursor:
        cursor.execute("select * from tb_cliente order by id_cliente asc limit 100")
        resultado = cursor.fetchall()
        tela_cliente.tableWidget.setRowCount(len(resultado))
        tela_cliente.tableWidget.setRowCount(9)
        for i in range(0, len(resultado)):
            for j in range(0, 9):
                tela_cliente.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(resultado[i][j])))


def editar():
    linha = tela_cliente.tableWidget.currentRow()
    print(linha)
    with conexao.cursor() as cursor:
        cursor.execute("select * from tb_cliente")
        resultado = cursor.fetchall()
        print(resultado[linha][0])
        print(resultado[linha][1])
        print(resultado[linha][2])
        print(resultado[linha][3])
        print(resultado[linha][4])
        print(resultado[linha][5])
        print(resultado[linha][6])
        print(resultado[linha][7])
        print(resultado[linha][8])
        tela_cliente.lineEdit.setText(resultado[linha][1])
        tela_cliente.lineEdit_2.setText(resultado[linha][2])
        tela_cliente.lineEdit_3.setText(resultado[linha][3])
        tela_cliente.lineEdit_4.setText(resultado[linha][4])
        tela_cliente.lineEdit_5.setText(resultado[linha][5])
        tela_cliente.lineEdit_6.setText(resultado[linha][6])
        tela_cliente.lineEdit_7.setText(resultado[linha][7])
        tela_cliente.lineEdit_8.setText(resultado[linha][8])

def atualizar():
    linha = tela_cliente.tableWidget.currentRow()
    print(linha)
    with conexao.cursor() as cursor:
        cursor.execute("Select * from tb_cliente")
        resultado = cursor.fetchall()
        # print(resultado[linha][0])
        id_at = str(resultado[linha][0])
        print(id_at)

    msg = QMessageBox()
    msg.setWindowTitle("Atualizar")
    msg.setText("Este dado será atualizado")
    msg.setInformativeText("Deseja atualizar?")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    resp = msg.exec()

    telefone = tela_cliente.lineEdit.text()
    nome = tela_cliente.lineEdit_2.text()
    datanasc = tela_cliente.lineEdit_3.text()
    cpf = tela_cliente.lineEdit_4.text()
    rg = tela_cliente.lineEdit_5.text()
    cnh = tela_cliente.lineEdit_6.text()
    endereco = tela_cliente.lineEdit_7.text()
    email = tela_cliente.lineEdit_8.text()
    #print(nome)
    #print(endereco)
    #print(cidade)
    if resp == QMessageBox.Yes:
        with conexao.cursor() as cursor:
            sql = "UPDATE tb_cliente SET telefone= %s, nome= %s, datanasc= %s, cpf= %s, rg= %s, cnh= %s, endereco= %s, email= %s Where id_cliente = '" + id_at + "'"
            cursor.execute(sql, (telefone, nome, datanasc, cpf, rg, cnh, endereco, email))
            conexao.commit()
            tela_cliente.label_10.setText("Atualizado com sucesso!!!")
            tela_cliente.lineEdit.setText("")
            tela_cliente.lineEdit_2.setText("")
            tela_cliente.lineEdit_3.setText("")
            tela_cliente.lineEdit_4.setText("")
            tela_cliente.lineEdit_5.setText("")
            tela_cliente.lineEdit_6.setText("")
            tela_cliente.lineEdit_7.setText("")
            tela_cliente.lineEdit_8.setText("")
            consultar()



def deletar():
    linha = tela_cliente.tableWidget.currentRow()
    print(linha)
    with conexao.cursor() as cursor:
        cursor.execute("SELECT * FROM tb_cliente order by id_cliente limit 100")
        resultado = cursor.fetchall()
        print(resultado)
        id_del = resultado[linha][0]
        # print(id_del)
        id = str(id_del)

        msg = QMessageBox()
        msg.setWindowTitle("excluir")
        msg.setText("Este dado será excluido")
        msg.setInformativeText("Deseja excluir?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()

        if resp == QMessageBox.Yes:
            sql = "DELETE FROM tb_cliente WHERE id_cliente = '"+id+"'"
            cursor.execute(sql)
            conexao.commit()
            consultar()


def voltar():
    tela_cliente.close()


app = QtWidgets.QApplication([])
tela_cliente = uic.loadUi("tela_cliente.ui")
tela_cliente.pushButton.clicked.connect(cadastrar)
tela_cliente.pushButton_2.clicked.connect(voltar)
tela_cliente.pushButton_3.clicked.connect(consultar)
tela_cliente.pushButton_6.clicked.connect(editar)
tela_cliente.pushButton_5.clicked.connect(deletar)
tela_cliente.pushButton_4.clicked.connect(atualizar)
tela_cliente.lineEdit_3.setInputMask("99/99/9999")

tela_cliente.show()
app.exec()
