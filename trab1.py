#!python3

import numpy as np
import threading
import time
import sys

CHAR_PATH = "@"



def introducao():
	print()
	print("Bem-vinde ao nosso trabalho!")
	print("Funciona da seguinte maneira:")
	print("- Você vai passar como entrada um labirinto, da maneira como proposto na especificação do trabalho.")
	print("- Em seguida todos os algoritmos irão executar, e os resultados de cada algoritmo serão impressos.")
	print("Atenção: o programa utiliza múltiplas threads para uma execução mais rápida.")
	print()

def ler_entrada():
	### Essa função realiza a leitura dos dados de entrada. ###
	dimm = input("Entre com as dimenções do labirinto (valores inteiros >= 1). > ").strip().split() # Obtem uma linha da entrada.
	if len(dimm) != 2: # Verifica se passou 2 inteiros.
		print()
		print("ERRO: você deve passar dois inteiros para o programa para a dimensão do labirinto em uma única linha.")
		sys.exit(-1)
	lab = np.empty([int(dimm[0]), int(dimm[1])], dtype=np.str) # Aloca array.
	print("Agora, entre com o labirinto abaixo. >")
	for i in range(lab.shape[0]): # Lê o labirinto.
		line = "".join(input().split())
		if len(line) != lab.shape[1]: # Verifica se está certo.
			print()
			print("ERRO: você passou uma linha cujo número de itens está errado!")
			sys.exit(-1)
		for j in range(lab.shape[1]): # Coloca os dados lidos da linha na array.
			lab[i, j] = line[j]
	return lab

def imprimir_resultados(algo, labirinto, path, time):
	global mutex
	for point in path:
		labirinto[point[0], point[1]] = CHAR_PATH
	mutex.acquire()
	print("== %s ==" % (algo))
	print("\tTempo de execução: %.5f segundos" % (time))
	if len(path) > 1:
		for line in labirinto:
			print("\t", end = "")
			for item in line:
				print(item, end = "")
			print()
	else:
		print("\tNenhum caminho encontrado.")
	print()
	mutex.release()


def algo_dfs_recursao(labirinto, point):
	if labirinto[point[0], point[1]] == "$":
		return [point]
	is_point_valid = lambda x, y : x >= 0 and x < labirinto.shape[0] \
		and y >= 0 and y < labirinto.shape[1] \
		and (labirinto[x, y] == "*" or labirinto[x, y] == "$")
	if is_point_valid(point[0] + 1, point[1]):
		labirinto[point[0], point[1]] = "!"
		ret = algo_dfs_recursao(labirinto, [point[0] + 1, point[1]]) # Descer.
		labirinto[point[0], point[1]] = "*"
		if ret is not None:
			return [point] + ret
	if is_point_valid(point[0], point[1] + 1):
		labirinto[point[0], point[1]] = "!"
		ret = algo_dfs_recursao(labirinto, [point[0], point[1] + 1]) # Direita.
		labirinto[point[0], point[1]] = "*"
		if ret is not None:
			return [point] + ret
	if is_point_valid(point[0] - 1, point[1]):
		labirinto[point[0], point[1]] = "!"
		ret = algo_dfs_recursao(labirinto, [point[0] - 1, point[1]]) # Subir.
		labirinto[point[0], point[1]] = "*"
		if ret is not None:
			return [point] + ret
	if is_point_valid(point[0], point[1] - 1):
		labirinto[point[0], point[1]] = "!"
		ret = algo_dfs_recursao(labirinto, [point[0], point[1] - 1]) # Esquerda.
		labirinto[point[0], point[1]] = "*"
		if ret is not None:
			return [point] + ret
	return None

def algo_dfs(labirinto):
	path = [ ]
	start_time = time.time()
	# Inicio do algoritmo.
	start_point = np.argwhere(labirinto == "#")[0].tolist()
	ret = algo_dfs_recursao(labirinto, start_point)
	if ret is not None:
		path = ret
	# Fim do algoritmo.
	end_time = time.time()
	imprimir_resultados("Algoritmo de Busca em Profundidade", labirinto, path, end_time - start_time)

def algo_bfs(labirinto):
	path = [ ]
	start_time = time.time()
	# Inicio do algoritmo.
	# Fim do algoritmo.
	end_time = time.time()
	imprimir_resultados("Algoritmo de Busca em Largura", labirinto, path, end_time - start_time)

def algo_best_first_search(labirinto):
	path = [ ]
	start_time = time.time()
	# Inicio do algoritmo.
	# Fim do algoritmo.
	end_time = time.time()
	imprimir_resultados("Algoritmo de Busca Best-First Search", labirinto, path, end_time - start_time)

def algo_a_star(labirinto):
	path = [ ]
	start_time = time.time()
	# Inicio do algoritmo.
	# Fim do algoritmo.
	end_time = time.time()
	imprimir_resultados("Algoritmo de Busca A*", labirinto, path, end_time - start_time)

def algo_hill_climbing(labirinto):
	path = [ ]
	start_time = time.time()
	# Inicio do algoritmo.
	# Fim do algoritmo.
	end_time = time.time()
	imprimir_resultados("Algoritmo de Busca Hill Climbing", labirinto, path, end_time - start_time)


### MAIN ###

introducao() # Imprimir texto de introdução.
labirinto = ler_entrada() # Ler o labirinto de entrada.

threads = [ ] # Lista de threads (para maior desempenho).
mutex = threading.Semaphore(1) # Mutex para impressão de resultados.
threads.append(threading.Thread(target=algo_dfs, args=(np.copy(labirinto),))) # Busca em profundidade.
threads.append(threading.Thread(target=algo_bfs, args=(np.copy(labirinto),))) # Busca em largura.
threads.append(threading.Thread(target=algo_best_first_search, args=(np.copy(labirinto),))) # Busca Best-First Search.
threads.append(threading.Thread(target=algo_a_star, args=(np.copy(labirinto),))) # Busca A*.
threads.append(threading.Thread(target=algo_hill_climbing, args=(np.copy(labirinto),))) # Hill Climbing.

print("Vamos iniciar a execução dos algoritmos. Por favor, aguarde...")
print()

for t in threads:
	t.start()

for t in threads:
	t.join()

print("FIM.")
print()


