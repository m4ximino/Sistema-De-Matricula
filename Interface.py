import trabalho2_ABN1_EdD
from typing import List
import banco
from time import sleep
import mysql.connector
from mysql.connector import Error

contas: List[trabalho2_ABN1_EdD.Aluno] = []
materias: List[trabalho2_ABN1_EdD.Materia] = []


def buscar_aluno(codigo: int) -> trabalho2_ABN1_EdD.Aluno:
    c: trabalho2_ABN1_EdD.Aluno = None

    if len(contas) > 0:
        for conta in contas:
            if conta.codigo == codigo:
                c = conta
    return c

def buscar_aluno_semestre(semestre: int) -> trabalho2_ABN1_EdD.Aluno:
    c: trabalho2_ABN1_EdD.Aluno = None

    al: List[trabalho2_ABN1_EdD.Aluno] = []
    if len(contas) > 0:
        for conta in contas:
            if conta.semestre == semestre:
                c = conta
                # al.append(c)
    return c

def buscar_aluno_prioridade(prioridade: int) -> trabalho2_ABN1_EdD.Aluno:
    c: trabalho2_ABN1_EdD.Aluno = None

    al: List[trabalho2_ABN1_EdD.Aluno] = []
    if len(contas) > 0:
        for conta in contas:
            if conta.prioridade == prioridade:
                c = conta
                al.append(c)
    return al

def buscar_cpr_materia(codigo: int) -> trabalho2_ABN1_EdD.Materia:
    c: trabalho2_ABN1_EdD.Materia = None
    if len(materias) > 0:
        for materia in materias:
            if materia.codigo == codigo:
                c = materia
    return c

def listar_contas() -> None:
    if len(contas) > 0:
        print('Listagem de contas')

        for conta in contas:
            print(conta)
            print('--------------------')
    else:
        print('Não existem contas cadastradas.')


def listar_materias() -> None:
    if len(materias) > 0:
            print('Listagem das Materias')

            for materia in materias:
                print(materia)
                print('--------------------')

    else:
        print('Não existem contas cadastradas.')


def pegar_materias():
    try:
        con = mysql.connector.connect(host='', database='', user='', password='')

        consulta_sql = f"SELECT * FROM materia"
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas = cursor.fetchall()

        for linha in linhas:
            materia: trabalho2_ABN1_EdD.Materia = trabalho2_ABN1_EdD.Materia(banco.pegar_valores_pre_requesitos(int(linha[0])),linha[4],linha[2],linha[3],linha[5], linha[1], linha[6])
            materias.append(materia)
    except mysql.connector.Error as erro:
        print("Erro ao fazer consulta nas tabela Mysql".format(erro))
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

def pegar_valores_alunos():
    try:
        con = mysql.connector.connect(host='', database='', user='', password='')

        consulta_sql = f"SELECT * FROM aluno"
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas = cursor.fetchall()
        for linha in linhas:
            cadastro:  trabalho2_ABN1_EdD.Aluno = trabalho2_ABN1_EdD.Aluno(linha[2],linha[3],linha[1],linha[4],banco.pegar_valores_materias_cursadas(int(linha[0])))
            contas.append(cadastro) 
    except mysql.connector.Error as erro:
        print("Erro ao fazer consulta nas tabela Mysql".format(erro))
    finally:
        if con.is_connected():
            cursor.close()
            con.close()


dict = {
    "fluxo padrão" : 0,
    "calouro" : 1,
    "fluxo individual" : 2,
    "formando" : 3
}
def addAlunoExec():
    nome = input("Digite seu Nome: ")
    periodos_validos = {"1", "2", "3", "4", "5", "6", "7", "8"}
    while (periodo := input("Digite seu Periodo: ")) not in periodos_validos:
        print(f"Por favor insira {', '.join(periodos_validos)}")
    periodo = int(periodo)
    if periodo > 1:
        i = 1
        historico = []
        while i != -1:
           i = int(input("Digite suas matérias cursadas em codigo: (digite -1 para sair)"))
           if i != -1:
               historico.append(i)
    else:
        prioridade = 1
        historico = []
    while (prioridade := input("Digite sua situação: ")) not in dict:
        print(f"Por favor insira {', '.join(dict)}")
    
    cadastro:  trabalho2_ABN1_EdD.Aluno = trabalho2_ABN1_EdD.Aluno(10,prioridade,nome,periodo,historico)
    print('Aluno adicionado com sucesso.')
    print('Dados da conta: ')
    print('-----------------')
    print(cadastro)
    contas.append(cadastro)
    if prioridade == "fluxo padrão":
        banco.inscricao_aluno(nome, 10, 0, periodo)
    elif prioridade == "calouro":
        banco.inscricao_aluno(nome, 10, 1, periodo)
    elif prioridade == "fluxo individual":
        banco.inscricao_aluno(nome, 10, 2, periodo)
    elif prioridade == "formando":
        banco.inscricao_aluno(nome, 10, 3, periodo)
    for materia in historico:
        banco.materias_cursadas(int(cadastro.codigo),int(materia))
    sleep(2)
    menu()


