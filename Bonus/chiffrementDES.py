from Extract_ConstantesDES import recupConstantesDES

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

    sdl = '\n'

    X = dict()
    clef = dict()
    tab = []
    tab_CP2=[]
    tab_G = []
    tab_D = []
    tab_G_D = []
    X=recupConstantesDES()

    CP_1 = X["CP_1"]
    CP_2 = X["CP_2"]

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
        if(compt%64==0):
            messageParPaquet[partieDuMessage]=msg
            msg=[]
            partieDuMessage+=1
            i=0
    
    for i in range(i,64):
        msg.insert(i,0)
    
    messageParPaquet[partieDuMessage]=msg

    return messageParPaquet

def permutationInitiale(message):
    X = dict()
    result = []
    X=recupConstantesDES()

    PI = X["PI"]
    compt = 0

    while compt < len(PI[0]) :
        result.insert(compt,int(message[PI[0][compt]]))
        compt+=1
    
    return result

def permutationInitialeInverse(message):
    X = dict()
    result = []
    X=recupConstantesDES()

    PI_I = X["PI_I"]
    compt = 0

    while compt < len(PI_I[0]) :
        result.insert(compt,int(message[PI_I[0][compt]]))
        compt+=1
    
    return result

def expansion(message):
    X = dict()
    result = []
    X=recupConstantesDES()

    E = X["E"]
    compt = 0

    while compt < len(E[0]) :
        result.insert(compt,int(message[E[0][compt]]))
        compt+=1
    
    return result

def permutationDesRondes(message):
    X = dict()
    result = []
    X=recupConstantesDES()

    PERM = X["PERM"]
    compt = 0

    while compt < len(PERM[0]) :
        result.insert(compt,int(message[PERM[0][compt]]))
        compt+=1
    
    return result


def chiffrer(message):
    i=0
    xor=[]
    tab_G = []
    tab_D = []
    
    X = dict()
    X=recupConstantesDES()

    dictClef = dictionnaireDes16Clefs()
    messageApresPI = permutationInitiale(message)

    for i in range(0,32):
        tab_G.insert(i,messageApresPI[i])
        tab_D.insert(i+32,messageApresPI[i+32])
    
    messageApresExpansion = expansion(tab_D)
    clef = dictClef[0]

    print(messageApresExpansion)
    print(clef)
    
    for i in range(0,48):
        if clef[i] == messageApresExpansion[i] : 
            xor.insert(i,0)
        else :
            xor.insert(i,1)
    
    print(xor)


    blocDe6Bits = dict()
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
        
    print(blocDe6Bits)

    blocDe6bitsResult = dict()

    i=1
    while i <= 8:
        x = int(str(blocDe6Bits[i][0])+str(blocDe6Bits[i][5]),2)
        y = int(str(blocDe6Bits[i][1])+str(blocDe6Bits[i][2])+str(blocDe6Bits[i][3])+str(blocDe6Bits[i][4]),2)
        
        longueur = len(bin(X["S"][i-1][x][y])[2:])
        if longueur == 1 :
            blocDe6bitsResult[i] = '000' + bin(X["S"][i-1][x][y])[2:]
        elif longueur == 2 :
            blocDe6bitsResult[i] = '00' + bin(X["S"][i-1][x][y])[2:]
        elif longueur == 3 :
            blocDe6bitsResult[i] = '0' + bin(X["S"][i-1][x][y])[2:]
        else : 
            blocDe6bitsResult[i] = bin(X["S"][i-1][x][y])[2:]
        i+=1

    print(blocDe6bitsResult)

    concatBlocDe6Bits = blocDe6bitsResult[1] +blocDe6bitsResult[2] +blocDe6bitsResult[3] +blocDe6bitsResult[4] +blocDe6bitsResult[5] +blocDe6bitsResult[6] +blocDe6bitsResult[7] +blocDe6bitsResult[8]
    print(concatBlocDe6Bits)
    
    messageApresPermutationRondes = permutationDesRondes(concatBlocDe6Bits)
    print(messageApresPermutationRondes)


    xor = []

    for i in range(0,32):
        if messageApresPermutationRondes[i] == tab_G[i] : 
            xor.insert(i,0)
        else :
            xor.insert(i,1)

    print(xor)
    
    tab_G = tab_D
    tab_D = xor

    print(tab_D)
    print(tab_G) 


print(chiffrer("1101110010111011110001001101010111100110111101111100001000110010"))

