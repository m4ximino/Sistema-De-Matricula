from sqlite3 import connect
import mysql.connector
from mysql.connector import Error

# Inserts no banco de dados
def inscricao_aluno(nome, coeficiente, prioridade, semestre):
    try:
        con = mysql.connector.connect(host='127.0.0.1', database='mydb', user='newuser', password='Whinttemore456@')
        cursor = con.cursor()
        inscricao = (f"INSERT INTO aluno (nome, coeficiente, prioridade, semestre) VALUES ('{nome}', '{coeficiente}', '{prioridade}', '{semestre}');")
        cursor.execute(inscricao)
        con.commit() 
    except mysql.connector.Error as erro:
        print("Erro ao fazer consulta nas tabela Mysql".format(erro))
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def inscricao_materia(aluno: int,materia: int):
    try:
        con = mysql.connector.connect(host='127.0.0.1', database='mydb', user='newuser', password='Whinttemore456@')
        cursor = con.cursor()
        inscricao = (f"INSERT INTO materias_inscritas (id_aluno, id_materias_cursadas) VALUES ({aluno}, {materia});")
        cursor.execute(inscricao)
        con.commit() 
    except mysql.connector.Error as erro:
        print("Erro ao fazer insert nas tabela Mysql".format(erro))
    finally:
        if con.is_connected():
            cursor.close()
            con.close()


def materias_cursadas(aluno,materia):
    try:
        con = mysql.connector.connect(host='127.0.0.1', database='mydb', user='newuser', password='Whinttemore456@')
        cursor = con.cursor()
        inscricao = (f"INSERT INTO materias_cursadas (id_aluno, id_materias_cursadas) VALUES ({aluno}, {materia});")
        cursor.execute(inscricao)
        con.commit() 
    except mysql.connector.Error as erro:
        print("Erro ao fazer insert nas tabela Mysql".format(erro))
    finally:
        if con.is_connected():
            cursor.close()
            con.close()


# Pegar valores banco de dados
def pegar_valores_materias_inscritas(aluno):
    try:
        con = mysql.connector.connect(host='127.0.0.1', database='mydb', user='newuser', password='Whinttemore456@')

        consulta_sql = f"SELECT * FROM materias_inscritas WHERE id_aluno = {aluno};"
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas = cursor.fetchall()
        
        materias = []

        for linha in linhas:
            materias.append(int(linha[2]))

        return materias
        
    except mysql.connector.Error as erro:
        return None
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def pegar_valores_pre_requesitos(id):
    try:
        con = mysql.connector.connect(host='127.0.0.1', database='mydb', user='newuser', password='Whinttemore456@')

        consulta_sql = f"SELECT * FROM pre_requisitos WHERE id_materias_ = {id};"
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas = cursor.fetchall()
        
        materias = []
        for linha in linhas:
            materias.append(int(linha[2]))
        return materias
    except mysql.connector.Error as erro:
        return None
    finally:
        if con.is_connected():
            cursor.close()
            con.close()


def pegar_valores_materias_cursadas(aluno):
    try:
        con = mysql.connector.connect(host='127.0.0.1', database='mydb', user='newuser', password='Whinttemore456@')

        consulta_sql = f"SELECT * FROM materias_cursadas WHERE id_aluno = {aluno};"
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas = cursor.fetchall()
        
        materias = []
        for linha in linhas:
            materias.append(int(linha[2]))
        
        return materias
    except mysql.connector.Error as erro:
        return None
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

# pegar_valores_materias_inscritas()
# pegar_materias()
# inscricao_materia()
# inscricao_aluno()
# pegar_valores_alunos()

# inscricao_materia(1,2)