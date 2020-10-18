#!python3

import numpy as np
import heapq
import math
import time
import sys



#
 #	~ Trabalho Prático 1: Busca ~
 #
 #	Grupo:
 #		Marcelo Duchêne (Nº USP 8596351)
 #		Matheus Carvalho Raimundo (Nº USP 10369014)
 #		Michelle Wingter da Silva (Nº USP 10783243)
 #
 #	Inteligência Artificial: SCC-0230 2020.2
 #
 #	 _______ _______ _______
 #	|   |   |               \
 #	|   |   |      \    |___|
 #	|   |    \      |   |
 #	|_______ _______|___|
 #
#



CHAR_PATH = "@" # Caractere usado para representar um caminho encontrado.
VISUAL_POINTS_MAX = 30 # Tamanho máximo para ser considerado "grande demais" no número de pontos.
VISUAL_ROW_MAX = 30 # Tamanho máximo para ser considerado "grande demais" no número de linhas.
VISUAL_COL_MAX = 30 # Tamanho máximo para ser considerado "grande demais" no número de colunas.



def introducao():
	### Essa função introduz o programa ao usuário. ###
	print("Bem-vinde ao nosso trabalho!")
	print("Funciona da seguinte maneira:")
	print("- Você vai passar como entrada um labirinto, da maneira como proposto na especificação do trabalho.")
	print("- Em seguida todos os algoritmos irão executar.")
	print("- Ao final da execução de cada algoritmo, será retornado os resultados para você. Se um caminho foi encontrado, os pontos do caminho e uma representação gráfica estarão disponíveis.")
	print()

def ler_entrada():
	### Essa função realiza a leitura dos dados de entrada. ###
	dimm = input("Entre com as dimenções do labirinto (valores inteiros >= 1). > ").strip().split() # Obtém uma linha da entrada.
	if len(dimm) != 2: # Verifica se passou 2 inteiros.
		print()
		print("ERRO: você deve passar dois inteiros para o programa para a dimensão do labirinto em uma única linha.")
		sys.exit(-1)
	lab = np.empty([int(dimm[0]), int(dimm[1])], dtype=np.str) # Aloca array.
	print("Agora, entre com o labirinto abaixo. >")
	current_i = 0
	while current_i < lab.shape[0] * lab.shape[1]: # Lê o labirinto.
		line = "".join(input().strip().split())
		for char in line:
			if char != "*" and char != "-" and char != "$" and char != "#":
				continue
			lab[int(current_i / lab.shape[1]), int(current_i % lab.shape[1])] = char
			current_i += 1
	return lab

def imprimir_resultados(algo, labirinto, path, time):
	### Essa função imprime os resultados de um algoritmo executado na tela. ###
	for point in path: # Para cada ponto no caminho solução encontrado...
		labirinto[point[0], point[1]] = CHAR_PATH # Colocar como "@" no labirinto (para representação visual).
	print("== %s ==" % (algo)) # Imprimir nome do algoritmo.
	print("\tTempo de execução: %.5f segundos" % (time)) # Imprimir tempo de execução.
	if len(path) > VISUAL_POINTS_MAX: # Se houver um caminho encontrado mas é muito grande...
		print("\tCaminho: encontrado, mas longo demais para exibir os %d pontos aqui." % (len(path)))
		if labirinto.shape[0] > VISUAL_ROW_MAX or labirinto.shape[1] > VISUAL_COL_MAX:
			print("\t(Labirinto grande demais para exibir representação visual.)")
		else:
			for line in labirinto: # Imprimir representação visual desse caminho.
				print("\t", end = "")
				for item in line:
					print(item, end = "")
				print()
	elif len(path) > 1: # Se houver um caminho encontrado...
		print("\tCaminho (%d): " % (len(path)), end="")
		for point in path:
			print("(%d, %d) " % (point[0], point[1]), end="") # Imprimir os pontos desse caminho.
		print()
		if labirinto.shape[0] > VISUAL_ROW_MAX or labirinto.shape[1] > VISUAL_COL_MAX:
			print("\t(Labirinto grande demais para exibir representação visual.)")
		else:
			for line in labirinto: # Imprimir representação visual desse caminho.
				print("\t", end = "")
				for item in line:
					print(item, end = "")
				print()
	else:
		print("\tNenhum caminho encontrado.")
	print()

def is_point_valid(labirinto, x, y):
	### Essa função apenas retorna TRUE se um ponto é válido para percorrer em um dado labirinto, e FALSE caso contrário. ###
	return x >= 0 and x < labirinto.shape[0] \
		and y >= 0 and y < labirinto.shape[1] \
		and (labirinto[x, y] == "*" or labirinto[x, y] == "$")

