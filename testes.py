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


campoDeBusca = '<trans_object_id'
campoDeBusca2 = '<filename>'
campoDeBusca3 = '<transname>'
campoDeBusca4 = '<directory>'
listaKtr = []
Diretorio = ""
caminhoPAI = (str(input(': ')))
varCaminho = "Internal.Entry.Current.Directory"
pula_linha = 0
#linha de informações
infoRow = 6
master.focus_set()
abas = ttk.Notebook(master)

aba1 = ttk.Frame(abas)
aba2 = ttk.Frame(abas)

master.iconbitmap("img/my_icon.ico")
frame = Frame(master)
master = master

master.title('Acerta os arquivos do repositório migrados de BD')
larguraTela = 500
alturaTela = 266
w, h = master.winfo_screenwidth(), master.winfo_screenheight()
print(str(int(w/2)))
w = (int(w/2)) - larguraTela + (int(larguraTela/2))
h = (int(h/2)) - alturaTela + (int(alturaTela/2)) - 40
master.geometry(str(larguraTela) + 'x' + str(alturaTela) + '+' + str(w) + '+' + str(h))
fontePadrao = ("Arial", "10")
frame.grid(row=1,column=0,padx=1,pady=1)

explore = ''

#tempo para espera de arquivos
#td(target=interface).start()
#print(menu_diretorios())

def trataDir():
    if Diretorio.get().replace(' ','') == '' or Diretorio.get() == None:
        td(target=inf,args=['Preencha o diretório!']).start()
    else:
        caminhoPAI = Diretorio.get().replace('\\', '/')
        print("|" + str(caminhoPAI) + "| OK")

def inicioKtr():
    trataDir()
    for file in listarGeral():
        if file[-4:] == '.kjb':
            replace(file)
    td(target=inf,args=['Acerto de arquivos finalizado!',1]).start()
        #return caminhoPAI

def inicioJdnc():
    td(target=inf,args=["Analizando arquivos .ktr e .kjb..."]).start()
    trataDir()
    lista = remove_repetidos(conexoes())
    print(lista)
    gravaRelatorio(lista)

def inf( string, nivel = None):
    print("inf: " + str(string))
    if nivel != None:
        Label(frame, text=string).grid(row=infoRow,column=0,columnspan=4,padx=5,pady=5,sticky=W+E)
    else:
        infoRow + 1
        Label(frame, text=string).grid(row=infoRow,column=0,columnspan=4,padx=5,pady=5,sticky=W+E)
        infoRow - 1

def onHelp( *args):
    v = TextViewer(frame, "Instruções", None, HELP_TEXT, font = ("Courier",10))

def destino():
    path = filedialog.askdirectory()
    Diretorio.delete(0,END)
    Diretorio.insert(0,str(path))
    diretorio = path

def title( tl):
    print('=' * 80)
    #print(f'{tl:^80}'.upper())
    print('=' * 80)
    print()

def listar_arquivos( caminho):
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
        td(target=inf,args=[str(novo)]).start()
    return(arquivos)

def listar_subDiretorios( caminho):
    subfolders = [f.path for f in os.scandir(caminho) if f.is_dir()]
    for caminho in list(subfolders):
        subfolders.extend(listar_subDiretorios(caminho))
        subfolders.sort()
    return subfolders

def listarGeral():
    files = []
    #(v) Lista todos os arquivos com excessão do diretório pai.
    for i in listar_arquivos(caminhoPAI):
        files.append(i)
    #(v) Junta ma mesma lista acima.
    for i in listar_subDiretorios(caminhoPAI):
        for arq in listar_arquivos(i):
            files.append(arq)
    return files

