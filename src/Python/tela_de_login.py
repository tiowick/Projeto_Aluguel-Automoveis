from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMenuBar, QMessageBox
from datetime import datetime, date, timedelta


import mysql.connector
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='bd_megacar'
    )
def chama_segunda_tela():
    primeira_tela.label_3.setText("")
    nome_usuario = primeira_tela.lineEdit.text()
    senha = primeira_tela.lineEdit_2.text()
    print(senha)
    print(nome_usuario)
    try:
        with conexao.cursor() as cursor:
            cursor.execute("select senha from  tb_usuario where email = '{}'".format(nome_usuario))
            senha_bd = cursor.fetchall()
            print(senha_bd[0][0])
    except:
        return primeira_tela.label_3.setText("Usuário ou Senha Incorreto!")
    if senha == senha_bd[0][0]:
        primeira_tela.close()
        segunda_tela.show()
        #primeira_tela.label_3.setText("Login com Sucesso!!")
    else:
        primeira_tela.label_3.setText("Dados de Login Incorretos!")

def logout():
    segunda_tela.close()
    primeira_tela.show()

#tela de cadastro

def tela_user():
    tela_usuario.show()


def cadastro_user():
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
                sql = "INSERT INTO tb_usuario (email, senha, dataNasc, endereco, nome, cpf, rg, cnh) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
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


def consultar_user():
    tela_usuario.close()
    tela_consulta.show()
    with conexao.cursor() as cursor:
        cursor.execute("Select email, senha, nome, dataNasc, cpf, rg, cnh, endereco from tb_usuario order by id_usuario asc limit 100")
        resultado = cursor.fetchall()
        tela_consulta.tableWidget.setRowCount(len(resultado))
        tela_consulta.tableWidget.setColumnCount(8)
        for i in range(0, len(resultado)):
            for j in range(0, 8):
                tela_consulta.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(resultado[i][j])))


def retornar_user():
    tela_consulta.close()
    tela_usuario.show()


def deletar_user():
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
            consultar_user()

def editar_user():
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


def atualizar_user():
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
            sql = "UPDATE tb_usuario SET senha= %s, nome= %s, dataNasc= %s, cpf= %s, rg= %s, cnh= %s, endereco= %s, email= %s where id_usuario = '" + id_at + "'"
            cursor.execute(sql, (senha, nome, nascimento, CPF, RG, CNH, endereço, email))
            conexao.commit()
            tela_consulta.label_10.setText("Usuario Atualizado com Sucesso!")
            consultar_user()


# TELA DE CLIENTES

def cadastrar_cl():
    telefone = tela_cliente.lineEdit.text()
    nome = tela_cliente.lineEdit_2.text()
    datanasc = tela_cliente.lineEdit_3.text()
    cpf = tela_cliente.lineEdit_4.text()
    rg = tela_cliente.lineEdit_5.text()
    cnh = tela_cliente.lineEdit_6.text()
    endereco = tela_cliente.lineEdit_7.text()
    email = tela_cliente.lineEdit_8.text()
    with conexao.cursor() as cursor:
        sql = "INSERT INTO tb_cliente (telefone,nome, dataNasc, cpf, rg, cnh, endereco, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
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

def consultar_cl():
    with conexao.cursor() as cursor:
        cursor.execute("select * from tb_cliente order by id_cliente asc limit 100")
        resultado = cursor.fetchall()
        tela_cliente.tableWidget.setRowCount(len(resultado))
        tela_cliente.tableWidget.setRowCount(9)
        for i in range(0, len(resultado)):
            for j in range(0, 9):
                tela_cliente.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(resultado[i][j])))


def editar_cl():
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

def atualizar_cl():
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
            consultar_cl()



def deletar_cl():
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
            consultar_cl()
def tela_cl():
    tela_cliente.show()


def voltar_cl():
    tela_cliente.close()

# TELA DE VEÍCULO

def cadastrar_v():
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
        sql = "INSERT INTO tb_veiculo (placa, cor, modelo, marca, categoria, renavam, valor_diaria) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (placa, cor, modelo, marca, categoria, renavam, diaria))
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

def voltar_v():
    tela_veiculo.close()
    segunda_tela.show()

def tela_v():
    tela_veiculo.show()


# TELA CONTROLE
def tela_con():
    tela_app.show()
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
    tela_app.comboBox.addItems(lista_c)
    tela_app.comboBox_2.addItems(lista_v)



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
        sql = "Select valor_diaria from tb_veiculo where placa= '"+placa+"'"
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
        sql = "Select valor_diaria from tb_veiculo where placa= '"+placa+"'"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result[0])
        valor_final = float(result[0]) * nu_dias
        print(valor_final)
        tela_app.lineEdit_4.setText(str(valor_final))


def salvar_con(false=None):
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



