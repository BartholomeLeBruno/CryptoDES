from Extract_ConstantesDES import recupConstantesDES
from ConvAlphaBin import conv_bin, nib_vnoc

CONSTANTES = recupConstantesDES()
PI = CONSTANTES['PI']
PI_I = CONSTANTES['PI_I']
E = CONSTANTES['E']
CP_1 = CONSTANTES['CP_1']
CP_2 = CONSTANTES['CP_2']
S = CONSTANTES['S'] # {int: [[int]]} 0 à 7
PERM = CONSTANTES['PERM']

def listToString(s): 
    str1 = "" 
    for ele in s: 
        str1 += str(ele)  
    return str1

def XOR(input1,input2):
    xor_result = []
    for i in range(0,len(input1)):
        xor_result.append(int(input1[i])^int(input2[i]))
    return xor_result

def decallageAGauche(tab):
    result = []
    compt = 0
    while compt < len(tab)-1 :
        result.insert(compt,tab[compt+1])
        compt +=1
    result.insert(compt,tab[0])
    return result
 
def dictionnaireDes16Clefs() :
    f = open("Clef_de_1.txt", "r")
    txt = f.read()
    f.close()
 
    clef = dict()
    tab = []
    tab_CP2=[]
    tab_G = []
    tab_D = []
    tab_G_D = []
 
    compt = 0
 
    while compt < len(CP_1[0]) :
        tab.insert(compt,int(txt[CP_1[0][compt]]))
        compt+=1
 
    tab_G = tab[:28]
    tab_D = tab[28:57]
 
    for i in range(0,16):
        tab_D=decallageAGauche(tab_D)
        tab_G=decallageAGauche(tab_G)
        tab_G_D = tab_G + tab_D
        compt = 0
        while compt < len(CP_2[0]) :
            tab_CP2.insert(compt,tab_G_D[CP_2[0][compt]])
            compt+=1
        clef[i]=tab_CP2
        tab_CP2=[]
 
    return clef
 
def decouperPar64(message):
    messageParPaquet = dict()
    msg = []
    i = 0
    j = 0
    compt = 0
    partieDuMessage = 0
 
    while compt < len(message) :
        msg.insert(i,message[compt])
        compt+=1
        i+=1
        if compt%64==0 :
            messageParPaquet[partieDuMessage]=msg
            msg=[]
            partieDuMessage+=1
            i=0
    if compt%64!=0 :
        for i in range(i,64):
            msg.insert(i,0)
        messageParPaquet[partieDuMessage]=msg
 
    return messageParPaquet
 
def permutationInitiale(message):
    result = []
    compt = 0
    while compt < len(PI[0]) :
        result.insert(compt,int(message[PI[0][compt]]))
        compt+=1
   
    return result
 
def permutationInitialeInverse(message):
    result = []
    compt = 0
    while compt < len(PI_I[0]) :
        result.insert(compt,int(message[PI_I[0][compt]]))
        compt+=1
   
    return result
 
def expansion(message):
    result = []
    compt = 0
    while compt < len(E[0]) :
        result.insert(compt,int(message[E[0][compt]]))
        compt+=1
   
    return result
 
def permutationDesRondes(message):
    result = []
    compt = 0
    while compt < len(PERM[0]) :
        result.insert(compt,int(message[PERM[0][compt]]))
        compt+=1
   
    return result
 
def calcule1RondeChiffrement(message,ronde):
    blocDe6Bits = dict()
    blocDe6bitsResult = dict()
    tab_G = []
    tab_D = []
    tabTemp=[]
    compt=0
    paquetDe6=1

    dictClef = dictionnaireDes16Clefs()
    for i in range(0,32):
        tab_G.insert(i,message[i])
        tab_D.insert(i+32,message[i+32])
 
    messageApresExpansion = expansion(tab_D)
    clef = dictClef[ronde]
   
    xor = XOR(clef,messageApresExpansion)
 
    for i in range(0,48):
        tabTemp.insert(compt,xor[i])
        compt+=1
        if compt%6 == 0:
            blocDe6Bits[paquetDe6]=tabTemp
            tabTemp=[]
            paquetDe6+=1
            compt=0
   
    i=1
    while i <= 8:
        x = int(str(blocDe6Bits[i][0])+str(blocDe6Bits[i][5]),2)
        y = int(str(blocDe6Bits[i][1])+str(blocDe6Bits[i][2])+str(blocDe6Bits[i][3])+str(blocDe6Bits[i][4]),2)
       
        longueur = len(bin(S[i-1][x][y])[2:])
        if longueur == 1 :
            blocDe6bitsResult[i] = '000' + bin(S[i-1][x][y])[2:]
        elif longueur == 2 :
            blocDe6bitsResult[i] = '00' + bin(S[i-1][x][y])[2:]
        elif longueur == 3 :
            blocDe6bitsResult[i] = '0' + bin(S[i-1][x][y])[2:]
        else :
            blocDe6bitsResult[i] = bin(S[i-1][x][y])[2:]
        i+=1
 
    concatBlocDe6Bits = blocDe6bitsResult[1] +blocDe6bitsResult[2] +blocDe6bitsResult[3] +blocDe6bitsResult[4] +blocDe6bitsResult[5] +blocDe6bitsResult[6] +blocDe6bitsResult[7] +blocDe6bitsResult[8]
    messageApresPermutationRondes = permutationDesRondes(concatBlocDe6Bits)
    xor = XOR(messageApresPermutationRondes,tab_G)
    tab_G = tab_D
    tab_D = xor
 
    return tab_G+tab_D
 
