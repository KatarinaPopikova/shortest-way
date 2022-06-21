# https://www.geeksforgeeks.org/union-find/
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html#scipy.spatial.KDTree.query


from scipy.spatial import distance
import time
from ast import literal_eval
from collections import defaultdict

import numpy
from scipy.spatial import KDTree
from statistics import mode


def read_file(file_path):
    all_vertices = []
    all_edges = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file:
            vertices = line.split()
            vertex1_index = add_vertex_to_vertices(all_vertices, literal_eval(vertices[0]))
            vertex2_index = add_vertex_to_vertices(all_vertices, literal_eval(vertices[1]))
            all_edges[vertex1_index].append(vertex2_index)
    return all_vertices, all_edges


def add_vertex_to_vertices(all_vertices, vertex):
    try:
        return all_vertices.index(vertex)
    except ValueError:
        all_vertices.append(vertex)
        return len(all_vertices) - 1


def update_connected_components(connected_components):
    for i in range(len(connected_components)):
        parent = find(connected_components, i)
        if parent != connected_components[i]:
            union(connected_components, i, parent)


def check_components(vertices, edges):
    connected_components = list(range(len(vertices)))
    for vertex1 in edges:
        for vertex2 in edges[vertex1]:
            union(connected_components, find(connected_components, vertex1), find(connected_components, vertex2))
    update_connected_components(connected_components)
    return connected_components


def union(components, x, y):
    if x < y:
        components[y] = x
    else:
        components[x] = y


def find(components, i):
    if components[i] == i:
        return i
    if components[i] != i:
        return find(components, components[i])


def get_index_of_main_component(connected_components):
    return mode(connected_components)


def vertex_division(connected_components, vertices, main_component):
    main_component_vertices = []
    other_vertices = []
    for index, component in enumerate(connected_components):
        if component != main_component:
            other_vertices.append(vertices[index])
        else:
            main_component_vertices.append(vertices[index])
    return main_component_vertices, other_vertices


def write_edge(file, edge_from_vertex, edge_to_vertex):
    add_edge_vertex1 = "[" + str(edge_from_vertex[0]) + "," + str(edge_from_vertex[1]) + "]"
    add_edge_vertex2 = "[" + str(edge_to_vertex[0]) + "," + str(edge_to_vertex[1]) + "]"
    file.write(add_edge_vertex1 + " " + add_edge_vertex2 + "\n")


def add_connections(connected_components, vertices, edges, path):
    file = open(path, 'w')
    main_component = get_index_of_main_component(connected_components)

    while not all_vertices_is_same_component(connected_components):
        main_component_vertices, other_vertices = vertex_division(connected_components, vertices, main_component)
        other_vertices_tree = KDTree(other_vertices)
        min_distances, min_distances_index = other_vertices_tree.query(main_component_vertices)
        min_distance_vertex_index = numpy.argmin(min_distances)
        edge_from_vertex = main_component_vertices[min_distance_vertex_index]
        edge_to_vertex = other_vertices[min_distances_index[min_distance_vertex_index]]

        write_edge(file, edge_from_vertex, edge_to_vertex)
        edge_from_vertex_index = vertices.index(edge_from_vertex)
        edge_to_vertex_index = vertices.index(edge_to_vertex)

        edges[edge_from_vertex_index].append(edge_to_vertex_index)

        founded_component = connected_components[edge_to_vertex_index]
        for index in range(len(connected_components)):
            if connected_components[index] == founded_component:
                connected_components[index] = main_component


def all_vertices_is_same_component(connected_components):
    for i in connected_components[1:]:
        if i != connected_components[0]:
            return False
    return True


def sum_euclidian_distances(added_edges):
    euclidian_distance = 0
    for line in added_edges:
        edges = line.split()
        euclidian_distance += distance.euclidean(list(map(int, edges[0][1:-1].split(","))),
                                                 list(map(int, edges[1][1:-1].split(","))))
    return euclidian_distance


def main():
    path = 'resources/graph_9857'
    vertices, edges = read_file(path + '.txt')
    start = time.perf_counter()
    connected_components = check_components(vertices, edges)
    add_connections(connected_components, vertices, edges, path + '_output.txt')
    end = time.perf_counter()
    if all_vertices_is_same_component(check_components(vertices, edges)):
        print("Graf je jeden komponent")
    else:
        print("Graf nie je jeden komponent")
    print("Časové trvanie: " + str(end - start))
    euclidian_distances = sum_euclidian_distances(open(path + '_output.txt', 'r'))
    print("Súčet euklidovských vzdialeností doplnených hrán: " + str(euclidian_distances))


if __name__ == '__main__':
    main()
