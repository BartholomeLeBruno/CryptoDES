from Extract_ConstantesDES import recupConstantesDES
from ConvAlphaBin import conv_bin, nib_vnoc
from sys import argv, exc_info

CONSTANTES = recupConstantesDES()

PI = CONSTANTES['PI']
PI_I = CONSTANTES['PI_I']
E = CONSTANTES['E']
CP_1 = CONSTANTES['CP_1']
CP_2 = CONSTANTES['CP_2']
S = CONSTANTES['S']
PERM = CONSTANTES['PERM']

def remplacerParValeurDeS(blocDe6Bits):
    blocDe6bitsResult = dict()
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
 
    return blocDe6bitsResult[1] +blocDe6bitsResult[2] +blocDe6bitsResult[3] +blocDe6bitsResult[4] +blocDe6bitsResult[5] +blocDe6bitsResult[6] +blocDe6bitsResult[7] +blocDe6bitsResult[8]
    
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
 
def dictionnaireDes16Clefs(clef) :

    clefs = dict()
    tab = []
    tab_CP2=[]
    tab_G = []
    tab_D = []
    tab_G_D = []
 
    compt = 0
 
    while compt < len(CP_1[0]) :
        tab.insert(compt,int(clef[CP_1[0][compt]]))
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
        clefs[i]=tab_CP2
        tab_CP2=[]
 
    return clefs
 
def decouperPar64(message):
    messageParPaquet = dict()
    msg = []
    i = 0
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
 
def calcule1RondeChiffrement(message,ronde,clef):
    blocDe6Bits = dict()
    tabTemp=[]
    compt=0
    paquetDe6=1

    dictClef = dictionnaireDes16Clefs(clef)
    tab_G,tab_D = message[:32], message[32:]
 
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
   
    concatBlocDe6Bits = remplacerParValeurDeS(blocDe6Bits)
    messageApresPermutationRondes = permutationDesRondes(concatBlocDe6Bits)
    xor = XOR(messageApresPermutationRondes,tab_G)
    tab_G = tab_D
    tab_D = xor
 
    return tab_G+tab_D
 
def calcule16RondesChiffrement(message,clef):

    message = permutationInitiale(message)
    for i in range (0,16):
        message = calcule1RondeChiffrement(message,i,clef)
   
    return message
 
def chiffrer(message,clef):
   
    blocsDe64Bits = decouperPar64(message)
    messageChiffrer=[]
 
    for i in range (0,len(blocsDe64Bits)):
        resultatDes16Rondes = calcule16RondesChiffrement(blocsDe64Bits[i],clef)
        messageChiffrer +=permutationInitialeInverse(resultatDes16Rondes)
 
    messageChiffrer=map(str,messageChiffrer)
    result=''.join(str(a) for a in  messageChiffrer)
    return nib_vnoc(result)
 
def calcule1RondeDechiffrement(message,ronde,clef):
    blocDe6Bits = dict()
    dictClef = dictionnaireDes16Clefs(clef)
    tab_G,tab_D = message[:32], message[32:]
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
 
    concatBlocDe6Bits = remplacerParValeurDeS(blocDe6Bits)
    messageApresPermutationRondes = permutationDesRondes(concatBlocDe6Bits)
    xor = XOR(messageApresPermutationRondes,tab_D)
    tab_D = tab_G
    tab_G = xor

    return tab_G+tab_D
 
def calcule16RondesDechiffrement(message,clef):

    message = permutationInitiale(message)
    for i in range (0,16):
        message = calcule1RondeDechiffrement(message,15-i,clef)

    return message
 
def dechiffrer(message,clef):
   
    blocsDe64Bits = decouperPar64(message)
    messageDechiffrer=[]
 
    for i in range (0,len(blocsDe64Bits)):
        resultatDes16Rondes = calcule16RondesDechiffrement(blocsDe64Bits[i],clef)
        messageDechiffrer +=permutationInitialeInverse(resultatDes16Rondes)
   
    messageDechiffrer=map(str,messageDechiffrer)
    result=''.join(str(a) for a in  messageDechiffrer)
    return nib_vnoc(result)
 
if __name__ == '__main__':

    if len(argv) < 4:
        print("\n\nle format de votre commande n'est pas correct \n python votreFichierADechiffrerOuAChiffrer votreClef leMotCleChiffrerOuDechiffrer \n\n")
        exit(1)

    f = open(argv[1], "r")
    txt = f.read()
    f.close()
    txt_binaire = conv_bin(txt)

    f = open(argv[2], "r")
    clef = f.read()
    f.close()

    if argv[3] == 'chiffrer':
        print(chiffrer(txt_binaire, clef))
    elif argv[3] == 'dechiffrer':
        print(dechiffrer(txt_binaire, clef))
    else : 
        print("\n\nveuillez taper 'chiffrer' ou 'dechiffrer' à la place de ",argv[3],"\n\n")
        exit(1)
