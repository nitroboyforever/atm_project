from flask import Flask, render_template, request

app = Flask(__name__)

# Simulated backend data
balance = 0
transaction_history = []
user_pin_login = 1234

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def handle_transaction():
    global balance, transaction_history

    user_name = request.form['user_name']
    user_pin = request.form['user_pin']
    action = request.form['action']
    amount = request.form.get('amount', '')

    if not user_name.isalpha():
        return "Invalid name. Only letters allowed."

    try:
        user_pin = int(user_pin)
    except:
        return "Invalid PIN. Must be numbers only."

    if user_pin != user_pin_login:
        return "Access denied. Wrong PIN."

    if action == 'balance':
        return f"Hello {user_name}, your current balance is ₦{balance}"

    elif action == 'deposit':
        try:
            amount = int(amount)
            balance += amount
            transaction_history.append(f"You deposited ₦{amount}")
            return f"Deposit successful. New balance is ₦{balance}"
        except:
            return "Invalid deposit amount."

    elif action == 'withdraw':
        try:
            amount = int(amount)
            if amount > balance:
                return "Insufficient funds."
            else:
                balance -= amount
                transaction_history.append(f"You withdrew ₦{amount}")
                return f"Withdrawal successful. New balance is ₦{balance}"
        except:
            return "Invalid withdrawal amount."

    elif action == 'history':
        if not transaction_history:
            return "No transactions yet."
        return "<br>".join(transaction_history)

    return "Invalid action."

if __name__ == '__main__':
    app.run(debug=True)

