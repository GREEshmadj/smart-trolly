from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_barcode', methods=['POST'])
def process_barcode():
    data = request.get_json()
    barcode = data['barcode']
    quantity = data['quantity']
    price = data['price']

    # Perform any processing needed for the barcode data
    # For demonstration, just return the processed data
    processed_data = {
        'barcode': barcode,
        'quantity': quantity,
        'price': price,
    }

    return jsonify(processed_data)

if __name__ == '__main__':
    app.run(debug=True)
