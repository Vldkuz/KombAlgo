from collections import defaultdict

def mark(V, c, f, s, t, forwards, backwards):
    delta = {v:10**10 for v in V}; parent = {s: None}; way = {}
    queue = [s]

    while (t not in queue) and len(queue) > 0:
        w = queue.pop(0)

        for v in forwards[w]:
            if (delta[v] == 10**10) and (c(w,v) - f(w,v)) > 0:
                delta[v] = min(delta[w], c(w,v) - f(w,v))
                parent[v] = w; queue.append(v); way[v] = 1

        for v in backwards[w]:
            if v != s:
                if (delta[v] == 10**10) and f(v,w) > 0:
                    delta[v] = min(delta[w], f(v,w))
                    parent[v] = w; queue.append(v); way[v] = -1

    return delta, parent, way




def ford(V, c, s, t, forwards, backwards):
    F = [[0 for _ in V] for _ in V]

    def f(i,j):
        return F[i][j]

    while True:
        delta, parent, way = mark(V, c, f, s, t, forwards, backwards)

        if delta[t]< 10**10:
            v = t

            while v != s:
                w = parent[v]
                if way[v] == 1:
                    F[w][v] += delta[t]
                else:
                    F[v][w] -= delta[t]
                v = w

        if delta[t] == 10**10:
            break

    return f



def maximum_matching(k, i, edges: set[tuple[int, int]]):
    V = [_ for _ in range(k+i+2)]; s = i + k; t = i + k + 1

    edges.update({(s,x) for x in V if x < k})
    edges.update({(y,t) for y in V if k <= y < i + k})

    weights = defaultdict(lambda : 0)

    forward = {x: [w for v,w in edges if v == x] for x in V}
    backward = {x: [v for v,w in edges if w == x] for x in V}

    for x,y in edges:
        weights[(x,y)] = 1

    def c(v,w):
        return weights[(v,w)]

    ans = ford(V, c, s, t, forward, backward)

    def _ans(v, w): return ans(v, w + k)

    return _ans


def main(f,o):
    k, i = map(int, f.readline().split())
    edges = set()

    for x in range(k):
        x_list = list(map(int, f.readline().split()))
        for y in filter(lambda t : t > 0 , x_list):
            edges.add((x, y + k - 1))

    ans = maximum_matching(k, i, edges)
    l = []

    for x in range(k):
        q = 0

        for y in range(i):
            if ans(x,y) > 0:
                q = y + 1
                break
        l.append(str(q))

    o.write(' '.join(l))






if __name__ == "__main__":
    with open("in.txt") as file:
        with open("out.txt", "w") as out:
            main(file, out)


