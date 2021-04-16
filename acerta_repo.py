# -*- coding:utf-8 -*-
#!/usr/bin/env python
#encoding: utf-8
#coding: utf-8
#!/usr/bin/env python3
#Autor Maurcio Rodrigues (mauriciosist@gmail.com)
import os, re, fileinput
import os.path
import shutil
import io

from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

caminhoInp = "C:\\Users\\hitma\\Desktop\\JUVO_GR_PRD_VWAUT"#str(input('Diretório: '))#
caminhoPAI = caminhoInp.replace('\\', '/')
varCaminho = "Internal.Entry.Current.Directory"
#caminhoPAI = 'C:/Users/hitma/Desktop/JUVO_GR_PRD_FIAT'
#caminhoPAI = "C:\Users\hitma\Desktop\ETLAS012 - Telefonia"
campoDeBusca = '<trans_object_id'
campoDeBusca2 = '<filename>'
campoDeBusca3 = '<transname>'
campoDeBusca4 = '<directory>'
listaKtr = []

def title(tl):
    print('=' * 80)
    #print(f'{tl:^80}'.upper())
    print('=' * 80)
    print()

def acess_dir(caminho):
    with os.scandir(caminho) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_dir():
                print(entry.name)

def listar_arquivos(caminho):
    arquivos = []
    with os.scandir(caminho) as it:
        for entrar in it:
            if not entrar.name.startswith('.') and entrar.is_file():
                #if entrar.name[-4:] == '.kjb' or entrar.name[-4:] == '.txt':
                #print(caminho+'/'+entrar.name)
                arquivos.append(caminho.replace("\\","/")+'/'+entrar.name)
    return(arquivos)

def listar_subDiretorios(caminho):
    subfolders = [f.path for f in os.scandir(caminho) if f.is_dir()]
    for caminho in list(subfolders):
        subfolders.extend(listar_subDiretorios(caminho))
        subfolders.sort()
    return subfolders

def word_replace(filename,old,new):
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
def replace(caminhoComArquivo):
    #Create temp file
    fh, abs_path = mkstemp()
    count = 0
    proximoKtr = False
    proximoKjb = False
    transname = False
    proxDirectoryKTR = False
    proxDirectoryKJB = False
    l1 = []
    l2 = []
    with fdopen(fh,'w',encoding="utf8") as novoArquivo:
        with open(caminhoComArquivo, encoding="utf8") as antigoArquivo:
            print(caminhoComArquivo)
            qLinha = 1
            for linha in antigoArquivo:
                ##########################################################
                if bool(proxDirectoryKTR):
                    if re.search('<directory>', str(linha), re.IGNORECASE):#<directory>
                        #print(linha)
                        linha2 = localizaSubstitui_KTR(str(linha))[1]
                        linha = localizaSubstitui_KTRdir(str(linha), caminhoComArquivo)
                        l1.append(linha2.replace('.ktr',''))
                        proxDirectoryKTR = False
                elif bool(proxDirectoryKJB):
                    if re.search('<directory>', str(linha), re.IGNORECASE):#<directory>
                        #print(linha)
                        linha2 = localizaSubstitui_KTR(str(linha))[1]
                        linha = localizaSubstitui_KTRdir(str(linha), caminhoComArquivo)
                        l1.append(linha2.replace('.kjb',''))
                        proxDirectoryKJB = False
                if bool(transname):
                    #print('transname: ',caminhoComArquivo)
                    if re.search('<transname>', str(linha), re.IGNORECASE):#<transname>
                        linha, linha2 = localizaSubstitui_KTR(str(linha))
                        l1.append(linha2)
                        transname = False
                        proxDirectoryKTR = True
                        count += 1
                        print('V.4 - linha: ' + str(qLinha) + ' --- ' + linha.replace('\n',''))
                    elif re.search('<jobname>', str(linha), re.IGNORECASE):#<jobname>
                        linha, linha2 = localizaSubstitui_KJB(str(linha))
                        l1.append(linha2)
                        transname = False
                        proxDirectoryKJB = True
                        count += 1
                        print('V.4 - linha: ' + str(qLinha) + ' --- ' + linha.replace('\n',''))
                #----------</////////////////////////////////////////////////////////////////////////////////////////
                #----------<filename> para kjb ou ktr
                # passo (2)
                if bool(proximoKtr):
                    #print('filename: ',caminhoComArquivo)
                    if re.search('<filename>', str(linha), re.IGNORECASE): #<filename>
                        linha, linha2 = localizaSubstitui_KTR(str(linha))
                        l1.append(linha2)
                        proximoKtr = False
                        proxDirectoryKTR = False
                        count += 1
                        print('V.7 - linhaKTR: ' + str(qLinha) + ' --- ' + linha.replace('\n',''))
                    else:
                        transname = True
                elif bool(proximoKjb):
                    #print('filename: ',caminhoComArquivo)
                    if re.search('<filename>', str(linha), re.IGNORECASE): #<filename>
                        linha, linha2 = localizaSubstitui_KJB(str(linha))
                        l1.append(linha2)
                        proximoKtr = False
                        proxDirectoryKJB = False
                        count += 1
                        print('V.7 - linhaKJB: ' + str(qLinha) + ' --- ' + linha.replace('\n',''))
                    else:
                        transname = True
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

