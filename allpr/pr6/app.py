from flask import Flask, render_template, request

app = Flask(__name__)

def compute_chain_order(p_dims):
    matrix_count = len(p_dims) - 1
    cost = [[0 for _ in range(matrix_count)] for _ in range(matrix_count)]
    split = [[0 for _ in range(matrix_count)] for _ in range(matrix_count)]

    for chain_len in range(2, matrix_count + 1):
        for start in range(matrix_count - chain_len + 1):
            end = start + chain_len - 1
            cost[start][end] = float('inf')
            for mid in range(start, end):
                current_cost = cost[start][mid] + cost[mid + 1][end] + p_dims[start] * p_dims[mid + 1] * p_dims[end + 1]
                if current_cost < cost[start][end]:
                    cost[start][end] = current_cost
                    split[start][end] = mid

    return cost, split

def build_optimal_sequence(split_matrix, start, end):
    if start == end:
        return f"M{start + 1}"
    else:
        middle = split_matrix[start][end]
        left_part = build_optimal_sequence(split_matrix, start, middle)
        right_part = build_optimal_sequence(split_matrix, middle + 1, end)
        return f"({left_part} x {right_part})"

@app.route('/', methods=['GET', 'POST'])
def homepage():
    total_matrices = None
    total_operations = None
    optimal_sequence = None
    cost_matrix = None

    if request.method == 'POST':
        matrix_dims = list(map(int, request.form['matrix_dims'].split(',')))
        total_matrices = len(matrix_dims) - 1
        cost_matrix, split_matrix = compute_chain_order(matrix_dims)
        optimal_sequence = build_optimal_sequence(split_matrix, 0, total_matrices - 1)
        total_operations = cost_matrix[0][-1]

        # Mark non-diagonal zeros as 'N/A'
        cost_matrix = [['N/A' if cell == 0 else cell for cell in row] for row in cost_matrix]

    return render_template('index.html',
                           total_operations=total_operations,
                           optimal_sequence=optimal_sequence,
                           cost_matrix=cost_matrix,
                           total_matrices=total_matrices)

if __name__ == '__main__':
    app.run(debug=True, port=5006)