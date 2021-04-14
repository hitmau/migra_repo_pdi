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

caminhoInp = str(input('Diretório: '))
caminhoPAI = caminhoInp.replace('\\', '/')
varCaminho = "${Internal.Entry.Current.Directory}"
#caminhoPAI = 'C:/Users/hitma/Desktop/JUVO_GR_PRD_FIAT'
#caminhoPAI = "C:\Users\hitma\Desktop\ETLAS012 - Telefonia"
campoDeBusca = '<trans_object_id'
campoDeBusca2 = '<filename>'
campoDeBusca3 = '<transname>'
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
    proximo = False
    proxdir = False
    l1 = []
    l2 = []
    with fdopen(fh,'w',encoding="utf8") as novoArquivo:
        with open(caminhoComArquivo, encoding="utf8") as antigoArquivo:
            for linha in antigoArquivo:
                ##########################################################
                if bool(proxdir):
                    #print('transname: ',caminhoComArquivo)
                    if re.search(campoDeBusca3, str(linha), re.IGNORECASE):#<transname>
                        linha, linha2 = localizaSubstitui_KTR(str(linha))
                        l1.append(linha2)
                        proxdir = False
                        count += 1
                if bool(proximo):
                    #print('filename: ',caminhoComArquivo)
                    if re.search(campoDeBusca2, str(linha), re.IGNORECASE): #<filename>
                        linha, linha2 = localizaSubstitui_KTR(str(linha))
                        l1.append(linha2)
                        proximo = False
                        count += 1
                    else:
                        proxdir = True
                if not bool(proximo):
                    if re.search(campoDeBusca, str(linha), re.IGNORECASE):#<trans_object_id>
                        proximo = True
                else:
                    proximo = False
                novoArquivo.write(linha)
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
        print('localizaSubstitui_KTR: ' + str(text))
        novoText = text.split('</')[0] + '.ktr</' + text.split('</')[1]
        return novoText, text.split('</')[0].split('>')[1] + '.ktr'
    else:
        #print("tem: "+ text)
        #listaKtr.append(text.split('</')[0].split('>')[1])
        return text, text.split('</')[0].split('>')[1]

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

    elif op == '5':  # POR EXTENÇÃO KTR
        files = []
        for i in listar_arquivos(caminhoPAI):
            files.append(i)
        for i in listar_subDiretorios(caminhoPAI):
            for arq in listar_arquivos(i):
                files.append(arq)
        for file in files:
            if file[-4:] == '.kjb':
                replace(file)
        #A = remove_repetidos(listaKtr)
        for i in sorted(listaKtr): print(i)

# ------------------------------------------------------------------------------------------- #
    else:
        print("Esta opção não está nas alternativas, tente novamente.\n")
        menu_diretorios()


print(menu_diretorios())
#replace('C:/Users/hitma/Desktop/JUVO_GR_PRD_FIAT/1/Nova pasta/Novo Documento de Texto (2).txt', 'a', 'A')