def consultar_con():
    with conexao.cursor() as cursor:
        cursor.execute("Select cliente, placa, pagamento, data_saida, data_retorno, data_entrega ,qnt_diaria, valor_aluguel from tb_controle")
        resultado = cursor.fetchall()
        tela_app.tableWidget.setRowCount(len(resultado))
        tela_app.tableWidget.setColumnCount(8)
        for i in range(0, len(resultado)):
            for j in range(0, 8):
                tela_app.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(resultado[i][j])))

def editar_con():
    linha = tela_app.tableWidget.currentRow()
    print(linha)
    with conexao.cursor() as cursor:
        cursor.execute("Select * from tb_controle")
        resultado = cursor.fetchall()
        # print(resultado)
        tela_app.lineEdit_3.setEnabled(1)
        tela_app.lineEdit.setText(resultado[linha][1])
        tela_app.lineEdit_2.setText(resultado[linha][2])
        tela_app.lineEdit_3.setText(resultado[linha][3])
        tela_app.spinBox.setValue(resultado[linha][4])
        valor_t = str(resultado[linha][5])
        # print(valor_t)
        tela_app.lineEdit_4.setText(valor_t)

def deletar_con():
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
            consultar_con()

def atualizar_con():
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
def voltar_con():
    tela_app.close()


#TELA DE SOBRE


def proximo_sb():
    tela_leitura.close()
    tela_leitura_2.show()

def anterior_sb():
    tela_leitura_2.close()
    tela_leitura.show()


def sair_sb():
    tela_leitura.close()

def tela_sb():
    tela_leitura.show()


def voltar_login():
    tela_usuario.close()
    primeira_tela.show()

def voltar_login2():
    tela_usuario.close()


app = QtWidgets.QApplication([])
primeira_tela = uic.loadUi("tela_de_login.ui")
segunda_tela = uic.loadUi("Tela_Principal.ui")
tela_usuario = uic.loadUi("tela_usuario.ui")
#cadastro_tela = uic.loadUi("tela_cadastro.ui")
primeira_tela.pushButton.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton_7.clicked.connect(logout)
primeira_tela.pushButton_2.clicked.connect(tela_user)
tela_consulta = uic.loadUi("consulta_usuario.ui")
tela_usuario.pushButton.clicked.connect(cadastro_user)
tela_usuario.pushButton_2.clicked.connect(voltar_login2)
tela_usuario.pushButton_3.clicked.connect(consultar_user)
tela_consulta.pushButton.clicked.connect(retornar_user)
tela_consulta.pushButton_2.clicked.connect(editar_user)
tela_consulta.pushButton_3.clicked.connect(atualizar_user)
tela_consulta.pushButton_4.clicked.connect(deletar_user)
segunda_tela.pushButton_.clicked.connect(tela_user)
segunda_tela.pushButton_2.clicked.connect(tela_cl)
segunda_tela.pushButton_3.clicked.connect(tela_v)
segunda_tela.pushButton_5.clicked.connect(tela_con)
segunda_tela.pushButton_6.clicked.connect(tela_sb)

tela_cliente = uic.loadUi("tela_cliente.ui")
tela_cliente.pushButton.clicked.connect(cadastrar_cl)
tela_cliente.pushButton_2.clicked.connect(voltar_cl)
tela_cliente.pushButton_3.clicked.connect(consultar_cl)
tela_cliente.pushButton_6.clicked.connect(editar_cl)
tela_cliente.pushButton_5.clicked.connect(deletar_cl)
tela_cliente.pushButton_4.clicked.connect(atualizar_cl)
tela_cliente.lineEdit_3.setInputMask("99/99/9999")

tela_veiculo = uic.loadUi("tela_veiculo.ui")
tela_veiculo.pushButton.clicked.connect(cadastrar_v)
tela_veiculo.pushButton_2.clicked.connect(voltar_v)

tela_app = uic.loadUi("controle_saida.ui")
tela_app.pushButton.clicked.connect(opcao_selecionada)
tela_app.pushButton_2.clicked.connect(salvar_con)
tela_app.pushButton_7.clicked.connect(consultar_con)
tela_app.pushButton_4.clicked.connect(editar_con)
tela_app.pushButton_5.clicked.connect(atualizar_con)
tela_app.pushButton_6.clicked.connect(deletar_con)
tela_app.pushButton_3.clicked.connect(voltar_con)
tela_app.lineEdit_2.setInputMask("99/99/9999 99:99")

tela_leitura = uic.loadUi("tela_leitura.ui")
tela_leitura_2 = uic.loadUi("tela_leitura_2.ui")
tela_leitura.pushButton_3.clicked.connect(sair_sb)
tela_leitura.pushButton.clicked.connect(proximo_sb)
tela_leitura_2.pushButton.clicked.connect(anterior_sb)

#segunda_tela.show()
primeira_tela.show()
app.exec()