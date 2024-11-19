from flask import Flask, render_template, request

app = Flask(__name__)

def knapsack_optimizer(items, capacity, weights, values):
    result_table = [[0 for x in range(capacity + 1)] for x in range(items + 1)]

    for i in range(1, items + 1):
        for j in range(capacity + 1):
            if weights[i-1] <= j:
                result_table[i][j] = max(result_table[i-1][j], values[i-1] + result_table[i-1][j - weights[i-1]])
            else:
                result_table[i][j] = result_table[i-1][j]

    optimal_value = result_table[items][capacity]
    return result_table, optimal_value

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        capacity = int(request.form['bag_capacity'])  
        items = int(request.form['item_count']) 

        values = list(map(int, request.form['item_values'].split(',')))
        weights = list(map(int, request.form['item_weights'].split(',')))

        result_table, optimal_value = knapsack_optimizer(items, capacity, weights, values)

        return render_template('index.html', result_table=result_table, optimal_value=optimal_value, values=values, weights=weights, capacity=capacity, items=items)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5007)