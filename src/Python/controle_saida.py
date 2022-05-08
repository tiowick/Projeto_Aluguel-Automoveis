from PyQt5 import uic, QtWidgets
import mysql.connector
from datetime import datetime, date, timedelta

from PyQt5.QtWidgets import QMessageBox

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='bd_megacar'
    )

cursor = conexao.cursor()
cursor.execute("Select * from tb_cliente")
clientes = cursor.fetchone()
#print(clientes)
lista_c=[]
while clientes != None:
    id_cliente = int(clientes[0])
    nome_cliente = clientes[2]
    lista_c.append(nome_cliente)
    clientes = cursor.fetchone()
#print(lista_c)

cursor = conexao.cursor()
cursor.execute("Select * from tb_veiculo")
veiculo = cursor.fetchone()

lista_v=[]
while veiculo != None:
    id_veiculo = (veiculo[0])
    nome_veiculo = veiculo[0]
    lista_v.append(nome_veiculo)
    veiculo = cursor.fetchone()
#print(lista_v)



nome = ""
id_ed= ""
def opcao_selecionada(false=None):
    try:
        tela_app.lineEdit.setEnabled(false)
        data_hora_inicio = datetime.today().strftime('%d/%m/%Y %H:%M')
        #print(data_hora_inicio)
        tela_app.lineEdit.setText(data_hora_inicio)
        tela_app.lineEdit_3.setEnabled(0)
        nu_dias = tela_app.spinBox.value()  # tela_app.lineEdit_5.text()
        nu_dias = int(nu_dias)
        print(nu_dias)
        diarias = datetime.today() + timedelta(days=nu_dias)
        diarias = diarias.strftime('%d/%m/%Y %H:%M')
        #print(diarias)
        tela_app.lineEdit_2.setText(diarias)
        tela_app.lineEdit_2.setEnabled(false)

        placa = tela_app.comboBox_2.currentText()
        print(placa)
        cursor = conexao.cursor()
        sql = "Select valor_diaria from tb_veiculo where placa= '" + placa + "'"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result[0])
        valor_final = float(result[0]) * nu_dias
        print(valor_final)
        tela_app.lineEdit_4.setText(str(valor_final))
    except:
        tela_app.lineEdit.setEnabled(false)
        data_hora_inicio = datetime.today().strftime('%d/%m/%Y %H:%M')
        # print(data_hora_inicio)
        tela_app.lineEdit.setText(data_hora_inicio)
        nu_dias = tela_app.spinBox.value()  # tela_app.lineEdit_5.text()
        nu_dias = int(nu_dias)
        print(nu_dias)
        diarias = datetime.today() + timedelta(days=nu_dias)
        diarias = diarias.strftime('%d/%m/%Y %H:%M')
        # print(diarias)
        tela_app.lineEdit_2.setText(diarias)
        tela_app.lineEdit_2.setEnabled(false)
        sql = "Select valor_diaria from tb_veiculo where placa= '" + placa + "'"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result[0])
        valor_final = float(result[0]) * nu_dias
        print(valor_final)
        tela_app.lineEdit_4.setText(str(valor_final))


def salvar(false=None):
    cliente = tela_app.comboBox.currentText()
    veiculo = tela_app.comboBox_2.currentText()
    f_pagamento= tela_app.comboBox_3.currentText()
    dt_saida = tela_app.lineEdit.text()
    dt_chegada = tela_app.lineEdit_2.text()
    dt_entrega = tela_app.lineEdit_3.text()
    qnt_d = tela_app.spinBox.value()
    valor_total = tela_app.lineEdit_4.text()
    qnt_d = int(qnt_d)
    valor_total = float(valor_total)
    print(cliente, f_pagamento, veiculo, dt_saida,dt_chegada,dt_entrega,qnt_d,valor_total)
    try:
        with conexao.cursor() as cursor:
            sql = "INSERT INTO tb_controle (cliente, placa, pagamento, data_saida, data_retorno, data_entrega ,qnt_diaria, valor_aluguel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,(cliente, veiculo, f_pagamento, dt_saida, dt_chegada,dt_entrega,qnt_d, valor_total))
            conexao.commit()
            #conexao.close()
            tela_app.label_10.setText("Inserido com Sucesso!!")
            tela_app.lineEdit.setText("")
            tela_app.lineEdit_2.setText("")
            tela_app.lineEdit_3.setText("")
            tela_app.lineEdit_4.setText("")
            tela_app.spinBox.setValue(0)
    except mysql.connector.Error as erro:
            print("Erro ao inserir os dados: ", erro)



def consultar():
    with conexao.cursor() as cursor:
        cursor.execute("Select cliente, placa, pagamento, data_saida, data_retorno, data_entrega ,qnt_diaria, valor_aluguel from tb_controle")
        resultado = cursor.fetchall()
        tela_app.tableWidget.setRowCount(len(resultado))
        tela_app.tableWidget.setColumnCount(8)
        for i in range(0, len(resultado)):
            for j in range(0, 8):
                tela_app.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(resultado[i][j])))

