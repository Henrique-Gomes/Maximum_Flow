import networkx as nx
import numpy as np

# retorna um vetor onde, para cada vertice, é somado todas as entradas
# e todas as saídas e armazenado o menor desses 2 valores
def vetor(M,orig,dest):
	vet = []
	for i in range(0,len(M)):
		entrada = 0
		saida = 0
		for j in range(0,len(M)):
			saida += M[i][j]
		for j in range(0,len(M)):
			entrada += M[j][i]

		if i==orig: 	#origem pode não ter entradas 
			vet.append(saida)	
		elif i==dest:	# destino pode não ter saídas
			vet.append(entrada)
		else:
			vet.append(min(entrada,saida)) 
	return vet

# retorna uma lista de tuplas que representam os caminhos
# o primeiro valor de cada tupla é o fluxo daquele caminho
# o segundo valor de cada tupla é uma lista com o trajeto
def fluxoMaximo(M,orig,dest):
	#armazena a lista de tuplas
	list = []
	conexo = True
	while(conexo):
		vet = vetor(M,orig,dest)
		# vertice com menor fluxo
		menor = 0
		# será setado como true novamente assim que for encontrado um caminho
		conexo = False
		# encontra o menor
		for i in range(1,len(M)-1):
			if (vet[i]>0 and vet[orig]>0 and vet[dest]>0):
				conexo = True
				# isso acima não é bem verdade, mas é porque quando um vertice não 
				# tem ligação o algoritmo automaticamente zera o fluxo dele
				# logo, se o vertice não tem fluxo zero, então o algoritmo ainda não
				# o descartou
			if ((vet[menor] > vet[i]) and (vet[i] > 0)):
				menor = i

		tem_caminho = True #tem caminho entre a origem e o menor, e entre o menor e o destino?

		while(tem_caminho):
			G = nx.from_numpy_matrix(M, create_using=nx.DiGraph())

			try:
				cam1 = nx.dijkstra_path(G, orig, menor) # origem ao vertice escolhido
				cam2 = nx.dijkstra_path(G, menor, dest) # vertice escolhido ao destino

				# se não deu exceção, então houve caminho
				tem_caminho = True		
			except:
				# se deu exceção, em tese, foi porque não houveram caminhos
				tem_caminho = False
				# zera este vértice para que ele não incomode mais
				for i in range(0,len(M)):
					M[i][menor] = 0 # zera entradas
					M[menor][i] = 0 # zera saidas

			if (tem_caminho):
				# cam é o caminho completo. elimina a reptição do vértice escolhido em cam1+cam2
				cam = (cam1+cam2[1::])
				# qual a menor aresta do caminho?
				menor_aresta = M[cam[0]][cam[1]]
				for i in range(0,len(cam)-1):
					if menor_aresta > M[cam[i]][cam[i+1]]:
						menor_aresta = M[cam[i]][cam[i+1]]

				# subtrai a menor aresta de cada aresta do caminho. Menor aresta zera
				for i in range(0,len(cam)-1):
					M[cam[i]][cam[i+1]] -= menor_aresta

				list.append((menor_aresta,cam))

	return list

"""M = np.array([[0, 8, 0, 0, 0, 0, 8, 0],
	          [0, 0, 3, 5, 0, 0, 0, 0],
	          [0, 0, 0, 0, 4, 0, 0, 4],
	          [0, 0, 0, 0, 4, 0, 0, 4],
	          [0, 0, 0, 0, 0, 8, 0, 0],
	          [0, 0, 0, 0, 0, 0, 0, 0],
	          [0, 0, 4, 4, 0, 0, 0, 0],
	          [0, 0, 0, 0, 0, 8, 0, 0]])"""

M = np.array([[ 0, 15, 20, 10,  0,  0,  0],
	          [ 0,  0,  0,  0,  2,  3,  0],
	          [ 0,  0,  0,  0,  4,  5, 15],
	          [ 0,  0,  0,  0,  5,  4,  0],
	          [ 0,  0,  0,  0,  0,  0, 15],
	          [ 0,  0,  0,  0,  0,  0, 10],
	          [ 0,  0,  0,  0,  0,  0,  0]])

teste = fluxoMaximo(M,0,6)
soma = 0
for i in range(0,len(teste)):
	soma += teste[i][0]
	print(str(teste[i][0])+"\t"+str(teste[i][1]))

print("\nFluxo máximo: "+str(soma))


input("\nenter para sair")