#
# CS 196 Data Hackerspace
# Assignment 1: Data Parsing and NumPy
# Due September 24th, 2018
#

import json
import csv
import numpy as np
import math


def histogram_times(filename):
    final_array = []
    for x in range(24):
        final_array.append(0)
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if line[1]:
                try:
                    temp = int(line[1][:2])
                    if 0 <= temp < 24:
                        final_array[temp] += 1
                except ValueError:
                    pass
    print(final_array)


def weigh_pokemons(filename, weight):
    pokemon_correct_weight = []
    with open(filename) as f:
        data = json.load(f)
    for i in range(len(data["pokemon"])):
        poke_weight = data["pokemon"][i]["weight"].split(" ")[0]
        if poke_weight == str(weight):
            pokemon_correct_weight.append(data["pokemon"][i]["name"])
    print(pokemon_correct_weight)

def single_type_candy_count(filename):
    total_candy_count = 0
    with open(filename) as f:
        data = json.load(f)
    for i in range(len(data["pokemon"])):
        if len(data["pokemon"][i]["type"]) == 1:
            try:
                data["pokemon"][i]["candy_count"]
                to_add = data["pokemon"][i]["candy_count"]
                total_candy_count += int(to_add)
            except KeyError:
                pass
    print(total_candy_count)

def reflections_and_projections(points):
    final_reflected_arr = np.zeros((2, points[0].size))
    for i in range(len(points[0])):
        x_coord = points[0, i]
        y_coord = points[1, i]
        y_coord -= 1
        y_coord = 1 - y_coord
        final_reflected_arr[0, i] = x_coord
        final_reflected_arr[1, i] = y_coord
    for i in range(len(final_reflected_arr[0])):
        x_coord = final_reflected_arr[0, i]
        y_coord = final_reflected_arr[1, i]

        rotate_matrix = np.array([[0, -1], [1, 0]])
        to_rotate = np.array([x_coord, y_coord])
        rotated_matrix = np.matmul(rotate_matrix, to_rotate)

        final_reflected_arr[0][i] = rotated_matrix[0]
        final_reflected_arr[1][i] = rotated_matrix[1]
    for i in range(len(final_reflected_arr[0])):
        x_coord = final_reflected_arr[0, i]
        y_coord = final_reflected_arr[1, i]

        project_matrix = np.array([[.1, .3], [.3, .9]])
        to_project = np.array([x_coord, y_coord])
        projected_matrix = np.matmul(project_matrix, to_project)

        final_reflected_arr[0][i] = projected_matrix[0]
        final_reflected_arr[1][i] = projected_matrix[1]
    print(final_reflected_arr)

def normalize(image):
    final_arr = np.zeros((len(image), len(image[0])))
    initial_max = 0
    initial_min = 225
    for i in range(len(image[0])):
        for j in range(len(image)):
            if image[i][j] > initial_max:
                initial_max = image[i][j]
            if image[i][j] < initial_min:
                initial_min = image[i][j]
    constant_multi = 255/(initial_max - initial_min)
    for i in range(len(image[0])):
        for j in range(len(image)):
            pixel_num = image[i][j]
            pixel_num -= initial_min
            pixel_num *= constant_multi
            final_arr[i][j] = int(pixel_num)
    print(final_arr)
    return final_arr




def sigmoid_normalize(image, a):
    final_arr = np.zeros((len(image), len(image[0])))
    initial_max = 0
    initial_min = 225
    constant_multi = 255 / (initial_max - initial_min)
    for i in range(len(image[0])):
        for j in range(len(image)):
            pixel_num = image[i][j]
            pixel_num -= 128
            multi = -1*(a**(-1))
            pixel_num *= multi
            pixel_num = 1 + (math.exp(pixel_num))
            pixel_num = 255*(pixel_num**(-1))
            final_arr[i][j] = int(pixel_num)
    print(final_arr)
    return final_arr


histogram_times('airplane_crashes.csv')
weigh_pokemons('pokedex.json', 10.0)
single_type_candy_count('pokedex.json')
image = np.array([[1, 2],[3, 4]])
temp = np.array(image)
reflections_and_projections(temp)
normalize(image)
sigmoid_normalize(image, 1000)