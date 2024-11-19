from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret_key_for_flash_messages'

class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

def build_huffman_tree(char_freq):
    nodes = [Node(char, freq) for char, freq in char_freq.items()]
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged = Node(None, left.freq + right.freq, left, right)
        nodes.append(merged)
    return nodes[0]

def generate_huffman_codes(root, current_code="", codes={}):
    if root is None:
        return
    if root.char is not None:
        codes[root.char] = current_code
    generate_huffman_codes(root.left, current_code + "0", codes)
    generate_huffman_codes(root.right, current_code + "1", codes)
    return codes

def encode(text, codes):
    try:
        return ''.join([codes[char] for char in text])
    except KeyError:
        return "Error: Invalid character in input."

def decode(encoded_text, root):
    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        current_node = current_node.left if bit == '0' else current_node.right
        if current_node.char is not None:
            decoded_text += current_node.char
            current_node = root
    return decoded_text

@app.route('/', methods=['GET', 'POST'])
def index():
    huffman_codes = {}
    encoded_text = ""
    decoded_text = ""
    char_freq = {}

    if request.method == 'POST':
        try:
            freq_input = request.form['char_freq'].strip().split(',')
            char_freq = {pair.split(':')[0].strip().upper(): float(pair.split(':')[1].strip()) for pair in freq_input}

            huffman_tree = build_huffman_tree(char_freq)
            huffman_codes = generate_huffman_codes(huffman_tree)

            action = request.form['action']
            input_text = request.form['input_text'].strip().upper()

            if action == 'encode':
                encoded_text = encode(input_text, huffman_codes)
            elif action == 'decode':
                decoded_text = decode(input_text, huffman_tree)

        except Exception as e:
            flash(f"Error: {e}. Please enter valid input.")
            return redirect(url_for('index'))

    return render_template('index.html', huffman_codes=huffman_codes, encoded_text=encoded_text, decoded_text=decoded_text)

if __name__ == '__main__':
    app.run(debug=True, port=5010)