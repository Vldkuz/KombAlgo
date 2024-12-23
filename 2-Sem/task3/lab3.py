def get_sm(field, i,j):
    for k in range(-1, 2, 2):
        if len(field) > i + k >= 0:
            if field[i + k][j] == "+":
                yield i + k, j

        if len(field[i]) > j + k >= 0:
            if field[i][j+k] == "+":
                yield i, j + k


def dfs(start_vertex: tuple[int, int], field: list[str], color: int, color_mas: list[str]):
    stack = [start_vertex]; color_mas[start_vertex] = color

    while len(stack) > 0:
        vertex = stack.pop()
        for sm_vertex in get_sm(field, vertex[0], vertex[1]):
            if sm_vertex not in color_mas:
                stack.append(sm_vertex)
                color_mas[sm_vertex] = color


def all_vertex(field: list[str]):
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "+":
                yield i, j

def get_comps(field: list[str]) -> int:
    vertexes = [x for x in all_vertex(field)]
    color_mas = {}; color = 1

    for vertex in vertexes:
        if vertex not in color_mas:
            dfs(vertex, field, color, color_mas)
            color += 1

    if len(color_mas) > 0:
        return max(color_mas.values())
    else:
        return 0



def main(in_file, out_file):
    with open(in_file, 'r') as in_fd:
        n, m = map(int, in_fd.readline().split())
        field = []

        for _ in range(n):
            field.append(in_fd.readline().strip())

        count_comps = get_comps(field)

    with open(out_file, 'w') as out_fd:
        out_fd.write(str(count_comps))









if __name__ == '__main__':
    main("in.txt", "out.txt")