def point_heuristic_distance(x, y, end_point):
	### Essa função retorna a distancia de um determinado ponto (x, y) a outro ponto de destino end_point, usada nos algoritmos de busca informada. ###
	#return math.sqrt(math.pow(x - end_point[0], 2) + math.pow(y - end_point[1], 2)) # Distância Euclidiana
	return abs(x - end_point[0]) + abs(y - end_point[1]) # Distância de Manhattan

def algo_dfs(labirinto):
	path = [ ]
	start_point = np.argwhere(labirinto == "#")[0].tolist()
	start_time = time.time()
	# Inicio do algoritmo.
	stack = [ start_point ] # Aloca pilha.
	antecessor = np.full(labirinto.shape, None, dtype=np.object) # Vetor de antecessores.
	while len(stack) > 0: # Enquanto existirem pontos a serem percorridos na pilha...
		point = stack.pop() # Retira do fim da pilha (então faz uma busca DFS).
		if labirinto[point[0], point[1]] == "$": # Solução encontrada! Gerar vetor com a solução e encerrar algoritmo.
			while point[0] != start_point[0] or point[1] != start_point[1]:
				path.insert(0, point)
				point = antecessor[point[0], point[1]]
			path.insert(0, start_point)
			break
		if is_point_valid(labirinto, point[0] - 1, point[1]) and antecessor[point[0] - 1, point[1]] is None: # Subir.
			stack.append([point[0] - 1, point[1]])
			antecessor[point[0] - 1, point[1]] = point
		if is_point_valid(labirinto, point[0] + 1, point[1]) and antecessor[point[0] + 1, point[1]] is None: # Descer.
			stack.append([point[0] + 1, point[1]])
			antecessor[point[0] + 1, point[1]] = point
		if is_point_valid(labirinto, point[0], point[1] - 1) and antecessor[point[0], point[1] - 1] is None: # Esquerda.
			stack.append([point[0], point[1] - 1])
			antecessor[point[0], point[1] - 1] = point
		if is_point_valid(labirinto, point[0], point[1] + 1) and antecessor[point[0], point[1] + 1] is None: # Direita.
			stack.append([point[0], point[1] + 1])
			antecessor[point[0], point[1] + 1] = point
	# Fim do algoritmo.
	end_time = time.time()
	imprimir_resultados("Algoritmo de Busca em Profundidade", labirinto, path, end_time - start_time)

def algo_bfs(labirinto):
	path = [ ]
	start_point = np.argwhere(labirinto == "#")[0].tolist()
	start_time = time.time()
	# Inicio do algoritmo.
	queue = [ start_point ] # Aloca fila.
	antecessor = np.full(labirinto.shape, None, dtype=np.object) # Vetor de antecessores.
	while len(queue) > 0: # Enquanto existirem pontos a serem percorridos na fila...
		point = queue.pop(0)  # Retira do começo da fila (então faz uma busca BFS).
		if labirinto[point[0], point[1]] == "$": # Solução encontrada! Gerar vetor com a solução e encerrar algoritmo.
			while point[0] != start_point[0] or point[1] != start_point[1]:
				path.insert(0, point)
				point = antecessor[point[0], point[1]]
			path.insert(0, start_point)
			break
		if is_point_valid(labirinto, point[0] - 1, point[1]) and antecessor[point[0] - 1, point[1]] is None: # Subir.
			queue.append([point[0] - 1, point[1]])
			antecessor[point[0] - 1, point[1]] = point
		if is_point_valid(labirinto, point[0] + 1, point[1]) and antecessor[point[0] + 1, point[1]] is None: # Descer.
			queue.append([point[0] + 1, point[1]])
			antecessor[point[0] + 1, point[1]] = point
		if is_point_valid(labirinto, point[0], point[1] - 1) and antecessor[point[0], point[1] - 1] is None: # Esquerda.
			queue.append([point[0], point[1] - 1])
			antecessor[point[0], point[1] - 1] = point
		if is_point_valid(labirinto, point[0], point[1] + 1) and antecessor[point[0], point[1] + 1] is None: # Direita.
			queue.append([point[0], point[1] + 1])
			antecessor[point[0], point[1] + 1] = point
	# Fim do algoritmo.
	end_time = time.time()
	imprimir_resultados("Algoritmo de Busca em Largura", labirinto, path, end_time - start_time)

