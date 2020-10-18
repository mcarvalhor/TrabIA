#!python3

import numpy as np
from math import ceil
import random
import heapq
import sys



#
 #	~ Trabalho Prático 1: Gerador de Labirintos ~
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



EMPTY = '*'
WALL = '-'
AGENT = '#'
GOAL = '$'
LINE_BREAK = '\n'
FOR_PRINT_BUF = 1000000000

movements = [[+1, 0], [0, +1]] # [[+1, 0], [-1, 0], [0, -1], [0, +1]]

def valid_point(width, height, point):
	return point[0] >= 0 and point[0] < width \
		and point[1] >= 0 and point[1] < height

def find_set(parent, v):
	if v == parent[v[0], v[1]]:
		return v
	parent[v[0], v[1]] = find_set(parent, parent[v[0], v[1]])
	return parent[v[0], v[1]]

def union_sets(parent, rank, a, b):
	a = find_set(parent, a)
	b = find_set(parent, b)
	if a != b:
		if rank[a[0], a[1]] < rank[b[0], b[1]]:
			tmp = a
			a = b
			b = tmp
		parent[b[0], b[1]] = a
		if rank[a[0], a[1]] == rank[b[0], b[1]]:
			rank[a[0], a[1]] += 1

def generate(width, height, verbose=True):
	''' Generate maze using Kruskal Minimum Spanning Tree Algorithm. '''
	# Alocate array.
	edges_dtype = np.dtype([('w', np.float), ('u', np.int, (2, )), ('v', np.int, (2, )), ('p', np.int, (2, ))])
	edges = np.empty([width*height*len(movements)], dtype=edges_dtype)
	parent = np.empty([width, height], dtype=tuple)
	array = np.full([width * 2 - 1, height * 2 - 1], WALL, dtype=np.str)
	rank = np.full([width, height], 0, dtype=np.int)

	print('Preenchendo... %.2f%% concluído' % (0.0), end="", file=sys.stderr)
	count = 0
	iterator = 0
	max = width * height
	for i in range(width):
		for j in range(height):
			if count % FOR_PRINT_BUF:
				print('\rPreenchendo... %.2f%% concluído' % (100.0*count/max), end="", file=sys.stderr)
			count += 1
			parent[i, j] = (i, j)
			array[i * 2, j * 2] = EMPTY
			for move in movements:
				adjacent = (i + move[0], j + move[1])
				edge = ((i, j), adjacent)
				if not valid_point(width, height, adjacent):
					continue
				weight = random.random()
				edges[iterator] = (weight, edge[0], edge[1], (2 * i + move[0], 2 * j + move[1]))
				iterator += 1
	print('\rPreenchendo... %.2f%% concluído.' % (100.0), file=sys.stderr)

	print('Ordenando...', end="", file=sys.stderr)
	edges = np.sort(edges[:iterator], order=['w'])
	print('\rOrdenando... %.2f%% concluído.' % (100.0), file=sys.stderr)

	cost = 0.0
	count = 0
	max = edges.shape[0]
	print('Processando... %.2f%% concluído' % (0.0), end="", file=sys.stderr)
	for edge in edges:
		if count % FOR_PRINT_BUF:
			print('\rProcessando... %.2f%% concluído' % (100.0*count/max), end="", file=sys.stderr)
		count += 1
		w = edge['w']
		u = tuple(edge['u'])
		v = tuple(edge['v'])
		p = tuple(edge['p'])
		if find_set(parent, u) != find_set(parent, v):
			cost += w
			array[p[0], p[1]] = EMPTY
			union_sets(parent, rank, u, v)
	print('\rProcessando... %.2f%% concluído.' % (100.0), file=sys.stderr)
	
	return array

if len(sys.argv) != 4:
	print("Como usar:", file=sys.stderr)
	print("\t> python3 %s WIDTH HEIGHT FILE" % (sys.argv[0]), file=sys.stderr)
	print("\tOnde WIDTH é o número de linhas e HEIGHT o número de colunas do labirinto que se deseja gerar, e FILE é o nome do arquivo para salvar os resultados.", file=sys.stderr)
	print(file=sys.stderr)
	sys.exit(0)

width = int(sys.argv[1])
height = int(sys.argv[2])
file_name = str(sys.argv[3]).strip()

if width < 5 or height < 5:
	print("Atenção:", file=sys.stderr)
	print("Tanto WIDTH como HEIGHT devem ser números inteiros maiores ou iguais a 5.", file=sys.stderr)
	print(file=sys.stderr)
	sys.exit(0)

if width % 2 == 0 or height % 2 == 0:
	print("Atenção:", file=sys.stderr)
	print("Devido a maneira como o código foi implementado, não é possível que WIDTH ou HEIGHT sejam pares. Mas não se preocupe, vamos ajustar tudo para você (consideraremos o ímpar imediatamente menor).", file=sys.stderr)
	print(file=sys.stderr)

width = int((width + 1) / 2)
height = int((height + 1) / 2)

print('Gerando labirinto %sx%s...' % (width * 2 - 1, height * 2 - 1), file=sys.stderr)

maze = generate(width, height)

maze[0, 0] = AGENT
maze[maze.shape[0] - 1, maze.shape[1] - 1] = GOAL

print('Salvando em arquivo...', end="", file=sys.stderr)
np.savetxt(file_name, maze, fmt="%s", delimiter="", newline=LINE_BREAK, header="%d %d"%(maze.shape[0], maze.shape[1]), comments="")
print('\rSalvando em arquivo... %.2f%% concluído' % (100.0), file=sys.stderr)

print('Pronto.', file=sys.stderr)
