from pes import read
from pes.strings import letraNome, verificaVit, confere, mostraNome, verificaEspaco
from pes.banco import acessaDB, verificaJogador, criaTabela, obterJogador, adicionaJogador, atualizaJogador
from random import seed, choice
from unidecode import unidecode
from datetime import datetime
import tkinter as tk


def ler(arquivo="dados/names", coluna="Nome", dificuldade=1):
    nameTemp = ""
    df = read.Read().readCol(adress=arquivo, col=coluna)
    seed(datetime.now().microsecond)
    while True:
        seed(datetime.now().microsecond)
        nameTemp = df[coluna].values[choice(df.index)]
        if (dificuldade == 1) and (len(nameTemp) < 6):
            break
        elif (dificuldade == 2) and (len(nameTemp) > 5) and (len(nameTemp) < 10):
            break
        elif dificuldade == 3 and (len(nameTemp) > 8):
            break
    return nameTemp.upper()


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()

        self.jogadorStatus = ["visitante", 0, 0, 0]
        self.dados = ["dados/names", "Nome"]
        self.dificuldade = 1
        self.box = tk.IntVar()
        self.nameOrg = ""
        self.name = unidecode(self.nameOrg)
        self.tam = len(self.name)
        self.nameVerifica = verificaEspaco(self.getName(), self.getTam())
        self.err = 0
        self.letras = []
        self.fim = False

        self.create()


    def create(self):
        self.getMaster().title("Jogo da Forca")
        self.getMaster().geometry("400x350")
        self.getMaster().iconbitmap("img/palito.ico")

        self.menuBar = tk.Menu(self.getMaster())
        self.menuBar.add_cascade(label="Escolha nomes", menu=self.criaMenu(self.menuBar))
        self.getMaster().config(menu=self.menuBar)

        self.criaLabel()
        self.criaRadioBotao()
        self.criaEntrada()
        self.criaBotao()
        self.imagem(local="img/boneco7.png")

    def click(self, teclado=""):
        if len(self.getEntrada1().get()) > 1:
            self.getEntrada1().delete(1, len(self.getEntrada1().get()))
        letra = (unidecode(self.getEntrada1().get())).upper()
        vericac = bool(confere(letra, self.getLetras()))

        if vericac:
            self.setLetras(letra)
            self.setNameVerifica(letraNome(letra, self.getName(), self.getNameVerifica(), self.getTam()))
            self.setLabelBarras(parametro="text", valor=mostraNome(self.getNameVerifica(), self.getTam()))
            self.setBot1("text", "Letra")
            self.setBot1("background", "gray")
            self.setLabelEntrada1(parametro="text", valor=self.getLetras())

            if not (letra in self.name):
                self.setErr(self.getErr() + 1)
                if self.getErr() < 7:
                    self.imagem("img/boneco" + str(self.getErr() + 1) + ".png")

        elif self.getErr() < 6 and not (verificaVit(self.getName(), self.getNameVerifica())):
            self.setBot1("text", "Inválida")
            self.setBot1("background", "red")

        self.getEntrada1().delete(0)
        if verificaVit(self.getName(), self.getNameVerifica()):
            self.setEntrada1(parametro="state", valor="disabled")
            if not self.getFim():
                self.popup(vitoria="venceu")
                self.setFim(True)
        elif self.getErr() > 5:
            self.setEntrada1(parametro="state", valor="disabled")
            if not self.getFim():
                self.popup(vitoria="perdeu")
                self.setFim(True)

    def usuario(self, teclado=""):
        connect = acessaDB(local="dados/", banco="jogadores.db")
        cursor = connect.cursor()
        criaTabela(cursor, "jogadores")
        if len(self.getEntrada2().get()) > 2 and (self.getEntrada2().get()[0] != " "):
            self.adicionaUsuario(cursor)

        self.mostraLabelJogado()
        self.atualisaLabelJogador()

        connect.commit()
        connect.close()

        self.getEntrada2().delete(0, len(self.getEntrada2().get()))


    def adicionaUsuario(self, cursor):
        usuario = verificaJogador(cursor, self.getEntrada2().get(), "jogadores")
        if usuario.fetchall() == []:
            self.setJogadorStatus([self.getEntrada2().get(), 0, 0, 0])
            adicionaJogador(cursor, self.getJogadorStatus(), "jogadores")
            print(verificaJogador(cursor, self.getEntrada2().get(), "jogadores").fetchall())

        usuario = obterJogador(cursor, self.getEntrada2().get(), "jogadores")
        jogador = self.convertCursorList(usuario)
        self.setJogadorStatus(jogador)

    def criaMenu(self, menuBar):
        self.menuOpcoes = tk.Menu(menuBar, tearoff=0)
        self.menuOpcoes.add_command(label="Pessoas", command=self.menuPessoas)
        self.menuOpcoes.add_command(label="Cidades brasileiras", command=self.menuCidades)
        self.menuOpcoes.add_command(label="Países", command=self.menuPaises)
        return self.menuOpcoes

    def menuPessoas(self):
        self.setDados(["dados/names", "Nome"])
        self.iniciar()

    def menuCidades(self):
        self.setDados(["dados/cidades", "Cidade"])
        self.iniciar()

    def menuPaises(self):
        self.setDados(["dados/paises", "País"])
        self.iniciar()

    def imagem(self, local="img/boneco1.png", row=5, column=3):
        self.img = tk.PhotoImage(file=local)
        self.label = tk.Label(self, image=self.img)
        self.label.grid(row=row, column=column)

    def iniciar(self):
        self.getLetras().clear()
        self.setNameOrg(ler(self.getDados()[0], self.getDados()[1], self.getDificuldade()))
        self.setName(unidecode(self.nameOrg))
        self.setTam(len(self.getName()))
        self.setNameVerifica(verificaEspaco(self.getName(), self.getTam()))
        self.setErr(0)
        self.setFim(False)

        self.setLabelNome(parametro="text", valor=self.getDados()[1])
        self.setLabelBarras(parametro="text", valor=mostraNome(self.getNameVerifica(), self.getTam()))
        self.setLabelEntrada1(parametro="text", valor=self.getLetras())

        self.getEntrada1().bind("<Return>", self.click)

        self.setBot1("text", "Letra")
        self.setBot1("command", self.click)
        self.setBot1("background", "gray")

        self.labelNome.grid(row=0, column=3)
        self.labelBarras.grid(row=1, column=3)
        self.labelEntrada1.grid(row=6, column=3)
        self.entrada1.grid(row=2, column=3)
        self.bot1.grid(row=3, column=3)

        self.imagem()
        
    def novoJogo(self):
        self.win.destroy()
        self.iniciar()
        self.setEntrada1(parametro="state", valor="normal")

    def popup(self, vitoria=""):
        self.win = tk.Toplevel()
        self.win.title("Escolha")
        self.win.geometry("300x150")

        if vitoria == "venceu":
            fim = tk.Label(self.win, text="Acertou: "+self.getNameOrg())
            fim.grid(row=0, column=0)
            self.win.imgFim = tk.PhotoImage(file="img/sorriso.png")
            tk.Label(self.win, image=(self.win.imgFim)).grid(row=3, column=0)
            self.setJogadorStatus([self.getJogadorStatus()[0], self.getJogadorStatus()[1] + 1, self.getJogadorStatus()[2], self.getJogadorStatus()[3]+1])

        else:
            fim = tk.Label(self.win, text="Errou: " + self.getNameOrg())
            fim.grid(row=0, column=0)
            self.win.imgFim = tk.PhotoImage(file="img/sorrisoT.png")
            tk.Label(self.win, image=(self.win.imgFim)).grid(row=3, column=0)
            self.setJogadorStatus(
                [self.getJogadorStatus()[0], self.getJogadorStatus()[1], self.getJogadorStatus()[2] + 1,
                 self.getJogadorStatus()[3] + 1])

        connect = acessaDB(local="dados/", banco="jogadores.db")
        cursor = connect.cursor()
        atualizaJogador(cursor, self.getJogadorStatus(), "jogadores")
        connect.commit()
        connect.close()

        self.atualisaLabelJogador()

        self.win.protocol("WM_DELETE_WINDOW", self.fechouWin)

        texto = tk.Label(self.win, text="Deseja continuar?")
        texto.grid(row=1, column=0)

        botN = tk.Button(self.win, text="Não", command=self.closed)
        botN.grid(row=1, column=2)

        botS = tk.Button(self.win, text="Sim", command=self.novoJogo)
        botS.grid(row=1, column=1)

    def closed(self):
        self.win.destroy()
        self.getMaster().destroy()

    def fechouWin(self):
        self.novoJogo()
        self.win.destroy()

    def getMaster(self):
        return self.master

    def getJogadorStatus(self):
        return self.jogadorStatus

    def getDados(self):
        return self.dados

    def getDificuldade(self):
        return self.dificuldade

    def getNameOrg(self):
        return self.nameOrg

    def getNameVerifica(self):
        return self.nameVerifica

    def getName(self):
        return self.name

    def getTam(self):
        return self.tam

    def getErr(self):
        return self.err

    def getLetras(self):
        return self.letras

    def getFim(self):
        return self.fim

    def getMenu(self):
        return self.menuBar

    def getEntrada1(self):
        return self.entrada1

    def getEntrada2(self):
        return self.entrada2

    def setJogadorStatus(self, jog):
        self.jogadorStatus = jog

    def setDados(self, dado):
        self.getDados().clear()
        self.getDados().append(dado[0])
        self.getDados().append(dado[1])

    def setDificuldade(self):
        self.dificuldade = self.box.get()
        self.iniciar()

    def setName(self, name):
        self.name = name

    def setNameOrg(self, name):
        self.nameOrg = name

    def setNameVerifica(self, novoName):
        self.nameVerifica = novoName

    def setErr(self, err):
        self.err = err

    def setFim(self, fim):
        self.fim = fim

    def setLetras(self, letra):
        self.letras.append(letra)

    def setTam(self, tam):
        self.tam = tam

    def setLabelNome(self, parametro, valor):
        self.labelNome[parametro] = valor

    def setLabelBarras(self, parametro, valor):
        self.labelBarras[parametro] = valor

    def setLabelEntrada1(self, parametro, valor):
        self.labelEntrada1[parametro] = "Letras: " + str(valor)

    def setLabelJogador(self, parametro, valor):
        self.labelJogador[parametro] = valor

    def setLabelAcertos(self, parametro, valor):
        self.labelAcertos[parametro] = valor

    def setLabelErros(self, parametro, valor):
        self.labelErros[parametro] = valor

    def setLabelTotal(self, parametro, valor):
        self.labelTotal[parametro] = valor

    def setEntrada1(self, parametro, valor):
        self.entrada1[parametro] = valor

    def setEntrada2(self, parametro, valor):
        self.entrada2[parametro] = valor

    def setBot1(self, parametro, valor):
        self.bot1[parametro] = valor

    def criaLabel(self):
        self.labelNome = tk.Label(self, text="Nome: ")
        self.labelBarras = tk.Label(self)
        self.labelEntrada1 = tk.Label(self)
        self.labelDificuldade = tk.Label(self, text="Dificuldade")
        self.labelJog = tk.Label(self, text="Jogador:")
        self.labelJogador = tk.Label(self)
        self.labelAcert = tk.Label(self, text="Acertos:")
        self.labelAcertos = tk.Label(self)
        self.labelErr = tk.Label(self, text="Erros:")
        self.labelErros = tk.Label(self)
        self.labelTot = tk.Label(self, text="Total:")
        self.labelTotal = tk.Label(self)
        self.labelDificuldade.grid(row=0, column=0)
        self.labelUsuario = tk.Label(self, text="Jogador:")
        self.labelUsuario.grid(row=7, column=3)

    def criaRadioBotao(self):
        self.radio1 = tk.Radiobutton(self, text="Fácil", command=self.setDificuldade, overrelief="solid",
                                     selectcolor="#ffff00", width=7, variable=self.box, value=1)
        self.radio1.select()
        self.radio1.grid(row=1, column=0)
        self.radio2 = tk.Radiobutton(self, text="Médio", command=self.setDificuldade, overrelief="solid",
                                     selectcolor="#ffff00", width=7, variable=self.box, value=2)
        self.radio2.grid(row=2, column=0)
        self.radio3 = tk.Radiobutton(self, text="Difícil", command=self.setDificuldade, overrelief="solid",
                                     selectcolor="#ffff00", width=7, variable=self.box, value=3)
        self.radio3.grid(row=3, column=0)

    def criaEntrada(self):
        self.entrada1 = tk.Entry(self, width=3)
        self.setEntrada1(parametro="textvariable", valor=0)
        self.entrada2 = tk.Entry(self, width=20)
        self.setEntrada2(parametro="textvariable", valor=1)
        self.entrada2.bind("<Return>", self.usuario)
        self.entrada2.grid(row=8, column=3)

    def criaBotao(self):
        self.bot1 = tk.Button(self)
        self.botUsuario = tk.Button(self, text="Adiciona/Acessa", command=self.usuario)
        self.botUsuario.grid(row=9, column=3)

    def mostraLabelJogado(self):
        self.labelJog.grid(row=0, column=4)
        self.labelJogador.grid(row=0, column=5)
        self.labelAcert.grid(row=1, column=4)
        self.labelAcertos.grid(row=1, column=5)
        self.labelErr.grid(row=2, column=4)
        self.labelErros.grid(row=2, column=5)
        self.labelTot.grid(row=3, column=4)
        self.labelTotal.grid(row=3, column=5)

    def atualisaLabelJogador(self):
        self.setLabelJogador("text", self.getJogadorStatus()[0])
        self.setLabelAcertos("text", self.getJogadorStatus()[1])
        self.setLabelErros("text", self.getJogadorStatus()[2])
        self.setLabelTotal("text", self.getJogadorStatus()[3])

    def convertCursorList(self, usuario):
        temp = []
        for cur in usuario:
            print("cursor " + str(cur))
            for i in range(1, len(cur)):
                temp.append(cur[i])
        return temp