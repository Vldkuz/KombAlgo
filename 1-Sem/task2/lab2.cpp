#include <iostream>
#include <map>
#include <vector>
#include <queue>
#include <algorithm>
#include <fstream>

class Graph
{
private:
    std::map<size_t, std::vector<size_t>> graph;
    std::istream* istream;
    std::ostream* ostream;
    static size_t front(std::queue<size_t>& queue) {
        size_t elem = queue.front();
        queue.pop();
        return elem;
    }

    static  std::pair<std::vector<size_t>, std::vector<size_t>> makeDols(std::vector<int>& colors) {
        std::vector<size_t> first; std::vector<size_t> second;
        for (int v = 1; v < colors.size(); ++v) {
            if (colors[v] == 0) { first.push_back(v);}
            else if (colors[v] == 1) { second.push_back(v);}
        }
        std::sort(first.begin(), first.end());
        std::sort(second.begin(), second.end());

        if (first.empty() || second.empty())
            return std::pair(first, second);

        if (first[0] > second[0])
            return std::pair(second, first);
        else
            return std::pair(first, second);
    }
public:
    Graph(std::istream* in, std::ostream* out){ istream = in; ostream = out;}
    void Input() {
        size_t N = 0;
        *istream >> N;

        for (size_t i = 1; i <= N; ++i) {
            int Vertex = -1;
            while (true) {
                *istream >> Vertex;
                if (Vertex == 0) break;
                graph[i].push_back(Vertex);
            }
        }
    }

    std::pair<std::vector<size_t>, std::vector<size_t>> isdicotyledonous() {
        std::vector<int> colors(graph.size() + 1, -1);

        std::queue<size_t> queue;
        size_t color = 0;
        size_t v = 1;
        queue.push(v);
            while (!queue.empty())
            {
                size_t vertex = front(queue);

                if (colors[vertex] == -1) {
                    colors[vertex] = color;
                    color = (color + 1) % 2;
                }
                else {
                    color = (colors[vertex] + 1) % 2;
                }


                std::vector<size_t> sm = graph[vertex];

                for (auto u : sm)
                {
                    if (colors[u] == -1) { queue.push(u); colors[u] = color;}
                    else if (colors[vertex] == colors[u]) {
                        std::vector<size_t> first;
                        std::vector<size_t> second;
                        return std::pair(first, second);
                    }
                }
            }

        return makeDols(colors);
    }

    void Out() {
        auto res = isdicotyledonous();

        if (res.first.empty()) {
            *ostream << "N" << std::endl;
            return;
        }

        *ostream << "Y" << std::endl;
        for (size_t u: res.first)
            *ostream << u << " ";

        *ostream << std::endl;

        for (size_t u: res.second)
            *ostream << u << " ";
    }
};



int main ()
{
    std::ifstream in("in.txt");
    std::ofstream out("out.txt");
    Graph graph(&in, &out);
    graph.Input();
    graph.Out();
    return 0;
}
