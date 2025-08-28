from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json  # Parse JSON payload
        print(f"Received data: {data}")
        # Process the data here (e.g., save to database, trigger actions)
        return jsonify({"message": "Webhook received!"}), 200
    else:
        return jsonify({"error": "Only POST requests are allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