def algo_best_first_search(labirinto):
	path = [ ]
	start_point = np.argwhere(labirinto == "#")[0].tolist()
	start_time = time.time()
	# Inicio do algoritmo.
	end_point = np.argwhere(labirinto == "$")[0].tolist()
	priority_queue = [ ] # Aloca fila de prioridade.
	antecessor = np.full(labirinto.shape, None, dtype=np.object) # Vetor de antecessores.
	heapq.heappush(priority_queue, (point_heuristic_distance(start_point[0], start_point[1], end_point), start_point)) # Adiciona o ponto inicial à fila de prioridade.
	while len(priority_queue) > 0: # Enquanto existirem pontos a serem percorridos na fila de prioridade...
		point = heapq.heappop(priority_queue)[1]  # Retira da fila de prioridades (baseando-se apenas na distancia até o ponto destino, função h(x)).
		if labirinto[point[0], point[1]] == "$": # Solução encontrada! Gerar vetor com a solução e encerrar algoritmo.
			while point[0] != start_point[0] or point[1] != start_point[1]:
				path.insert(0, point)
				point = antecessor[point[0], point[1]]
			path.insert(0, start_point)
			break
		if is_point_valid(labirinto, point[0] - 1, point[1]) and antecessor[point[0] - 1, point[1]] is None: # Subir.
			heapq.heappush(priority_queue, (point_heuristic_distance(point[0] - 1, point[1], end_point), [point[0] - 1, point[1]]))
			antecessor[point[0] - 1, point[1]] = point
		if is_point_valid(labirinto, point[0] + 1, point[1]) and antecessor[point[0] + 1, point[1]] is None: # Descer.
			heapq.heappush(priority_queue, (point_heuristic_distance(point[0] + 1, point[1], end_point), [point[0] + 1, point[1]]))
			antecessor[point[0] + 1, point[1]] = point
		if is_point_valid(labirinto, point[0], point[1] - 1) and antecessor[point[0], point[1] - 1] is None: # Esquerda.
			heapq.heappush(priority_queue, (point_heuristic_distance(point[0], point[1] - 1, end_point), [point[0], point[1] - 1]))
			antecessor[point[0], point[1] - 1] = point
		if is_point_valid(labirinto, point[0], point[1] + 1) and antecessor[point[0], point[1] + 1] is None: # Direita.
			heapq.heappush(priority_queue, (point_heuristic_distance(point[0], point[1] + 1, end_point), [point[0], point[1] + 1]))
			antecessor[point[0], point[1] + 1] = point
	# Fim do algoritmo.
	end_time = time.time()
	imprimir_resultados("Algoritmo de Busca Best-First Search", labirinto, path, end_time - start_time)

def algo_a_star(labirinto):
	path = [ ]
	start_point = np.argwhere(labirinto == "#")[0].tolist()
	start_time = time.time()
	# Inicio do algoritmo.
	end_point = np.argwhere(labirinto == "$")[0].tolist()
	priority_queue = [ ] # Aloca fila de prioridade.
	antecessor = np.full(labirinto.shape, None, dtype=np.object) # Vetor de antecessores.
	heapq.heappush(priority_queue, (point_heuristic_distance(start_point[0], start_point[1], end_point) + 0, start_point)) # Adiciona o ponto inicial à fila de prioridade.
	while len(priority_queue) > 0: # Enquanto existirem pontos a serem percorridos na fila de prioridade...
		point_priority = heapq.heappop(priority_queue) # Retira da fila de prioridades. f(x) = g(x) + h(x)
		point = point_priority[1] # x.
		current_priority = max(point_priority[0] - point_heuristic_distance(point[0], point[1], end_point), 0) + 1 # g(x) = f(x) - h(x).
		if labirinto[point[0], point[1]] == "$": # Solução encontrada! Gerar vetor com a solução e encerrar algoritmo.
			while point[0] != start_point[0] or point[1] != start_point[1]:
				path.insert(0, point)
				point = antecessor[point[0], point[1]][1]
			path.insert(0, start_point)
			break
		if is_point_valid(labirinto, point[0] - 1, point[1]) and (antecessor[point[0] - 1, point[1]] is None or antecessor[point[0] - 1, point[1]][0] > current_priority + point_heuristic_distance(point[0] - 1, point[1], end_point)): # Subir.
			next_priority = current_priority + point_heuristic_distance(point[0] - 1, point[1], end_point)
			heapq.heappush(priority_queue, (next_priority, [point[0] - 1, point[1]]))
			antecessor[point[0] - 1, point[1]] = [next_priority, point]
		if is_point_valid(labirinto, point[0] + 1, point[1]) and (antecessor[point[0] + 1, point[1]] is None or antecessor[point[0] + 1, point[1]][0] > current_priority + point_heuristic_distance(point[0] + 1, point[1], end_point)): # Descer.
			next_priority = current_priority + point_heuristic_distance(point[0] + 1, point[1], end_point)
			heapq.heappush(priority_queue, (next_priority, [point[0] + 1, point[1]]))
			antecessor[point[0] + 1, point[1]] = [next_priority, point]
		if is_point_valid(labirinto, point[0], point[1] - 1) and (antecessor[point[0], point[1] - 1] is None or antecessor[point[0], point[1] - 1][0] > current_priority + point_heuristic_distance(point[0], point[1] - 1, end_point)): # Esquerda.
			next_priority = current_priority + point_heuristic_distance(point[0], point[1] - 1, end_point)
			heapq.heappush(priority_queue, (next_priority, [point[0], point[1] - 1]))
			antecessor[point[0], point[1] - 1] = [next_priority, point]
		if is_point_valid(labirinto, point[0], point[1] + 1) and (antecessor[point[0], point[1] + 1] is None or antecessor[point[0], point[1] + 1][0] > current_priority + point_heuristic_distance(point[0], point[1] + 1, end_point)): # Direita.
			next_priority = current_priority + point_heuristic_distance(point[0], point[1] + 1, end_point)
			heapq.heappush(priority_queue, (next_priority, [point[0], point[1] + 1]))
			antecessor[point[0], point[1] + 1] = [next_priority, point]
	# Fim do algoritmo.
	end_time = time.time()
	imprimir_resultados("Algoritmo de Busca A*", labirinto, path, end_time - start_time)