def calcule16RondesChiffrement(message):

    message = permutationInitiale(message)
    for i in range (0,16):
        message = calcule1RondeChiffrement(message,i)
   
    return message
 
def chiffrer(message):
   
    blocsDe64Bits = decouperPar64(message)
    messageChiffrer=[]
 
    for i in range (0,len(blocsDe64Bits)):
        resultatDes16Rondes = calcule16RondesChiffrement(blocsDe64Bits[i])
        messageChiffrer +=permutationInitialeInverse(resultatDes16Rondes)
 
    return messageChiffrer
 
def calcule1RondeDechiffrement(message,ronde):
    tab_G = []
    tab_D = []
    blocDe6bitsResult = dict()
    blocDe6Bits = dict()

    dictClef = dictionnaireDes16Clefs()
    for i in range(0,32):
        tab_G.insert(i,message[i])
        tab_D.insert(i+32,message[i+32])
 
    messageApresExpansion = expansion(tab_G)
    clef = dictClef[ronde]

    xor=XOR(clef,messageApresExpansion) 
    tabTemp=[]
    compt=0
    paquetDe6=1
 
    for i in range(0,48):
        tabTemp.insert(compt,xor[i])
        compt+=1
 
        if compt%6 == 0:
            blocDe6Bits[paquetDe6]=tabTemp
            tabTemp=[]
            paquetDe6+=1
            compt=0
 
    i=1
    while i <= 8:
        x = int(str(blocDe6Bits[i][0])+str(blocDe6Bits[i][5]),2)
        y = int(str(blocDe6Bits[i][1])+str(blocDe6Bits[i][2])+str(blocDe6Bits[i][3])+str(blocDe6Bits[i][4]),2)
       
        longueur = len(bin(S[i-1][x][y])[2:])
        if longueur == 1 :
            blocDe6bitsResult[i] = '000' + bin(S[i-1][x][y])[2:]
        elif longueur == 2 :
            blocDe6bitsResult[i] = '00' + bin(S[i-1][x][y])[2:]
        elif longueur == 3 :
            blocDe6bitsResult[i] = '0' + bin(S[i-1][x][y])[2:]
        else :
            blocDe6bitsResult[i] = bin(S[i-1][x][y])[2:]
        i+=1
 
    concatBlocDe6Bits = blocDe6bitsResult[1] +blocDe6bitsResult[2] +blocDe6bitsResult[3] +blocDe6bitsResult[4] +blocDe6bitsResult[5] +blocDe6bitsResult[6] +blocDe6bitsResult[7] +blocDe6bitsResult[8]
    messageApresPermutationRondes = permutationDesRondes(concatBlocDe6Bits)
    xor = XOR(messageApresPermutationRondes,tab_D)
    tab_D = tab_G
    tab_G = xor

    return tab_G+tab_D
 
def calcule16RondesDechiffrement(message):

    message = permutationInitiale(message)
    for i in range (0,16):
        message = calcule1RondeDechiffrement(message,15-i)

    return message
 
def dechiffrer(message):
   
    blocsDe64Bits = decouperPar64(message)
    messageDechiffrer=[]
 
    for i in range (0,len(blocsDe64Bits)):
        resultatDes16Rondes = calcule16RondesDechiffrement(blocsDe64Bits[i])
        messageDechiffrer +=permutationInitialeInverse(resultatDes16Rondes)
   
    return messageDechiffrer
 
 
f = open("Chiffrement_DES_de_1.txt", "r")
txt = f.read()
f.close()
 
#txt_binaire = conv_bin(txt)
#txt_binaire_chiffre = déchiffrer(txt_binaire)
print(dechiffrer("1000100000110110101000010001001111001011011000001001010010010000"))
print(chiffrer("1101110010111011110001001101010111100110111101111100001000110010"))

#txt_binaire_chiffre=map(str,txt_binaire_chiffre)
#txtt=''.join(str(a) for a in  txt_binaire_chiffre)
#print(nib_vnoc(txtt))