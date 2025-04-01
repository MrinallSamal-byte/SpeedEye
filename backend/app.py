from flask import Flask, render_template, jsonify
from database.db_operations import fetch_all_speed_data, fetch_all_challans

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/speed_data')
def speed_data():
    data = fetch_all_speed_data()
    return jsonify(data)

@app.route('/api/challans')
def challans():
    data = fetch_all_challans()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