def localizaSubstitui_KTR(text):
    novoText = ''
    if not re.search('.ktr', text, re.IGNORECASE):
        #print('localizaSubstitui_KTR: ' + str(text))
        novoText = text.split('</')[0] + '.ktr</' + text.split('</')[1]
        return novoText, text.split('</')[0].split('>')[1] + '.ktr'
    else:
        #print("tem: "+ text)
        #listaKtr.append(text.split('</')[0].split('>')[1])
        return text, text.split('</')[0].split('>')[1]

def localizaSubstitui_KJB(text, dirOrigem):
    novoText = ''
    ok = False
    if not re.search('.kjb', text, re.IGNORECASE):
        novoText = text.split('</')[0] + '.kjb</' + text.split('</')[1]
        ok = True
    #teste com / no inicio "/JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
    if novoText.replace('\\','/').split('>')[1][0] == '/':
        if bool(ok) and len(novoText.replace('\\','/').split('/')) == 4 and novoText.replace('\\','/').split('/')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
            novoText = '      <filename>${' + varCaminho + '}/' + novoText.split('</')[0].split('/')[-1] + '</filename>'
            ok = True
        elif not bool(ok) and len(text.replace('\\','/').split('/')) == 4 and text.replace('\\','/').split('/')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
            novoText = '      <filename>${' + varCaminho + '}/' + text.split('</')[0].split('/')[-1] + '</filename>'
            ok = True
    else: #teste sem / no inicio "JUVO_GR_PRD_VWAUT/JUVO_GR_PRD_VWAUT_DIA_1001_PRECASTRO.kjb"
        if bool(ok) and len(novoText.replace('\\','/').split('/')) == 3 and novoText.replace('\\','/').split('/')[0].split('>')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
            novoText = '      <filename>${' + varCaminho + '}/' + novoText.split('</')[0].split('/')[-1] + '</filename>'
            ok = True
        elif not bool(ok) and len(text.replace('\\','/').split('/')) == 3 and text.replace('\\','/').split('/')[0].split('>')[1] == dirOrigem.replace('\\','/').split('/')[-2]:
            novoText = '      <filename>${' + varCaminho + '}/' + text.split('</')[0].split('/')[-1] + '</filename>'
            ok = True
    if bool(ok):
        return novoText, text.split('</')[0].split('>')[1] +'.kjb'
    else:
        return text, text.split('</')[0].split('>')[1] +'.kjb'

def localizaSubstitui_KTRdir(text, dirOrigem):
    novoText = ''
    print("antivo dir: " + text)
    if len(text.split('</')[0].split('>')[1:]) == 1 and text.split('</')[0].split('>')[1:][0] == dirOrigem.split('/')[-2]:
        #print('localizaSubstitui_KTR: ' + str(text))
        novoText = text.split('</')[0].split('>')[0] + '>${' + varCaminho + '}</' + text.split('</')[1]
        print("novo dir: " + novoText)
        return novoText
    else:
        #print("tem: "+ text)
        #listaKtr.append(text.split('</')[0].split('>')[1])
        return text

def insereVariavelDir(dir, text):
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

def acertaDirKtr(lista1):
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

def invertKjb(string):
    lCp = []
    count = 1
    for i in range(len(string.split('/'))):
        inverso = len(string.split('/')) - count
        lCp.append(string.split('/')[inverso])
        count += 1
    return lCp

def invertKtr(lista):
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

def menu_diretorios():
    title('Navegando pelo Menu DIRETORIOS')
    print('Escolha sua opção: ')
    op = str(input('''
        [1] - Criar diretórios
        [2] - Acertar diretório com ${Internal.Entry.Current.Directory}.
        [3] - Acessar diretórios
        [4] - Listar Arquivos
        [5] - Por extenção .ktr (transformação)
        [0] - Retornar/Sair
        Opção: ''')).lower()
    print()

    if op == '0':
        exit(1)

# ------------------------------------------------------------------------------------------- #
    elif op == '5':  # POR EXTENÇÃO KTR
        files = []
        #(v) Lista todos os arquivos .kjb com excessão do diretório pai.
        for i in listar_arquivos(caminhoPAI):
            files.append(i)
        #(v) Junta ma mesma lida acima. Todos os .Kjb da
        for i in listar_subDiretorios(caminhoPAI):
            for arq in listar_arquivos(i):
                files.append(arq)
        for file in files:
            if file[-4:] == '.kjb':
                replace(file)
        """
        l1 = []
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
                    if principal == ktrs:
        """
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
    elif op == '4':  # LISTAR ARQUIVOS
        print(listar_arquivos(caminhoPAI))
        print(os.getcwd())
        menu_diretorios()


# ------------------------------------------------------------------------------------------- #
    else:
        print("Esta opção não está nas alternativas, tente novamente.\n")
        menu_diretorios()


print(menu_diretorios())
#replace('C:/Users/hitma/Desktop/JUVO_GR_PRD_FIAT/1/Nova pasta/Novo Documento de Texto (2).txt', 'a', 'A')
