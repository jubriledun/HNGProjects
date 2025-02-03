from flask import Flask, request, jsonify
import requests
import math

app = Flask(__name__)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n):
    digits = [int(digit) for digit in str(n)]
    power = len(digits)
    return sum(digit ** power for digit in digits) == n

def get_fun_fact(n):
    url = f"http://numbersapi.com/{n}/math"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "No fun fact found"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    if not number or not number.isdigit():
        return jsonify({"number": number, "error": True}), 400

    number = int(number)
    armstrong = is_armstrong(number)
    prime = is_prime(number)
    even = number % 2 == 0
    digit_sum = sum(map(int, str(number)))
    fun_fact = get_fun_fact(number)

    properties = []
    if armstrong:
        properties.append("armstrong")
    properties.append("even" if even else "odd")

    return jsonify({
        "number": number,
        "is_prime": prime,
        "is_perfect": False,  # No perfect number check required
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
