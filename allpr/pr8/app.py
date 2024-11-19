from flask import Flask, render_template, request

app = Flask(__name__)


def lcs(X, Y):
    m = len(X)
    n = len(Y)
    

    L = [[0 for i in range(n+1)] for j in range(m+1)]
    
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])

    lcs_str = ""
    i = m
    j = n
    while i > 0 and j > 0:
        if X[i-1] == Y[j-1]:
            lcs_str += X[i-1]
            i -= 1
            j -= 1
        elif L[i-1][j] > L[i][j-1]:
            i -= 1
        else:
            j -= 1

    lcs_str = lcs_str[::-1]  
    
    return L, lcs_str
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        X = request.form['string1'].upper()
        Y = request.form['string2'].upper()

       
        L, lcs_str = lcs(X, Y)
        lcs_length = len(lcs_str)

        return render_template('index.html', X=X, Y=Y, table=L, lcs=lcs_str, length=lcs_length)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5008)