def word_replace( filename,old,new):
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
def replace( caminhoComArquivo):
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
                        linha2 = localizaSubstitui_KTR(str(linha),'//')[1]
                        linha = localizaSubstitui_dir(str(linha), caminhoComArquivo)
                        l1.append(linha2.replace('.ktr','').replace('.kjb',''))
                        proxDirectory = False
                #----------</////////////////////////////////////////////////////////////////////////////////////////
                #----------<transname> e <jobname> nome do arquivo na versão 4
                # passo (3)
                if bool(transname):
                    #print('transname: ',caminhoComArquivo)
                    if re.search('<transname>', str(linha), re.IGNORECASE):#<transname>
                        linha, linha2 = localizaSubstitui_KTR(str(linha),'//')
                        l1.append(linha2)
                        transname = False
                        proxDirectory = True
                        count += 1
                        print('V.4 - linha (T): ' + str(qLinha) + ' --- ' + linha.replace('\n',''))
                if bool(jobname):
                    if re.search('<jobname>', str(linha), re.IGNORECASE):#<jobname>
                        linha, linha2 = localizaSubstitui_KJB(str(linha),'//')
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
                        linha, linha2 = localizaSubstitui_KTR(str(linha),caminhoComArquivo)
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
                        linha, linha2 = localizaSubstitui_KJB(str(linha), caminhoComArquivo)
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
            listaKtr.append(l2)
            l1 = []
            l2 = []
    #Copy the file permissions from the old file to the new file
    copymode(caminhoComArquivo, abs_path)
    #Remove original file
    remove(caminhoComArquivo)
    #Move new file
    move(abs_path, caminhoComArquivo)

#replace2

def replace2( caminhoComArquivo):
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

def localizaSubstitui_KTR( text, dirOrigem):
    if not re.search('.ktr', text, re.IGNORECASE):
        text = text.split('</')[0] + '.ktr</' + text.split('</')[1]
    #teste com / no inicio "/JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
    if text.replace('\\','/').split('>')[1][0] == '/':
        if len(text.replace('\\','/').split('/')) == 4 and text.replace('\\','/').split('/')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
            text = '      <filename>${' + varCaminho + '}/' + text.split('</')[0].split('/')[-1] + '</filename>'
    else: #teste sem / no inicio "JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
        if len(text.replace('\\','/').split('/')) == 3 and text.replace('\\','/').split('/')[0].split('>')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
            text = '      <filename>${' + varCaminho + '}/' + text.split('</')[0].split('/')[-1] + '</filename>'
    return text, text.split('</')[0].split('>')[1]

#directory-#######################################################################################################

def localizaSubstitui_KJB( text, dirOrigem):
    if not re.search('.kjb', text, re.IGNORECASE):
        text = text.split('</')[0] + '.kjb</' + text.split('</')[1]
    #teste com / no inicio "/JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
    if text.replace('\\','/').split('>')[1][0] == '/':
        if len(text.replace('\\','/').split('/')) == 4 and text.replace('\\','/').split('/')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
            text = '      <filename>${' + varCaminho + '}/' + text.split('</')[0].split('/')[-1] + '</filename>'
    else: #teste sem / no inicio "JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
        if len(text.replace('\\','/').split('/')) == 3 and text.replace('\\','/').split('/')[0].split('>')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
            text = '      <filename>${' + varCaminho + '}/' + text.split('</')[0].split('/')[-1] + '</filename>'
    return text, text.split('</')[0].split('>')[1]

#directory-#######################################################################################################

def localizaSubstitui_dir( text, dirOrigem):
    ultimoDir = dirOrigem.split('/')[-2]
    original = text
    text = text.replace('      <directory>','').replace('\\','/')
    text = text.replace('&#47;', '/').replace('<directory>','').replace('</directory>','')
    print("Antigo dir: " + text.replace('\n',''))
    #teste com / no inicio "/JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
    if text[0] == '/' and len(text.split('/')) == 2 and text.split('/')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
        text = '      <directory>${' + varCaminho + '}' + text + '</directory>'
        print("Novo dir1: " + text.replace('\n',''))
    #teste sem / no inicio "JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
    elif len(text.split('/')) == 2 and text.split('/')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
        text = '      <directory>${' + varCaminho + '}/' + text + '</filename>'
        print("Novo dir2: " + text.replace('\n',''))
    else:
        text = '      <directory>' + newDir(text.replace('\n',''), dirOrigem) + '</directory>\n'
        print("Novo dir3: " + text.replace('\n',''))
    return text

########################################################################################################

def countDir( text, ultimoDir):
    textOriginal = text
    dir = text.split('/')
    indice = -1
    for i in range(len(dir)):
        if dir[i] == ultimoDir:
            indice = i
            break
    if indice != -1:
        text = '${'+ varCaminho + '}'
    for i in range(len(dir)):
        if i > indice:
            text = text + '/' + dir[i]
    textOriginal = text
    return text.replace('\n','')

########################################################################################################

def newDir( text, dirOrigem):
    var = '${'+ varCaminho + '}'
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

def insereVariavelDir( dir, text):
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

def remove_repetidos(l):
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
"""
def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l"""
########################################################################################################

