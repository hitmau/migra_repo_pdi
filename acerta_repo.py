# -*- coding:utf-8 -*-
#!/usr/bin/env python
#encoding: utf-8
#coding: utf-8
#!/usr/bin/env python3
#Autor Maurcio Rodrigues (mauriciosist@gmail.com)
import os, re, fileinput, os.path, shutil, io, xmltodict
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
from PIL import Image, ImageTk
import PIL.Image, time
try:
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
    #from tkinter import filedialog
    from tkinter import messagebox
except:
    #from Tkinter import *
    import tkFileDialog as filedialog
    #from Tkinter import filedialog as filedialog
    import tkMessageBox as messagebox
from threading import Thread as td

class Server:
    def __init__(self, master=None):
        campoDeBusca = '<trans_object_id'
        campoDeBusca2 = '<filename>'
        campoDeBusca3 = '<transname>'
        campoDeBusca4 = '<directory>'
        self.listaKtr = []
        self.Diretorio = ""
        self.caminhoPAI = ""
        self.varCaminho = "Internal.Entry.Current.Directory"
        self.pula_linha = 0
        #linha de informações
        self.infoRow = 6
        master.focus_set()
        abas = ttk.Notebook(master)

        self.aba1 = ttk.Frame(abas)
        self.aba2 = ttk.Frame(abas)

        master.iconbitmap("img/my_icon.ico")
        self.frame = Frame(master)
        self.master = master

        master.title('Acerta os arquivos do repositório migrados de BD')
        larguraTela = 500
        alturaTela = 266
        w, h = master.winfo_screenwidth(), master.winfo_screenheight()
        print(str(int(w/2)))
        w = (int(w/2)) - larguraTela + (int(larguraTela/2))
        h = (int(h/2)) - alturaTela + (int(alturaTela/2)) - 40
        master.geometry(str(larguraTela) + 'x' + str(alturaTela) + '+' + str(w) + '+' + str(h))
        fontePadrao = ("Arial", "10")
        self.frame.grid(row=1,column=0,padx=1,pady=1)

        self.explore = ''
        self.HELP_TEXT = """
(C) 2019-2020 Jebs Web Soluções em TI

Informações importantes:
    1. Este aplicativo é de autoria interna da JebsWeb.
    2. É de exprema importância que o navegador que é utilizado pelo
       programa não seja manipulado.
    3. O navegador e o programa podem ser minimizados para que funcionem
       em segundo plano.
    4. A varredura pode demorar várias horas.
    5. Algumas coisas podes imfluenciar no tempo de término:
       4.1. O desempenho do servidor onde está alocado o Pentaho Server.
       4.2. A internet, caso não esteja na mesma rede do servidor.
       4.3. O número de usuários utilizando o serviço.
       4.4. O desempenho da máquina que está rodando o programa.
    6. Se um diretório ou arquivo demorar muito para ser exibido o
       programa irá pular o mesmo. (se demorar muito)

Índice
=========================================
1.0 O que este programa faz?
2.0 Como usar
=========================================

1.0 O que este programa faz?
--------------------------------------------------------------------------
    Este programa foi desencolvido para facilitar o backup e migração dos
    arquivos localizado no diretório do Pentaho Server Comunity,
    desempenhando um papel fundamental quando o assunto é mão de obra.
    O mesmo exporta os códigos MDX de consultas salvas do SAIKU em
    arquivos .txt denominados com o usuário dono dessa(s) consulta(s).
    Também podemos extrair em um único arquivo (Relatório) a relação de
    todos os diretórios e arquivos existendes nos diretórios do
    Pentaho Server.

2.0 Como usar
--------------------------------------------------------------------------
    Ao abrir o sistema devemos inserir alguns campos obrigatórios
    demarcados com um (*), do contrário os demais são opcionais.

    Relação de campos:
    -> URL: Endereço onde se encontra o serviço do Pentaho Server.
    -> Usuário: O usuário administrador (ou um usuário com perfil de
        administrador.
    -> Senha: A senha desse usuário.
    -> Diretório: O diretório onde os arquivos de backup serão salvos.
    -> Obter cód. MDX: Marcando essa opção o sistema irá buscar e salvar
        todos os diretórios que contena arquivos .saiku.
    -> Obter Relatório geral: Marcando essa opção o sistema irá salvar a
        relação geral dos diretórios e arquivos.
    -> Id. início: Opção não obrigatória, podemos inserir um número
        (índice do diretório) que queremos que se inicie.
    -> Id. dim: Opção não obrigatórioa, podemos inserir um número (íncide
        de diretório) que queremos que a varre_5dura finalize.

    Exemplos dos campos Id. Início e Id. fim:
    - varre_5dura do usuário 100 ao usuário 149:
    	O sistema rodará apenas entre essa faixa de diretórios.
    - A internet travou e foi gerado o arquivo 393 - João.silva:
    	Para rodar novamente podemos preencher o "Id. Início" = 392 e
        deixar o "Id. fim" em branco para continuar até o final.

Descrição dos arquivos:
    1. Arquivo app.py
        Arquivo base. Roda pelo terminal.
    2. Arquivo Backup.
        Textos inseridos no app, ao clicar em iniciar ele salva neste arquivo.
    3. Arquivo relatorio.
        Exemplo de relatório emitido com a opção "Obter relatorio geral" ativo.
    4. Diretório Img.
        Necessário para carregar as logos do app.
    5. Diretório Drives:
        Drivers dos navegadores.
"""
        #tempo para espera de arquivos
        td(target=self.interface).start()
        #print(self.menu_diretorios())

    def trataDir(self):
        if self.Diretorio.get().replace(' ','') == '' or self.Diretorio.get() == None:
            td(target=self.inf,args=['Preencha o diretório!']).start()
        else:
            self.caminhoPAI = self.Diretorio.get().replace('\\', '/')
            print("|" + str(self.caminhoPAI) + "| OK")

    def inicioKtr(self):
        self.trataDir()
        for file in self.listarGeral():
            if file[-4:] == '.kjb':
                self.replace(file)
        td(target=self.inf,args=['Acerto de arquivos finalizado!',1]).start()
            #return self.caminhoPAI

    def inicioJdnc(self):
        td(target=self.inf,args=["Analizando arquivos .ktr e .kjb..."]).start()
        self.trataDir()
        lista = self.remove_repetidos(self.conexoes())
        print(lista)
        self.gravaRelatorio(lista)

    def interface(self):
        try:
            self.pula_linha = 0
            try:
                imagem = PIL.Image.open("img/logo.png")
                print(imagem)
                imagem = imagem.resize((150,50), PIL.Image.ANTIALIAS)
                photoimagem =  ImageTk.PhotoImage(imagem)
                self.logo = Label(self.master, image=photoimagem)
                self.logo.imagem = photoimagem
                self.logo.grid(row=self.pula_linha,column=0,columnspan=1,padx=5,pady=3)
            except Exception as e:
                print("erro: " + str(e))
                pass
            try:
                #icone explore
                imagemEx = PIL.Image.open("img/explore.png")
                imagemEx = imagemEx.resize((15,15))
                self.explore =  ImageTk.PhotoImage(imagemEx)
            except Exception as a:
                print("erro explorer: " + str(a))
                pass

            self.pula_linha = self.pula_linha + 1
            Label(self.frame, text="Informe o diretório e seja feliz!").grid(column=0,columnspan=4,padx=5,pady=5,sticky=W+E)
            #Velocidade
            #Nome e campo do url
            self.pula_linha = self.pula_linha + 1
            #Label(self.frame, text="(1) - Por extenção .ktr nas transformações e acertar").grid(row=self.pula_linha,column=0,padx=1,pady=3,sticky=N)
            #self.pula_linha = self.pula_linha + 1
            #Label(self.frame, text="      diretórios que se encontram no mesmo nível.").grid(row=self.pula_linha,column=0,padx=1,pady=3,sticky=N)
            #self.pula_linha = self.pula_linha + 1
            #Label(self.frame, text="URL").grid(row=self.pula_linha,column=0,padx=1,pady=3,sticky=N)
            #self.url = Entry(self.frame)
            #self.url.grid(row=self.pula_linha,column=1,columnspan=3,padx=5,pady=5,sticky=W+E)

            #Nome e campo de Usuário
            #self.pula_linha = self.pula_linha + 1
            #Label(self.frame, text="Nome:").grid(row=self.pula_linha,column=0,padx=5,pady=3)
            #self.nome = Entry(self.frame)
            #self.nome.grid(row=self.pula_linha,column=1,padx=5,pady=5,sticky=W)

            ##Nome e campo de senha
            #Label(self.frame, text="Senha:").grid(row=self.pula_linha,column=2,padx=5,pady=3)
            #self.senha = Entry(self.frame)
            #self.senha["show"] = "#"
            #self.senha.grid(row=self.pula_linha,column=3,padx=5,pady=5,sticky=W)

            #Suposta linha de separação
            #PanedWindow(orient=VERTICAL).grid(row=4,column=0,columnspan=4,padx=5,pady=5)
            #m.pack(fill=BOTH, expand=1)

            #Nome e campo com botão de diretório
            self.pula_linha = self.pula_linha + 1
            Label(self.frame, text="Diretório:").grid(row=self.pula_linha,column=0,padx=3,pady=3,sticky=W+E)
            self.Diretorio = Entry(self.frame)
            self.Diretorio["width"] = 66
            self.Diretorio.grid(row=self.pula_linha,column=1,columnspan=3, padx=5,pady=5,sticky=W)
            self.BtnBuscarDiretorio = Button(self.frame, image = self.explore)
            self.BtnBuscarDiretorio["text"] = "Dir"
            self.BtnBuscarDiretorio["font"] = ("Calibri", "8")
            self.BtnBuscarDiretorio["command"] = self.destino
            self.BtnBuscarDiretorio.grid(row=self.pula_linha,column=3,padx=5,pady=5,sticky=E)

            #check boxs
            #self.pula_linha = self.pula_linha + 1
            #try:
            #    self.checkSaiku = IntVar()
            #    self.saiku = Checkbutton(self.frame, text='Obter cód. MDX', variable = self.checkSaiku, command=self.check_statusSaiku)
            #    self.saiku.toggle()
            #    self.saiku.grid(row=self.pula_linha,column=1,columnspan=2,padx=5,pady=5,sticky=W)
            #except Exception as b:
            #    print("erro " + str(b))
            #check boxs
            #try:
            #    self.checkRelatorio = IntVar()
            #    self.relatorio = Checkbutton(self.frame, text='Obter Relatório geral', variable = self.checkRelatorio, command=self.check_statusRelatorio)
            #    self.relatorio.grid(row=self.pula_linha,column=2,columnspan=2,padx=5,pady=5,sticky=W)
            #except Exception as c:
            #    print("erro " + str(c))


            #Índice de início
            #self.pula_linha = self.pula_linha + 1
            #Label(self.frame, text="Id. início:").grid(row=self.pula_linha,column=0,padx=5,pady=5,sticky=W)
            #self.inicio = Entry(self.frame)
            #self.inicio.grid(row=self.pula_linha,column=1,padx=5,pady=5,sticky=W)
            #self.inicio = Spinbox(self.frame, from_=1, to=100000).grid(row=7,column=1,padx=5,pady=5,sticky=W)

            #Índice de fim
            #Label(self.frame, text="Id. fim:").grid(row=self.pula_linha,column=2,padx=5,pady=5,sticky=W)
            #self.fim = Entry(self.frame)
            #self.fim.grid(row=self.pula_linha,column=3,padx=5,pady=5,sticky=E)

            #self.pula_linha = self.pula_linha + 1
            #Label(self.frame, text="Como está sua internet?").grid(row=self.pula_linha,column=0,columnspan=4,padx=5,pady=5,sticky=W+E)

            #Velocidade
            #self.pula_linha = self.pula_linha + 1
            #try:
            #    self.radioResult = IntVar()
            #    self.radioResult.set(50)
            #    self.netVelocidade0 = Radiobutton(self.frame, text='Rápida', variable = self.radioResult, value=1)#, command=self.check_statusRelatorio)
            #    self.netVelocidade0.grid(row=self.pula_linha,column=0,columnspan=1,padx=5,pady=5)
            #except Exception as d:
            #    print("erro " + str(d))

            #Velocidade
            #self.netVelocidade1 = Radiobutton(self.frame, text='Normal', variable = self.radioResult, value=10)#, command=self.check_statusRelatorio)
            #self.netVelocidade1.grid(row=self.pula_linha,column=1,columnspan=1,padx=5,pady=5)

            #Velocidade
            #self.netVelocidade2 = Radiobutton(self.frame, text='Lenta', variable = self.radioResult, value=50)#, command=self.check_statusRelatorio)
            #self.netVelocidade2.grid(row=self.pula_linha,column=2,columnspan=1,padx=5,pady=5)

            #Velocidade
            #self.netVelocidade3 = Radiobutton(self.frame, text='Parada', variable = self.radioResult, value=100)#, command=self.check_statusRelatorio)
            #self.netVelocidade3.grid(row=self.pula_linha,column=3,columnspan=1,padx=5,pady=5)

            #Botão de iniciar
            self.pula_linha = self.pula_linha + 1
            self.iniciar = Button(self.frame)
            self.iniciar["text"] = "Por .ktr e .kjb nas sub rotinas."
            self.iniciar["font"] = ("Calibri", "8")
            self.iniciar["command"] = self.inicioKtr
            self.iniciar.grid(row=self.pula_linha,column=0,columnspan=4,padx=5,pady=5,sticky=W+E)

            #Botão de iniciar
            self.pula_linha = self.pula_linha + 1
            self.iniciar2 = Button(self.frame)
            self.iniciar2["text"] = "Gerar arquivo jdbc a partir de artefatos do pdi."
            self.iniciar2["font"] = ("Calibri", "8")
            self.iniciar2["command"] = self.inicioJdnc
            self.iniciar2.grid(row=self.pula_linha,column=0,columnspan=4,padx=5,pady=5,sticky=W+E)

            self.pula_linha = self.pula_linha + 4
            self.aboutButton = Button(self.frame, text="Instruções",command=self.onHelp )
            self.aboutButton.grid(row = self.pula_linha, column = 0, padx = 10, sticky = E+W)
            #informações
            td(target=self.inf,args=['Preencha os campos e clique em iniciar!',1]).start()
            #Versao
            self.pula_linha = self.pula_linha
            Label(self.frame, text="V. 1.0").grid(row=self.pula_linha,column=3,padx=5,pady=5,sticky=E)
            #self.backupTexto('start')
        except IOError:
            print("I/O erro")
        except ValueError:
            print("Não foi possível converter o dado para inteiro.")
        except:
            print("Erro inesperado:")
            raise

    def inf(self, string, nivel = None):
        print("inf: " + str(string))
        if nivel != None:
            Label(self.frame, text=string).grid(row=self.infoRow,column=0,columnspan=4,padx=5,pady=5,sticky=W+E)
        else:
            self.infoRow + 1
            Label(self.frame, text=string).grid(row=self.infoRow,column=0,columnspan=4,padx=5,pady=5,sticky=W+E)
            self.infoRow - 1

    def onHelp(self, *args):
        v = TextViewer(self.frame, "Instruções", None, self.HELP_TEXT, font = ("Courier",10))

    def destino(self):
        path = filedialog.askdirectory()
        self.Diretorio.delete(0,END)
        self.Diretorio.insert(0,str(path))
        self.diretorio = path

    def title(self, tl):
        print('=' * 80)
        #print(f'{tl:^80}'.upper())
        print('=' * 80)
        print()

    def listar_arquivos(self, caminho):
        arquivos = []
        try:
            with os.scandir(caminho) as it:
                for entrar in it:
                    if not entrar.name.startswith('.') and entrar.is_file():
                        #if entrar.name[-4:] == '.kjb' or entrar.name[-4:] == '.txt':
                        #print(caminho+'/'+entrar.name)
                        arquivos.append(caminho.replace("\\","/")+'/'+entrar.name)
        except Exception as e:
            novo = str(e)[:80] + "..."
            td(target=self.inf,args=[str(novo)]).start()
        return(arquivos)

    def listar_subDiretorios(self, caminho):
        subfolders = [f.path for f in os.scandir(caminho) if f.is_dir()]
        for caminho in list(subfolders):
            subfolders.extend(self.listar_subDiretorios(caminho))
            subfolders.sort()
        return subfolders

    def listarGeral(self):
        files = []
        #(v) Lista todos os arquivos com excessão do diretório pai.
        for i in self.listar_arquivos(self.caminhoPAI):
            files.append(i)
        #(v) Junta ma mesma lista acima.
        for i in self.listar_subDiretorios(self.caminhoPAI):
            for arq in self.listar_arquivos(i):
                files.append(arq)
        return files

    def word_replace(self, filename,old,new):
        c=0
        with io.open(filename,'r+', encoding='utf8') as f:
            a=f.read()
            b=a.split()
            for i in range(0,len(b)):
                if b[i]==old:
                    c=c+1
            old=old.center(len(old)+2)
            new=new.center(len(new)+2)
            d=a.replace(old,new,c)
            f.truncate(0)
            f.seek(0)
            f.write(d)
        print('All words have been replaced!!!')

    #replace('C:/Users/hitma/Desktop/JUVO_GR_PRD_FIAT/1/Nova pasta/Novo Documento de Texto (2).txt', 'a', 'A')
    def replace(self, caminhoComArquivo):
        #Create temp file
        fh, abs_path = mkstemp()
        count = 0
        proximoKtr = False
        proximoKjb = False
        transname = False
        jobname = False
        proxDirectory = False
        l1 = []
        l2 = []
        with fdopen(fh,'w',encoding="utf8") as novoArquivo:
            with open(caminhoComArquivo, encoding="utf8") as antigoArquivo:
                print()
                print(caminhoComArquivo)
                qLinha = 1
                for linha in antigoArquivo:
                    #----------</////////////////////////////////////////////////////////////////////////////////////////
                    #----------<directory> nome do diretório na versão 4
                    # passo (4)
                    if bool(proxDirectory):
                        if re.search('<directory>', str(linha), re.IGNORECASE):#<directory>
                            #print("kjb ===================================-=-=-" + linha)
                            linha2 = self.localizaSubstitui_KTR(str(linha),'//')[1]
                            linha = self.localizaSubstitui_dir(str(linha), caminhoComArquivo)
                            l1.append(linha2.replace('.ktr','').replace('.kjb',''))
                            proxDirectory = False
                    #----------</////////////////////////////////////////////////////////////////////////////////////////
                    #----------<transname> e <jobname> nome do arquivo na versão 4
                    # passo (3)
                    if bool(transname):
                        #print('transname: ',caminhoComArquivo)
                        if re.search('<transname>', str(linha), re.IGNORECASE):#<transname>
                            linha, linha2 = self.localizaSubstitui_KTR(str(linha),'//')
                            l1.append(linha2)
                            transname = False
                            proxDirectory = True
                            count += 1
                            print('V.4 - linha (T): ' + str(qLinha) + ' --- ' + linha.replace('\n',''))
                    if bool(jobname):
                        if re.search('<jobname>', str(linha), re.IGNORECASE):#<jobname>
                            linha, linha2 = self.localizaSubstitui_KJB(str(linha),'//')
                            l1.append(linha2)
                            jobname = False
                            proxDirectory = True
                            count += 1
                            print('V.4 - linha (J): ' + str(qLinha) + ' --- ' + linha.replace('\n',''))
                    #----------</////////////////////////////////////////////////////////////////////////////////////////
                    #----------<filename> para kjb ou ktr
                    # passo (2)
                    if bool(proximoKtr):
                        #print('filename: ',caminhoComArquivo)
                        if re.search('<filename>', str(linha), re.IGNORECASE): #<filename>
                            linha, linha2 = self.localizaSubstitui_KTR(str(linha),caminhoComArquivo)
                            l1.append(linha2)
                            proximoKtr = False
                            proxDirectory = False
                            count += 1
                            print('V.7 - linha(KTR): ' + str(qLinha) + ' --- ' + linha.replace('\n',''))
                        else:
                            transname = True
                            proximoKtr = False
                    if bool(proximoKjb):
                        #print('filename: ',caminhoComArquivo)
                        if re.search('<filename>', str(linha), re.IGNORECASE): #<filename>
                            linha, linha2 = self.localizaSubstitui_KJB(str(linha), caminhoComArquivo)
                            l1.append(linha2)
                            proximoKjb = False
                            proxDirectory = False
                            count += 1
                            print('V.7 - linha(KJB): ' + str(qLinha) + ' --- ' + linha.replace('\n',''))
                        else:
                            jobname = True
                            proximoKjb = False
                    #----------</////////////////////////////////////////////////////////////////////////////////////////
                    #----------</////////////////////////////////////////////////////////////////////////////////////////
                    #passo (1)
                    if not bool(proximoKtr):
                        if re.search('<trans_object_id', str(linha), re.IGNORECASE):#<trans_object_id>
                            proximoKtr = True
                    if not bool(proximoKjb):
                        if re.search('<job_object_id', str(linha), re.IGNORECASE):#<job_object_id>
                            proximoKjb = True
                    else:
                        proximoKtr = False
                        proximoKjb = False
                    novoArquivo.write(linha)
                    qLinha += 1
                qLinha = 1
                l2.append(count)
                l2.append(caminhoComArquivo)
                count = 0
                l2.append(l1)
                self.listaKtr.append(l2)
                l1 = []
                l2 = []
        #Copy the file permissions from the old file to the new file
        copymode(caminhoComArquivo, abs_path)
        #Remove original file
        remove(caminhoComArquivo)
        #Move new file
        move(abs_path, caminhoComArquivo)

    #replace2

    def replace2(self, caminhoComArquivo):
        #Create temp file
        fh, abs_path = mkstemp()
        count = 0
        with fdopen(fh,'w',encoding="utf8") as novoArquivo:
            with open(caminhoComArquivo, encoding="utf8") as antigoArquivo:
                #print(str(count) + ' - ' + caminhoComArquivo)
                qLinha = 1
                try:
                    for linha in antigoArquivo:
                        novoArquivo.write(linha)
                        qLinha += 1
                    #print("Total de linhas: " + str(qLinha))
                    #print()
                except Exception as e:
                    print("ERRO: NO ARQUIVO: " + str(caminhoComArquivo))
                    print("Motivo: " + str(e))
                    pass
        #Copy the file permissions from the old file to the new file
        copymode(caminhoComArquivo, abs_path)
        #Remove original file
        remove(caminhoComArquivo)
        #Move new file
        move(abs_path, caminhoComArquivo)

    #directory-#######################################################################################################

    def localizaSubstitui_KTR(self, text, dirOrigem):
        if not re.search('.ktr', text, re.IGNORECASE):
            text = text.split('</')[0] + '.ktr</' + text.split('</')[1]
        #teste com / no inicio "/JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
        if text.replace('\\','/').split('>')[1][0] == '/':
            if len(text.replace('\\','/').split('/')) == 4 and text.replace('\\','/').split('/')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
                text = '      <filename>${' + self.varCaminho + '}/' + text.split('</')[0].split('/')[-1] + '</filename>'
        else: #teste sem / no inicio "JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
            if len(text.replace('\\','/').split('/')) == 3 and text.replace('\\','/').split('/')[0].split('>')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
                text = '      <filename>${' + self.varCaminho + '}/' + text.split('</')[0].split('/')[-1] + '</filename>'
        return text, text.split('</')[0].split('>')[1]

    #directory-#######################################################################################################

    def localizaSubstitui_KJB(self, text, dirOrigem):
        if not re.search('.kjb', text, re.IGNORECASE):
            text = text.split('</')[0] + '.kjb</' + text.split('</')[1]
        #teste com / no inicio "/JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
        if text.replace('\\','/').split('>')[1][0] == '/':
            if len(text.replace('\\','/').split('/')) == 4 and text.replace('\\','/').split('/')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
                text = '      <filename>${' + self.varCaminho + '}/' + text.split('</')[0].split('/')[-1] + '</filename>'
        else: #teste sem / no inicio "JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
            if len(text.replace('\\','/').split('/')) == 3 and text.replace('\\','/').split('/')[0].split('>')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
                text = '      <filename>${' + self.varCaminho + '}/' + text.split('</')[0].split('/')[-1] + '</filename>'
        return text, text.split('</')[0].split('>')[1]

    #directory-#######################################################################################################

    def localizaSubstitui_dir(self, text, dirOrigem):
        ultimoDir = dirOrigem.split('/')[-2]
        original = text
        text = text.replace('      <directory>','').replace('\\','/')
        text = text.replace('&#47;', '/').replace('<directory>','').replace('</directory>','')
        print("Antigo dir: " + text.replace('\n',''))
        #teste com / no inicio "/JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
        if text[0] == '/' and len(text.split('/')) == 2 and text.split('/')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
            text = '      <directory>${' + self.varCaminho + '}' + text + '</directory>'
            print("Novo dir1: " + text.replace('\n',''))
        #teste sem / no inicio "JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
        elif len(text.split('/')) == 2 and text.split('/')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
            text = '      <directory>${' + self.varCaminho + '}/' + text + '</filename>'
            print("Novo dir2: " + text.replace('\n',''))
        else:
            text = '      <directory>' + newDir(text.replace('\n',''), dirOrigem) + '</directory>\n'
            print("Novo dir3: " + text.replace('\n',''))
        return text

    ########################################################################################################

    def countDir(self, text, ultimoDir):
        textOriginal = text
        dir = text.split('/')
        indice = -1
        for i in range(len(dir)):
            if dir[i] == ultimoDir:
                indice = i
                break
        if indice != -1:
            text = '${'+ self.varCaminho + '}'
        for i in range(len(dir)):
            if i > indice:
                text = text + '/' + dir[i]
        textOriginal = text
        return text.replace('\n','')

    ########################################################################################################

    def newDir(self, text, dirOrigem):
        var = '${'+ self.varCaminho + '}'
        lista = []
        listaText = text.split('/')
        listaDir = dirOrigem.split('/')[:-1]
        countText = len(listaText) -1
        countDir = len(listaDir) -1
        encontrou = False
        for i in range(countDir):
            print("dir-"+listaDir[countDir])
            for j in range(countText):
                #print("text-"+listaText[countText])
                if listaDir[countDir] == listaText[countText]:
                    lista.append(listaText[countText])
                    countText -= 1
                    encontrou = True
                    break
            if bool(encontrou):
                break
            countDir -= 1
        print(lista)
        lista = lista[:-1]
        index = len(lista) -1
        for i in range(len(lista)):
            var = var + '/' + lista[index]
            index -= 1
        if bool(encontrou):
            return var.replace('\n','')
        else:
            return text.replace('\n','')

    ########################################################################################################

    def insereVariavelDir(self, dir, text):
        #pega apenas diretório do text (do arquivo)
        a = text.split('\\')
        arquivo = a.pop(-1)
        arquivo = arquivo.split('<')[0]
        text = a[0].split('>')[1]
        for i in a[1:]:
            text += '/' + i
            #pega apenas diretório do arquivo localizado
            a = dir.split('/')
            a.pop(-1)
            dir = a[0]
            for i in a[1:]:
                dir += '/' + i
            return dir, text

    ########################################################################################################

    def remove_repetidos(self, l):
        lista = l
        i = 0
        while i < len(lista):
            j = i + 1
            while j < len(lista):
                if lista[j] == lista[i]:
                    del(lista[j])
                else:
                    j = j + 1
            i = i + 1
        return sorted(lista)

    ########################################################################################################

    def acertaDirKtr(self, lista1):
        lista = []
        count = 0
        for i in range(len(lista1)):
            try:
                a = str(lista1[count+1] + '/')
                b = str(lista1[count])
                lista.append(a + b)
                count += 2
            except:
                    pass
        return lista

    ########################################################################################################

    def invertKjb(self, string):
        lCp = []
        count = 1
        for i in range(len(string.split('/'))):
            inverso = len(string.split('/')) - count
            lCp.append(string.split('/')[inverso])
            count += 1
        return lCp

    ########################################################################################################

    def invertKtr(self, lista):
        lCs = []
        for file in lista:
            count = 1
            lCs1 = []
            for i in range(len(file.split('/'))):
                #print(file.split('/')[i])
                inverso = len(file.split('/')) - count
                lCs1.append(file.split('/')[inverso])
                count += 1
            lCs.append(lCs1)
        return lCs

    ########################################################################################################

    def gravaRelatorio(self, lista): #gravaRelatorio("C:/Users/hitma/Documents/Github/migra_repo_pdi/Nova pasta", lista)
        nomeArquivo = self.caminhoPAI + "/relatorio.txt"
        l = lista
        lista = []
        for i in l:
            for j in i:
                lista.append(str(j) + "\n")
                print(j)
            lista.append("\n")
        try:
            arquivo = open(nomeArquivo, 'w')
            arquivo.writelines(lista)
            arquivo.close()
            a=[]
            for i in lista:
                if i != '' or i != None or i != '\n':
                    print(i)
                    a.append(i)
            td(target=self.inf,args=["Arquivo 'Relatorio.txt' criado no diretório! Total de cerca de" + str(int(len(a)/5)) + " conexões."]).start()
        except Exception as e:
            print("Erro ao criar arquivo Relatório! " + str(e))

    ########################################################################################################

    def remove_repetidos(self, lista):
        l = []
        for i in lista:
            if i not in l:
                l.append(i)
        l.sort()
        return l

    ########################################################################################################

    def stringConn(self, server = '', database = '', port = '', name = '', tipo = ''):
        if server == None:
            server = ''
        try:
            # POSTGRESQS /////////////////////////////////////////////////////////
            if tipo == 'POSTGRESQL':
                if server == None:
                    return 'javax.sql.DataSource', 'org.postgresql.Driver', 'jdbc:postgresql://' + database
                else:
                    return 'javax.sql.DataSource', 'org.postgresql.Driver', 'jdbc:postgresql://' + str(server) + ':' + str(port) + '/hibernate?searchpath=' + str(database)
            # ORACLE /////////////////////////////////////////////////////////
            elif tipo == 'ORACLE': #jdbc:oracle:thin:@' + str(server) + ':' + str(port) + ':' + str(name)
                if server == None:
                    return 'javax.sql.DataSource', 'oracle.jdbc.OracleDriver', 'jdbc:oracle:thin:@' + database
                else:
                    return 'javax.sql.DataSource', 'oracle.jdbc.OracleDriver', 'jdbc:oracle:thin:@' + str(server) + ':' + str(port) + ':' + str(database)
            # MSSQL /////////////////////////////////////////////////////////
            elif tipo == 'MYSQL':
                if server == None:
                    return 'javax.sql.DataSource', 'com.mysql.jdbc.Driver', database
                else:
                    return 'javax.sql.DataSource', 'com.mysql.jdbc.Driver', 'jdbc:mysql://' + str(server) + '/foodmart?useCursorFetch=true'
            # MSSQLNATIVE /////////////////////////////////////////////////////////
            elif tipo == 'MSSQLNATIVE':
                if server == None:
                    return 'javax.sql.DataSource', 'com.microsoft.sqlserver.jdbc.SQLServerDriver', 'jdbc:sqlserver:' + database
                else: #jdbc:jtds:sqlserver://<ur_server:port>;UseNTLMv2=true;Domain=AD;Trusted_Connection=yes"
                    return 'javax.sql.DataSource', 'com.microsoft.sqlserver.jdbc.SQLServerDriver', 'jdbc:sqlserver://' + str(server) + ':' + str(port) + ';databasename=' + str(database) + ';integratedsecurity=true'
            #/////////////////////////////////////////////////////////
            elif tipo == 'H2':
                if server == None:
                    return 'javax.sql.DataSource', 'org.h2.Driver', 'jdbc:h2:file:' + database
                else:                                               #jdbc:h2:mem:AZ;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE
                    return 'javax.sql.DataSource', 'org.h2.Driver', 'jdbc:h2:file:' + str(server) + '/'+ str(database) + ';DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE'
            #/////////////////////////////////////////////////////////
            elif tipo == 'HYPERSONIC':
                if server == None:
                    return 'javax.sql.DataSource', 'org.hsqldb.jdbcDriver', 'jdbc:hsqldb:' + database
                else:
                    return 'javax.sql.DataSource', 'org.hsqldb.jdbcDriver', 'jdbc:hsqldb:' + str(server) + '/' + str(database)
            #/////////////////////////////////////////////////////////
            elif tipo == 'INFORMIX':
                if server == None:
                    return 'javax.sql.DataSource', 'com.informix.jdbc.IfxDriver', 'jdbc:bea:informix://' + database
                else:                                                             #jdbc:bea:informix://dbserver1:1543;informixServer=dbserver1;databaseName=dbname
                    return 'javax.sql.DataSource', 'com.informix.jdbc.IfxDriver', 'jdbc:bea:informix://' + str(server) + ':' + str(port) + '/' + str(database)
            #/////////////////////////////////////////////////////////
            elif tipo == 'INGRES':
                if server == None:
                    return 'javax.sql.DataSource', 'com.ingres.jdbc.IngresDriver', 'jdbc:ingres://' + database
                else:                                                    #jdbc:ingres://<hostname>:<port>/<database>;UID=<user>;PWD=<password>
                    return 'javax.sql.DataSource', 'com.ingres.jdbc.IngresDriver', 'jdbc:ingres://' + str(server) + ':' + str(port) + '/' + str(database)
            #/////////////////////////////////////////////////////////
            elif tipo == 'LucidDB':
                if server == None:
                    return 'javax.sql.DataSource', 'org.luciddb.jdbc.LucidDbClientDriver', 'jdbc:luciddb:' + database
                else:                                                                       #jdbc:luciddb:rmi://localhost;schema=BIZARRO
                    return 'javax.sql.DataSource', 'org.luciddb.jdbc.LucidDbClientDriver', 'jdbc:luciddb:' + str(server) + ':' + str(port) + ';schema=' + str(database)
            #/////////////////////////////////////////////////////////
            elif tipo == 'MONETDB':
                if server == None:
                    return 'javax.sql.DataSource', 'driver_MSSQLNATIVE', 'jdbc:monetdb://' + database
                else:
                    return 'javax.sql.DataSource', 'driver_MSSQLNATIVE', 'jdbc:monetdb://' + str(server) + ':' + str(port) + '/' + str(database)
            #/////////////////////////////////////////////////////////
            elif tipo == 'MSSQL':
                if server == None:
                    return 'javax.sql.DataSource', 'com.microsoft.sqlserver.jdbc.SQLServerDriver', 'jdbc:sqlserver:' + database
                else: #jdbc:jtds:sqlserver://<ur_server:port>;UseNTLMv2=true;Domain=AD;Trusted_Connection=yes"
                    return 'javax.sql.DataSource', 'com.microsoft.sqlserver.jdbc.SQLServerDriver', 'jdbc:sqlserver://' + str(server) + ':' + str(port) + ';databasename=' + str(database) + ';integratedsecurity=true'
            # POSTGRESQS /////////////////////////////////////////////////////////
            else:
                if server == None:
                    return 'javax.sql.DataSource', 'driver_de_conexao_faltando', database
                else:
                    return 'javax.sql.DataSource', 'driver_de_conexao_faltando', server
        except Exception as e:
            print("Erro: " + str(e))

    ########################################################################################################

    def conexoes(self):
        geral = []
        for file in self.listarGeral():
            try:
                #print(files)#if file[-4:] == '.kjb':
                with open(file) as files:#'C:/Users/hitma/Desktop/Assistencia_original/JUVO_GR_PRD_CAIXA/DT_PROCESSO_DIA_1003.ktr') as files: #file) as files:#
                    doc = xmltodict.parse(files.read())
                try:
                    for i in doc['job']['connection']:
                        l = []
                        nomeConn = i['name'] + '/'
                        type, driver, url = self.stringConn(i['server'],i['database'], i['port'], i['name'], i['type'])
                        print(nomeConn + 'type=' + str(i['type']))
                        #print(nomeConn + 'server=' + str(i['server']))
                        #print(nomeConn + 'database=' + str(i['database']))
                        #print(nomeConn + 'port=' + str(i['port']))
                        #print(nomeConn + 'name=' + str(i['name']))
                        #print(nomeConn + 'user=' + str(i['username']))
                        #print(nomeConn + 'password=' + str(i['password']))
                        #print()
                        #l.append(nomeConn + 'name=' + str(i['name']))
                        #l.append(nomeConn + 'type=' + str(i['type']))
                        #l.append(nomeConn + 'server=' + str(i['server']))
                        #l.append(nomeConn + 'database=' + str(i['database']))
                        #l.append(nomeConn + 'port=' + str(i['port']))
                        #l.append(nomeConn + 'user=' + str(i['username']))
                        #l.append(nomeConn + 'password=' + str(i['password']))
                        l.append(nomeConn + 'type=' + str(type))
                        l.append(nomeConn + 'driver=' + str(driver))
                        l.append(nomeConn + 'url=' + str(url.replace(":-1:","").replace(":None:","")))
                        l.append(nomeConn + 'user=' + str(i['username']))
                        l.append(nomeConn + 'password=' + str(i['password']))
                        geral.append(l)
                except:
                    for i in doc['transformation']['connection']:
                        l = []
                        nomeConn = i['name'] + '/'
                        type, driver, url = self.stringConn(i['server'],i['database'], i['port'], i['name'], i['type'])
                        print(nomeConn + 'type=' + str(i['type']))
                        #print(nomeConn + 'server=' + str(i['server']))
                        #print(nomeConn + 'database=' + str(i['database']))
                        #print(nomeConn + 'port=' + str(i['port']))
                        #print(nomeConn + 'name=' + str(i['name']))
                        #print(nomeConn + 'user=' + str(i['username']))
                        #print(nomeConn + 'password=' + str(i['password']))
                        #print()
                        #l.append(nomeConn + 'name=' + str(i['name']))
                        #l.append(nomeConn + 'type=' + str(i['type']))
                        #l.append(nomeConn + 'server=' + str(i['server']))
                        #l.append(nomeConn + 'database=' + str(i['database']))
                        #l.append(nomeConn + 'port=' + str(i['port']))
                        #l.append(nomeConn + 'user=' + str(i['username']))
                        #l.append(nomeConn + 'password=' + str(i['password']))
                        l.append(nomeConn + 'type=' + str(type))
                        l.append(nomeConn + 'driver=' + str(driver))
                        l.append(nomeConn + 'url=' + str(url.replace(":-1:","").replace(":None:","")))
                        l.append(nomeConn + 'user=' + str(i['username']))
                        l.append(nomeConn + 'password=' + str(i['password']))
                        geral.append(l)
                    pass
            except Exception as a:
                print(file)
                print("Erro no arquivo: " + str(a))
                pass
        return geral

    def home(self):
        for file in self.listarGeral():
            if file[-4:] == '.kjb':
                replace(file)

    def menu_diretorios(self):
        title('Navegando pelo Menu DIRETORIOS')
        print('Escolha sua opção: ')
        op = str(input('''
            [1] - Atualizar data de modificação de todos os arquivos dentro do diretório.
            [2] - Acertar diretório com ${Internal.Entry.Current.Directory} no primeiro nível.
            [3] - Acessar diretórios
            [4] - Listar Arquivos
            [5] - ok Por extenção .ktr nas transformações e acertar diretórios que se encontram no mesmo nível.
            [6] - Extrair conexões dos arquivos kjb e ktr.
            [0] - Retornar/Sair
            Opção: ''')).lower()
        print()

        if op == '0':
            exit(1)

    # ------------------------------------------------------------------------------------------- #
        elif op == '1':  # POR EXTENÇÃO KTR
            for file in self.listarGeral():
                #if file[-4:] == '.kjb':
                replace2(file)
    # ------------------------------------------------------------------------------------------- #
        elif op == '5':  # POR EXTENÇÃO KTR
            for file in self.listarGeral():
                if file[-4:] == '.kjb':
                    replace(file)
            """            l1 = []
            for i in listaKtr:
                print(i[2])
                lista = []
                lista.append(i[0])
                lista.append(i[1])
                lista.append(acertaDirKtr(i[2]))
                l1.append(lista)
            #(v) arruma os diretórios dos arquivos ktr para ficarem antes do nome do arquivo.
            l2 = []
            for i in l1:
                lista = []
                lista.append(i[0])
                lista.append(invertKjb(i[1]))
                lista.append(invertKtr(i[2]))
                l2.append(lista)
            #(A) OK
            for kjb in l2:
                for principal in kjb[1][1:]:
                    for ktrs in kjb[2][1:]:
                        if principal == ktrs:"""
    # ------------------------------------------------------------------------------------------- #
        elif op == '2':  # ACESSAR DIRETORIOS
            print('_' * 40)
            acess_dir(self.caminhoPAI)
            tem = (str(input('Informe o nome da pasta a ser acessada: ')))
            dir_acesso = tem
            if not os.path.exists(dir_acesso):
                j = 'S'
                while j == 'S':
                    j = str(input('Pasta inexistente. Deseja tentar outra? [S/N]')).upper()
            else:
                for caminho, pastas, arquivos in os.walk(self.caminhoPAI):
                    for pasta in pastas[:]:
                        if pasta == dir_acesso:
                            caminho = tem
                            os.chdir(caminho)
                            print('Pasta acessada!')
            print('_' * 40)

            menu_diretorios()
    # ------------------------------------------------------------------------------------------- #
        elif op == '3':  # ACESSAR DIRETORIOS
            print('_' * 40)
            acess_dir(self.caminhoPAI)
            tem = (str(input('Informe o nome da pasta a ser acessada: ')))
            dir_acesso = tem
            if not os.path.exists(dir_acesso):
                j = 'S'
                while j == 'S':
                    j = str(input('Pasta inexistente. Deseja tentar outra? [S/N]')).upper()
            else:
                for caminho, pastas, arquivos in os.walk(self.caminhoPAI):
                    for pasta in pastas[:]:
                        if pasta == dir_acesso:
                            caminho = tem
                            os.chdir(caminho)
                            print('Pasta acessada!')
            print('_' * 40)

            self.menu_diretorios()
    # ------------------------------------------------------------------------------------------- #
        elif op == '6':  # POR EXTENÇÃO KTR
            lista = self.remove_repetidos(self.conexoes())
            print(lista)
            #self.gravaRelatorio(self.caminhoPAI, lista)
    # ------------------------------------------------------------------------------------------- #
        elif op == '4':  # LISTAR ARQUIVOS
            print(self.listar_arquivos(self.caminhoPAI))
            print(os.getcwd())
            self.menu_diretorios()


    # ------------------------------------------------------------------------------------------- #
        else:
            print("Esta opção não está nas alternativas, tente novamente.\n")
            self.menu_diretorios()

