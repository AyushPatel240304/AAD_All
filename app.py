from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def home():
    # Render the homepage with practical buttons
    return render_template('index.html')

@app.route('/practical/<int:practical_id>')
def practical_redirect(practical_id):
    # Map practical ID to the port where its app is running
    practical_port_map = {
        1: 5001,  # Practical 1 runs on port 5001
        2: 5002,
        3: 5003,
        4: 5004,
        5: 5005,
        6: 5006,
        7: 5007,
        8: 5008,
        9: 5009,
        10: 5010,
        11: 5011,
        12: 5012,
        # Add more mappings as needed
    }
    # Get the port for the selected practical
    port = practical_port_map.get(practical_id)

    if port:
        # Redirect to the correct port
        return redirect(f'http://127.0.0.1:{port}/')
    else:
        # Handle invalid practical ID
        return "Practical not found!", 404

if __name__ == '__main__':
    app.run(debug=True)