def acertaDirKtr( lista1):
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

def invertKjb( string):
    lCp = []
    count = 1
    for i in range(len(string.split('/'))):
        inverso = len(string.split('/')) - count
        lCp.append(string.split('/')[inverso])
        count += 1
    return lCp

########################################################################################################

def invertKtr( lista):
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

def gravaRelatorio( lista): #gravaRelatorio("C:/Users/hitma/Documents/Github/migra_repo_pdi/Nova pasta", lista)
    nomeArquivo = caminhoPAI + "/relatorio.txt"
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
        td(target=inf,args=["Arquivo 'Relatorio.txt' criado no diretório! Total de cerca de" + str(int(len(a)/5)) + " conexões."]).start()
    except Exception as e:
        print("Erro ao criar arquivo Relatório! " + str(e))

########################################################################################################


########################################################################################################

def stringConn( server = '', database = '', port = '', name = '', tipo = ''):
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

def conexoes():
    geral = []
    for file in listarGeral():
        try:
            #print(files)#if file[-4:] == '.kjb':
            with open(file) as files:#'C:/Users/hitma/Desktop/Assistencia_original/JUVO_GR_PRD_CAIXA/DT_PROCESSO_DIA_1003.ktr') as files: #file) as files:#
                doc = xmltodict.parse(files.read())
            try:
                for i in doc['job']['connection']:
                    l = []
                    nomeConn = i['name'] + '/'
                    type, driver, url = stringConn(i['server'],i['database'], i['port'], i['name'], i['type'])
                    #print(nomeConn + 'type=' + str(i['type']))
                    print('server=' + str(i['server']))
                    print('database=' + str(i['database']))
                    #print(nomeConn + 'port=' + str(i['port']))
                    #print(nomeConn + 'name=' + str(i['name']))
                    #print(nomeConn + 'user=' + str(i['username']))
                    #print(nomeConn + 'password=' + str(i['password']))
                    #print()
                    #l.append(nomeConn + 'name=' + str(i['name']))
                    #l.append(nomeConn + 'type=' + str(i['type']))
                    l.append('server=' + str(i['server']))
                    l.append('database=' + str(i['database']))
                    #l.append(nomeConn + 'port=' + str(i['port']))
                    #l.append(nomeConn + 'user=' + str(i['username']))
                    #l.append(nomeConn + 'password=' + str(i['password']))
                    #l.append(nomeConn + 'type=' + str(type))
                    #l.append(nomeConn + 'driver=' + str(driver))
                    #l.append(nomeConn + 'url=' + str(url))
                    #l.append(nomeConn + 'user=' + str(i['username']))
                    #l.append(nomeConn + 'password=' + str(i['password']))
                    geral.append(l)
            except:
                for i in doc['transformation']['connection']:
                    l = []
                    nomeConn = i['name'] + '/'
                    type, driver, url = stringConn(i['server'],i['database'], i['port'], i['name'], i['type'])
                    #print(nomeConn + 'type=' + str(i['type']))
                    print('server=' + str(i['server']))
                    print('database=' + str(i['database']))
                    #print(nomeConn + 'port=' + str(i['port']))
                    #print(nomeConn + 'name=' + str(i['name']))
                    #print(nomeConn + 'user=' + str(i['username']))
                    #print(nomeConn + 'password=' + str(i['password']))
                    #print()
                    #l.append(nomeConn + 'name=' + str(i['name']))
                    #l.append(nomeConn + 'type=' + str(i['type']))
                    l.append('server=' + str(i['server']))
                    l.append('database=' + str(i['database']))
                    #l.append(nomeConn + 'port=' + str(i['port']))
                    #l.append(nomeConn + 'user=' + str(i['username']))
                    #l.append(nomeConn + 'password=' + str(i['password']))
                    #l.append(nomeConn + 'type=' + str(type))
                    #l.append(nomeConn + 'driver=' + str(driver))
                    #l.append(nomeConn + 'url=' + str(url))
                    #l.append(nomeConn + 'user=' + str(i['username']))
                    #l.append(nomeConn + 'password=' + str(i['password']))
                    geral.append(l)
                pass
        except Exception as a:
            print(file)
            print("Erro no arquivo: " + str(a))
            pass
    return geral

def home():
    for file in listarGeral():
        if file[-4:] == '.kjb':
            replace(file)

def menu_diretorios():
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
        for file in listarGeral():
            #if file[-4:] == '.kjb':
            replace2(file)