def algo_hill_climbing(labirinto):
	path = [ ]
	start_point = np.argwhere(labirinto == "#")[0].tolist()
	start_time = time.time()
	# Inicio do algoritmo.
	end_point = np.argwhere(labirinto == "$")[0].tolist()
	antecessor = np.full(labirinto.shape, None, dtype=np.object) # Vetor de antecessores.
	point = start_point # Começa com ponto inicial.
	while True: # As condições de parada do algoritmo já estão determinada abaixo.
		if labirinto[point[0], point[1]] == "$": # Solução encontrada! Gerar vetor com a solução e encerrar algoritmo.
			while point[0] != start_point[0] or point[1] != start_point[1]:
				path.insert(0, point)
				point = antecessor[point[0], point[1]]
			path.insert(0, start_point)
			break
		nearest_point = None
		nearest_distance = float("inf")
		if is_point_valid(labirinto, point[0] - 1, point[1]) and antecessor[point[0] - 1, point[1]] is None: # Subir.
			if nearest_distance > point_heuristic_distance(point[0] - 1, point[1], end_point):
				nearest_point = [point[0] - 1, point[1]]
				nearest_distance = point_heuristic_distance(point[0] - 1, point[1], end_point)
		if is_point_valid(labirinto, point[0] + 1, point[1]) and antecessor[point[0] + 1, point[1]] is None: # Descer.
			if nearest_distance > point_heuristic_distance(point[0] + 1, point[1], end_point):
				nearest_point = [point[0] + 1, point[1]]
				nearest_distance = point_heuristic_distance(point[0] + 1, point[1], end_point)
		if is_point_valid(labirinto, point[0], point[1] - 1) and antecessor[point[0], point[1] - 1] is None: # Esquerda.
			if nearest_distance > point_heuristic_distance(point[0], point[1] - 1, end_point):
				nearest_point = [point[0], point[1] - 1]
				nearest_distance = point_heuristic_distance(point[0], point[1] - 1, end_point)
		if is_point_valid(labirinto, point[0], point[1] + 1) and antecessor[point[0], point[1] + 1] is None: # Direita.
			if nearest_distance > point_heuristic_distance(point[0], point[1] + 1, end_point):
				nearest_point = [point[0], point[1] + 1]
				nearest_distance = point_heuristic_distance(point[0], point[1] + 1, end_point)
		if nearest_point == None or nearest_distance > point_heuristic_distance(point[0], point[1], end_point):
			break
		antecessor[nearest_point[0], nearest_point[1]] = point
		point = nearest_point
	# Fim do algoritmo.
	end_time = time.time()
	imprimir_resultados("Algoritmo de Busca Hill Climbing", labirinto, path, end_time - start_time)



### MAIN ###

introducao() # Imprimir texto de introdução.
labirinto = ler_entrada() # Ler o labirinto de entrada.

print("Vamos iniciar a execução dos algoritmos. Por favor, aguarde...")
print()

algo_dfs(np.copy(labirinto)) # Busca em profundidade.
algo_bfs(np.copy(labirinto)) # Busca em largura.
algo_best_first_search(np.copy(labirinto)) # Busca Best-First Search.
algo_a_star(np.copy(labirinto)) # Busca A*.
algo_hill_climbing(np.copy(labirinto)) # Hill Climbing.


