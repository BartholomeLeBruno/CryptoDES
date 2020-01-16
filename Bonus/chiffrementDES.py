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
    
    messageParPaquet[partieDuMessage+1]=msg

    return messageParPaquet


def permutationInitiale(message):
    X = dict()
    result = []
    X=recupConstantesDES()

    CP_1 = X["PI"]
    compt = 0

    while compt < len(CP_1[0]) :
        result.insert(compt,int(message[CP_1[0][compt]]))
        compt+=1
    
    return result

        


print(decouperPar64("messsageesttroplongilfautlediviserenplusieurspaquetde64bitspourpouvoirlechiffrernormalementabcdefghijklmnopqrstuvwxyzabcdefghijklmn"))
print(permutationInitiale("1101110010111011110001001101010111100110111101111100001000110010"))

