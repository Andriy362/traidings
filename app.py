from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Початковий баланс
initial_balance = {"value": 1078}  # Баланс на старті

# Список угод для тестування
deals = [
    {"id": 1, "open_date": "2025-05-01", "open_time": "10:00", "close_date": "2025-05-02", "close_time": "12:00", "symbol": "EURUSD", "direction": "Buy", "open_price": 1.1000, "close_price": 1.1200, "commission": 0.01, "result": 200, "comment": "Profit"},
    {"id": 2, "open_date": "2025-05-01", "open_time": "14:00", "close_date": "2025-05-02", "close_time": "16:00", "symbol": "GBPUSD", "direction": "Sell", "open_price": 1.3000, "close_price": 1.2900, "commission": 0.02, "result": -100, "comment": "Loss"}
]

@app.route('/')
def index():
    return render_template('index.html', deals=deals, initial_balance=initial_balance["value"])

@app.route('/add', methods=['GET', 'POST'])
def add_deal():
    if request.method == 'POST':
        new_deal = {
            "id": len(deals) + 1,
            "open_date": request.form['open_date'],
            "open_time": request.form['open_time'],
            "close_date": request.form['close_date'],
            "close_time": request.form['close_time'],
            "symbol": request.form['symbol'],
            "direction": request.form['direction'],
            "open_price": float(request.form['open_price']),
            "close_price": float(request.form['close_price']),
            "commission": float(request.form['commission']),
            "result": float(request.form['result']),
            "comment": request.form.get('comment', '')
        }
        # Оновлюємо баланс
        initial_balance["value"] += new_deal["result"]
        deals.append(new_deal)
        return redirect(url_for('index'))
    return render_template('add_deal.html')

@app.route('/edit/<int:deal_id>', methods=['GET', 'POST'])
def edit_deal(deal_id):
    deal = next((d for d in deals if d["id"] == deal_id), None)
    if not deal:
        return "Угода не знайдена", 404

    if request.method == 'POST':
        # Віднімаємо старий результат від балансу
        initial_balance["value"] -= deal["result"]

        # Оновлюємо дані угоди
        deal["open_date"] = request.form['open_date']
        deal["open_time"] = request.form['open_time']
        deal["close_date"] = request.form['close_date']
        deal["close_time"] = request.form['close_time']
        deal["symbol"] = request.form['symbol']
        deal["direction"] = request.form['direction']
        deal["open_price"] = float(request.form['open_price'])
        deal["close_price"] = float(request.form['close_price'])
        deal["commission"] = float(request.form['commission'])
        deal["result"] = float(request.form['result'])
        deal["comment"] = request.form.get('comment', '')

        # Додаємо новий результат до балансу
        initial_balance["value"] += deal["result"]

        return redirect(url_for('index'))
    return render_template('edit_deal.html', deal=deal)

@app.route('/delete/<int:deal_id>', methods=['POST'])
def delete_deal(deal_id):
    global deals
    deal = next((d for d in deals if d["id"] == deal_id), None)
    if not deal:
        return "Угода не знайдена", 404

    # Оновлюємо баланс при видаленні угоди
    initial_balance["value"] -= deal["result"]

    deals = [d for d in deals if d["id"] != deal_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