class TextViewer(Toplevel):
    """
    Simples texto da introdução!
    """
    def __init__(self, parent, title, fileName, data=None, xsize = 625, ysize = 500, font = None):
        """If data exists, load it into viewer, otherwise try to load file.

        fileName - string, should be an absolute filename
        """
        Toplevel.__init__(self, parent)
        self.configure(borderwidth=5)
        self.geometry("=%dx%d+%d+%d" % (xsize, ysize,
                                        parent.winfo_rootx() + 10,
                                        parent.winfo_rooty() + 10))
        #elguavas - config placeholders til config stuff completed
        self.bg = '#ffffff'
        self.fg = '#000000'

        self.font = font
        self.CreateWidgets()
        self.title(title)
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.Ok)
        self.parent = parent
        self.textView.focus_set()
        #key bindings for this dialog
        self.bind('<Return>',self.Ok) #dismiss dialog
        self.bind('<Escape>',self.Ok) #dismiss dialog
        if data:
            self.textView.insert(0.0, data)
        else:
            self.LoadTextFile(fileName)
        self.textView.config(state=DISABLED)
        self.wait_window()

    def LoadTextFile(self, fileName):
        textFile = None
        try:
            textFile = open(fileName, 'r')
        except IOError:
            tkMessageBox.showerror(title='File Load Error',
                    message='Unable to load file %r .' % (fileName,))
        else:
            self.textView.insert(0.0,textFile.read())

    def CreateWidgets(self):
        frameText = Frame(self, relief=SUNKEN, height=700)
        frameButtons = Frame(self)
        self.buttonOk = Button(frameButtons, text='Close',
                               command=self.Ok, takefocus=FALSE)
        self.scrollbarView = Scrollbar(frameText, orient=VERTICAL,
                                       takefocus=FALSE, highlightthickness=0)

        self.textView = Text(frameText, wrap=WORD, highlightthickness=0,
                             fg=self.fg, bg=self.bg)
        if self.font:
            self.textView.configure(font = self.font)

        self.scrollbarView.config(command=self.textView.yview)
        self.textView.config(yscrollcommand=self.scrollbarView.set)
        self.buttonOk.pack()
        self.scrollbarView.pack(side=RIGHT,fill=Y)
        self.textView.pack(side=LEFT,expand=TRUE,fill=BOTH)
        frameButtons.pack(side=BOTTOM,fill=X)
        frameText.pack(side=TOP,expand=TRUE,fill=BOTH)

    def Ok(self, event=None):
        self.destroy()

main = Tk()
Server(main)
main.mainloop()
#replace('C:/Users/hitma/Desktop/JUVO_GR_PRD_FIAT/1/Nova pasta/Novo Documento de Texto (2).txt', 'a', 'A')
