#objeto matéria a ser adicionado tanto em histórico quanto no cronograma de cada aluno
#define horário no cronograma, pendências e o bloco de origem de cada matéria
#A inicialização de cada uma dessas classes será feita recebendo dados do Banco de Dados
from tokenize import String

from numpy import mat


dictDias = {
    "Seg":0,
    "Ter":1,
    "Qua":2,
    "Qui":3,
    "Sex":4
}

dictHoras = {
    "07:30-09:10":[0],
    "09:20-11:00":[1],
    "11:10-12:50":[2],
    "09:20-12:00":[1,2],
    "13:30-15:10":[3],
    "15:20-17:00":[4],
    "13:30-17:00":[3,4],
    "17:10-18:50":[5],
    "15:20-18:50":[4,5]
}

class Dia():
    def __init__(self, horas) -> None:
        self.horaNome = horas
        self.horario = [False for _ in range(6)]
        if horas != "":
            for i in dictHoras[horas]:
                self.horario [i] = True

class Materia():
    contador: int = 1

    def __init__(self, pendencia, bloco, dia, horas, eletiva, nome, vagas) -> None:
        self.diaNome = dia
        self.vagas = vagas
        self.__codigo: int = Materia.contador 
        self.dia = [Dia("") for _ in range(5)]
        self.dia[dictDias[dia[:3]]] = Dia(horas)
        if len(dia) > 3:
            if len(dia) > 6:
                self.dia[0] = Dia(horas)
                self.dia[1] = Dia(horas)
                self.dia[2] = Dia(horas)
                self.dia[3] = Dia(horas)
            else:
                self.dia[dictDias[dia[4:]]] = Dia(horas)
        self.eletiva = eletiva
        self.nome = nome
        self.pendencia = pendencia
        self.bloco = bloco
        Materia.contador += 1

    @property
    def codigo(self: object) -> int:
        return self.__codigo
    
    def __str__(self: object) -> str:
        return f'Código: {self.__codigo} \nNome: {self.nome} \nDia: {self.diaNome}' \
            f'\nBloco: {self.bloco}\nComplemento: {self.eletiva} \nPendencia: {self.pendencia}'

#objeto aluno a ser trabalhado
#definido por coeficiente, cronograma, histórico e prioridade(1: fluxo padrão, 2: calouro, 3: fluxo individual, 4: formando)
class Aluno():
    contador: int = 1

    def __init__(self, coeficiente, prioridade, nome, semestre, historico):
        self.__codigo: int = Aluno.contador
        self.nome = nome
        self.coeficiente = coeficiente
        self.prioridade = prioridade
        self.cronograma = []
        self.historico = historico
        self.__matricula = []
        self.semestre = semestre
        Aluno.contador += 1
#funções internas de Aluno definidas como: Adicionar Matéria e Remover Matéria
    
    @property
    def codigo(self: object) -> int:
        return self.__codigo

    @property
    def matricula(self: object) -> int:
        return self.__matricula

    
    def checkPend(self, materia: Materia) -> bool:
        c=0
        for i in materia.pendencia:
            for j in self.historico:
                if i == j:
                    c+=1
                    break
        if c == len(materia.pendencia):
            return True
        else:
            return False

    def checkRepetCron(self, materia: Materia) -> bool:
            for j in self.cronograma:
                if materia == j.codigo:
                    return True
    def checkRepet(self, materia: Materia) -> bool:
            for j in self.historico:
                if materia == j:
                    return True
    def addMateria(self, materia: Materia):
        print("Matricula de "+ self.nome+" em "+ materia.nome)
        if self.checkRepet(materia.codigo) is True or self.checkRepetCron(materia.codigo) is True:
            return print("Matrícula impossível: Matéria já Cursada")
        elif materia.vagas <= 0:
            return print("Matrícula impossível: Sem vagas")
        elif self.checkPend(materia):
            if len(self.cronograma) > 0:
                if len(self.cronograma) < 10:
                    for i in self.cronograma:
                        for j in range(5):
                            for z in range(6):
                                if materia.dia[j].horario[z] is True and i.dia[j].horario[z] is True:
                                    return print("Matrícula impossível: Horário conflitante")
                                else:
                                    self.cronograma.append(materia)
                                    self.__matricula.append(materia.nome)
                                    print("Matrícula realizada!")
                                    materia.vagas -= 1
                                    return self
                else:
                    return print("Matrícula impossivel: Número máximo de matérias excedido")
            else:
                self.cronograma.append(materia)
                self.__matricula.append(materia.nome)
                print("Matrícula realizada!")
                materia.vagas -= 1
                return self
        else:
            return print("Matrícula impossível: Pendências para a matéria selecionada")
    def remMateria(self, materia: Materia):
        if len(self.cronograma) <= 3:
            return print("Remoção impossivel: Número mínimo de matrículas não alcançado")
        else:
            for i in range(len(self.cronograma)):
                if self.cronograma[i].codigo == materia.codigo:
                    self.cronograma.pop(i)
                    self.matricula.pop(i)
                    materia.vagas += 1
                    return print("Remoção de matrícula realizada!")
            return print("Remoção impossível: Matéria não existe na matrícula do aluno")
   
    #Define as materias que podem ser matriculadas no aluno, baseado no seu historico
    def CheckMateriasPossiveis(self, grade):
        MateriasPossiveis = []
        for i in grade:
            if self.checkRepet(i) == False:
                if self.checkPend(i) == True:
                    MateriasPossiveis.append(i)
        return MateriasPossiveis

    def __str__(self: object) -> str:
        return f'Código: {self.codigo} \nNome: {self.nome} \nCoeficiente: {self.coeficiente}' \
            f'\nPrioridade: {self.prioridade}\nPeriodo: {self.semestre}\nCronograma: {self.matricula}\nHistorico: {self.historico}'

 
 
