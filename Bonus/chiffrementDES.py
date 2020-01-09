from Extract_ConstantesDES import recupConstantesDES


f = open("Clef_de_1.txt", "r")
txt = f.read()
f.close()

sdl = '\n'

X = dict()
tab = []
tab_G = []
tab_D = []

X=recupConstantesDES()
PI = X["PI"]

compt = 0

while compt < len(PI[0]) :
    if (compt + 1 % 8) != 0 : 
        tab.insert(compt,int(txt[PI[0][compt]]))
        compt+=1

print("taille" , len(tab))
print("tab" , tab)

#tab_G = tab.columns[0:]



