from random import randint
from random import random
Mutacao=0.01
CrossOver=0.6
NumGeracoes=5
Individuos=4
Populacao=[]


def gerar_populacao():
    for i in range(Individuos):
        linha=[1,1,1,1,1]
        while(conversor(linha)<-10 or conversor(linha)>10):
            for j in range(5):
                linha[j]=randint(0,1)
        Populacao.append(linha)

def conversor(aux):
    soma=0
    for i in range(4):
        soma+=aux[i+1]*(2**(3-i))
    if(aux[0]==1):
        soma=-soma
    return soma
    
def funcao(aux):
    x=conversor(aux)
    return ((x**2)-(3*x)+4)

def melhor_individuo(aux):
    melhor=aux[0]
    menor_valor=funcao(aux[0])
    for i in range(Individuos-1):
        if(funcao(aux[i+1])<menor_valor):
            melhor=aux[i+1]
            menor_valor=funcao(aux[i+1])
    return melhor

def torneio(aux):
    sel1=aux[randint(0,3)]
    sel2=aux[randint(0,3)]
    if(funcao(sel1)<funcao(sel2)):
        return sel1
    else:
        return sel2

def crossover(aux):
    if (random()<=CrossOver):
        aux2=[]
        corte1=randint(1,4)
        corte2=randint(1,4)
        pai1=torneio(aux)
        pai2=torneio(aux)
        aux2.append(pai1[:corte1]+pai2[corte1:])
        aux2.append(pai1[corte1:]+pai2[:corte1])
        aux2.append(pai1[:corte2]+pai2[corte2:])
        aux2.append(pai1[corte2:]+pai2[:corte2])
        return aux2
    else:
        return aux

def elitismo(aux,melhor):
    pior_valor=funcao(aux[0])
    pior=0
    for i in range(Individuos):
        if(pior_valor<funcao(aux[i])):
           pior=i
           pior_valor=funcao(aux[i])
    aux[pior]=melhor
    return aux

def mutacao(aux):
    aux2=aux
    for i in range(len(Populacao[0])-1):
        if(random()<=Mutacao):
            aux2[i]=abs(aux[i]-1)
    return aux

def algoritmo(aux):
    n=0
    gerar_populacao()
    print("População inicial")
    print(aux)
    decimais=[]
    for i in range(Individuos):
        decimais.append(conversor(aux[i]))
    print(decimais)
    while(n<NumGeracoes):
        melhor=melhor_individuo(aux)
        aux=crossover(aux)
        for i in range(Individuos):
            aux[i]=mutacao(aux[i])
        aux=elitismo(aux,melhor)
        print()
        print(n+1,"Geração")
        print(aux)
        decimais=[]
        for i in range(Individuos):
            decimais.append(conversor(aux[i]))
        print(decimais)
        n+=1

algoritmo(Populacao)
