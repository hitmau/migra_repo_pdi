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

caminhoPAI = 'C:/Users/hitma/Desktop/JUVO_GR_PRD_FIAT'

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
def replace(caminhoComArquivo, textoAntigo, textoNovo):
    #Create temp file
    fh, abs_path = mkstemp()
    count = 1
    with fdopen(fh,'w') as novoArquivo:
        with open(caminhoComArquivo) as antigoArquivo:
            for linha in antigoArquivo:
                #if linha.lower() == '<trans_object_id/>':
                #linha = linha.encode('utf8')
                print(str(count) + ' ----------' + str(linha))
                if re.search(str(linha.replace(' ','')), 'trans_object_id', re.IGNORECASE):
                    print(str(count) + ' ----------' + linha)
                    #count += 1
                    #novoArquivo.write(linha.replace(textoAntigo, textoNovo))
    #Copy the file permissions from the old file to the new file
    #copymode(caminhoComArquivo, abs_path)
    #Remove original file
    #remove(caminhoComArquivo)
    #Move new file
    #move(abs_path, caminhoComArquivo)

def menu_diretorios():
    title('Navegando pelo Menu DIRETORIOS')
    print('Escolha sua opção: ')
    op = str(input('''
        [1] - Criar diretórios
        [2] - Apagar diretórios
        [3] - Acessar diretórios
        [4] - Listar Arquivos
        [5] - Por extenção .ktr (transformação)
        [0] - Retornar/Sair
        Opção: ''')).lower()
    print()

    if op == '0':
        exit(1)

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
        #listar_subDiretorios(listar_arquivos(caminhoPAI))
        #subfolders = [f.path for f in os.scandir(caminho) if f.is_dir()]
        #files = listar_arquivos(caminhoPAI)
        for i in listar_subDiretorios(caminhoPAI):
            #print(i)
            for arq in listar_arquivos(i):
                files.append(arq)
            #files.append(i)
        #print(files)
        #for i in files: print(i)
        for file in files:
            if file[-4:] == '.txt':
                os.chdir(file)
                Filelist = os.listdir()
                print('File list: ',Filelist)

                NomeFile = input ("Insert file name: ")

                CarOr = input ("Text to search: ")

                CarNew = input ("New text: ")

        #if re.search(texto1.lower(), texto2.lower(), re.IGNORECASE):
        #files.pop(-1)
        #for i in files: print(i)
        #print(str(listar_subDiretorios(caminhoPAI)))
        #for i in range(len(listar_subDiretorios(caminhoPAI))):
        #    print(str(i)+ '- ' + listar_subDiretorios(caminhoPAI)[i])
# ------------------------------------------------------------------------------------------- #
    else:
        print("Esta opção não está nas alternativas, tente novamente.\n")
        menu_diretorios()


#print(menu_diretorios())
replace('C:/Users/hitma/Desktop/JUVO_GR_PRD_FIAT/1/Nova pasta/Novo Documento de Texto (2).txt', 'a', 'A')
