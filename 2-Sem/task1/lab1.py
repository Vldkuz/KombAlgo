import copy
from collections import defaultdict

MAGIC_BIG_NUMBER = 10**9
from array import array

def massive2sets(s: list[int], n: int):
    vertices_ptrs = [(i, el) for  i, el in enumerate(s[:s.index(n)])]
    edges = {}
    vertices = {x for x,y in vertices_ptrs}

    for i in range(len(vertices_ptrs)):
        if i == len(vertices) - 1:
            next_ptr = n
        else:
            _, next_ptr = vertices_ptrs[i + 1]

        v, ptr = vertices_ptrs[i]
        vertices_weights = s[ptr - 1:next_ptr - 1]

        for j in range(0, len(vertices_weights) - 1, 2):
            w = vertices_weights[j] - 1
            weight = vertices_weights[j+1]
            edges[(v,w)] = weight

    for x in vertices:
        for y in vertices:
            if (x,y) not in edges:
                edges[(x,y)] = MAGIC_BIG_NUMBER

    return vertices, edges

def find_min_w_vertex(vertices: set[int], dist):
    minn_d = dist[0]
    vertex = None

    for v in vertices:
        if dist[v] < minn_d:
            minn_d = dist[v]
            vertex = v

    return vertex




def find_spanning_tree(s: list[int], n: int):
    vertices, edges = massive2sets(s, n); w = vertices.pop()
    t = set(); nearest = [MAGIC_BIG_NUMBER for _ in range(n)]; distance = copy.deepcopy(nearest)
    count_vertices = len(vertices); summ_spanning_tree = 0

    for v in vertices:
        nearest[v] = w
        distance[v] = edges.get((v,w)) or MAGIC_BIG_NUMBER

    while len(t) <= count_vertices - 1:
        v = find_min_w_vertex(vertices, distance)
        t.add((v, nearest[v]))
        summ_spanning_tree += edges[(v, nearest[v])]
        vertices -= {v}

        for u in vertices:
            if distance[u] > edges[(u,v)]:
                distance[u] = edges[(u,v)]
                nearest[u] = v

    return t, summ_spanning_tree


def make_linked_list(t: set[tuple[int, int]]):
    linked_list = defaultdict(list)
    for u,v in t:
        linked_list[u+1].append(v+1); linked_list[v+1].append(u+1)
    return linked_list


def main():
    array_adjacency = []

    with open("in.txt") as f:
        lines = f.readlines()
        n = int(lines[0])
        for line in lines[1:]:
            array_adjacency += list(map(int, line.split()))

    array_adjacency = array_adjacency[:-1]
    edges, weight_sp = find_spanning_tree(array_adjacency, n)
    out = make_linked_list(edges)

    with open("out.txt", "w") as f:
        keys = sorted(out.keys())
        for key in keys:
            for val in sorted(out[key]):
                f.write(f'{val} ')
            f.write('0\n')
        f.write(f'{weight_sp}')





if __name__ == '__main__':
    # p = [6, 10, 14, 20, 22, 2, 25, 3, 4, 1, 25, 3, 0, 1, 4, 2, 0, 4, 7, 3, 7, 32167]
    # t, summ = find_spanning_tree(p, 22)
    # print(make_linked_list(t))
    main()


