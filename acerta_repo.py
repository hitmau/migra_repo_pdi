# -*- coding:utf-8 -*-
import os, re
import os.path
import shutil

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
                print('\t', entry.name)

def listar_subDiretorios(caminho):
    subfolders = [f.path for f in os.scandir(caminho) if f.is_dir()]
    for caminho in list(subfolders):
        subfolders.extend(listar_subDiretorios(caminho))
        subfolders.sort()
    return subfolders

def listar_arquivos(caminho):
    arquivos = []
    with os.scandir(caminho) as it:
        for entrar in it:
            if not entrar.name.startswith('.') and entrar.is_file():
                #if entrar.name[-4:] == '.kjb' or entrar.name[-4:] == '.txt':
                #print('\t', entrar.name)
                arquivos.append(entrar.name)
    return(arquivos)


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
        print(files)
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


print(menu_diretorios())
