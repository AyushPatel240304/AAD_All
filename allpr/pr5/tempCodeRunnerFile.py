from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def min_coins(coins, value):
    dp = [float('inf')] * (value + 1)
    dp[0] = 0
    for i in range(1, value + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[value]

# Index route (homepage)
@app.route('/')
def index():
    return render_template('index.html')

# Route for Task 1 page
@app.route('/task1', methods=['GET', 'POST'])
def task1():
    coins = [1, 4, 6]
    result = None
    values = []
    results = []
    
    if request.method == 'POST':
        value = int(request.form['value'])
        result = min_coins(coins, value)
        
        # Comparative analysis for different input sizes
        for i in range(1, value + 1):
            values.append(i)
            results.append(min_coins(coins, i))
        
        # Plotting the graph with green line color
        plt.figure(figsize=(10, 6))
        plt.plot(values, results, marker='o', color='green')
        plt.title('Minimum Coins Required for Different Values')
        plt.xlabel('Value')
        plt.ylabel('Minimum Coins')
        plt.grid(True)
        
        # Save plot to a string in base64 format
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        
        return render_template('task1.html', result=result, value=value, plot_url=plot_url)
    
    return render_template('task1.html')

if __name__ == '__main__':
    app.run(debug=True)
