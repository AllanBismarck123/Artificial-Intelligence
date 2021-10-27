from random import randint
from random import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as mp
from matplotlib import cm
import numpy as np
import imageio
import matplotlib.patches as mpatches

MAX_POPULACAO = 100 #NÚMERO DE INDIVÍDUOS DA POPULACAO
max_iter = 100 #NÚMERO MÁXIMO DE ITERAÇÕES
VALOR_MINIMO = -100 #VALOR MÍNIMO PARA X, Y OU Z
VALOR_MAXIMO = 100 #VALOR MÁXIMO PARA X, Y OU Z
INERCIA =0.8    #VARIA DE 0.4 À 1.4
MELHOR_POSICAO_GLOBAL = [] #VARIÁVEL QUE SERÁ USADA PARA GUARDAR A MELHOR POSIÇÃO GLOBAL.
R1 = 0.5
R2 = 0.8
#R1 E R2 SÃO VARIÁVEIS ALEATÓRIAS QUE ASSUMEM VALORES ENTRE 0 E 1, É DO PRÓPRIO ALGORITMO.
C1 = 1 #GRAU DE CONFIANÇA DA MELHOR POSIÇÃO LOCAL DE CADA PARTÍCULA.
C2 = 2 #GRAU DE CONFIANÇA DA MELHOR POSIÇÃO GLOBAL(A MELHOR POSIÇÃO ENTRE TODAS DO ENXAME).
#COSTUMAM VARIAR DE 0 A 4.
figuras = []

def funcao(ponto):
    x=ponto[0]
    y=ponto[1]
    ponto[2]=(round(x**2 + y**2 + 5,3))
    return ponto[2]

class particula:
    def __init__(self):
        #INICIALIZA A POSIÇÃO ATUAL DE CADA PARTÍCULA
        self.pos_atual=[randint(VALOR_MINIMO,VALOR_MAXIMO),randint(VALOR_MINIMO,VALOR_MAXIMO),randint(VALOR_MINIMO,VALOR_MAXIMO)]
        #INICIALIZA A VELOCIDADE ATUAL DE CADA PARTÍCULA
        self.vel_atual=[randint(VALOR_MINIMO,VALOR_MAXIMO),randint(VALOR_MINIMO,VALOR_MAXIMO),randint(VALOR_MINIMO,VALOR_MAXIMO)]
        self.melhor_pos_local=self.pos_atual #INICIALIZA A MELHOR POSIÇÃO LOCAL COMO A POSIÇÃO ATUAL
    
    def atualizar_velocidade(self,MELHOR_POSICAO_GLOBAL):
        aux1 = [0]*3
        aux2 = [0]*3
        aux3 = [0]*3
        for i in range(3):
            #Essa função round é só para arrendondar os valores para 3 casas decimais
            aux1[i]=(round(INERCIA*self.vel_atual[i],3))
            aux2[i]=(round(C1*R1*(self.melhor_pos_local[i]-self.pos_atual[i]),3))
            aux3[i]=(round(C2*R2*(MELHOR_POSICAO_GLOBAL[i]-self.pos_atual[i]),3))
        for j in range(3):
            #Cálculo da velocidade no próximo instante.
            self.vel_atual[j]=round(aux1[j]+aux2[j]+aux3[j],3)
            if(self.vel_atual[j]>1):
                self.vel_atual[j]=1
            if(self.vel_atual[j]<-1):
                self.vel_atual[j]=-1
    
    def atualizar_posicao(self):
        for i in range(3):
            #Cálculo da posição no próximo instante.
            self.pos_atual[i]=round(self.pos_atual[i]+self.vel_atual[i],3)
            #limita as coordenadas X e Y, pois Z vai ser usado para ver os resultados, já que F(X,Y)=Z
            if(self.pos_atual[i]>VALOR_MAXIMO and i!=2): 
                self.pos_atual[i]=VALOR_MAXIMO
            if(self.pos_atual[i]<VALOR_MINIMO and i!=2):
                self.pos_atual[i]=VALOR_MINIMO
            
def PSO():
    swarm=[]
    for i in range(MAX_POPULACAO):# gera uma populacao de particulas
        swarm.append(particula())
    MELHOR_POSICAO_GLOBAL=swarm[0].pos_atual
    for i in range(3):
        MELHOR_POSICAO_GLOBAL[i]=round(MELHOR_POSICAO_GLOBAL[i])
    k=0
    while k<max_iter:
        fig = mp.figure()
        ax = fig.add_subplot(111,projection = '3d')
        X1 = np.arange(-100, 100, 0.5)
        Y1 = np.arange(-100, 100, 0.5)
        X1, Y1 = np.meshgrid(X1, Y1)
        Z1 = X1**2 + Y1**2 + 5
        ax.plot_wireframe(X1, Y1, Z1, rstride = 10,cstride = 10,color = 'green')
        red_patch = mpatches.Patch(color='black', label='Partículas')
        global_patch = mpatches.Patch(color='yellow', label='Global')
        ax.legend(handles=[red_patch,global_patch])
        for i in range(MAX_POPULACAO):
            ax.set_title(str(k)+' Gerações',loc='right')
            ax.scatter(swarm[i].pos_atual[0],swarm[i].pos_atual[1],swarm[i].pos_atual[2],c='black')
            #Verificação para atualização da melhor posição local da partícula
            if funcao(swarm[i].pos_atual)>=funcao(swarm[i].melhor_pos_local):
                swarm[i].melhor_pos_local=swarm[i].pos_atual
            #Verificação para atualização da melhor posição global(enxame)
            if funcao(swarm[i].pos_atual)>=funcao(MELHOR_POSICAO_GLOBAL):
                MELHOR_POSICAO_GLOBAL=swarm[i].pos_atual
            swarm[i].atualizar_velocidade(MELHOR_POSICAO_GLOBAL)
            swarm[i].atualizar_posicao()
        ax.scatter(MELHOR_POSICAO_GLOBAL[0],MELHOR_POSICAO_GLOBAL[1],MELHOR_POSICAO_GLOBAL[2],c='yellow')
        mp.savefig(str(i)+'.png')
        figuras.append(imageio.imread(str(i)+'.png'))
        k+=1
        print(MELHOR_POSICAO_GLOBAL)
    imageio.mimsave('PSO.gif', figuras)

print('Global')
#Chamada do algoritmo
PSO()




