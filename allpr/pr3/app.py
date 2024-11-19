from flask import Flask, render_template, request, jsonify, send_file
import time
import matplotlib.pyplot as plt
import io
import random

app = Flask(__name__)

# Sorting algorithms
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)

@app.route('/')
def index():
    return render_template('index.html')

# Task 1 page and functionality
@app.route('/task1')
def task1():
    return render_template('task1.html')

# Sorting logic associated with task1
@app.route('/sort', methods=['POST'])
def sort():
    data = request.json
    arr = data['arr']
    
    start_time = time.time()
    bubble_sorted = bubble_sort(arr.copy())
    bubble_time = time.time() - start_time

    start_time = time.time()
    merge_sorted = merge_sort(arr.copy())
    merge_time = time.time() - start_time

    start_time = time.time()
    quick_sorted = quick_sort(arr.copy())
    quick_time = time.time() - start_time

    return jsonify({
        'bubble_sorted': bubble_sorted,
        'merge_sorted': merge_sorted,
        'quick_sorted': quick_sorted,
        'bubble_time': bubble_time * 1000,  
        'merge_time': merge_time * 1000,  
        'quick_time': quick_time * 1000  
    })

# Plotting logic associated with task1
@app.route('/plot', methods=['GET'])
def plot():
    sizes = [10, 50, 100, 500, 1000]
    bubble_times = []
    merge_times = []
    quick_times = []

    for size in sizes:
        arr = [random.randint(0, 1000) for _ in range(size)]

        start_time = time.time()
        bubble_sort(arr.copy())
        bubble_times.append((time.time() - start_time) * 1000)

        start_time = time.time()
        merge_sort(arr.copy())
        merge_times.append((time.time() - start_time) * 1000)

        start_time = time.time()
        quick_sort(arr.copy())
        quick_times.append((time.time() - start_time) * 1000)

    plt.figure(figsize=(12, 6))
    plt.plot(sizes, bubble_times, label='Bubble Sort', marker='o')
    plt.plot(sizes, merge_times, label='Merge Sort', marker='o')
    plt.plot(sizes, quick_times, label='Quick Sort', marker='o')
    plt.xlabel('Number of Elements')
    plt.ylabel('Time (ms)')
    plt.title('Sorting Algorithm Performance Comparison')
    plt.legend()
    plt.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, port=5003)