# -*- coding: utf-8 -*-
"""Projeto1.ipynb

"""

# Gustavo José da Silveira Mello

# Importando as bibliotecas necessárias para a impressão do tabuleiro
import random
import numpy as np # for board printing
import seaborn as sns # for board printing
import matplotlib.pyplot as plt # for board printing

# Função para imprimir o tabuleiro
def board(solution):
    matrix = np.zeros([len(solution),len(solution)], dtype=int)
    matrix = matrix.tolist()
    for item in solution:
        for i in range(len(solution)):
            if i == item:
                for j in range(len(solution)):
                    if  j == solution.index(item):
                        matrix[i][j] = 1

    l =[]
    for i in range(0, len(solution)):
        l.append(i)

    plt.figure(figsize=(5,5))
    sns.heatmap(matrix, linewidths=.8,cbar=False,cmap='Set3',xticklabels=l,yticklabels=l)

# Função para gerar um cromossomo aleatório
def random_chromosome(size):
    board = [0] * size
    for i in range(size):
        board[i] = random.randint(0, size-1)
    return board

# Função para calcular o fitness do cromossomo, fit 28 é o maior para 8 rainhas, que signfica que existem 28 pares de rainhas sem sofrer ataques
def fitness(board):
    collisions = 0
    for i in range(len(board)):
        for j in range(i+1, len(board)):
            if board[i] == board[j]:
                collisions += 1
            elif abs(board[i] - board[j]) == abs(i - j):
                collisions += 1
    return (board_size*(board_size-1))/2 - collisions

# Função para selecionar os cromossomos para reprodução por meio de torneio
def selection(population, tournament_size):
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=lambda x: fitness(x))

# Função para realizar o crossover entre dois cromossomos
def crossover(parent1, parent2):
    child = [0] * len(parent1)
    crossover_point = random.randint(1, len(parent1)-2)
    child[:crossover_point] = parent1[:crossover_point]
    child[crossover_point:] = parent2[crossover_point:]
    return mutation(child)

# Função para realizar a mutação no cromossomo
def mutation(board):
    mutation_rate = 0.2
    for i in range(len(board)):
        if random.random() < mutation_rate:
            board[i] = random.randint(0, len(board)-1)
    return board

# Função para executar o algoritmo genético
def genetic_algorithm(population_size, tournament_size, elite_size, max_iterations, board_size, crossover_rate, optimal_solution):
    # Gerando a população inicial
    population = [random_chromosome(board_size) for i in range(population_size)]
    best_fitness_history = []  # Lista para armazenar o melhor fitness a cada iteração
    i = 0  # Contador de gerações
    # Execução do algoritmo até alcançar o número máximo de iterações ou encontrar a solução ótima
    while i < max_iterations:
        # Ordenando a população pelo fitness
        population = sorted(population, key=lambda x: fitness(x), reverse=True)
        # Adição do melhor fitness da geração atual ao histórico
        best_fitness_history.append(fitness(population[0]))
        # Se a solução ótima for encontrada, encerra a execução e exibe a geração e fitness
        if fitness(population[0]) == optimal_solution:
            print("\nA solução foi encontrada na geração:", i+1, "| Seu Fitness é de:",fitness(population[0]))
            break
        # Seleção dos indivíduos para elite e geração de descendentes
        elite = population[:elite_size]
        new_gen = []
        for j in range(population_size - elite_size):
            parent1 = selection(population, tournament_size)
            parent2 = selection(population, tournament_size)
            if random.random() < crossover_rate:
              child = crossover(parent1, parent2)
            else:
                child = parent1.copy()
            new_gen.append(child)
        # Nova geração é formada pela elite e descendentes gerados
        population = elite + new_gen
        # Exibição da melhor solução e fitness da geração atual
        print("Geração:", i+1," | Cromossomo:", population[0]," | Fit:", best_fitness_history[-1])
        i += 1
    # Retorno da solução encontrada
    return population[0]

# Solicitação do tamanho do tabuleiro
print("Qual o número de rainhas?")
board_size = int(input())

# Definição dos parâmetros do algoritmo
population_size = 200

tournament_size = 5

elite_size = 4

max_iterations = 500

crossover_rate = 0.7

optimal_solution = (board_size*(board_size-1))/2


# Execução do algoritmo
solution = genetic_algorithm(population_size, tournament_size, elite_size, max_iterations, board_size, crossover_rate, optimal_solution)

# Exibição da solução encontrada
print("\nSua disposição foi de:", solution)
board(solution)