def editar():
    linha = tela_app.tableWidget.currentRow()
    print(linha)
    with conexao.cursor() as cursor:
        cursor.execute("Select * from tb_controle")
        resultado = cursor.fetchall()
        #print(resultado)
        tela_app.lineEdit_3.setEnabled(1)
        tela_app.lineEdit.setText(resultado[linha][1])
        tela_app.lineEdit_2.setText(resultado[linha][2])
        tela_app.lineEdit_3.setText(resultado[linha][3])
        tela_app.spinBox.setValue(resultado[linha][4])
        valor_t = str(resultado[linha][5])
        #print(valor_t)
        tela_app.lineEdit_4.setText(valor_t)

def deletar():
    linha = tela_app.tableWidget.currentRow()
    #print(linha)
    with conexao.cursor() as cursor:
        cursor.execute("SELECT * FROM tb_controle")
        resultado = cursor.fetchall()
        #print(resultado)
        id_del = resultado[linha][0]
        #print(id_del)
        id = str(id_del)
        msg = QMessageBox()
        msg.setWindowTitle("Excluir")
        msg.setText("Esta dado será excluído.")
        msg.setInformativeText("Deseja Excluir?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            sql = "DELETE FROM tb_controle WHERE id_controle = '"+id+"'"
            cursor.execute(sql)
            conexao.commit()
            consultar()

def atualizar():
    linha = tela_app.tableWidget.currentRow()
    #print(linha)
    with conexao.cursor() as cursor:
        cursor.execute("Select * from tb_controle")
        resultado = cursor.fetchall()
        #print(resultado[linha][0])
        id_at = str(resultado[linha][0])
        print(id_at)

    msg = QMessageBox()
    msg.setWindowTitle("Atualizar")
    msg.setText("Esta dado será Atualizado.")
    msg.setInformativeText("Deseja Atualizar?")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    resp = msg.exec()

    cliente = tela_app.comboBox.currentText()
    veiculo = tela_app.comboBox_2.currentText()
    f_pagamento = tela_app.comboBox_3.currentText()
    dt_saida = tela_app.lineEdit.text()
    dt_chegada = tela_app.lineEdit_2.text()
    dt_entrega = tela_app.lineEdit_3.text()
    qnt_d = tela_app.spinBox.value()
    valor_total = tela_app.lineEdit_4.text()
    qnt_d = int(qnt_d)
    valor_total = float(valor_total)
    if resp == QMessageBox.Yes:
        with conexao.cursor() as cursor:
            sql = "UPDATE tb_controle SET data_retorno = %s, data_entrega = %s, qnt_diaria = %s, valor_aluguel = %s where id_controle = '"+id_at+"'"
            cursor.execute(sql,(dt_chegada,dt_entrega,qnt_d, valor_total))
            conexao.commit()
            tela_app.label_10.setText("Atualizado com Sucesso!!")
            tela_app.lineEdit.setText("")
            tela_app.lineEdit_2.setText("")
            tela_app.lineEdit_3.setText("")
            tela_app.lineEdit_4.setText("")
            tela_app.spinBox.setValue(0)

def entrega():
    data_hora_inicio = datetime.today().strftime('%d/%m/%Y %H:%M')
    print(data_hora_inicio)
    tela_app.lineEdit_3.setText(data_hora_inicio)

app = QtWidgets.QApplication([])
tela_app = uic.loadUi("controle_saida.ui")
tela_app.comboBox.addItems(lista_c)
tela_app.comboBox_2.addItems(lista_v)
tela_app.pushButton.clicked.connect(opcao_selecionada)
tela_app.pushButton_2.clicked.connect(salvar)
tela_app.pushButton_7.clicked.connect(consultar)
tela_app.pushButton_4.clicked.connect(editar)
tela_app.pushButton_5.clicked.connect(atualizar)
tela_app.pushButton_6.clicked.connect(deletar)
tela_app.lineEdit_2.setInputMask("99/99/9999 99:99")
#tela_app.pushButton_3.clicked.connect(entrega)

tela_app.show()
app.exec()

""" try:
      cursor = conexao.cursor()
      sql = "Select id_cadastro from tb_cadastro where nome= '"+nome+"'"
      cursor.execute(sql)
      result = cursor.fetchone()
      nu_dias = tela_app.spinBox.value()     #tela_app.lineEdit_5.text()
      nu_dias = int(nu_dias)
      print(nu_dias)
      print(result[0])
      diarias = datetime.today() + timedelta(days=nu_dias)
      diarias = diarias.strftime('%d/%m/%Y %H:%M')
      print(diarias)
      tela_app.lineEdit_2.setText(diarias)
      tela_app.lineEdit_2.setEnabled(false)

      data_hora_inicio =datetime.today().strftime('%d/%m/%Y %H:%M')
      print(data_hora_inicio)
      tela_app.lineEdit.setText(data_hora_inicio)"""