#MATRICULA EM 4 ETAPAS, ORDENADAS POR PRIORIDADE
 
#Grade é uma lista composta de matérias da lista curso, inicializada na função "Matricula2"
 
def MatriculaExec(aluno: Aluno, grade: Materia) -> Aluno:
    for i in grade:
        aluno.addMateria(i)
 
#Curso possui apenas as matérias obrigatorias e eletivas do curso do aluno
 
def MatriculaIndividual(aluno, curso):
    print("escreva -1 para sair")
    grade = []
    i = 0
    if aluno.prioridade == 2 or aluno.prioridade == 3:
        materia  = int(input("("+aluno.nome+")Selecione as matérias, em codigo, do curso que você quer adicionar: "))
        if materia != -1:
            grade.append(curso[materia-1])
        else:
            print("Você deve adicionar pelo menos 3 matérias na grade")
            grade.pop
        while len(grade)<=10:
            i+=1
            materia = int(input("("+aluno.nome+") Selecione as matérias do curso, em codigo, que você quer adicionar: "))
            if i >3 and i < 10:
                if materia != -1:
                    grade.append(curso[materia-1])
                else:
                    break
            elif i < 3:
                if materia != -1:
                    grade.append(curso[materia-1])
                else:
                    print("Você deve adicionar pelo menos 3 matérias na grade")
                    break
    else:
        materia = int(input("("+aluno.nome+") Selecione as eletivas, em codigo, do curso que você quer adicionar: "))
        if materia == -1:
            return MatriculaExec(aluno, grade)
        else:
            grade.append(curso[materia-1])
        for i in curso:
            materia = int(input("("+aluno.nome+") Selecione as eletivas do curso, em codigo, que você quer adicionar: "))
            if materia != -1:
                grade.append(curso[materia-1])
            else:
                break
    return MatriculaExec(aluno, grade)
 
def MatriculaPadrao(aluno: Aluno, curso: Materia) -> Aluno:
    if aluno.semestre == 2:
        MatriculaExec(aluno, curso[6:9])
    elif aluno.semestre == 3:
        MatriculaExec(aluno, curso[10:13])
    elif aluno.semestre == 4:
        MatriculaExec(aluno, curso[14:17])
    elif aluno.semestre == 5:
        MatriculaExec(aluno, curso[19:22])
    elif aluno.semestre == 6:
        MatriculaExec(aluno, curso[23])
    elif aluno.semestre == 7:
        MatriculaExec(aluno, curso[24:25])
    return MatriculaIndividual(aluno, curso)
 
#AlunosPrio é uma lista com todos os alunos marcados com uma determinada prioridade a ser reutilizada
#em chamadas subsequentes da função "Matricula"
 
def Matricula(alunosPrio, curso: Materia) -> Aluno:
    for aluno in alunosPrio:
        if aluno.prioridade == 1:
            MatriculaExec(aluno, curso[:5])
        elif aluno.prioridade == 0:
            aluno = MatriculaPadrao(aluno, curso)
        elif aluno.prioridade == 2:
            aluno = MatriculaIndividual(aluno, curso)
    return alunosPrio
#Recebe Alunos do banco de dados, ordena em função da prioridade e armazena em 4 listas
#executa Matrícula para cada uma das listas.
 
def addAluno(coeficiente: int, prioridade: int, nome: str, historico: Materia, semestre: int) -> Aluno:
    aluno = Aluno(10, coeficiente, prioridade, nome, semestre)
    for i in historico:
        aluno.historico[i] = historico[i]
    return aluno
 
 
#Ajuste de matricula, permite adições, remoções e trocas de matérias entre alunos
#trocas só podem ocorrer contanto que o aluno que recebe a matéria tenha menos matérias matriculadas
#do que o aluno que concede a matéria
def Ajuste(aluno1: Aluno, aluno2: Aluno, materia: Materia):
    if aluno2 is None:
        aluno1.addMateria(materia)
        return aluno1
    elif aluno1 is None:
        aluno2.addMateria(materia)
        return aluno2
    else:
        if len(aluno2.cronograma) < len(aluno1.cronograma):
            if len(aluno2.cronograma)<=3:
                aluno2.remMateria(materia)
            elif len(aluno1.cronograma)>=10:
                aluno1.addMateria(materia)    
            else:    
                aluno1.addMateria(materia)
                aluno2.remMateria(materia)
        else:
            print("Não foi possivel realizar a troca, "+aluno2.nome+" tem mais matrículas que "+aluno1.nome)
    return
 
 
#Ordena alunos na ordem decrescente de Coeficiente
#Pode-se adicionar matérias de outros blocos de origem (Matérias fora de "Grade")
def Reajuste(aluno: Aluno, materia: Materia, ação: str):
    if ação == "Remoção":
        aluno.remMateria(materia)
    elif ação == "Matricula":
        aluno.addMateria(materia)
    else:
        ("Ação impossivel nesse momento.")
    return
 