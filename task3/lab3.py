import sys

INP_FILE = 'in.txt'
OUT_FILE = 'out.txt'


def transform_to_previous(l_next: list[list[int]]):
    prev = []
    for i in range(0, len(l_next)):
        v_i_prev = []
        for j in range(0, len(l_next)):
            if not len(l_next[j]):
                continue

            if i in l_next[j]:
                v_i_prev.append(j)
        prev.append(v_i_prev)

    return prev


def topological_sort(l_next: list[list[int]], l_prev: list[list[int]]):
    out_v = []
    v_mapper = {}
    reverse_mapper = {}

    for v_list in l_next:
        out_v.append(len(v_list))

    stack = []
    n = len(l_next) - 1

    for i in range(len(l_next)):
        if out_v[i] == 0:
            stack.append(i)

    while len(stack) > 0:
        k = stack.pop()
        v_mapper[k] = n
        reverse_mapper[n] = k
        n -= 1

        for w in l_prev[k]:
            out_v[w] -= 1

            if out_v[w] == 0:
                stack.append(w)

    return v_mapper, reverse_mapper


def find_path(start, end, prev_list, weight: dict[(int, int): int]):
    parents = [-1 for _ in range(len(prev_list))]
    distance = [-sys.maxsize for _ in range(len(prev_list))]
    distance[0] = 0
    parents[start] = start

    for m in range(1, len(distance)):
        for w in prev_list[m]:
            th_w = distance[w] + weight[w, m]
            if th_w > distance[m]:
                distance[m] = th_w
                parents[m] = w

    path = []
    cur = end

    while parents[cur] != cur:

        if parents[cur] == -1:
            return None

        path.append(cur)
        cur = parents[cur]

    path.append(start)

    return path[::-1], distance[end]


def rebuild_list_mapper(l: list[list[int]], topologic_mapper: dict[int: int], weight: dict[(int, int): int]):
    prev = [[0] for _ in range(len(l))]
    rebuild_weight = {}

    for i in range(len(l)):
        mapped_v = topologic_mapper[i]
        mapped_list = []

        for v in l[i]:
            rebuild_weight[(topologic_mapper[v], mapped_v)] = weight[(v, i)]
            mapped_list.append(topologic_mapper[v])

        prev[mapped_v] = mapped_list

    return prev, rebuild_weight


def main():
    with open(INP_FILE, 'r') as in_f, open(OUT_FILE, 'w') as out_f:
        n = int(in_f.readline())
        v_next = []
        weight = {}

        for i in range(0, n):
            line = list(map(int, in_f.readline().split(' ')[:-1]))

            v_i_next_weight = []
            for next_v in range(0, len(line) - 1, 2):
                v = int(line[next_v]) - 1
                i_v_weight = int(line[next_v + 1])

                v_i_next_weight.append(v)
                weight[(i, v)] = i_v_weight

            v_next.append(v_i_next_weight)

        s, v = int(in_f.readline()) - 1, int(in_f.readline()) - 1
        v_prev = transform_to_previous(v_next)
        topologic_mapper, rev_topological_mapper = topological_sort(v_next, v_prev)
        topologically_sorted, weight = rebuild_list_mapper(v_prev, topologic_mapper, weight)
        ans = find_path(topologic_mapper[s], topologic_mapper[v], topologically_sorted, weight)

        if ans is None:
            out_f.write('N')
        else:
            path, weight_path = ans[0],ans[1]
            mapped_path = list(map(lambda x: rev_topological_mapper[x] + 1, path))
            out_f.write('Y\n')
            out_f.write(f'{' '.join(map(str, mapped_path))}\n')
            out_f.write(str(weight_path))


if __name__ == '__main__':
    main()