# ------------------------------------------------------------------------------------------- #
    elif op == '5':  # POR EXTENÇÃO KTR
        for file in listarGeral():
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
        acess_dir(caminhoPAI)
        tem = (str(input('Informe o nome da pasta a ser acessada: ')))
        dir_acesso = tem
        if not os.path.exists(dir_acesso):
            j = 'S'
            while j == 'S':
                j = str(input('Pasta inexistente. Deseja tentar outra? [S/N]')).upper()
        else:
            for caminho, pastas, arquivos in os.walk(caminhoPAI):
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
        acess_dir(caminhoPAI)
        tem = (str(input('Informe o nome da pasta a ser acessada: ')))
        dir_acesso = tem
        if not os.path.exists(dir_acesso):
            j = 'S'
            while j == 'S':
                j = str(input('Pasta inexistente. Deseja tentar outra? [S/N]')).upper()
        else:
            for caminho, pastas, arquivos in os.walk(caminhoPAI):
                for pasta in pastas[:]:
                    if pasta == dir_acesso:
                        caminho = tem
                        os.chdir(caminho)
                        print('Pasta acessada!')
        print('_' * 40)

        menu_diretorios()
# ------------------------------------------------------------------------------------------- #
    elif op == '6':  # POR EXTENÇÃO KTR
        lista = remove_repetidos(conexoes())
        #print(lista)
        #gravaRelatorio(caminhoPAI, lista)
# ------------------------------------------------------------------------------------------- #
    elif op == '4':  # LISTAR ARQUIVOS
        print(listar_arquivos(caminhoPAI))
        print(os.getcwd())
        menu_diretorios()


# ------------------------------------------------------------------------------------------- #
    else:
        print("Esta opção não está nas alternativas, tente novamente.\n")
        menu_diretorios()

class TextViewer(Toplevel):
    """
    Simples texto da introdução!
    """
    def __init__( parent, title, fileName, data=None, xsize = 625, ysize = 500, font = None):
        """If data exists, load it into viewer, otherwise try to load file.

        fileName - string, should be an absolute filename
        """
        Toplevel.__init__( parent)
        configure(borderwidth=5)
        geometry("=%dx%d+%d+%d" % (xsize, ysize,
                                        parent.winfo_rootx() + 10,
                                        parent.winfo_rooty() + 10))
        #elguavas - config placeholders til config stuff completed
        bg = '#ffffff'
        fg = '#000000'

        font = font
        CreateWidgets()
        title(title)
        transient(parent)
        grab_set()
        protocol("WM_DELETE_WINDOW", Ok)
        parent = parent
        textView.focus_set()
        #key bindings for this dialog
        bind('<Return>',Ok) #dismiss dialog
        bind('<Escape>',Ok) #dismiss dialog
        if data:
            textView.insert(0.0, data)
        else:
            LoadTextFile(fileName)
        textView.config(state=DISABLED)
        wait_window()

    def LoadTextFile( fileName):
        textFile = None
        try:
            textFile = open(fileName, 'r')
        except IOError:
            tkMessageBox.showerror(title='File Load Error',
                    message='Unable to load file %r .' % (fileName,))
        else:
            textView.insert(0.0,textFile.read())

    def CreateWidgets():
        frameText = Frame( relief=SUNKEN, height=700)
        frameButtons = Frame()
        buttonOk = Button(frameButtons, text='Close',
                               command=Ok, takefocus=FALSE)
        scrollbarView = Scrollbar(frameText, orient=VERTICAL,
                                       takefocus=FALSE, highlightthickness=0)

        textView = Text(frameText, wrap=WORD, highlightthickness=0,
                             fg=fg, bg=bg)
        if font:
            textView.configure(font = font)

        scrollbarView.config(command=textView.yview)
        textView.config(yscrollcommand=scrollbarView.set)
        buttonOk.pack()
        scrollbarView.pack(side=RIGHT,fill=Y)
        textView.pack(side=LEFT,expand=TRUE,fill=BOTH)
        frameButtons.pack(side=BOTTOM,fill=X)
        frameText.pack(side=TOP,expand=TRUE,fill=BOTH)

    def Ok( event=None):
        destroy()

main = Tk()
Server(main)
main.mainloop()
#replace('C:/Users/hitma/Desktop/JUVO_GR_PRD_FIAT/1/Nova pasta/Novo Documento de Texto (2).txt', 'a', 'A')
