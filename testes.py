from itertools import permutations
import sys

def findPermutation(wrd):
    """ Encontre a permutação das palavras """
    parmutationList = permutations(wrd)
    for item in parmutationList:
        print(''.join(item))

def checkWord(wrd, wordLine):
    """ Verifica se a palavra existe no arquivo ou não """
    for line in wordLine:
            if re.search('trans_object_id' + re.escape(wrd) + 'teste', line, flags=re.IGNORECASE):
                findPermutation(wrd)
                return

    print('This word is not available')


def main():
    """ Main function """
    word = ''
    with open('C:/Users/hitma/Desktop/JUVO_GR_PRD_FIAT/1/Nova pasta/Novo Documento de Texto (2).txt', 'r+') as f:
    #word = sys.argv[1].upper()
        word = f.read()
        checkWord(word, f)
        f.close()

if __name__ == '__main__':
    main()