def menu() -> None:
    print('=====================================')
    print('============== ATM ==================')
    print('============ SIE WEB ===============')
    print('=====================================')

    print('Selecione uma opção no menu: ')
    print('1 - Inscrever Aluno')
    print('2 - Inscrever Materia no Aluno')
    print('3 - Ajuste')
    print('4 - Reajuste')
    print('5 - Grade Curricular')
    print('6 - Lista de Alunos')
    print('7 - Consultar Aluno')
    print('8 - Encerrar')
    entradas_validas = ('1', '2', '3', '4', '5', "6", "7", "8")
    opcao: int = int(input())

    if opcao == 1:
        addAlunoExec()
    elif opcao == 2:
        if len(contas) > 0:
            # print(buscar_aluno_prioridade(0), materias)
            trabalho2_ABN1_EdD.Matricula(buscar_aluno_prioridade(0), materias)
            trabalho2_ABN1_EdD.Matricula(buscar_aluno_prioridade(1), materias)
            trabalho2_ABN1_EdD.Matricula(buscar_aluno_prioridade(2), materias)
            trabalho2_ABN1_EdD.Matricula(buscar_aluno_prioridade(3), materias)
        else:
            print('Ainda não existem alunos cadastrados.')
        sleep(2)
        menu()
    elif opcao == 3:
        if len(contas) > 0:
            codigo1: int = int(input('Informe o codigo do Aluno 1: '))
            conta1: trabalho2_ABN1_EdD.Aluno = buscar_aluno(codigo1)
            
            codigo2: int = int(input('Informe o codigo do Aluno 2: '))
            conta2: trabalho2_ABN1_EdD.Aluno = buscar_aluno(codigo2)

            materia: int = int(input('Informe o id da materia: '))
            materia_estrutura : trabalho2_ABN1_EdD.Materia = buscar_cpr_materia(materia)


            if conta1 and conta2:
                trabalho2_ABN1_EdD.Ajuste(conta1, conta2, materia_estrutura)
            elif conta1 is None:
                trabalho2_ABN1_EdD.Ajuste(conta1, conta2, materia_estrutura)
            elif conta2 is None:
                trabalho2_ABN1_EdD.Ajuste(conta1, conta2, materia_estrutura)
            else:
                print('Nennhum dos alunos foram encontrados.')
        else:
            print('Ainda não existem alunos cadastrados.')
        sleep(2)
        menu()
    elif opcao == 4:
        print('1 - Remoção')
        print('2 - Matricula')
        acao = int(input())
        if acao == 1:
            acao =  "Remoção"
        elif acao == 2:
            acao = "Matricula"
        else:
            print("Ação impossivel nesse momento.")
        codigo: int = int(input('Informe o codigo da sua conta: '))
        conta: trabalho2_ABN1_EdD.Aluno = buscar_aluno(codigo)

        materia: int = int(input('Informe o id da materia: '))
        materia_estrutura : trabalho2_ABN1_EdD.Materia = buscar_cpr_materia(materia)
        if conta:
            trabalho2_ABN1_EdD.Reajuste(conta,materia_estrutura, acao)
        else:
            print(f"Não foi encontrado esse Aluno {codigo}")
        sleep(2)
        menu()
    elif opcao == 5:
        listar_materias()
        sleep(2)
        menu()
    elif opcao == 6:
        listar_contas()
        sleep(2)
        menu()
    elif opcao == 7:
        codigo1: int = int(input('Informe o codigo do Aluno 1: '))
        conta1: trabalho2_ABN1_EdD.Aluno = buscar_aluno(codigo1)
        if conta1:
            print(conta1)
        else: print("Aluno não cadastrado.")
        sleep(2)
        menu()
    elif opcao == 8:
        for aluno in contas:
            for materia in aluno.cronograma:
                banco.inscricao_materia(int(aluno.codigo),int(materia.codigo))

        print('Até mais!')
        sleep(2)
        exit(0)

    

pegar_valores_alunos()
pegar_materias()
menu()
# print(buscar_aluno_semestre(3))
# print(buscar_aluno(1))
# listar_materias()
# print(buscar_cpr_materia(1))
# print(buscar_aluno_prioridade(1))