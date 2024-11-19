from flask import Flask, render_template
import math

app = Flask(__name__)

def tsp(dp, dist, mask, pos, n):
    if mask == (1 << n) - 1:
        return dist[pos][0], [(pos + 1, 1)]  
    if (mask, pos) in dp:
        return dp[(mask, pos)]

    ans = math.inf
    min_path = []

    for city in range(n):
        if (mask & (1 << city)) == 0:
            newAns, path = tsp(dp, dist, mask | (1 << city), city, n)
            newAns += dist[pos][city]

            if newAns < ans:
                ans = newAns
                min_path = [(pos + 1, city + 1)] + path  

    dp[(mask, pos)] = (ans, min_path)
    return ans, min_path

def find_minimum_cost(dist):
    n = len(dist)
    dp = {} 
    min_cost, path = tsp(dp, dist, 1, 0, n)
    return min_cost, path

@app.route('/')
def index():
    dist = [
        [float('inf'), 20, 30, 10, 11],
        [15, float('inf'), 16, 4, 2],
        [3, 5, float('inf'), 2, 4],
        [19, 6, 18, float('inf'), 3],
        [16, 4, 7, 16, float('inf')]
    ]

    min_cost, path = find_minimum_cost(dist)

    return render_template('index.html', min_cost=min_cost, path=path)

if __name__ == '__main__':
    app.run(debug=True, port=5012)