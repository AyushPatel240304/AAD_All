from flask import Flask, request, render_template
import sys

app = Flask(__name__)

def dijkstra(graph, start_node):
    n = len(graph)
    visited = [False] * n
    distance = [sys.maxsize] * n
    previous = [-1] * n  
    distance[start_node] = 0

    for _ in range(n):
        min_distance = sys.maxsize
        min_index = -1


        for i in range(n):
            if not visited[i] and distance[i] < min_distance:
                min_distance = distance[i]
                min_index = i

        visited[min_index] = True

        for j in range(n):
            if graph[min_index][j] != float('inf') and not visited[j]:
                new_dist = distance[min_index] + graph[min_index][j]
                if new_dist < distance[j]:
                    distance[j] = new_dist
                    previous[j] = min_index  

    return distance, previous

def construct_path(previous, node, cities):
    path = []
    while node != -1:
        path.insert(0, cities[node])
        node = previous[node]
    return ' -> '.join(path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    cities = ['A', 'B', 'C', 'D', 'E']
    graph = [
        [0, 20, 30, float('inf'), float('inf')],
        [float('inf'), 0, float('inf'), 15, float('inf')],
        [float('inf'), float('inf'), 0, float('inf'), 25],
        [float('inf'), float('inf'), float('inf'), 0, 10],
        [float('inf'), float('inf'), float('inf'), float('inf'), 0]
    ]
    start_city = request.form['start_city']
    start_node = cities.index(start_city)
    distances, previous = dijkstra(graph, start_node)

    result = []
    for i in range(len(cities)):
        if distances[i] == sys.maxsize:
            result.append((cities[i], '∞', 'No path'))
        else:
            path = construct_path(previous, i, cities)
            result.append((cities[i], distances[i], path))

    return render_template('result.html', result=result, start_city=start_city)

if __name__ == '__main__':
    app.run(debug=True, port=5011)