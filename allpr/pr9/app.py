from flask import Flask, render_template, request

app = Flask(__name__)

def greedy_knap(p, w, mw):
    ratio = []
    for i in range(len(p)):
        ratio.append(p[i] / w[i])

    for i in range(len(ratio)):
        for j in range(len(ratio) - i - 1):
            if ratio[j] < ratio[j + 1]:
                ratio[j], ratio[j + 1] = ratio[j + 1], ratio[j]
                p[j], p[j + 1] = p[j + 1], p[j]
                w[j], w[j + 1] = w[j + 1], w[j]

    items_used = [0 for _ in range(len(p))]

    profit = 0
    for i in range(len(p)):
        if w[i] < mw:
            mw = mw - w[i]
            profit += p[i]
            items_used[i] = 1
        elif mw == 0:
            break
        elif w[i] > mw:
            j = mw * ratio[i]
            profit += j
            mw -= mw
            items_used[i] = j / p[i]

    return profit,items_used,p,w,ratio

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        profits = list(map(int, request.form['profits'].split()))
        weights = list(map(int, request.form['weights'].split()))
        max_weight = int(request.form['max_weight'])

        max_profit ,items_used , sorted_profits , sorted_weights , sorted_ratio  = greedy_knap(profits,weights,max_weight)

        return render_template('index.html' , max_profit = max_profit , items_used = items_used ,sorted_profits = sorted_profits ,sorted_weights = sorted_weights , sorted_ratio = sorted_ratio)

    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True, port=5009)