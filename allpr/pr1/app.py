from flask import Flask, render_template, request 
app = Flask(__name__) 
def compare_chefs(chef1_scores, chef2_scores): 
    points_for_chef1 = 0 
    points_for_chef2 = 0 
    for i in range(3): 
        if chef1_scores[i] > chef2_scores[i]: 
            points_for_chef1 += 1 
        elif chef1_scores[i] < chef2_scores[i]: 
            points_for_chef2 += 1 
    return [points_for_chef1, points_for_chef2] 
 
@app.route('/') 
def index(): 
    return render_template('index.html') 

# Route for Task 1 page
@app.route('/task1')
def task1():
    return render_template('task1.html')

# Route for Task 2 page
@app.route('/task2')
def task2():
    return render_template('task2.html')

 
@app.route('/compare', methods=['POST']) 
def compare(): 
    chef1_scores = [ 
        int(request.form['chef1_presentation']), 
        int(request.form['chef1_taste']), 
        int(request.form['chef1_hygiene']) 
    ] 
    chef2_scores = [ 
        int(request.form['chef2_presentation']), 
        int(request.form['chef2_taste']), 
        int(request.form['chef2_hygiene']) 
    ] 
    result = compare_chefs(chef1_scores, chef2_scores) 
    return render_template('result.html', result=result) 

#  Task 2 

def find_closest_to_zero_pair(arr):
    arr.sort()
    left=0
    right = len(arr) - 1 
    min_sum = float('inf') 
    closest_pair = None

    while left < right: 
        current_sum = arr[left] + arr[right] 
 
        if abs(current_sum) < abs(min_sum): 
            min_sum = current_sum 
            closest_pair = (arr[left], arr[right]) 
 
        if current_sum < 0: 
            left += 1 
        else: 
            right -= 1 
            return closest_pair\
            
@app.route('/find_pair', methods=['POST']) 
def find_pair(): 
    input_array = request.form['input_array'] 
    arr = list(map(int, input_array.split(','))) 
    closest_pair = find_closest_to_zero_pair(arr) 
    return render_template('result1.html', input_array=input_array, 
closest_pair=closest_pair) 
         
if __name__ == '__main__':
    app.run(debug=True, port=5001)