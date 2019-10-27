import pywavefront
import math
import numpy as np
import pyglet
import sys

cube = pywavefront.Wavefront('tinker.obj', collect_faces=True)

vertices = cube.vertices
faces = cube.mesh_list[0].faces

EDGE_LENGTHS = np.array([100,100,100])

min_coordinates = np.array([9999 ,9999, 9999])
max_coordinates = np.array([-9999 ,-9999, -9999])

for vertex in vertices:
    for i in range(0,3):
        if(vertex[i] < min_coordinates[i]):
            min_coordinates[i]=vertex[i]
        if(vertex[i] > max_coordinates[i]):
            max_coordinates[i]=vertex[i]

#
delta_coordinates = np.array([0,0,0])
for i in range(0, 3):
    delta_coordinates = max_coordinates - min_coordinates

print("max coordinates:", max_coordinates)
print("min coordinates", min_coordinates)
print("delta coordinates", delta_coordinates)

def find_scaling_factor(delta_coordinates, EDGE_LENGTH):
    scaling_factors = 0
    for i in range(0, 3):
        #this assumes that it's a cube
        max_delta = np.max(delta_coordinates)
        scaling_factors = (EDGE_LENGTHS[0] / max_delta)*(48/50)
    print("scaling factor", scaling_factors)
    return scaling_factors

def find_midpoint(v1, v2):
    return v1 + (v2-v1)/2

def form_edge(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    delta_v = v2 - v1

    len_delta_v = int(np.sqrt(np.sum(delta_v**2))) + 1
    new_vertices = []
    for i in range(0, 2*len_delta_v):
        new_vertices.append(v1 + (i/(2*len_delta_v))*delta_v)

    return new_vertices


def connect_edges(edge1, edge2):

    new_vertices = []

    if(len(edge1) < len(edge2)):
        edge1, edge2 = edge2, edge1

    delta_vertex_number = len(edge1) - len(edge2)

    odd_coef = 0
    if(delta_vertex_number % 2 == 1):
        odd = 1

    padding = int(delta_vertex_number/2)

    shortened_edge1 = edge1[padding+odd_coef: -padding + 1]

    for i in range(0, len(edge2)):
        new = form_edge(edge1[i], edge2[i])
        for vertex in new:
            new_vertices.append(vertex)

    return new_vertices


def form_surfaces(faces, vertices):

    new_vertices = []
    # print(faces, ">>>>")
    for face in faces:
        v1_v2 = form_edge(vertices[face[1]], vertices[face[0]])
        v1_v3 = form_edge(vertices[face[0]], vertices[face[2]])
        v2_v3 = form_edge(vertices[face[1]], vertices[face[2]])

        edges = [v1_v2, v1_v3, v2_v3] #fix this lmao it's so inefficient
        # edge_lengths = [len(v1_v2), len(v1_v3), len(v2_v3)]
        # l1 = np.argmax(edge_lengths)
        # edge_lengths[l1] = 0
        # l2 = np.argmax(edge_lengths)
        #
        #
        # l1_edge = edges[l1]
        # l2_edge = edges[l2]

        new_vertices.extend(connect_edges(edges[0], edges[1]))
        new_vertices.extend(connect_edges(edges[1], edges[2]))
        new_vertices.extend(connect_edges(edges[2], edges[0]))



        # two_max_edges = [edges[l1], edges[l2]]

    return new_vertices

def shift(shift_vector, vertices):
    new_vertices = []
    for vertex in vertices:
        new_vertices.append(vertex + shift_vector)
    return new_vertices

def scale(scaling_factor, vertices):
    new_vertices = []
    for vertex in vertices:
        new_vertices.append(scaling_factor * vertex)
    return new_vertices

shifted_vertices = shift(min_coordinates*-1, vertices)
scaled_vertices = scale(find_scaling_factor(delta_coordinates, EDGE_LENGTHS), shifted_vertices)
edges = form_surfaces(faces, scaled_vertices)

min_coordinates = np.array([9999, 9999, 9999])

for vertex in edges:
    for i in range(0,3):
        if(vertex[i] < min_coordinates[i]):
            min_coordinates[i]=vertex[i]

shifted_again = shift((min_coordinates)*-1, edges)

cube_space = np.zeros((EDGE_LENGTHS[0],EDGE_LENGTHS[1],EDGE_LENGTHS[2]))

for vertex in shifted_again:
    cube_space[int(vertex[0])][int(vertex[1])][int(vertex[2])] = 1

sys.setrecursionlimit(EDGE_LENGTHS[0]**3)

def fill(coordinates, cube_space):
    x = coordinates[0]
    y = coordinates[1]
    z = coordinates[2]
    cube_space[x][y][z] = 1
    if(cube_space[x][y][z+1] == 0):
        cube_space[x][y][z+1] = 1
        cube_space = fill([x, y, z+1], cube_space)
    if(cube_space[x][y][z-1] == 0):
        cube_space[x][y][z-1] = 1
        cube_space = fill([x, y, z-1], cube_space)
    if(cube_space[x][y+1][z] == 0):
        cube_space[x][y+1][z] = 1
        cube_space = fill([x, y+1, z], cube_space)
    if(cube_space[x][y-1][z] == 0):
        cube_space[x][y-1][z] = 1
        cube_space = fill([x, y-1, z], cube_space)
    if(cube_space[x+1][y][z] == 0):
        cube_space[x+1][y][z] = 1
        cube_space = fill([x+1, y, z], cube_space)
    if(cube_space[x-1][y][z] == 0):
        cube_space[x-1][y][z] = 1
        cube_space =fill([x-1, y, z], cube_space)
    return cube_space
avg = np.average(shifted_again, axis=0).astype(int)

# cube_space = fill(avg, cube_space)

from vpython import sphere, vec, color, box, vector

for i in range(EDGE_LENGTHS[0]):
    for j in range(EDGE_LENGTHS[1]):
        for k in range(EDGE_LENGTHS[2]):
            if(cube_space[i][j][k] == 1):
                box(pos=vec(i,j,k), color=color.hsv_to_rgb(vector(i/50 + .5,j/50 + .5,k/50 +.5)), opacity=0.7)
