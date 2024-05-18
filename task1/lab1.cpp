#include <iostream>
#include <stack>
#include <fstream>
#include <vector>
#include <algorithm>

class Graph
{
private:
    bool** graph;
    size_t size;
    std::istream* istream;
    std::ostream* ostream;
    static std::vector<size_t> getCycle(std::vector<size_t> & from, size_t lastV) {
        std::vector<size_t> cycle = {lastV};
        for (size_t v = from[lastV]; v != lastV; v = from[v]) {
            cycle.push_back(v);
        }
        return cycle;
    }

    void dfs(bool** graph, size_t v, int* visited, std::vector<size_t>& fromList, std::vector<size_t>& cycle)
    {
        visited[v] = 1;
        for (size_t to = 0; to < size; ++to)
        {
            if (to == fromList[v])
                continue;

            if (visited[to] == 0 && graph[v][to]) {
                fromList[to] = v;
                dfs(graph, to, visited, fromList, cycle);
                if (!cycle.empty()) return;
            }
            else if (visited[to] == 1 && graph[v][to]) {
                fromList[to] = v;
                cycle = getCycle(fromList, to);
                return;
            }
        }
        visited[v] = 2;
    }

    static void showCycle(std::vector<size_t> loop, std::ostream& out) {
        out << "N" << std::endl;
        std::sort(loop.begin(), loop.end());

        for (int i : loop){
            out << i + 1 << " ";
        }
    }
public:
    explicit Graph(size_t N, std::istream* istream, std::ostream* ostream) {
        size = N;
        graph = new bool*[size];
        this->istream = istream;
        this->ostream = ostream;

        for (size_t i = 0; i < size; ++i)
            graph[i] = new bool[size];
    }

    ~Graph() {
        for (size_t i = 0; i < size; ++i)
            delete[] graph[i];
    }

    void input()
    {
        for (size_t i = 0; i < size; ++i)
            for (size_t j = 0; j < size; ++j)
                *istream >> graph[i][j];
    }

    void outCycle()
    {
        int* visited = new int[size];
        std::vector<size_t> fromList(size, -1);
        std::vector<size_t> loop;

        for (size_t v = 0; v < size && loop.empty(); ++v)
        {
            if (visited[v] == 2)
                continue;

            dfs(graph, v, visited, fromList,loop);
        }

        if (loop.empty()) {
            *ostream << "A";
            return;
        }

        showCycle(loop,*ostream);
        delete[] visited;
    }
};


int main()
{
    std::ifstream in("in.txt");
    std::ofstream out("out.txt");
    size_t N = 0;
    in >> N;
    Graph graph(N,&in,&out);
    graph.input();
    graph.outCycle();
    return 0;
}
